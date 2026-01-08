from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple
import random

from agents.agent import Agent


@dataclass
class Monster(Agent):
    rng: Optional[random.Random] = None

    def __init__(self, name: str = "Monster", rng: Optional[random.Random] = None):
        super().__init__(name=name, health=60, stamina=100)
        self.rng = rng or random.Random()

    def act(self, sim):
        # Move randomly; if adjacent to Dek, attempt attack by stepping into Dek cell (blocked) -> attack
        dx, dy = self.rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nx, ny = sim.grid.wrap(self.x + dx, self.y + dy)

        if (nx, ny) == (sim.dek.x, sim.dek.y):
            # attack Dek
            sim.combat.hit(attacker=self, defender=sim.dek)
            self.log_action("attack_dek")
            return None

        moved = sim.grid.move(self, nx, ny)
        self.log_action("move" if moved else "blocked")
        return None


@dataclass
class Adversary(Monster):
    territory_radius: int = 3

    def __init__(self, rng: Optional[random.Random] = None):
        super().__init__(name="Ultimate Adversary", rng=rng)
        self.health = 220
        self.territory_radius = 3

    def act(self, sim, boss_center: Tuple[int, int]):
        # Boss slowly roams but not too far
        if sim.rng.random() < 0.5:
            return None

        dx, dy = sim.rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nx, ny = sim.grid.wrap(self.x + dx, self.y + dy)
        # Avoid moving into occupied cells
        sim.grid.move(self, nx, ny)
        self.log_action("roam")
        return None
