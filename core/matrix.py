"""Matrix4 — Ma trận 4×4 cho các phép biến đổi đồng nhất (homogeneous transforms).

Không implement toán thật (để trống / raise NotImplementedError).
"""

from __future__ import annotations
import numpy as np
import numpy.typing as npt
from typing import Optional


class Matrix4:
    """Ma trận 4×4 lưu dưới dạng numpy ndarray shape (4,4)."""

    def __init__(self, data: Optional[npt.NDArray[np.float64]] = None) -> None:
        """Khởi tạo với mảng 4×4, mặc định là identity."""
        self.data: npt.NDArray[np.float64]

    @staticmethod
    def identity() -> Matrix4:
        """Ma trận đơn vị 4×4."""
        raise NotImplementedError("TODO: Phase 2 — identity matrix")

    @staticmethod
    def translation(tx: float, ty: float, tz: float) -> Matrix4:
        """Ma trận tịnh tiến theo vector (tx, ty, tz)."""
        raise NotImplementedError("TODO: Phase 2 — translation matrix")

    @staticmethod
    def rotation_x(angle_rad: float) -> Matrix4:
        """Ma trận quay quanh trục X."""
        raise NotImplementedError("TODO: Phase 2 — rotation X matrix")

    @staticmethod
    def rotation_y(angle_rad: float) -> Matrix4:
        """Ma trận quay quanh trục Y."""
        raise NotImplementedError("TODO: Phase 2 — rotation Y matrix")

    @staticmethod
    def rotation_z(angle_rad: float) -> Matrix4:
        """Ma trận quay quanh trục Z."""
        raise NotImplementedError("TODO: Phase 2 — rotation Z matrix")

    @staticmethod
    def scale(sx: float, sy: float, sz: float) -> Matrix4:
        """Ma trận tỉ lệ (scale)."""
        raise NotImplementedError("TODO: Phase 2 — scale matrix")

    @staticmethod
    def perspective(fov_rad: float, aspect: float, near: float, far: float) -> Matrix4:
        """Ma trận chiếu phối cảnh (perspective projection)."""
        raise NotImplementedError("TODO: Phase 2 — perspective matrix")

    @staticmethod
    def look_at(eye: "Vector3", target: "Vector3", up: "Vector3") -> Matrix4:
        """Ma trận view (look-at) từ vị trí camera, điểm nhìn và vector up."""
        raise NotImplementedError("TODO: Phase 2 — look-at matrix")