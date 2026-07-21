from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple

from core.vector import Vector3


@dataclass
class Vertex:
    position: Vector3
    normal: Optional[Vector3] = None  # để trống, sẽ tính ở Giai đoạn 3 (Gouraud)


@dataclass
class Face:
    a: int
    b: int
    c: int  # chỉ số 3 đỉnh trong Mesh.vertices, thứ tự CCW nhìn từ ngoài vào mặt

    def indices(self) -> Tuple[int, int, int]:
        return (self.a, self.b, self.c)


@dataclass
class Mesh:
    vertices: List[Vertex]
    faces: List[Face]