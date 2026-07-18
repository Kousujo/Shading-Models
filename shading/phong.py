"""Phong Shading — nội suy pháp tuyến, tính màu từng pixel."""

from __future__ import annotations
from shading.base import ShadingStrategy
from core.vector import Vector3


class PhongShading(ShadingStrategy):
    """Phong shading: nội suy pháp tuyến trong tam giác, tính màu per-pixel."""

    def shade(
        self,
        vertex: Vector3,
        normal: Vector3,
        light_dir: Vector3,
        view_dir: Vector3,
    ) -> float:
        raise NotImplementedError("TODO: Phase 7 — Phong shading")