import math
import os

from typing import Callable
from geometry.mesh import Vertex, Face, Mesh
from core.vector import Vector3
from geometry.mesh import WireframeModel

def load_wireframe_from_txt(filepath: str) -> WireframeModel:
    """
    Đọc đúng định dạng 6.5.1: dòng 1 = 'm n' (m đỉnh, n cạnh),
    m dòng toạ độ (x y z), n dòng cặp chỉ số cạnh — ĐÁNH SỐ TỪ 1 giống sách,
    nên phải trừ 1 khi nạp vào list Python (list bắt đầu từ 0).
    """
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    num_vertices, num_edges = map(int, lines[0].split())
    vertices = [Vertex(Vector3(*map(float, lines[1 + i].split()))) for i in range(num_vertices)]

    edges = []
    for i in range(num_edges):
        v1, v2 = map(int, lines[1 + num_vertices + i].split())
        edges.append((v1 - 1, v2 - 1))  # 1-indexed (sách) -> 0-indexed (Python)

    return WireframeModel(vertices, edges)

def load_mesh_from_txt(filepath: str) -> Mesh:
    """Đọc dữ liệu đa diện từ file text và trả về đối tượng Mesh."""
    if not os.path.exists(filepath):
        print(f"Lỗi: Không tìm thấy file {filepath}")
        return Mesh([], [])

    vertices = []
    faces = []

    with open(filepath, 'r') as f:
        # Bỏ qua các dòng trống
        lines = [line.strip() for line in f if line.strip()]
        
        # Đọc dòng đầu tiên: Số đỉnh, Số mặt
        num_vertices, num_faces = map(int, lines[0].split())
        
        # Đọc toạ độ đỉnh
        for i in range(1, num_vertices + 1):
            x, y, z = map(float, lines[i].split())
            vertices.append(Vertex(Vector3(x, y, z)))
            
        # Đọc các mặt (chỉ số index)
        for i in range(num_vertices + 1, num_vertices + 1 + num_faces):
            a, b, c = map(int, lines[i].split())
            faces.append(Face(a, b, c))

    return Mesh(vertices, faces)

def create_parametric_surface(
    func: Callable[[float, float], Vector3],
    u_min: float, u_max: float, u_steps: int,
    v_min: float, v_max: float, v_steps: int
) -> Mesh:
    """Cỗ máy dệt lưới 3D tự động từ phương trình tham số."""
    vertices = []
    faces = []

    # 1. Sinh đỉnh (tạo lưới u_steps+1 x v_steps+1)
    for i in range(u_steps + 1):
        # Tính tỷ lệ từ 0 -> 1, sau đó map vào khoảng [u_min, u_max]
        u = u_min + (u_max - u_min) * (i / u_steps) if u_steps > 0 else u_min
        for j in range(v_steps + 1):
            v = v_min + (v_max - v_min) * (j / v_steps) if v_steps > 0 else v_min
            
            # Gọi hàm toán học func(u, v) để lấy toạ độ 3D
            vertices.append(Vertex(func(u, v)))

    # 2. Sinh mặt tam giác (Quét qua các ô vuông và chẻ đôi)
    for i in range(u_steps):
        for j in range(v_steps):
            # Công thức tính index 1D từ toạ độ 2D (i, j)
            row_len = v_steps + 1
            p1 = i * row_len + j
            p2 = i * row_len + (j + 1)
            p3 = (i + 1) * row_len + (j + 1)
            p4 = (i + 1) * row_len + j

            # Quy tắc bàn tay phải (CCW)
            faces.append(Face(p1, p2, p3))
            faces.append(Face(p1, p3, p4))

    return Mesh(vertices, faces)

def create_sphere(radius=1.5, lat_steps=20, lon_steps=30):
    """Mặt cầu tối ưu qua create_parametric_surface."""
    return create_parametric_surface(
        lambda u, v: Vector3(
            radius * math.cos(u) * math.cos(v),
            radius * math.sin(v),
            radius * math.sin(u) * math.cos(v)
        ),
        u_min=0, u_max=2 * math.pi, u_steps=lon_steps,
        v_min=-math.pi / 2, v_max=math.pi / 2, v_steps=lat_steps
    )

def create_torus(major_radius=1.0, minor_radius=0.5, sweep_steps=30, tube_steps=20):
    """Hình xuyến tối ưu qua create_parametric_surface."""
    return create_parametric_surface(
        lambda u, v: Vector3(
            (major_radius + minor_radius * math.cos(v)) * math.cos(u),
            minor_radius * math.sin(v),
            (major_radius + minor_radius * math.cos(v)) * math.sin(u)
        ),
        u_min=0, u_max=2 * math.pi, u_steps=sweep_steps,
        v_min=0, v_max=2 * math.pi, v_steps=tube_steps
    )

def create_ellipsoid(rx=1.5, ry=1.0, rz=0.8):
    # X = rx*cos(u)cos(v), Z = ry*sin(u)cos(v), Y = rz*sin(v)
    return create_parametric_surface(
        lambda u, v: Vector3(rx * math.cos(u) * math.cos(v), rz * math.sin(v), ry * math.sin(u) * math.cos(v)),
        0, 2 * math.pi, 30,          # Góc u (kinh độ)
        -math.pi / 2, math.pi / 2, 20 # Góc v (vĩ độ)
    )

def create_hyperboloid():
    # Đây là mặt Yên ngựa (Hyperbolic Paraboloid): Y = u^2 - v^2
    return create_parametric_surface(
        lambda u, v: Vector3(u, u**2 - v**2, v),
        -1.2, 1.2, 20, 
        -1.2, 1.2, 20
    )

def create_cylinder(radius=1.0, height=2.0):
    # X = R*cos(u), Z = R*sin(u), Y = v
    return create_parametric_surface(
        lambda u, v: Vector3(radius * math.cos(u), v, radius * math.sin(u)),
        0, 2 * math.pi, 30,
        -height / 2, height / 2, 10
    )

def create_cone(radius=1.0, height=2.0):
    # Đỉnh nón ở y = height/2, đáy ở y = -height/2
    return create_parametric_surface(
        lambda u, v: Vector3(
            (1 - v) * radius * math.cos(u), 
            height/2 - v * height, 
            (1 - v) * radius * math.sin(u)
        ),
        0, 2 * math.pi, 30,
        0.0, 1.0, 20 # v chạy từ 0 (đỉnh) đến 1 (đáy)
    )

def create_paraboloid(a=1.0, b=1.0):
    # Chảo Parabol: Y = v^2. Trục v chạy từ 0 đến 1.5
    return create_parametric_surface(
        lambda u, v: Vector3(a * v * math.cos(u), v**2 - 1.0, b * v * math.sin(u)),
        0, 2 * math.pi, 30,
        0.0, 1.2, 20
    )