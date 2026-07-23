# So sánh các mô hình tô bóng (Shading Models)

## Mục tiêu

Xây dựng **software renderer** từ đầu bằng **Python thuần** (KHÔNG dùng OpenGL/GLSL)
để cài đặt và so sánh 4 mô hình tô bóng:

1. **Flat Shading** — tô phẳng, toàn mặt một màu ✅
2. **Gouraud Shading** — nội suy màu đỉnh ✅
3. **Phong Shading** — nội suy pháp tuyến per-pixel, specular Phong cổ điển (R·V)^α ✅
4. **Blinn-Phong Shading** — biến thể dùng half-vector (N·H)^α ✅

Đồ án cuối kỳ môn **Đồ hoạ máy tính** (báo cáo dự kiến 11–12/8/2026).

## Tính năng đã cài đặt

- ✅ **Vector3** — dot, cross, normalize, các phép toán cơ bản
- ✅ **Matrix4** — rotation (x/y/z), translation, scale, row-vector convention
- ✅ **Pipeline đồ hoạ** — model transform → perspective projection → rasterization
- ✅ **Rasterization** — tô tam giác bằng toạ độ trọng tâm (barycentric)
- ✅ **Z-buffer** — khử mặt khuất
- ✅ **Wireframe** — hiển thị khung lưới xanh (hỗ trợ cả Mesh và WireframeModel)
- ✅ **Flat Shading** — Lambert diffuse + ambient light
- ✅ **Gouraud Shading** — cùng Lambert, nhưng tính per-vertex rồi nội suy màu trong rasterizer
- ✅ **Dynamic lighting** — ánh sáng orbit quanh mô hình, minh hoạ N·L thay đổi theo thời gian thực
- ✅ **Trục toạ độ XYZ** — đỏ/xanh lá/xanh dương, xoay đồng bộ với vật thể
- ✅ **Phong Shading (cổ điển)** — specular dùng reflect vector R = 2(N·L)N − L, (R·V)^α
- ✅ **Blinn-Phong Shading** — specular dùng half-vector H = normalize(L+V), (N·H)^α (rẻ hơn, đốm sáng rộng hơn)
- ✅ **12 mô hình 3D** — 5 khối đa diện đều + 7 mặt tham số (xem danh sách bên dưới)
- ✅ **5 pure wireframes** — mô hình chỉ gồm đỉnh + cạnh (định dạng 6.5.1 giáo trình)
- ✅ **Converter** — công cụ chuyển Mesh → pure wireframe, lọc đường chéo đồng phẳng
- ✅ **Control Panel** (pygame_gui):
  - Chọn shading mode (Wireframe / Flat / Gouraud / Phong / Blinn-Phong)
  - Chọn mô hình 3D (dropdown)
  - Slider tốc độ xoay (0.0–3.0 rad/s)
  - Slider khoảng cách camera (2.0–15.0)

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
├── GouraudShading       ✅ Hoàn thành
├── PhongShading         ✅ Hoàn thành
├── BlinnPhongShading    ✅ Hoàn thành
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
├── models/         # .txt files — platonic solids
│   └── pure_wireframes/  # .txt files — wireframe (chỉ đỉnh + cạnh)
├── raytracer/      # (tuỳ chọn, giai đoạn sau)
├── converter.py    # Công cụ chuyển Mesh → pure wireframe
├── main.py         # Entry point
├── requirements.txt
├── README.md
└── .gitignore
```

### Danh sách mô hình 3D

| Mô hình | Loại | Đỉnh | Mặt / Cạnh |
|---------|------|------|------------|
| Tetrahedron | Khối đa diện đều (4 mặt) | 4 | 4 mặt |
| Cube | Khối đa diện đều (6 mặt) | 8 | 6 mặt |
| Octahedron | Khối đa diện đều (8 mặt) | 6 | 8 mặt |
| Dodecahedron | Khối đa diện đều (12 mặt) | 20 | 12 mặt |
| Icosahedron | Khối đa diện đều (20 mặt) | 12 | 20 mặt |
| Sphere | Mặt tham số | 651 | 1.200 mặt |
| Torus | Mặt tham số | 651 | 1.200 mặt |
| Ellipsoid | Mặt tham số | 651 | 1.200 mặt |
| Hyperboloid (Saddle) | Mặt tham số | 441 | 800 mặt |
| Cylinder | Mặt tham số | 341 | 600 mặt |
| Cone | Mặt tham số | 651 | 1.200 mặt |
| Paraboloid | Mặt tham số | 651 | 1.200 mặt |

Ngoài ra, 5 khối đa diện đều có **pure wireframe** (chỉ đỉnh + cạnh, định dạng 6.5.1) trong `models/pure_wireframes/`.

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

- **Dropdown "Wireframe / Flat / Gouraud / Phong / Blinn-Phong"** — chuyển chế độ hiển thị
- **Dropdown chọn mô hình** — chuyển đổi mô hình 3D
- **Slider "Rotation Speed"** — điều chỉnh tốc độ xoay (0.0–3.0 rad/s)
- **Slider "Camera Distance"** — phóng to / thu nhỏ (2.0–15.0)
- **Nút ✕ trên cửa sổ** — thoát

### Công cụ converter

```bash
python converter.py
```
Chuyển đổi file mesh `.txt` → pure wireframe (lọc đường chéo đồng phẳng). Kết quả ghi vào `models/pure_wireframes/`.

## Tiến độ phát triển

| Phase | Nội dung | Trạng thái |
|-------|----------|------------|
| Phase 0 | Scaffold project, venv, thư mục | ✅ |
| Phase 1 | Vector3, Matrix4, wireframe cube | ✅ |
| Phase 2 | Pipeline, rasterizer, Z-buffer, Flat shading, 12 models, UI, pure wireframes | ✅ |
| Phase 3 | Gouraud shading + vertex normals, dynamic lighting, trục toạ độ | ✅ |
| Phase 4 | Phong shading cổ điển — nội suy pháp tuyến per-pixel, specular (R·V)^α | ✅ |
| Phase 5 | Blinn-Phong shading — half-vector (N·H)^α | ✅ |
| Phase 6 | Camera view/projection matrix, Scene quản lý | 🔜 |
| Phase 7 | So sánh, tinh chỉnh, báo cáo | 🔜 |

## Git Workflow

Mỗi giai đoạn là một commit riêng, message theo format `[Phase N] <mô tả ngắn>`.
Tag lớn: `v1-wireframe`, `v2-flat-shading`, `v3-gouraud`, `v4-phong`, `v5-blinn-phong`.

## Giấy phép

Dự án học tập cá nhân.
