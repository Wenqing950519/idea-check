import unittest

from src.claim_atomizer import ClaimAtomizer
from src.models import Claim


class AtomizationTests(unittest.TestCase):
    def test_keeps_parent_and_builds_explicit_dependencies(self) -> None:
        parent = Claim.from_dict({
            "claim_id": "C-010",
            "parent_id": None,
            "source_location": "section-1:p1",
            "original_text": "系統 A 使用索引資料，而且結構化資料直接提高引用率。",
            "atomic_claim": "系統 A 使用索引資料，而且結構化資料直接提高引用率。",
            "claim_type": "CAUSAL",
            "verification_required": True,
            "dependencies": [],
            "author_assertion_level": "strong",
            "risk_flags": ["CAUSAL_LANGUAGE"]
        })
        result = ClaimAtomizer().atomize(parent)
        self.assertEqual(result.parent.claim_id, "C-010")
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.parent.dependencies, ["C-010-A", "C-010-B"])
        self.assertTrue(all(child.parent_id == "C-010" for child in result.children))


if __name__ == "__main__":
    unittest.main()
