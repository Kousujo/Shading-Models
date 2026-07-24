import pygame
import numpy as np
import pygame.surfarray
import math
from geometry.primitives import load_mesh_from_txt, load_wireframe_from_txt, create_sphere, create_torus, create_ellipsoid, create_hyperboloid, create_cylinder, create_cone, create_paraboloid
from geometry.mesh import face_normal, compute_vertex_normals
from core.matrix import Matrix4
from core.vector import Vector3
from pipeline.transform import TransformPipeline
from rasterizer.zbuffer import ZBuffer
from rasterizer.rasterizer import Rasterizer
from shading.flat import FlatShading
from shading.gouraud import GouraudShading
from shading.phong import PhongShading
from shading.blinn_phong import BlinnPhongShading
from shading.unlit import UnlitShading
from scene.light import Light
from app.ui import ControlPanel

WIDTH, HEIGHT = 1280, 720
SCALE = 150
BACKGROUND_COLOR = (80, 80, 80)


def to_screen(x: float, y: float) -> tuple[int, int]:
    return int(WIDTH / 2 + x * SCALE), int(HEIGHT / 2 - y * SCALE)


class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CG Shading Demo")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 18)

        # Registry: thêm mode/model mới ở giai đoạn sau chỉ cần thêm 1 dòng ở đây.
        self.modes = {
            "Wireframe": None,
            "Flat": FlatShading(base_color=(200, 120, 60)),
            "Gouraud": GouraudShading(base_color=(200, 120, 60)),
            "Phong": PhongShading(base_color=(200, 120, 60), shininess=32.0),
            "Blinn-Phong": BlinnPhongShading(base_color=(200, 120, 60), shininess=32.0),
        }
        self.models = {
            "Tetrahedron": {
                "mesh": lambda: load_mesh_from_txt("models/tetrahedron.txt"),
                "pure": lambda: load_wireframe_from_txt("models/pure_wireframes/tetrahedron_wireframe.txt")
            },
            "Cube": {
                "mesh": lambda: load_mesh_from_txt("models/cube.txt"),
                "pure": lambda: load_wireframe_from_txt("models/pure_wireframes/cube_wireframe.txt")
            },
            "Octahedron": {
                "mesh": lambda: load_mesh_from_txt("models/octahedron.txt"),
                "pure": lambda: load_wireframe_from_txt("models/pure_wireframes/octahedron_wireframe.txt")
            },
            "Dodecahedron": {
                "mesh": lambda: load_mesh_from_txt("models/dodecahedron.txt"),
                "pure": lambda: load_wireframe_from_txt("models/pure_wireframes/dodecahedron_wireframe.txt")
            },
            "Icosahedron": {
                "mesh": lambda: load_mesh_from_txt("models/icosahedron.txt"),
                "pure": lambda: load_wireframe_from_txt("models/pure_wireframes/icosahedron_wireframe.txt")
            },
            "Sphere": lambda: create_sphere(),
            "Torus": lambda: create_torus(),
            "Ellipsoid": lambda: create_ellipsoid(),
            "Hyperboloid (Saddle)": lambda: create_hyperboloid(),
            "Cylinder": lambda: create_cylinder(),
            "Cone": lambda: create_cone(),
            "Paraboloid": lambda: create_paraboloid()
        }

        self.ui = ControlPanel((WIDTH, HEIGHT), self.modes, self.models)
        self.current_model_name = self.ui.selected_model
        self.current_mode_name = self.ui.selected_mode
        self.mesh = self._load_mesh_for(self.current_model_name, self.current_mode_name)

        self.pipeline = TransformPipeline(eye_distance=5.0)
        self.zbuffer = ZBuffer(WIDTH, HEIGHT)
        self.framebuffer = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
        self.rasterizer = Rasterizer(self.framebuffer, self.zbuffer)
        self.light = Light(position=Vector3(3, 3, 3))
        self.light_marker_mesh = create_sphere(radius=0.15, lat_steps=6, lon_steps=10)
        self.light_marker_shading = UnlitShading(color=(255, 255, 180))
        self.eye = Vector3(0, 0, self.pipeline.eye_distance)
        self.angle = 0.0
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_input()
            self.update(dt)
            self.render()
        pygame.quit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.ui.process_event(event)

    def update(self, dt: float):
        # Ánh sáng orbit quanh model — minh hoạ trực quan N·L thay đổi theo thời gian thực
        light_angle = self.angle * 1.5
        self.light.position = Vector3(4 * math.cos(light_angle), 3, 4 * math.sin(light_angle))

        # Đọc tốc độ xoay trực tiếp từ thanh trượt UI
        self.angle += self.ui.rotation_speed * dt
        
        # Đồng bộ khoảng cách camera nếu người dùng kéo thanh trượt
        if self.pipeline.eye_distance != self.ui.eye_distance:
            self.pipeline.eye_distance = self.ui.eye_distance
            self.eye.z = self.ui.eye_distance  # Quan trọng: Cập nhật vị trí mắt để ánh sáng chiếu đúng

        self.ui.update(dt)
        
        # Kiểm tra xem người dùng có đổi Model hoặc đổi Mode trên UI không
        model_changed = self.ui.selected_model != self.current_model_name
        mode_changed = self.ui.selected_mode != self.current_mode_name

        # update()
        if model_changed or mode_changed:
            self.current_model_name = self.ui.selected_model
            self.current_mode_name = self.ui.selected_mode
            self.mesh = self._load_mesh_for(self.current_model_name, self.current_mode_name)

    def _load_mesh_for(self, model_name: str, mode_name: str):
        model_source = self.models[model_name]
        if isinstance(model_source, dict):
            mesh = model_source["pure" if mode_name == "Wireframe" else "mesh"]()
        else:
            mesh = model_source()
        if hasattr(mesh, "faces"):
            compute_vertex_normals(mesh)
        return mesh

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        model = Matrix4.rotation_y(self.angle) @ Matrix4.rotation_x(self.angle * 0.2)

        self.render_ground_grid()

        if self.ui.selected_mode == "Wireframe":
            self.render_wireframe(model)
        else:
            self.render_solid(model, self.modes[self.ui.selected_mode])

        self.render_axes(model)
        self.render_stats()
        self.ui.draw(self.screen)
        pygame.display.flip()

    def render_wireframe(self, model: Matrix4) -> None:
        if hasattr(self.mesh, "edges"):          # WireframeModel: dùng cạnh có sẵn
            edges = self.mesh.edges # type: ignore
        else:                                      # Mesh tam giác: suy ra cạnh từ mặt (như cũ)
            edges = set()
            for face in self.mesh.faces:
                a, b, c = face.indices()
                for i, j in ((a, b), (b, c), (c, a)):
                    edges.add((min(i, j), max(i, j)))

        for i, j in edges:
            w1 = model.transform_point(self.mesh.vertices[i].position)
            w2 = model.transform_point(self.mesh.vertices[j].position)
            p1 = to_screen(*self.pipeline.project(w1))
            p2 = to_screen(*self.pipeline.project(w2))
            pygame.draw.line(self.screen, (0, 255, 100), p1, p2)

    def render_solid_object(self, mesh, model: Matrix4, shading) -> None:
        """Vẽ 1 mesh qua pipeline: transform → project → rasterize + z-test.
        Dùng chung cho model chính và quả cầu đèn (occlusion đúng giữa 2 object)."""
        for face in mesh.faces:
            a, b, c = face.indices()
            world = [model.transform_point(mesh.vertices[i].position) for i in (a, b, c)]
            screen = [to_screen(*self.pipeline.project(w)) for w in world]
            depths = [w.z for w in world]

            if getattr(shading, "per_pixel", False):
                world_normals = [model.transform_direction(mesh.vertices[i].normal) for i in (a, b, c)]
                self.rasterizer.draw_triangle_phong(
                    (screen[0], screen[1], screen[2]), (depths[0], depths[1], depths[2]),
                    world, world_normals, shading, self.light, self.eye,
                )
            elif getattr(shading, "per_vertex", False):
                world_normals = [model.transform_direction(mesh.vertices[i].normal) for i in (a, b, c)]
                vertex_colors = [shading.shade(world[k], world_normals[k], self.light, self.eye) for k in range(3)]
                self.rasterizer.draw_triangle_gouraud(
                    (screen[0], screen[1], screen[2]), (depths[0], depths[1], depths[2]), vertex_colors,
                )
            else:
                normal = face_normal(*world)
                centroid = Vector3(
                    sum(w.x for w in world) / 3, sum(w.y for w in world) / 3, sum(w.z for w in world) / 3,
                )
                color = shading.shade(centroid, normal, self.light, self.eye)
                self.rasterizer.draw_triangle_flat(
                    (screen[0], screen[1], screen[2]), (depths[0], depths[1], depths[2]), color,
                )

    def render_solid(self, model: Matrix4, shading) -> None:
        if not hasattr(self.mesh, "faces"):
            self.render_wireframe(model)
            return

        self.zbuffer.clear()
        self.framebuffer[:] = BACKGROUND_COLOR

        self.render_solid_object(self.mesh, model, shading)

        light_model = Matrix4.translation(self.light.position.x, self.light.position.y, self.light.position.z)
        self.render_solid_object(self.light_marker_mesh, light_model, self.light_marker_shading)

        pygame.surfarray.blit_array(self.screen, self.framebuffer)

    def render_ground_grid(self) -> None:
        """Lưới nền cố định mặt XZ, y = -1.5 — không xoay theo model, chỉ để định vị không gian.
        ponytail: khi camera quá gần (eye_distance <= extent), grid lines có z tiến tới
        mặt phẳng mắt gây factor=0 trong phép chiếu phối cảnh (chia cho 0).
        Thay vì clip line chính xác, ta skip toàn bộ line nếu bất kỳ điểm đầu/cuối nào
        có z >= eye_distance — vài ô biến mất khi zoom gần, chấp nhận được cho grid định vị."""
        grid_color = (55, 55, 60)
        extent, step = 4, 1
        y = -1.5
        E = self.pipeline.eye_distance  # khoảng cách mắt, dùng để guard z quá gần mắt

        for i in range(-extent, extent + 1, step):
            # Guard: bỏ qua line nếu bất kỳ điểm nào có z >= E (factor ≤ 0 → ZeroDivisionError)
            w1 = Vector3(i, y, -extent)
            w2 = Vector3(i, y, extent)
            if w1.z >= E or w2.z >= E:
                continue
            p1 = to_screen(*self.pipeline.project(w1))
            p2 = to_screen(*self.pipeline.project(w2))
            pygame.draw.line(self.screen, grid_color, p1, p2)

            w3 = Vector3(-extent, y, i)
            w4 = Vector3(extent, y, i)
            if w3.z >= E or w4.z >= E:
                continue
            p1 = to_screen(*self.pipeline.project(w3))
            p2 = to_screen(*self.pipeline.project(w4))
            pygame.draw.line(self.screen, grid_color, p1, p2)

    def render_axes(self, model: Matrix4) -> None:
        """Vẽ 3 trục toạ độ X(đỏ)/Y(xanh lá)/Z(xanh dương) từ gốc, dài 2.5 đơn vị.
        Dùng model matrix để trục xoay đồng bộ với vật thể."""
        origin = model.transform_point(Vector3(0, 0, 0))
        axes = [
            (Vector3(2.5, 0, 0), (255, 0, 0)),    # X — đỏ
            (Vector3(0, 2.5, 0), (0, 255, 0)),    # Y — xanh lá
            (Vector3(0, 0, 2.5), (0, 0, 255)),    # Z — xanh dương
        ]
        for tip_world, color in axes:
            tip = model.transform_point(tip_world)
            p_origin = to_screen(*self.pipeline.project(origin))
            p_tip = to_screen(*self.pipeline.project(tip))
            pygame.draw.line(self.screen, color, p_origin, p_tip, 2)

    def render_stats(self) -> None:
        """Hiển thị FPS, số tam giác, tên model/mode ở góc dưới-trái."""
        fps = self.clock.get_fps()
        tri_count = len(self.mesh.faces) if hasattr(self.mesh, "faces") else 0
        text = f"FPS: {fps:5.1f}   Model: {self.current_model_name} ({tri_count} tris)   Mode: {self.current_mode_name}"
        surf = self.font.render(text, True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(surf, (10, HEIGHT - 30))

