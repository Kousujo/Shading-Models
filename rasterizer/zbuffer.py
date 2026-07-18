"""ZBuffer — depth-buffer để khử mặt khuất.

Không implement (để trống / raise NotImplementedError).
"""

from __future__ import annotations


class ZBuffer:
    """Quản lý depth buffer — so sánh độ sâu trước khi vẽ pixel."""

    def __init__(self, width: int, height: int) -> None:
        """Khởi tạo buffer kích thước width × height."""
        raise NotImplementedError("TODO: Phase 4 — z-buffer init")

    def test_and_set(self, x: int, y: int, depth: float) -> bool:
        """Kiểm tra độ sâu tại (x, y).

        Args:
            x, y: Toạ độ pixel.
            depth: Độ sâu cần kiểm tra.

        Returns:
            True nếu pixel gần hơn (depth < buffer hiện tại), False nếu bị che.
        """
        raise NotImplementedError("TODO: Phase 4 — z-buffer test_and_set")