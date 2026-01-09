from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PreyProfile:
    worthy: bool
    vulnerable: bool
    protected: bool


@dataclass(frozen=True)
class Judgement:
    should_challenge: bool
    message: str = ""


class ClanRules:
    """
    Encodes the Yautja Clan Code (brief page 8) in simple logic:
    - Hunt the worthy (worthy=True)
    - Do not harm the unworthy / protected targets
    - Challenges may occur if honour low or actions suspicious
    """

    def is_hunt_allowed(self, prey: PreyProfile) -> bool:
        if prey.protected:
            return False
        if not prey.worthy:
            return False
        if prey.vulnerable:
            return False
        return True

    def judge_dek(self, honour: int, last_actions: List[str]) -> Judgement:
        # If Dek repeatedly retreats or dishonour-attacks, clan pushes a challenge.
        recent = " ".join(last_actions[-5:])
        suspicious = ("retreat_exhausted" in recent) or ("dishonour_attack" in recent)

        if honour < -5 or suspicious:
            return Judgement(should_challenge=True, message="Your actions bring shame. Prove yourself.")
        if honour < 10:
            return Judgement(should_challenge=False, message="Improve your honour. Hunt the worthy.")
        return Judgement(should_challenge=False, message="Your path is acceptable. Continue the hunt.")
