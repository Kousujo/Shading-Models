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
        self.mesh = create_cube(size=2.0)
        self.pipeline = TransformPipeline(eye_distance=5.0)
        self.zbuffer = ZBuffer(WIDTH, HEIGHT)
        self.rasterizer = Rasterizer(self.screen, self.zbuffer)
        self.shading = FlatShading(base_color=(200, 120, 60))
        self.light = Light(position=Vector3(3, 3, 3))
        self.eye = Vector3(0, 0, self.pipeline.eye_distance)
        self.angle = 0.0
        self.mode = "wireframe"  # phím 1 = wireframe, phím 2 = flat
        self.running = True

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.mode = "wireframe"
                elif event.key == pygame.K_2:
                    self.mode = "flat"
                pygame.display.set_caption(f"CG Shading Demo - Mode: {self.mode}")

    def update(self):
        self.angle += 0.02

    def render(self):
        self.screen.fill((0, 0, 0))
        model = Matrix4.rotation_y(self.angle)
        if self.mode == "wireframe":
            self.render_wireframe(model)
        else:
            self.render_solid(model)
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

    def render_solid(self, model: Matrix4) -> None:
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
            color = self.shading.shade(centroid, normal, self.light, self.eye)

            self.rasterizer.draw_triangle(
                (screen[0], screen[1], screen[2]),
                (depths[0], depths[1], depths[2]),
                shade_fn=lambda w0, w1, w2: color,
            )