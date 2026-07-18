"""Blinn-Phong Shading — biến thể Phong dùng half-vector."""

from __future__ import annotations
from shading.base import ShadingStrategy
from core.vector import Vector3


class BlinnPhongShading(ShadingStrategy):
    """Blinn-Phong shading: thay góc phản xạ bằng half-vector giữa light & view."""

    def shade(
        self,
        vertex: Vector3,
        normal: Vector3,
        light_dir: Vector3,
        view_dir: Vector3,
    ) -> float:
        raise NotImplementedError("TODO: Phase 7 — Blinn-Phong shading")