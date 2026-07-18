"""Mesh & các thành phần liên quan: Vertex, Face, Mesh.

Không implement logic hình học (để trống / raise NotImplementedError).
"""

from __future__ import annotations
from typing import List, Tuple, Optional
from core.vector import Vector3


class Vertex:
    """Đỉnh với vị trí và pháp tuyến."""

    __slots__ = ("position", "normal")

    def __init__(self, position: Vector3, normal: Optional[Vector3] = None) -> None:
        self.position: Vector3 = position
        self.normal: Vector3 = normal if normal is not None else Vector3(0, 0, 0)


class Face:
    """Mặt tam giác — lưu chỉ số của 3 đỉnh."""

    __slots__ = ("indices",)

    def __init__(self, i0: int, i1: int, i2: int) -> None:
        self.indices: Tuple[int, int, int] = (i0, i1, i2)


class Mesh:
    """Lưới 3D gồm danh sách đỉnh và danh sách mặt."""

    __slots__ = ("vertices", "faces")

    def __init__(self) -> None:
        self.vertices: List[Vertex] = []
        self.faces: List[Face] = []