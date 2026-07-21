from shading.base import ShadingStrategy, scale_color, RGB
from core.vector import Vector3


class FlatShading(ShadingStrategy):
    """1 màu duy nhất cho cả mặt: Lambert (N.L) + ambient."""

    def __init__(self, base_color: RGB = (200, 200, 200), ambient: float = 0.15):
        self.base_color = base_color
        self.ambient = ambient

    def shade(self, position: Vector3, normal: Vector3, light, eye: Vector3) -> RGB:
        to_light = (light.position - position).normalize()
        diffuse = max(0.0, normal.dot(to_light))
        intensity = self.ambient + (1 - self.ambient) * diffuse * light.intensity
        return scale_color(self.base_color, intensity)