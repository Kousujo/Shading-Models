"""Flat Shading — tô phẳng, toàn bộ mặt 1 màu."""

from __future__ import annotations
from shading.base import ShadingStrategy
from core.vector import Vector3


class FlatShading(ShadingStrategy):
    """Flat shading: dùng pháp tuyến mặt, tính 1 màu cho cả tam giác."""

    def shade(
        self,
        vertex: Vector3,
        normal: Vector3,
        light_dir: Vector3,
        view_dir: Vector3,
    ) -> float:
        raise NotImplementedError("TODO: Phase 5 — Flat shading")