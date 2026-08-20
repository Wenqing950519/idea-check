from .models import Claim, ClaimType, SearchIntent, SearchTask, VerificationPlan


class VerificationPlanner:
    """Build balanced search tasks; never frame the goal as proving the author."""

    def plan(self, claim: Claim, max_search_budget: int = 5) -> VerificationPlan:
        quoted = f'"{claim.atomic_claim}"'
        intents = [
            (SearchIntent.SUPPORT, quoted),
            (SearchIntent.DIRECT_SOURCE, f"{quoted} original study official source"),
            (SearchIntent.CONTRADICTION, f"{quoted} contradiction no effect limitations"),
            (SearchIntent.BOUNDARY, f"{quoted} boundary conditions population timeframe"),
        ]
        if claim.claim_type == ClaimType.CAUSAL:
            intents.append((SearchIntent.ALTERNATIVE_EXPLANATION, f"{quoted} alternative explanation confounding correlation"))
        tasks = [SearchTask(claim.claim_id, intent, query, index + 1) for index, (intent, query) in enumerate(intents)]
        return VerificationPlan(claim.claim_id, tasks[:max_search_budget], max_search_budget)
