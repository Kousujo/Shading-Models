# Clinerules — Đồ án Computer Graphics: So sánh các mô hình tô bóng (Shading Models)

## Mục đích & cấu trúc 3-file

File này là **rule chính**, dùng chung với 2 rule phụ luôn bật trong cùng folder `.clinerules/`:
- `ponytail.md` — kỷ luật "lazy senior dev": bậc thang lười biếng hợp lý (không viết code thừa)
- `karpathy-guidelines.md` — kỷ luật "think before coding": nêu giả định rõ ràng, đơn giản tối
  đa, sửa đúng phạm vi, thực thi theo mục tiêu có thể kiểm chứng

Cả 3 file được nạp mỗi phiên làm việc, không cần gọi thủ công. (Lược bỏ phần skills/MCP tools
trong template project cũ vì dự án này không dùng codegraph/headroom/agent-reach hay bộ 40
skill — nếu sau này bạn cài thêm, thêm 1 mục riêng vào đây, đừng dựng khung sẵn cho thứ chưa
tồn tại.)

## Thứ tự ưu tiên khi các rule "va" nhau

1. **Ranh giới cứng của dự án này** (mục bên dưới) — không rule phụ nào được ghi đè, kể cả khi
   ponytail nói "code càng ít càng tốt, 1 dòng là được".
2. **karpathy-guidelines**, đặc biệt mục 1 "Think Before Coding" — nếu không chắc một việc có
   thuộc "thuật toán cốt lõi" (ranh giới cứng bên dưới) hay không, DỪNG LẠI và hỏi, không tự
   suy đoán.
3. **ponytail** — áp dụng cho MỌI thứ nằm ngoài ranh giới cứng: scaffold, boilerplate, git,
   vòng lặp Pygame, xử lý input... Bậc thang lười (stdlib → tính năng platform → dependency có
   sẵn → 1 dòng → code mới) áp dụng bình thường ở đây, và quy tắc "để lại 1 check chạy được cho
   logic non-trivial" của ponytail cũng áp dụng — nhưng chỉ cho phần Cline tự viết, không áp
   dụng cho phần thuật toán vì Cline không được viết phần đó.

## Bối cảnh dự án

Đồ án cuối kỳ môn Đồ hoạ máy tính (báo cáo dự kiến 11-12/8/2026). Xây dựng một **software
renderer từ đầu bằng Python thuần** (KHÔNG dùng OpenGL/GLSL) để cài đặt và so sánh 4 mô hình
tô bóng: Flat, Gouraud, Phong, Blinn-Phong. Chủ dự án hiện có kiến thức gần như bằng 0 về đồ
hoạ máy tính, học lý thuyết song song với việc code. Dự án học tập cá nhân, không phải sản
phẩm thương mại — ưu tiên rõ ràng, dễ giải thích hơn hiệu năng.

## RANH GIỚI CỨNG: Cline không code thay phần thuật toán cốt lõi

Đây là luật DUY NHẤT trong 3 file có quyền override bậc thang lười của ponytail.

Cline CHỈ được hỗ trợ:
- Scaffold thư mục/file, venv, requirements.txt, .gitignore, README
- Git: commit, tag, branch nếu cần
- Boilerplate không liên quan thuật toán CG: vòng lặp Pygame, đọc input bàn phím/chuột (chỉ
  phần đọc, không phải phần tính view matrix), lưu ảnh, in log/FPS
- Class/function signature kèm docstring + type hint, thân hàm để trống
  (`pass` / `raise NotImplementedError("TODO: Phase X")`)
- Giải thích công thức bằng lời/pseudocode khi được hỏi

Cline TUYỆT ĐỐI KHÔNG tự ý implement, kể cả khi có vẻ đơn giản hoặc người dùng quên nhắc:
- Toán vector/ma trận (dot, cross, normalize, translation/rotation/scale/projection/look_at)
- Rasterization tam giác, z-buffer/khử mặt khuất
- Pháp tuyến mặt và pháp tuyến đỉnh
- Công thức chiếu sáng của từng shading model
- Bất kỳ phần nào thuộc nhóm "thuật toán cốt lõi"

Nếu không chắc → áp dụng karpathy-guidelines mục 1: hỏi lại người dùng, không tự quyết.

## Kiến trúc bắt buộc

- Top-level: **Game Loop** — `initialize()` → `while running: handle_input() → update(dt) →
  render()`
- `render()`: **Pipeline Architecture** — Scene data → Transform (Model/View/Projection) →
  Rasterizer (+Z-buffer) → Shading → Framebuffer
- Shading: **Strategy Pattern** — abstract `ShadingStrategy.shade(vertex, normal, light,
  camera)`, các class con `FlatShading`/`GouraudShading`/`PhongShading`/`BlinnPhongShading`
- Không tự ý đổi kiến trúc (MVC, ECS...) trừ khi được yêu cầu rõ ràng

## Cấu trúc thư mục cố định

```
core/           # vector.py, matrix.py — toán thuần
geometry/       # mesh.py, primitives.py (cube, sphere...)
pipeline/       # transform.py — Model/View/Projection
rasterizer/     # rasterizer.py, zbuffer.py
shading/        # base.py (ShadingStrategy) + flat.py/gouraud.py/phong.py/blinn_phong.py
scene/          # camera.py, light.py, scene.py
app/            # application.py — game loop, input, cửa sổ Pygame
raytracer/      # (tuỳ chọn, module độc lập, giai đoạn sau)
main.py
requirements.txt
README.md
.gitignore
```

## Dependencies được duyệt

- `numpy`, `pygame` — bắt buộc
- `Pillow` — tuỳ chọn (screenshot cho báo cáo)
- Không tự ý thêm dependency mới mà không hỏi trước — khớp trực tiếp với bậc thang ponytail
  (mục 5: dùng dependency đã cài, không phải "muốn gì cài nấy")

## Quy ước code

- Tên biến/hàm/class tiếng Anh; docstring/comment giải thích ý nghĩa toán học có thể tiếng
  Việt (hữu ích khi tổng hợp báo cáo)
- Rõ ràng, dễ giải thích > tối ưu/thông minh
- Type hint đầy đủ cho function signature
- Khi sửa code cũ: chỉ sửa đúng phần liên quan (karpathy mục 3 "Surgical Changes") — không
  "tiện tay" refactor hay đổi format chỗ khác

## Git workflow

- Mỗi giai đoạn (Phase 1–7 theo kế hoạch đã thống nhất) = 1 commit riêng, message theo format
  `[Phase N] <mô tả ngắn>`; gắn git tag sau mỗi giai đoạn lớn (`v1-wireframe`,
  `v2-flat-shading`, `v3-gouraud`, `v4-phong`, `v5-blinn-phong`...)
- Trước khi thực hiện một tác vụ nhiều bước (ví dụ scaffold cả project), nêu ngắn gọn plan kèm
  bước verify cho từng bước — đúng tinh thần karpathy-guidelines mục 4 "Goal-Driven Execution"
- Không rebase/force-push lịch sử — lịch sử commit dùng làm bằng chứng "quá trình phát triển"
  khi viết báo cáo

## Khi không chắc

Luôn hỏi lại người dùng thay vì tự quyết định, đặc biệt về: thêm dependency mới, đổi kiến
trúc, hoặc bất cứ điều gì có thể chạm vào ranh giới cứng ở trên. Đây chính là bước "Alignment"
của karpathy-guidelines áp dụng riêng cho dự án này.
