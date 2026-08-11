---
name: internship-offer-decision
description: Make an actionable now decision for a university student choosing whether to accept a specific 3–6 month internship Offer after interviewing. Reconstruct the likely role, assess portable learning and resume outcomes, research only decision-changing claims, apply a conservative Base Case to missing evidence, and produce report.json, report.md, and a Traditional Chinese report.html brief. Use for small-company-first, role-first internship Offer choices with Company, Job Title, JD, interview notes, Offer terms, student background, or alternatives. Do not use for job search, resume editing, interview preparation, employer question lists, enterprise due diligence, or broad company risk investigations.
---

# Internship Offer Decision

Apply these hard constraints without exception unless the user explicitly says they have another company conversation or negotiation and asks for help using it:

1. **THE VERDICT MUST BE ACTIONABLE NOW.** Make a current `take`, `conditional_take`, or `decline` decision. Never use `preliminary_only`, `insufficient_information`, or defer the decision.
2. Do not ask the user to return to the company. Do not write employer questions, interview questions, Offer-before-confirmation lists, or “continue interviewing” advice.
3. Do not make the verdict depend on information that might be obtained later.
4. Do not refuse to decide because evidence is sparse. Sparse evidence lowers confidence and constrains the Base Case; it does not prevent the decision.

Answer one question: if the student commits the next 3–6 months now, what can they realistically take away, and is that return worth the time and real opportunity cost?

Read these references before producing a report:

- Read [references/methodology.md](references/methodology.md) to reconstruct the role and apply the Base Case.
- Read [references/scoring.md](references/scoring.md) before assigning scores or a verdict.
- Read [references/evidence.md](references/evidence.md) before researching or citing claims.
- Read [references/output-contract.md](references/output-contract.md) before writing `report.json`, `report.md`, or `report.html`.

## Interpret the available evidence

Use `input_level` only to communicate evidence coverage, never to gate action:

| Level | Available input | Effect |
| --- | --- | --- |
| `company_title` | Company + Job Title | Make the most conservative current decision with low confidence. |
| `jd` | Add JD | Reconstruct likely work and score the Base Case. |
| `interview` | Add interview notes/transcript | Improve role, manager, and operating-model assessment. |
| `full` | Add Offer terms, student background, and alternatives | Improve fit and opportunity-cost precision. |

Every report still contains a final verdict and five numeric scores. Do not invent facts to make an input level look richer.

## Apply the Base Case

Classify decision-relevant claims before scoring:

- **Confirmed:** include in the Base Case.
- **Plausible but unverified:** describe only as upside; do not use it to raise formal scores.
- **Unknown:** lower confidence. Where a high score requires the missing fact, use a conservative middle-to-low Base Case rather than assuming the best case.
- **Negative Evidence:** include directly in risk and Base Case.

Examples: absent mentor evidence does not prove no mentor exists, but it cannot earn a high mentorship assessment. Unproven ownership cannot earn high role-substance or resume-outcome credit. Missing metrics or portfolio rights lower confidence and bound outcome claims.

## Execute the core workflow

1. Reconstruct the intern’s likely work; do not repeat the JD.
2. Locate that work relative to the company’s core product, service delivery, customer value, or revenue flow.
3. Start the 3–6 month section with exactly three truthful, Base-Case resume experiences. For each, include a usable resume bullet, quantification clues the student can personally retain, and methods worth learning from. Then infer the remaining skills, projects, metrics, and artifacts.
4. Research only public claims that could change the decision. Stop when further research would not change the verdict.
5. Evaluate work degradation, learning stagnation, weak mentorship, unmeasurable outcomes, management risks, and opportunity cost. Make the verdict now from the Base Case.

Use these lenses when relevant:

- **Organizational Coherence:** legal/brand identity, Founder/CEO, location, team size, product, and recruiting story.
- **Labor Model:** how interns, contractors, freelancers, and remote juniors are used.
- **Autonomy ≠ Mentorship:** assess Ownership, Feedback, Mentorship, and Methodology independently.

Escalate into legal, financial, director, court, regulatory, or government-record research only when a concrete signal exists or it changes the Offer decision. Avoid exhaustive OSINT pipelines.

## Produce one source of truth

Create `report.json` first. It is the only source of truth; do not add claims to Markdown or HTML that are absent from JSON.

Run the required checks and render:

```bash
python scripts/validate_report.py report.json
python scripts/validate_report.py report.json --markdown report.md
python scripts/render_html.py report.json report.html
python scripts/validate_report.py report.json --markdown report.md --html report.html
```

Deliver `report.json`, `report.md`, and `report.html`. Include **主要決策不確定性** as an explanation of evidence gaps, score effects, and Base Case assumptions only. Do not present it as a list of questions or required user actions.
