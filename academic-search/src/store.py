from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable

from .contracts import (
    ActionRecord,
    ActionType,
    AnalysisArtifact,
    ClaimStatus,
    Document,
    EvidencePolarity,
    Hypothesis,
    ResearchClaim,
    ResearchEvidence,
    Source,
    to_dict,
)


class ResearchStore:
    """Canonical SQLite evidence store. SQLite is the source of truth; exports are views."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.fts_available = False
        self.initialize()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "ResearchStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def initialize(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS sources (
              source_id TEXT PRIMARY KEY, dedupe_key TEXT UNIQUE NOT NULL,
              provider TEXT NOT NULL, provider_id TEXT NOT NULL, title TEXT NOT NULL,
              authors_json TEXT NOT NULL, year INTEGER, doi TEXT, url TEXT,
              source_type TEXT NOT NULL, publication_status TEXT NOT NULL,
              abstract TEXT NOT NULL, oa_url TEXT, cited_by_count INTEGER NOT NULL,
              referenced_ids_json TEXT NOT NULL, metadata_json TEXT NOT NULL, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS documents (
              document_id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES sources(source_id),
              title TEXT NOT NULL, content TEXT NOT NULL, locator TEXT NOT NULL,
              mime_type TEXT NOT NULL, content_hash TEXT UNIQUE NOT NULL,
              metadata_json TEXT NOT NULL, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS evidence (
              evidence_id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES sources(source_id),
              document_id TEXT NOT NULL REFERENCES documents(document_id), claim_id TEXT,
              passage TEXT NOT NULL, locator TEXT NOT NULL, polarity TEXT NOT NULL,
              retrieval_query TEXT NOT NULL, score REAL NOT NULL, source_quality TEXT NOT NULL,
              metadata_json TEXT NOT NULL, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS claims (
              claim_id TEXT PRIMARY KEY, text TEXT NOT NULL, status TEXT NOT NULL,
              evidence_ids_json TEXT NOT NULL, counterevidence_ids_json TEXT NOT NULL,
              hypothesis_id TEXT, rationale TEXT NOT NULL, human_review_required INTEGER NOT NULL,
              created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS hypotheses (
              hypothesis_id TEXT PRIMARY KEY, text TEXT NOT NULL, rationale TEXT NOT NULL,
              status TEXT NOT NULL, linked_claim_ids_json TEXT NOT NULL, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS analyses (
              analysis_id TEXT PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL,
              command TEXT, input_locator TEXT, output_locator TEXT, summary TEXT NOT NULL,
              metadata_json TEXT NOT NULL, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS actions (
              action_id TEXT PRIMARY KEY, action_type TEXT NOT NULL, status TEXT NOT NULL,
              target_id TEXT, provider TEXT, query TEXT, detail_json TEXT NOT NULL, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS edges (
              from_id TEXT NOT NULL, relation TEXT NOT NULL, to_id TEXT NOT NULL,
              metadata_json TEXT NOT NULL DEFAULT '{}', PRIMARY KEY(from_id, relation, to_id)
            );
            CREATE INDEX IF NOT EXISTS evidence_claim_idx ON evidence(claim_id);
            CREATE INDEX IF NOT EXISTS actions_type_idx ON actions(action_type, status);
            CREATE INDEX IF NOT EXISTS edges_from_idx ON edges(from_id);
            """
        )
        try:
            self.connection.execute(
                "CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(document_id UNINDEXED, title, content)"
            )
            self.fts_available = True
        except sqlite3.OperationalError:
            self.fts_available = False
        self.connection.commit()

    @staticmethod
    def _json(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)

    def upsert_source(self, source: Source) -> str:
        existing = self.connection.execute(
            "SELECT source_id FROM sources WHERE dedupe_key = ?", (source.dedupe_key,)
        ).fetchone()
        if existing and existing["source_id"] != source.source_id:
            return str(existing["source_id"])
        self.connection.execute(
            """INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(source_id) DO UPDATE SET
               dedupe_key=excluded.dedupe_key, provider=excluded.provider,
               provider_id=excluded.provider_id, title=excluded.title,
               authors_json=excluded.authors_json, year=excluded.year, doi=excluded.doi,
               url=excluded.url, source_type=excluded.source_type,
               publication_status=excluded.publication_status, abstract=excluded.abstract,
               oa_url=excluded.oa_url, cited_by_count=excluded.cited_by_count,
               referenced_ids_json=excluded.referenced_ids_json, metadata_json=excluded.metadata_json""",
            (
                source.source_id, source.dedupe_key, source.provider, source.provider_id,
                source.title, self._json(source.authors), source.year, source.doi, source.url,
                source.source_type, source.publication_status, source.abstract, source.oa_url,
                source.cited_by_count, self._json(source.referenced_ids),
                self._json(source.metadata), source.created_at,
            ),
        )
        self.connection.commit()
        return source.source_id

    def upsert_document(self, document: Document) -> str:
        existing = self.connection.execute(
            "SELECT document_id FROM documents WHERE content_hash = ?", (document.content_hash,)
        ).fetchone()
        if existing and existing["document_id"] != document.document_id:
            return str(existing["document_id"])
        self.connection.execute(
            """INSERT INTO documents VALUES (?,?,?,?,?,?,?,?,?)
               ON CONFLICT(document_id) DO UPDATE SET title=excluded.title, content=excluded.content,
               locator=excluded.locator, mime_type=excluded.mime_type,
               metadata_json=excluded.metadata_json""",
            (
                document.document_id, document.source_id, document.title, document.content,
                document.locator, document.mime_type, document.content_hash,
                self._json(document.metadata), document.created_at,
            ),
        )
        if self.fts_available:
            self.connection.execute("DELETE FROM documents_fts WHERE document_id = ?", (document.document_id,))
            self.connection.execute(
                "INSERT INTO documents_fts(document_id,title,content) VALUES (?,?,?)",
                (document.document_id, document.title, document.content),
            )
        self.connection.commit()
        return document.document_id

    def upsert_evidence(self, evidence: ResearchEvidence) -> None:
        self.connection.execute(
            """INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(evidence_id) DO UPDATE SET passage=excluded.passage,
               locator=excluded.locator, polarity=excluded.polarity, score=excluded.score,
               metadata_json=excluded.metadata_json""",
            (
                evidence.evidence_id, evidence.source_id, evidence.document_id, evidence.claim_id,
                evidence.passage, evidence.locator, evidence.polarity.value,
                evidence.retrieval_query, evidence.score, evidence.source_quality,
                self._json(evidence.metadata), evidence.created_at,
            ),
        )
        self.connection.commit()

    def upsert_claim(self, claim: ResearchClaim) -> None:
        self.connection.execute(
            """INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?)
               ON CONFLICT(claim_id) DO UPDATE SET text=excluded.text, status=excluded.status,
               evidence_ids_json=excluded.evidence_ids_json,
               counterevidence_ids_json=excluded.counterevidence_ids_json,
               hypothesis_id=excluded.hypothesis_id, rationale=excluded.rationale,
               human_review_required=excluded.human_review_required""",
            (
                claim.claim_id, claim.text, claim.status.value,
                self._json(claim.evidence_ids), self._json(claim.counterevidence_ids),
                claim.hypothesis_id, claim.rationale, int(claim.human_review_required),
                claim.created_at,
            ),
        )
        self.connection.commit()

    def upsert_hypothesis(self, hypothesis: Hypothesis) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO hypotheses VALUES (?,?,?,?,?,?)",
            (
                hypothesis.hypothesis_id, hypothesis.text, hypothesis.rationale,
                hypothesis.status, self._json(hypothesis.linked_claim_ids), hypothesis.created_at,
            ),
        )
        self.connection.commit()

    def upsert_analysis(self, analysis: AnalysisArtifact) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO analyses VALUES (?,?,?,?,?,?,?,?,?)",
            (
                analysis.analysis_id, analysis.title, analysis.status.value, analysis.command,
                analysis.input_locator, analysis.output_locator, analysis.summary,
                self._json(analysis.metadata), analysis.created_at,
            ),
        )
        self.connection.commit()

    def log_action(self, action: ActionRecord) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO actions VALUES (?,?,?,?,?,?,?,?)",
            (
                action.action_id, action.action_type.value, action.status, action.target_id,
                action.provider, action.query, self._json(action.detail), action.created_at,
            ),
        )
        self.connection.commit()

    def add_edge(self, from_id: str, relation: str, to_id: str, metadata: dict[str, Any] | None = None) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO edges VALUES (?,?,?,?)",
            (from_id, relation, to_id, self._json(metadata or {})),
        )
        self.connection.commit()

    def search_documents(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        terms = [term for term in query.replace('"', ' ').split() if term]
        if not terms:
            return []
        rows: Iterable[sqlite3.Row]
        if self.fts_available:
            safe_query = " OR ".join(f'"{term.replace(chr(34), "")}"' for term in terms)
            try:
                rows = self.connection.execute(
                    """SELECT d.*, bm25(documents_fts) AS lexical_rank
                       FROM documents_fts JOIN documents d USING(document_id)
                       WHERE documents_fts MATCH ? ORDER BY lexical_rank LIMIT ?""",
                    (safe_query, limit),
                ).fetchall()
            except sqlite3.OperationalError:
                rows = []
        else:
            pattern = f"%{terms[0]}%"
            rows = self.connection.execute(
                "SELECT *, 0.0 AS lexical_rank FROM documents WHERE title LIKE ? OR content LIKE ? LIMIT ?",
                (pattern, pattern, limit),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_document(self, document_id: str) -> dict[str, Any] | None:
        row = self.connection.execute("SELECT * FROM documents WHERE document_id = ?", (document_id,)).fetchone()
        return dict(row) if row else None

    def list_documents(self, limit: int = 200) -> list[dict[str, Any]]:
        return [dict(row) for row in self.connection.execute(
            "SELECT *, 0.0 AS lexical_rank FROM documents ORDER BY created_at DESC, document_id LIMIT ?",
            (limit,),
        ).fetchall()]

    def get_source(self, source_id: str) -> dict[str, Any] | None:
        row = self.connection.execute("SELECT * FROM sources WHERE source_id = ?", (source_id,)).fetchone()
        return dict(row) if row else None

    def evidence_for_claim(self, claim_id: str) -> list[ResearchEvidence]:
        rows = self.connection.execute("SELECT * FROM evidence WHERE claim_id = ?", (claim_id,)).fetchall()
        return [self._evidence_from_row(row) for row in rows]

    def graph_neighbors(self, ids: Iterable[str]) -> set[str]:
        values = list(dict.fromkeys(ids))
        if not values:
            return set()
        placeholders = ",".join("?" for _ in values)
        rows = self.connection.execute(
            f"SELECT from_id,to_id FROM edges WHERE from_id IN ({placeholders}) OR to_id IN ({placeholders})",
            values + values,
        ).fetchall()
        return {str(value) for row in rows for value in (row["from_id"], row["to_id"])} - set(values)

    def successful_actions(self, action_type: ActionType, target_id: str | None = None) -> list[dict[str, Any]]:
        sql = "SELECT * FROM actions WHERE action_type = ? AND status = 'SUCCESS'"
        params: list[Any] = [action_type.value]
        if target_id is not None:
            sql += " AND target_id = ?"
            params.append(target_id)
        return [dict(row) for row in self.connection.execute(sql, params).fetchall()]

    def export_jsonl(self, table: str, path: str | Path) -> Path:
        allowed = {"sources", "documents", "evidence", "claims", "hypotheses", "analyses", "actions", "edges"}
        if table not in allowed:
            raise ValueError(f"Unsupported export table: {table}")
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        rows = self.connection.execute(f"SELECT * FROM {table}").fetchall()
        output.write_text(
            "".join(json.dumps(dict(row), ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )
        return output

    def export_markdown_ledger(self, path: str | Path) -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        rows = self.connection.execute(
            "SELECT evidence_id,claim_id,polarity,locator,passage,source_id FROM evidence ORDER BY evidence_id"
        ).fetchall()
        lines = ["# Evidence Ledger", "", "| Evidence | Claim | Polarity | Source | Locator | Passage |", "|---|---|---|---|---|---|"]
        for row in rows:
            passage = str(row["passage"]).replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {row['evidence_id']} | {row['claim_id'] or ''} | {row['polarity']} | {row['source_id']} | {row['locator']} | {passage} |")
        output.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return output

    @staticmethod
    def _evidence_from_row(row: sqlite3.Row) -> ResearchEvidence:
        return ResearchEvidence(
            evidence_id=row["evidence_id"], source_id=row["source_id"],
            document_id=row["document_id"], claim_id=row["claim_id"], passage=row["passage"],
            locator=row["locator"], polarity=EvidencePolarity(row["polarity"]),
            retrieval_query=row["retrieval_query"], score=row["score"],
            source_quality=row["source_quality"], metadata=json.loads(row["metadata_json"]),
            created_at=row["created_at"],
        )
