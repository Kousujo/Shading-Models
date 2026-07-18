"""Primitives — hàm sinh khối cơ bản (cube, sphere, ...).

Trả về Mesh rỗng tạm thời; sẽ implement ở phase geometry.
"""

from __future__ import annotations
from geometry.mesh import Mesh


def create_cube() -> Mesh:
    """Tạo lưới hình lập phương.

    Returns:
        Mesh: Mesh rỗng (TODO: implement geometry).
    """
    raise NotImplementedError("TODO: Phase 3 — cube geometry")


def create_sphere(segments: int = 16) -> Mesh:
    """Tạo lưới hình cầu xấp xỉ bằng lưới tam giác.

    Args:
        segments: Số lát cắt (resolution) theo từng trục.

    Returns:
        Mesh: Mesh rỗng (TODO: implement geometry).
    """
    raise NotImplementedError("TODO: Phase 3 — sphere geometry")