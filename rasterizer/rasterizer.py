from typing import Callable, Tuple
import pygame

RGB = Tuple[int, int, int]
ScreenPoint = Tuple[float, float]


class Rasterizer:
    """Rasterize 1 tam giác bằng toạ độ trọng tâm. Không biết gì về world space -
    chỉ nhận toạ độ MÀN HÌNH + độ sâu từng đỉnh, và 1 hàm shade_fn(w0,w1,w2)->RGB
    để tô màu từng pixel. Thiết kế vậy để Gouraud/Phong ở giai đoạn sau chỉ cần
    đổi shade_fn, không phải viết lại phần rasterize."""

    def __init__(self, surface: pygame.Surface, zbuffer):
        self.surface = surface
        self.zbuffer = zbuffer

    def draw_triangle(
        self,
        screen_pts: Tuple[ScreenPoint, ScreenPoint, ScreenPoint],
        depths: Tuple[float, float, float],
        shade_fn: Callable[[float, float, float], RGB],
    ) -> None:
        (x0, y0), (x1, y1), (x2, y2) = screen_pts
        min_x = max(int(min(x0, x1, x2)), 0)
        max_x = min(int(max(x0, x1, x2)), self.zbuffer.width - 1)
        min_y = max(int(min(y0, y1, y2)), 0)
        max_y = min(int(max(y0, y1, y2)), self.zbuffer.height - 1)

        area = self._edge(x0, y0, x1, y1, x2, y2)
        if area == 0:
            return  # tam giác suy biến (3 điểm thẳng hàng)

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                px, py = x + 0.5, y + 0.5
                w0 = self._edge(x1, y1, x2, y2, px, py) / area
                w1 = self._edge(x2, y2, x0, y0, px, py) / area
                w2 = self._edge(x0, y0, x1, y1, px, py) / area
                if w0 < 0 or w1 < 0 or w2 < 0:
                    continue

                depth = w0 * depths[0] + w1 * depths[1] + w2 * depths[2]
                if self.zbuffer.test_and_set(x, y, depth):
                    self.surface.set_at((x, y), shade_fn(w0, w1, w2))

    @staticmethod
    def _edge(ax, ay, bx, by, cx, cy) -> float:
        return (cx - ax) * (by - ay) - (cy - ay) * (bx - ax)