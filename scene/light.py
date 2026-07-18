"""Light — nguồn sáng điểm (point light)."""

from __future__ import annotations
from core.vector import Vector3


class Light:
    """Nguồn sáng điểm đơn giản."""

    def __init__(
        self,
        position: Vector3 | None = None,
        color: tuple[float, float, float] = (1.0, 1.0, 1.0),
        intensity: float = 1.0,
    ) -> None:
        self.position: Vector3 = position if position is not None else Vector3(0, 5, 5)
        self.color: tuple[float, float, float] = color
        self.intensity: float = intensity