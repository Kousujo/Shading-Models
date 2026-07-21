from geometry.mesh import Vertex, Face, Mesh
from core.vector import Vector3


def create_cube(size: float = 2.0) -> Mesh:
    h = size / 2
    positions = [
        Vector3(-h, -h, -h), Vector3(h, -h, -h),   # 0, 1
        Vector3(h, h, -h), Vector3(-h, h, -h),      # 2, 3
        Vector3(-h, -h, h), Vector3(h, -h, h),       # 4, 5
        Vector3(h, h, h), Vector3(-h, h, h),          # 6, 7
    ]
    vertices = [Vertex(p) for p in positions]
    faces = [
        Face(4, 5, 6), Face(4, 6, 7),   # trước (+Z)
        Face(1, 0, 3), Face(1, 3, 2),    # sau   (-Z)
        Face(5, 1, 2), Face(5, 2, 6),     # phải  (+X)
        Face(0, 4, 7), Face(0, 7, 3),      # trái  (-X)
        Face(3, 7, 6), Face(3, 6, 2),       # trên  (+Y)
        Face(0, 1, 5), Face(0, 5, 4),        # dưới  (-Y)
    ]
    return Mesh(vertices, faces)