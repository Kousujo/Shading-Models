from core.vector import Vector3
from core.matrix import Matrix4


class TransformPipeline:
    """
    Model -> Phép chiếu phối cảnh theo đúng công thức 6.2.1 giáo trình:
    x' = x / (1 - z/E),  y' = y / (1 - z/E),  mắt đặt tại (0,0,E), E > 0.
    Yêu cầu: P.z < E (điểm phải nằm trước mắt).
    """

    def __init__(self, eye_distance: float = 5):
        self.eye_distance = eye_distance

    def project(self, v: Vector3, model: Matrix4) -> tuple[float, float]:
        world = model.transform_point(v)
        factor = 1 - world.z / self.eye_distance
        # ponytail: chưa xử lý factor <= 0 (điểm ở sau/ngay tại mắt) - với cube nhỏ
        # + eye_distance=5 mặc định thì luôn an toàn ở Giai đoạn 1. Cần xử lý khi
        # object lớn hơn hoặc camera lại gần.
        return world.x / factor, world.y / factor