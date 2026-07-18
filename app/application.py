"""Application — Pygame game loop boilerplate.

Đây là boilerplate được phép viết đầy đủ (không phải thuật toán CG).
"""

from __future__ import annotations
import sys
import pygame


class Application:
    """Quản lý vòng lặp chính và cửa sổ Pygame."""

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: str = "Shading Models — Software Renderer",
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.title: str = title
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self.running: bool = False

    def _init_pygame(self) -> None:
        """Khởi tạo Pygame, cửa sổ, clock."""
        pygame.init()
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def _handle_events(self) -> None:
        """Xử lý sự kiện — hiện chỉ xử lý QUIT."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self, dt: float) -> None:
        """Cập nhật logic mỗi frame.

        Args:
            dt: Delta time (giây) từ frame trước.
        """
        pass  # TODO: Phase 4+ — cập nhật camera, object rotation, ...

    def _render(self) -> None:
        """Vẽ framebuffer lên màn hình (tạm thời: nền đen)."""
        # ponytail: clear screen to black each frame
        # Upgrade path: replace with full software rasterization pipeline
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def _cleanup(self) -> None:
        """Dọn dẹp trước khi thoát."""
        pygame.quit()

    def run(self) -> None:
        """Vòng lặp chính: init → handle events → update → render."""
        self._init_pygame()
        self.running = True

        while self.running:
            dt = self.clock.tick(60) / 1000.0  # seconds, cố định ~60 FPS
            self._handle_events()
            self._update(dt)
            self._render()

        self._cleanup()
        sys.exit()