from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import random

from agents.agent import Agent


@dataclass
class Predator(Agent):
    honour: int = 0
    patrol_style: str = "random"
    rng: Optional[random.Random] = None

    def __init__(self, name: str, patrol_style: str = "random", rng: Optional[random.Random] = None):
        super().__init__(name=name, health=120, stamina=80)
        self.honour = 0
        self.patrol_style = patrol_style
        self.rng = rng or random.Random()
        self._patrol_phase = 0

    def act(self, sim):
        # Default predators just patrol (Dek overrides)
        self.patrol(sim)
        return None

    def patrol(self, sim) -> None:
        if not self.spend_stamina(1):
            self.recover(2)
            self.log_action("rest")
            return

        # Two styles: random or square path (shows design choice)
        if self.patrol_style == "square":
            moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            dx, dy = moves[self._patrol_phase % 4]
            # linger then rotate
            if self.rng.random() < 0.3:
                self._patrol_phase += 1
        else:
            dx, dy = self.rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        moved = sim.grid.move(self, self.x + dx, self.y + dy)
        if moved:
            self.log_action("patrol")
        else:
            self.log_action("blocked")

    def is_alive(self) -> bool:
        return self.health > 0
