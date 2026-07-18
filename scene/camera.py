"""Camera — định nghĩa góc nhìn cho renderer."""

from __future__ import annotations
from core.vector import Vector3
from core.matrix import Matrix4


class Camera:
    """Camera với vị trí, hướng nhìn, góc FOV."""

    def __init__(
        self,
        position: Vector3 | None = None,
        target: Vector3 | None = None,
        up: Vector3 | None = None,
        fov: float = 60.0,
    ) -> None:
        self.position: Vector3 = position if position is not None else Vector3(0, 0, 5)
        self.target: Vector3 = target if target is not None else Vector3(0, 0, 0)
        self.up: Vector3 = up if up is not None else Vector3(0, 1, 0)
        self.fov: float = fov

    def get_view_matrix(self) -> Matrix4:
        """Trả về ma trận view (look-at)."""
        raise NotImplementedError("TODO: Phase 2 — camera view matrix")

    def get_projection_matrix(self, aspect: float, near: float = 0.1, far: float = 100.0) -> Matrix4:
        """Trả về ma trận chiếu phối cảnh (perspective).

        Args:
            aspect: Tỉ lệ chiều rộng / chiều cao (width/height).
            near, far: Khoảng clipping plane gần và xa.
        """
        raise NotImplementedError("TODO: Phase 2 — camera projection matrix")