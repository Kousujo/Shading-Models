from core.vector import Vector3


class TransformPipeline:
    """
    Model -> Phép chiếu phối cảnh theo đúng công thức 6.2.1 giáo trình:
    x' = x / (1 - z/E),  y' = y / (1 - z/E),  mắt đặt tại (0,0,E), E > 0.
    Yêu cầu: P.z < E (điểm phải nằm trước mắt).
    """

    def __init__(self, eye_distance: float = 5.0):
        self.eye_distance = eye_distance

    def project(self, world: Vector3) -> tuple[float, float]:
        factor = 1 - world.z / self.eye_distance
        return world.x / factor, world.y / factor