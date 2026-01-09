from __future__ import annotations

from enum import Enum


class HonourEvent(Enum):
    # Positive / worthy actions
    FIGHT_WORTHY = 1
    DEFEAT_BOSS = 2
    SURVIVE_CLAN_CHALLENGE = 3
    AID_ALLY = 4
    REST_DISCIPLINE = 5

    # Negative / dishonourable actions
    RETREAT = 10
    BREAK_CODE = 11
    DIE_DISHONOUR = 12


class HonourSystem:
    """
    Simple, transparent scoring model (easy to explain in report):
    - Rewards worthy hunts and success against the adversary
    - Penalises retreat, breaking code, and dishonour
    """

    def delta(self, event: HonourEvent) -> int:
        table = {
            HonourEvent.FIGHT_WORTHY: +3,
            HonourEvent.DEFEAT_BOSS: +25,
            HonourEvent.SURVIVE_CLAN_CHALLENGE: +6,
            HonourEvent.AID_ALLY: +4,
            HonourEvent.REST_DISCIPLINE: +1,
            HonourEvent.RETREAT: -4,
            HonourEvent.BREAK_CODE: -10,
            HonourEvent.DIE_DISHONOUR: -20,
        }
        return table.get(event, 0)
