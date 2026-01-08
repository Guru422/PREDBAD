from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List
import abc


@dataclass
class Agent(abc.ABC):
    name: str
    health: int
    stamina: int
    x: int = 0
    y: int = 0
    recent_actions: List[str] = field(default_factory=list)

    def log_action(self, action: str) -> None:
        self.recent_actions.append(action)
        # keep short history for clan judgement
        if len(self.recent_actions) > 10:
            self.recent_actions.pop(0)

    def spend_stamina(self, cost: int) -> bool:
        if self.stamina < cost:
            return False
        self.stamina -= cost
        return True

    def recover(self, amount: int) -> None:
        self.stamina = min(100, self.stamina + amount)

    @abc.abstractmethod
    def act(self, sim) -> Optional[object]:
        """Perform one turn. Can return an HonourEvent or None."""
        raise NotImplementedError
