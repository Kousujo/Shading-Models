"""Rasterize 1 tri giác bằng toạ độ trọng tâm. Không biết gì về world frame —
chỉ nhận toạ độ MÀN HÌNH + độ sâu từng đỉnh, và 1 hàm shade_fn(w0,w1,w2)->RGB
để tô màu từng pixel. Thiết kế vậy để Gouraud/Phong ở giai đoạn sau chỉ cần
đổi shade_fn, không phải viết lại phần rasterize.

Lưu ý: framebuffer là numpy array shape (WIDTH, HEIGHT, 3) dtype uint8 —
ghi pixel bằng indexing, không dùng pygame.Surface.set_at() (quá chậm)."""

import numpy as np

class Rasterizer:
    def __init__(self, framebuffer: np.ndarray, zbuffer):
        self.framebuffer = framebuffer   # numpy array (width, height, 3), uint8
        self.zbuffer = zbuffer

    def draw_triangle_flat(self, screen_pts, depths, color: tuple[int, int, int]) -> None:
        """Vẽ tam giác 1 màu bằng numpy, không lặp Python theo từng pixel.
        ponytail: giả định màu không đổi trong cả tam giác (đúng cho Flat).
        Gouraud/Phong (màu đổi theo từng pixel) sẽ cần cách khác, chưa giải quyết ở đây."""
        (x0, y0), (x1, y1), (x2, y2) = screen_pts
        min_x = max(int(min(x0, x1, x2)), 0)
        max_x = min(int(max(x0, x1, x2)), self.zbuffer.width - 1)
        min_y = max(int(min(y0, y1, y2)), 0)
        max_y = min(int(max(y0, y1, y2)), self.zbuffer.height - 1)
        if max_x < min_x or max_y < min_y:
            return

        area = self._edge(x0, y0, x1, y1, x2, y2)
        if area == 0:
            return

        xs = np.arange(min_x, max_x + 1) + 0.5
        ys = np.arange(min_y, max_y + 1) + 0.5
        px, py = np.meshgrid(xs, ys, indexing="ij")   # lưới toạ độ cả vùng, tính 1 lần

        w0 = self._edge(x1, y1, x2, y2, px, py) / area
        w1 = self._edge(x2, y2, x0, y0, px, py) / area
        w2 = self._edge(x0, y0, x1, y1, px, py) / area
        inside = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not np.any(inside):
            return

        depth = w0 * depths[0] + w1 * depths[1] + w2 * depths[2]
        zbuf_region = self.zbuffer.buffer[min_x:max_x + 1, min_y:max_y + 1]
        closer = inside & (depth > zbuf_region)
        if not np.any(closer):
            return

        zbuf_region[closer] = depth[closer]
        self.framebuffer[min_x:max_x + 1, min_y:max_y + 1][closer] = color

    @staticmethod
    def _edge(ax, ay, bx, by, cx, cy):
        return (cx - ax) * (by - ay) - (cy - ay) * (bx - ax)