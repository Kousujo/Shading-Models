"""Rasterizer — vẽ tam giác trên framebuffer.

Không implement thuật toán (để trống / raise NotImplementedError).
"""

from __future__ import annotations
from typing import Optional
from shading.base import ShadingStrategy
from core.vector import Vector3
from rasterizer.zbuffer import ZBuffer


class Rasterizer:
    """Rasterizer vẽ tam giác lên framebuffer với z-buffer."""

    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.zbuffer: ZBuffer = ZBuffer(width, height)

    def draw_triangle(
        self,
        v0: Vector3,
        v1: Vector3,
        v2: Vector3,
        shading_strategy: Optional[ShadingStrategy] = None,
    ) -> None:
        """Vẽ một tam giác với thuật toán rasterize (scanline hoặc barycentric).

        Args:
            v0, v1, v2: Ba đỉnh tam giác sau biến đổi projection.
            shading_strategy: Strategy tô bóng (None → wireframe hoặc màu mặc định).
        """
        raise NotImplementedError("TODO: Phase 4 — triangle rasterization")