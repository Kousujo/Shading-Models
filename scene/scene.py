"""Scene — tập hợp tất cả đối tượng trong một cảnh."""

from __future__ import annotations
from typing import List
from geometry.mesh import Mesh
from scene.camera import Camera
from scene.light import Light


class Scene:
    """Quản lý danh sách mesh, camera, và nguồn sáng trong một cảnh."""

    def __init__(self) -> None:
        self.meshes: List[Mesh] = []
        self.camera: Camera = Camera()
        self.lights: List[Light] = []