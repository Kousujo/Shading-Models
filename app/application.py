import pygame
from geometry.primitives import create_cube
from geometry.mesh import face_normal
from core.matrix import Matrix4
from core.vector import Vector3
from pipeline.transform import TransformPipeline
from rasterizer.zbuffer import ZBuffer
from rasterizer.rasterizer import Rasterizer
from shading.flat import FlatShading
from scene.light import Light
from app.ui import ControlPanel

WIDTH, HEIGHT = 800, 600
SCALE = 150


def to_screen(x: float, y: float) -> tuple[int, int]:
    return int(WIDTH / 2 + x * SCALE), int(HEIGHT / 2 - y * SCALE)


class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CG Shading Demo")
        self.clock = pygame.time.Clock()

        # Registry: thêm mode/model mới ở giai đoạn sau chỉ cần thêm 1 dòng ở đây.
        self.modes = {"Wireframe": None, "Flat": FlatShading(base_color=(200, 120, 60))}
        self.models = {"Cube": create_cube}

        self.ui = ControlPanel((WIDTH, HEIGHT), self.modes, self.models)
        self.current_model_name = self.ui.selected_model
        self.mesh = self.models[self.current_model_name]()

        self.pipeline = TransformPipeline(eye_distance=5.0)
        self.zbuffer = ZBuffer(WIDTH, HEIGHT)
        self.rasterizer = Rasterizer(self.screen, self.zbuffer)
        self.light = Light(position=Vector3(3, 3, 3))
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
        self.angle += 0.02
        self.ui.update(dt)
        if self.ui.selected_model != self.current_model_name:
            self.current_model_name = self.ui.selected_model
            self.mesh = self.models[self.current_model_name]()

    def render(self):
        self.screen.fill((0, 0, 0))
        model = Matrix4.rotation_y(self.angle)

        if self.ui.selected_mode == "Wireframe":
            self.render_wireframe(model)
        else:
            self.render_solid(model, self.modes[self.ui.selected_mode])

        self.ui.draw(self.screen)
        pygame.display.flip()

    def render_wireframe(self, model: Matrix4) -> None:
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

    def render_solid(self, model: Matrix4, shading) -> None:
        self.zbuffer.clear()
        for face in self.mesh.faces:
            a, b, c = face.indices()
            world = [model.transform_point(self.mesh.vertices[i].position) for i in (a, b, c)]
            screen = [to_screen(*self.pipeline.project(w)) for w in world]
            depths = [w.z for w in world]

            normal = face_normal(*world)
            centroid = Vector3(
                sum(w.x for w in world) / 3,
                sum(w.y for w in world) / 3,
                sum(w.z for w in world) / 3,
            )
            color = shading.shade(centroid, normal, self.light, self.eye)

            self.rasterizer.draw_triangle(
                (screen[0], screen[1], screen[2]),
                (depths[0], depths[1], depths[2]),
                shade_fn=lambda w0, w1, w2: color,
            )