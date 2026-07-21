# So sánh các mô hình tô bóng (Shading Models)

## Mục tiêu

Xây dựng **software renderer** từ đầu bằng **Python thuần** (KHÔNG dùng OpenGL/GLSL)
để cài đặt và so sánh 4 mô hình tô bóng:

1. **Flat Shading** — tô phẳng, toàn mặt một màu ✅
2. **Gouraud Shading** — nội suy màu đỉnh 🔜
3. **Phong Shading** — nội suy pháp tuyến, tính màu per-pixel 🔜
4. **Blinn-Phong Shading** — biến thể dùng half-vector 🔜

Đồ án cuối kỳ môn **Đồ hoạ máy tính** (báo cáo dự kiến 11–12/8/2026).

## Tính năng đã cài đặt (Phase 2)

- ✅ **Vector3** — dot, cross, normalize, các phép toán cơ bản
- ✅ **Matrix4** — rotation (x/y/z), translation, scale, row-vector convention
- ✅ **Pipeline đồ hoạ** — model transform → perspective projection → rasterization
- ✅ **Rasterization** — tô tam giác bằng toạ độ trọng tâm (barycentric)
- ✅ **Z-buffer** — khử mặt khuất
- ✅ **Wireframe** — hiển thị khung lưới xanh
- ✅ **Flat Shading** — Lambert diffuse + ambient light
- ✅ **12 mô hình 3D** — 5 khối đa diện đều + 7 mặt tham số (xem danh sách bên dưới)
- ✅ **Control Panel** (pygame_gui):
  - Chọn shading mode (Wireframe / Flat)
  - Chọn mô hình 3D (dropdown)
  - Slider tốc độ xoay
  - Slider khoảng cách camera

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
├── FlatShading          ✅ Hoàn thành
├── GouraudShading       🔜 Stub — chờ implement
├── PhongShading         🔜 Stub — chờ implement
└── BlinnPhongShading    🔜 Stub — chờ implement
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
│   └── ui.py       # ControlPanel — pygame_gui dropdowns + sliders
├── models/         # .txt files — platonic solids (tetrahedron, cube...)
├── raytracer/      # (tuỳ chọn, giai đoạn sau)
├── main.py         # Entry point
├── requirements.txt
├── README.md
└── .gitignore
```

### Danh sách mô hình 3D

| Mô hình | Loại | Vertex |
|---------|------|--------|
| Tetrahedron | Khối đa diện đều (4 mặt) | 4 |
| Cube | Khối đa diện đều (6 mặt) | 8 |
| Octahedron | Khối đa diện đều (8 mặt) | 6 |
| Dodecahedron | Khối đa diện đều (12 mặt) | 20 |
| Icosahedron | Khối đa diện đều (20 mặt) | 12 |
| Sphere | Mặt tham số | 651 |
| Torus | Mặt tham số | 651 |
| Ellipsoid | Mặt tham số | 651 |
| Hyperboloid (Saddle) | Mặt tham số | 441 |
| Cylinder | Mặt tham số | 341 |
| Cone | Mặt tham số | 651 |
| Paraboloid | Mặt tham số | 651 |

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

### Điều khiển

- **Dropdown "Wireframe / Flat"** — chuyển chế độ hiển thị
- **Dropdown chọn mô hình** — chuyển đổi mô hình 3D
- **Slider "Rotation Speed"** — điều chỉnh tốc độ xoay
- **Slider "Camera Distance"** — phóng to / thu nhỏ (2.0–15.0)
- **Nút ✕ trên cửa sổ** — thoát

## Tiến độ phát triển

| Phase | Nội dung | Trạng thái |
|-------|----------|------------|
| Phase 0 | Scaffold project, venv, thư mục | ✅ |
| Phase 1 | Vector3, Matrix4, wireframe cube | ✅ |
| Phase 2 | Pipeline, rasterizer, Z-buffer, Flat shading, models, UI | ✅ |
| Phase 3 | Gouraud shading + vertex normals | 🔜 |
| Phase 4 | Phong shading | 🔜 |
| Phase 5 | Blinn-Phong shading | 🔜 |
| Phase 6 | Camera view/projection matrix, Scene quản lý | 🔜 |
| Phase 7 | So sánh, tinh chỉnh, báo cáo | 🔜 |

## Git Workflow

Mỗi giai đoạn là một commit riêng, message theo format `[Phase N] <mô tả ngắn>`.
Tag lớn: `v1-wireframe`, `v2-flat-shading`, `v3-gouraud`, `v4-phong`, `v5-blinn-phong`.

## Giấy phép

Dự án học tập cá nhân.
