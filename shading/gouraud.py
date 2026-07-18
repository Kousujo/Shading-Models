"""Gouraud Shading — nội suy màu đỉnh, sau đó nội suy qua tam giác."""

from __future__ import annotations
from shading.base import ShadingStrategy
from core.vector import Vector3


class GouraudShading(ShadingStrategy):
    """Gouraud shading: tính màu tại từng đỉnh, nội suy màu trong tam giác."""

    def shade(
        self,
        vertex: Vector3,
        normal: Vector3,
        light_dir: Vector3,
        view_dir: Vector3,
    ) -> float:
        raise NotImplementedError("TODO: Phase 6 — Gouraud shading")