from __future__ import annotations

from typing import Optional, Any, Tuple
import random

from environment.cell import Cell


class Grid:
    """2D wraparound grid. One occupant per cell (simple + clear for marking)."""

    def __init__(self, width: int, height: int, rng: Optional[random.Random] = None):
        self.width = max(20, width)
        self.height = max(20, height)
        self.rng = rng or random.Random()

        self.cells = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]

    def wrap(self, x: int, y: int) -> Tuple[int, int]:
        return x % self.width, y % self.height

    def get_cell(self, x: int, y: int) -> Cell:
        x, y = self.wrap(x, y)
        return self.cells[y][x]

    def get_occupant(self, x: int, y: int) -> Optional[Any]:
        return self.get_cell(x, y).occupant

    def place(self, entity: Any, x: int, y: int) -> None:
        x, y = self.wrap(x, y)
        cell = self.get_cell(x, y)
        if cell.occupant is not None:
            raise ValueError(f"Cell ({x},{y}) is occupied by {cell.occupant}.")
        cell.occupant = entity
        entity.x, entity.y = x, y

    def move(self, entity: Any, new_x: int, new_y: int) -> bool:
        new_x, new_y = self.wrap(new_x, new_y)
        dest = self.get_cell(new_x, new_y)
        if dest.occupant is not None:
            return False

        src = self.get_cell(entity.x, entity.y)
        src.occupant = None
        dest.occupant = entity
        entity.x, entity.y = new_x, new_y
        return True

    @staticmethod
    def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)

