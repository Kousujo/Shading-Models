import math
from core.vector import Vector3

def calculate_normal(p1, p2, p3):
    """Tính pháp tuyến của mặt tam giác (p1, p2, p3)."""
    v1 = p2 - p1
    v2 = p3 - p1
    # Tích có hướng (Cross product)
    normal = Vector3(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )
    return normal.normalize()

def convert_to_pure_wireframe(input_filepath, output_filepath, threshold_angle_deg=1.0):
    with open(input_filepath, 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    num_vertices, num_faces = map(int, lines[0].split())
    
    # Read vertices
    raw_verts = [list(map(float, lines[1 + i].split())) for i in range(num_vertices)]
    verts_vec = [Vector3(*v) for v in raw_verts]
    
    # Read faces
    faces = [list(map(int, lines[num_vertices + 1 + i].split())) for i in range(num_faces)]

    # 1. Tính Pháp tuyến cho từng mặt tam giác
    face_normals = []
    for f in faces:
        p1, p2, p3 = verts_vec[f[0]], verts_vec[f[1]], verts_vec[f[2]]
        face_normals.append(calculate_normal(p1, p2, p3))

    # 2. Gom nhóm các mặt chung cạnh
    # Key: edge tuple (v1, v2), Value: list indices của các mặt chứa cạnh đó
    edge_to_faces = {}
    for f_idx, f in enumerate(faces):
        for i in range(3):
            v1, v2 = f[i], f[(i + 1) % 3]
            edge = (min(v1, v2), max(v1, v2))
            if edge not in edge_to_faces:
                edge_to_faces[edge] = []
            edge_to_faces[edge].append(f_idx)

    # 3. Lọc bỏ đường chéo (Cạnh nối 2 tam giác đồng phẳng)
    clean_edges = []
    cos_threshold = math.cos(math.radians(threshold_angle_deg))

    for edge, shared_faces in edge_to_faces.items():
        # Nếu cạnh chỉ thuộc về 1 mặt -> Cạnh viền ngoài -> GIỮ
        if len(shared_faces) == 1:
            clean_edges.append(edge)
        elif len(shared_faces) == 2:
            n1 = face_normals[shared_faces[0]]
            n2 = face_normals[shared_faces[1]]
            # Tích vô hướng (Dot product) để kiểm tra góc giữa 2 pháp tuyến
            dot = n1.x * n2.x + n1.y * n2.y + n1.z * n2.z
            
            # Nếu 2 mặt KHÔNG đồng phẳng (góc tạo bởi 2 mặt lớn hơn ngưỡng) -> GIỮ
            if dot < cos_threshold:
                clean_edges.append(edge)
            # Ngược lại: 2 mặt cùng nằm trên 1 mặt phẳng -> Đây là đường chéo thừa -> BỎ!

    # Ghi ra file
    with open(output_filepath, 'w') as f:
        f.write(f"{num_vertices} {len(clean_edges)}\n")
        for v in lines[1:num_vertices + 1]:
            f.write(v + "\n")
        for e in sorted(clean_edges):
            f.write(f"{e[0] + 1} {e[1] + 1}\n")

if __name__ == "__main__":
    convert_to_pure_wireframe("models/cube.txt", "models/pure_wireframes/cube_wireframe.txt")
    convert_to_pure_wireframe("models/dodecahedron.txt", "models/pure_wireframes/dodecahedron_wireframe.txt")
    convert_to_pure_wireframe("models/icosahedron.txt", "models/pure_wireframes/icosahedron_wireframe.txt")
    convert_to_pure_wireframe("models/octahedron.txt", "models/pure_wireframes/octahedron_wireframe.txt")
    convert_to_pure_wireframe("models/tetrahedron.txt", "models/pure_wireframes/tetrahedron_wireframe.txt")