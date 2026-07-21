import pygame

from geometry.primitives import create_cube
from core.matrix import Matrix4
from pipeline.transform import TransformPipeline

WIDTH, HEIGHT = 1280, 720
SCALE = 150  # đơn vị world -> pixel


def to_screen(x: float, y: float) -> tuple[int, int]:
    return int(WIDTH / 2 + x * SCALE), int(HEIGHT / 2 - y * SCALE)  # lật trục Y (màn hình Y hướng xuống)


class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CG Shading Demo - Giai doan 1: Wireframe")
        self.clock = pygame.time.Clock()
        self.mesh = create_cube(size=2.0)
        self.pipeline = TransformPipeline(eye_distance=5)
        self.angle = 0.0
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

    def update(self):
        self.angle += 0.005

    def render(self):
        self.screen.fill((0, 0, 0))
        model = Matrix4.rotation_y(self.angle) @ Matrix4.rotation_x(self.angle * 0.5)

        edges = set()
        for face in self.mesh.faces:
            a, b, c = face.indices()
            for i, j in ((a, b), (b, c), (c, a)):
                edges.add((min(i, j), max(i, j)))

        for i, j in edges:
            p1 = self.pipeline.project(self.mesh.vertices[i].position, model)
            p2 = self.pipeline.project(self.mesh.vertices[j].position, model)
            pygame.draw.line(self.screen, (0, 255, 100), to_screen(*p1), to_screen(*p2))

        pygame.display.flip()