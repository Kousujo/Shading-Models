from abc import ABC, abstractmethod
from core.vector import Vector3

RGB = tuple[int, int, int]


def scale_color(color: RGB, factor: float) -> RGB:
    """Nhân màu theo hệ số cường độ sáng, luôn trả về đúng 3 phần tử."""
    factor = max(0.0, min(1.0, factor))
    r, g, b = color
    return (int(r * factor), int(g * factor), int(b * factor))


def lambert_intensity(position: Vector3, normal: Vector3, light, ambient: float) -> float:
    """Cường độ Lambert (ambient + diffuse) cho 1 điểm. Dùng chung cho Flat, Gouraud, Phong."""
    to_light = (light.position - position).normalize()
    diffuse = max(0.0, normal.dot(to_light))
    return min(1.0, ambient + (1 - ambient) * diffuse * light.intensity)


class ShadingStrategy(ABC):
    per_vertex: bool = False  # True nếu cần đánh giá tại từng đỉnh (Gouraud) thay vì 1 lần/mặt (Flat)
    per_pixel: bool = False   # True nếu cần tính màu tại từng pixel (Phong/Blinn-Phong)

    @abstractmethod
    def shade(self, position: Vector3, normal: Vector3, light, eye: Vector3) -> RGB:
        ...