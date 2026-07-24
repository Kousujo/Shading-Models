"""Shading không tính ánh sáng — luôn 1 màu cố định. Dùng cho vật thể đại diện
(quả cầu ánh sáng...) không cần tuân N·L."""

from shading.base import ShadingStrategy, RGB
from core.vector import Vector3


class UnlitShading(ShadingStrategy):
    """Luôn trả về màu cố định, bỏ qua light/normal/eye."""

    def __init__(self, color: RGB = (255, 255, 180)):
        self.color = color

    def shade(self, position: Vector3, normal: Vector3, light, eye: Vector3) -> RGB:
        return self.color