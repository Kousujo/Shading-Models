"""Vector3 — Đại diện cho vector/điểm trong không gian 3D.

Không implement toán thật (để trống / raise NotImplementedError).
"""

from __future__ import annotations
from typing import Union


class Vector3:
    """Vector 3 thành phần (x, y, z)."""

    __slots__ = ("x", "y", "z")

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: Vector3) -> Vector3:
        """Cộng hai vector."""
        raise NotImplementedError("TODO: Phase 1 — vector addition")

    def __sub__(self, other: Vector3) -> Vector3:
        """Trừ hai vector."""
        raise NotImplementedError("TODO: Phase 1 — vector subtraction")

    def dot(self, other: Vector3) -> float:
        """Tích vô hướng (dot product)."""
        raise NotImplementedError("TODO: Phase 1 — dot product")

    def cross(self, other: Vector3) -> Vector3:
        """Tích có hướng (cross product)."""
        raise NotImplementedError("TODO: Phase 1 — cross product")

    def length(self) -> float:
        """Độ dài vector (magnitude)."""
        raise NotImplementedError("TODO: Phase 1 — vector length")

    def normalize(self) -> Vector3:
        """Trả về vector đơn vị cùng hướng (unit vector)."""
        raise NotImplementedError("TODO: Phase 1 — vector normalize")