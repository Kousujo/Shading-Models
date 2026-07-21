from abc import ABC, abstractmethod
from core.vector import Vector3

RGB = tuple[int, int, int]


def scale_color(color: RGB, factor: float) -> RGB:
    """Nhân màu theo hệ số cường độ sáng, luôn trả về đúng 3 phần tử."""
    factor = max(0.0, min(1.0, factor))
    r, g, b = color
    return (int(r * factor), int(g * factor), int(b * factor))


class ShadingStrategy(ABC):
    @abstractmethod
    def shade(self, position: Vector3, normal: Vector3, light, eye: Vector3) -> RGB:
        ...