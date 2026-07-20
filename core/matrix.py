# core/matrix.py
from __future__ import annotations
import math
import numpy as np

from core.vector import Vector3


class Matrix4:
    """
    Ma trận biến đổi 4x4 theo đúng quy ước giáo trình (Chương 5.1, 6.1):
    - Điểm là vector HÀNG dạng thuần nhất (x, y, z, 1)
    - Áp dụng biến đổi bằng cách nhân bên phải: X' = X . M
    - Tịnh tiến nằm ở HÀNG cuối (không phải cột cuối như convention OpenGL)
    - Ghép nhiều phép biến đổi: M = M1 . M2 nghĩa là áp M1 trước, M2 sau
      (đúng thứ tự đọc trái sang phải, khác với kiểu M2.M1.v hay gặp ở tài liệu khác)
    """

    __slots__ = ("data",)

    def __init__(self, data: np.ndarray):
        assert data.shape == (4, 4)
        self.data = data

    @staticmethod
    def identity() -> "Matrix4":
        return Matrix4(np.identity(4))

    @staticmethod
    def translation(tx: float, ty: float, tz: float) -> "Matrix4":
        m = np.identity(4)
        m[3, 0], m[3, 1], m[3, 2] = tx, ty, tz
        return Matrix4(m)

    @staticmethod
    def scale(sx: float, sy: float, sz: float) -> "Matrix4":
        m = np.identity(4)
        m[0, 0], m[1, 1], m[2, 2] = sx, sy, sz
        return Matrix4(m)

    @staticmethod
    def rotation_x(theta: float) -> "Matrix4":
        c, s = math.cos(theta), math.sin(theta)
        m = np.identity(4)
        m[1, 1], m[1, 2] = c, s
        m[2, 1], m[2, 2] = -s, c
        return Matrix4(m)

    @staticmethod
    def rotation_y(theta: float) -> "Matrix4":
        c, s = math.cos(theta), math.sin(theta)
        m = np.identity(4)
        m[0, 0], m[0, 2] = c, -s
        m[2, 0], m[2, 2] = s, c
        return Matrix4(m)

    @staticmethod
    def rotation_z(theta: float) -> "Matrix4":
        c, s = math.cos(theta), math.sin(theta)
        m = np.identity(4)
        m[0, 0], m[0, 1] = c, s
        m[1, 0], m[1, 1] = -s, c
        return Matrix4(m)

    def __matmul__(self, other: "Matrix4") -> "Matrix4":
        return Matrix4(self.data @ other.data)

    def transform_point(self, v: Vector3) -> Vector3:
        row = np.array([v.x, v.y, v.z, 1.0])
        result = row @ self.data
        return Vector3(result[0], result[1], result[2])

    def __repr__(self) -> str:
        return f"Matrix4(\n{self.data}\n)"
    
if __name__ == "__main__":
    x_axis, y_axis, z_axis = Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1)
    r = Matrix4.rotation_z(math.pi / 2).transform_point(x_axis)
    assert r == y_axis, r          # quay X quanh Z 90° -> Y
    r = Matrix4.rotation_x(math.pi / 2).transform_point(y_axis)
    assert r == z_axis, r          # quay Y quanh X 90° -> Z
    r = Matrix4.rotation_y(math.pi / 2).transform_point(z_axis)
    assert r == x_axis, r          # quay Z quanh Y 90° -> X

    t = Matrix4.translation(1, 2, 3).transform_point(Vector3(0, 0, 0))
    assert t == Vector3(1, 2, 3), t
    print("Matrix4 OK")