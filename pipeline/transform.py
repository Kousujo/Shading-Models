"""TransformPipeline — áp dụng Model / View / Projection lên mesh.

Không implement (để trống / raise NotImplementedError).
"""

from __future__ import annotations
from geometry.mesh import Mesh
from core.matrix import Matrix4


class TransformPipeline:
    """Pipeline biến đổi: Model → World, View, Projection."""

    def apply(self, mesh: Mesh, model: Matrix4, view: Matrix4, projection: Matrix4) -> Mesh:
        """Biến đổi toàn bộ đỉnh của mesh qua pipeline.

        Args:
            mesh: Mesh đầu vào (object-space).
            model: Ma trận model (object → world).
            view: Ma trận view (world → camera).
            projection: Ma trận chiếu (camera → clip space).

        Returns:
            Mesh: Mesh sau biến đổi.
        """
        raise NotImplementedError("TODO: Phase 4 — transform pipeline")