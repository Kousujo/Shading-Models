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

    def draw_triangle_gouraud(self, screen_pts, depths, vertex_colors) -> None:
        """Vẽ tam giác nội suy màu theo barycentric (Gouraud), vectorised numpy."""
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
        px, py = np.meshgrid(xs, ys, indexing="ij")

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

        c0, c1, c2 = np.array(vertex_colors[0]), np.array(vertex_colors[1]), np.array(vertex_colors[2])
        color = w0[..., None] * c0 + w1[..., None] * c1 + w2[..., None] * c2  # nội suy màu theo barycentric
        color = np.clip(color, 0, 255).astype(np.uint8)

        region = self.framebuffer[min_x:max_x + 1, min_y:max_y + 1]
        region[closer] = color[closer]

    def draw_triangle_phong(self, screen_pts, depths, world_pts, normals, shading_model, light, eye) -> None:
        """Vẽ tam giác với Phong shading: nội suy pháp tuyến + vị trí world-space,
        tính màu per-pixel bằng shade_array. Chỉ tính cho pixel vượt qua Z-test."""
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
        px, py = np.meshgrid(xs, ys, indexing="ij")

        w0 = self._edge(x1, y1, x2, y2, px, py) / area
        w1 = self._edge(x2, y2, x0, y0, px, py) / area
        w2 = self._edge(x0, y0, x1, y1, px, py) / area

        inside = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not np.any(inside):
            return

        depth = w0 * depths[0] + w1 * depths[1] + w2 * depths[2]
        zbuf_region = self.zbuffer.buffer[min_x:max_x + 1, min_y:max_y + 1]

        # Chỉ xử lý các pixel gần camera nhất (qua Z-test)
        closer = inside & (depth > zbuf_region)
        if not np.any(closer):
            return
        zbuf_region[closer] = depth[closer]

        # Trích xuất barycentric của CÁC PIXEL HỢP LỆ (shape: (K, 1))
        valid_w0 = w0[closer][..., None]
        valid_w1 = w1[closer][..., None]
        valid_w2 = w2[closer][..., None]

        # Chuyển đổi đỉnh và pháp tuyến sang numpy
        p0, p1, p2 = [np.array([p.x, p.y, p.z]) for p in world_pts]
        n0, n1, n2 = [np.array([n.x, n.y, n.z]) for n in normals]

        # Nội suy vị trí và pháp tuyến tại từng pixel
        interp_pos = valid_w0 * p0 + valid_w1 * p1 + valid_w2 * p2
        interp_norm = valid_w0 * n0 + valid_w1 * n1 + valid_w2 * n2

        # Tính màu sắc hàng loạt bằng Phong Shading
        colors = shading_model.shade_array(interp_pos, interp_norm, light, eye)

        # Gán màu vào framebuffer
        region = self.framebuffer[min_x:max_x + 1, min_y:max_y + 1]
        region[closer] = colors

    @staticmethod
    def _edge(ax, ay, bx, by, cx, cy):
        return (cx - ax) * (by - ay) - (cy - ay) * (bx - ax)