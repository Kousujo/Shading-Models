from dataclasses import dataclass
from core.vector import Vector3


@dataclass
class Light:
    position: Vector3
    color: tuple[int, int, int] = (255, 255, 255)
    intensity: float = 1.0