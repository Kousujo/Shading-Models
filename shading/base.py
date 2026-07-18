"""ShadingStrategy — abstract base class cho Strategy Pattern.

Mỗi shading model kế thừa class này và implement shade().
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from core.vector import Vector3


class ShadingStrategy(ABC):
    """Interface cho các chiến lược tô bóng."""

    @abstractmethod
    def shade(
        self,
        vertex: Vector3,
        normal: Vector3,
        light_dir: Vector3,
        view_dir: Vector3,
    ) -> float:
        """Tính cường độ sáng tại một điểm.

        Args:
            vertex: Vị trí điểm cần tô (world space hoặc view space).
            normal: Pháp tuyến tại điểm đó.
            light_dir: Vector hướng đến nguồn sáng.
            view_dir: Vector hướng đến camera.

        Returns:
            float: Cường độ sáng (0.0 = tối, 1.0 = sáng nhất).
        """
        ...