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

@dataclass
class WireframeModel:
    """Đúng cấu trúc 'mô hình WireFrame' mục 6.5.1 giáo trình: chỉ đỉnh + cạnh, không có mặt."""
    vertices: List[Vertex]
    edges: List[Tuple[int, int]]

def face_normal(p0: Vector3, p1: Vector3, p2: Vector3) -> Vector3:
    """Pháp tuyến mặt từ 3 điểm, theo thứ tự đỉnh CCW nhìn từ ngoài vào."""
    return (p1 - p0).cross(p2 - p0).normalize()


def compute_vertex_normals(mesh: "Mesh") -> None:
    """Pháp tuyến đỉnh = trung bình pháp tuyến các mặt kề, rồi normalize.
    Ghi trực tiếp vào Vertex.normal (mutate mesh tại chỗ), tính 1 lần khi load mesh."""
    accum = [Vector3(0, 0, 0) for _ in mesh.vertices]
    for face in mesh.faces:
        a, b, c = face.indices()
        p0, p1, p2 = mesh.vertices[a].position, mesh.vertices[b].position, mesh.vertices[c].position
        n = face_normal(p0, p1, p2)
        accum[a] += n
        accum[b] += n
        accum[c] += n
    for i, v in enumerate(mesh.vertices):
        v.normal = accum[i].normalize()