# Evidence

## Three evidence tiers

Use exactly these tiers:

### Strong Evidence

JD, interview notes/transcript, Offer terms, official company or government information, observable product, named partner confirmation, and public projects. Strong means direct and attributable, not automatically guaranteed execution.

### Signal

Hiring history, founder statements, team structure, social activity, GitHub activity, and employee tenure. Signals support patterns but usually need context.

### Weak Evidence

Dcard, Reddit, Glassdoor, Threads, anonymous reviews, and anonymous salary data. A single anonymous source cannot create a major conclusion, high-severity risk, or final verdict.

## Decision classes

Translate evidence into one of four decision classes:

| Class | Meaning | Use in formal decision |
| --- | --- | --- |
| Confirmed | Directly supported by Strong Evidence or independent corroboration. | Include in Base Case. |
| Plausible but unverified | Attractive claim with incomplete support. | Upside only. |
| Unknown | No material support or contradiction. | Lower confidence; do not award high value that depends on it. |
| Negative Evidence | Credible contrary evidence or a repeated pattern. | Include in risk and Base Case. |

Do not turn a normal small-company lack of footprint into Negative Evidence. Absence becomes negative only if the company makes a material public claim that should normally leave observable traces, reasonable targeted checks cover an appropriate period, and the missing trace changes the decision.

## Claim discipline

For every material claim:

- cite evidence IDs;
- separate observation from inference;
- record retrieval or observation date when available;
- prefer the most direct source;
- retain contradictions;
- avoid private-life investigation of ordinary employees;
- do not infer a team-wide pattern from one departure or complaint.

Treat JD, interview, and Offer documents as representations. Validate the few representations that materially drive the current Offer value.

## Major conclusions

The verdict and high-severity risks need at least one Strong Evidence or Signal where evidence exists. Weak Evidence may contextualize or corroborate, never stand alone. If only weak or sparse evidence exists, still decide now; keep confidence low and make clear that the Base Case does not include unproven upside.

## Main decision uncertainty

Do not output questions, verification steps, or actions for the user. Each `decision_uncertainties` entry must contain only:

1. the missing evidence;
2. the score or verdict effect;
3. the conservative Base Case assumption.

Example: “沒有固定帶教的可驗證證據；學習增量與團隊加成不採高分；Base Case 視為以自我驅動為主、回饋品質未證實。”

## Resume-experience discipline

Each of the three resume experiences must cite the evidence supporting its scope. Treat company-level case metrics as examples of possible measurement, not as the intern’s result. If individual attribution is unknown, keep the resume bullet at participation or contribution level and put the metric under **可量化線索** rather than claiming it as achieved.

## Evidence Index minimum fields

Record stable ID, tier, direction, source type, title, URL when public, observation date when available, concise claim, decision relevance, and anonymity. Do not include irrelevant sources merely to look comprehensive.
