# core/vector.py
from __future__ import annotations
import math


class Vector3:
    """Vector 3 chiều - dùng cho pháp tuyến, hướng ánh sáng, hướng camera..."""

    __slots__ = ("x", "y", "z")

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __iadd__(self, other: "Vector3") -> "Vector3":
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other: "Vector3") -> "Vector3":
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, scalar: float) -> "Vector3":
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    __rmul__ = __mul__

    def dot(self, other: "Vector3") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector3") -> "Vector3":
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        return math.sqrt(self.dot(self))

    def normalize(self) -> "Vector3":
        l = self.length()
        if l == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / l, self.y / l, self.z / l)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3):
            return False
            
        return (math.isclose(self.x, other.x, abs_tol=1e-9) and
                math.isclose(self.y, other.y, abs_tol=1e-9) and
                math.isclose(self.z, other.z, abs_tol=1e-9))

    def __repr__(self) -> str:
        return f"Vector3({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"
    

if __name__ == "__main__":
    a = Vector3(1, 0, 0)
    b = Vector3(0, 1, 0)
    assert a.dot(b) == 0                   # vuông góc → dot = 0
    assert abs(Vector3(3, 4, 0).length() - 5.0) < 1e-9  # tam giác 3-4-5
    c = a.cross(b)
    assert (c.x, c.y, c.z) == (0, 0, 1)    # trục X cross trục Y = trục Z
    print("Vector3 OK") 