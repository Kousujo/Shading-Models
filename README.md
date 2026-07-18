# So sánh các mô hình tô bóng (Shading Models)

## Mục tiêu

Xây dựng **software renderer** từ đầu bằng **Python thuần** (KHÔNG dùng OpenGL/GLSL)
để cài đặt và so sánh 4 mô hình tô bóng:

1. **Flat Shading** — tô phẳng, toàn mặt một màu
2. **Gouraud Shading** — nội suy màu đỉnh
3. **Phong Shading** — nội suy pháp tuyến, tính màu per-pixel
4. **Blinn-Phong Shading** — biến thể dùng half-vector

Đồ án cuối kỳ môn **Đồ hoạ máy tính** (báo cáo dự kiến 11–12/8/2026).

## Kiến trúc

### Vòng lặp chính (Game Loop)

```
initialize()
while running:
    handle_input()
    update(dt)
    render()
```

### Pipeline đồ hoạ (render)

```
Scene → Transform (Model/View/Projection) → Rasterizer (+Z-buffer) → Shading → Framebuffer
```

### Shading: Strategy Pattern

```
ShadingStrategy (abstract)
├── FlatShading
├── GouraudShading
├── PhongShading
└── BlinnPhongShading
```

## Cấu trúc thư mục

```
Shading-Models/
├── core/           # vector.py, matrix.py — toán thuần
├── geometry/       # mesh.py, primitives.py (cube, sphere...)
├── pipeline/       # transform.py — Model/View/Projection
├── rasterizer/     # rasterizer.py, zbuffer.py
├── shading/        # base.py + flat/gouraud/phong/blinn_phong.py
├── scene/          # camera.py, light.py, scene.py
├── app/            # application.py — game loop, input, Pygame
├── raytracer/      # (tuỳ chọn, giai đoạn sau)
├── main.py         # Entry point
├── requirements.txt
├── README.md
└── .gitignore
```

## Hướng dẫn cài đặt & chạy

### Yêu cầu

- Python 3.10+
- pip / venv

### Cài đặt

```bash
# Tạo virtual environment
python -m venv .venv

# Kích hoạt (Windows)
.venv\Scripts\activate
# Hoặc (macOS/Linux)
source .venv/bin/activate

# Cài dependencies
pip install -r requirements.txt
```

### Chạy

```bash
python main.py
```

> **Lưu ý:** `main.py` hiện chỉ mở cửa sổ Pygame với nền đen. Các chức năng
> tô bóng sẽ được thêm dần qua từng phase.

## Git Workflow

Mỗi giai đoạn là một commit riêng, message theo format `[Phase N] <mô tả ngắn>`.
Các tag lớn: `v1-wireframe`, `v2-flat-shading`, `v3-gouraud`, `v4-phong`, `v5-blinn-phong`.

## Giấy phép

Dự án học tập cá nhân.
