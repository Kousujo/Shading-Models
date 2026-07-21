class ZBuffer:
    """Lưu độ sâu (z) của điểm gần camera nhất đã vẽ tại mỗi pixel.
    z càng LỚN nghĩa là càng GẦN camera (do camera đặt tại (0,0,E), E>0 - xem pipeline/transform.py)."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.buffer = [[float("-inf")] * width for _ in range(height)]

    def test_and_set(self, x: int, y: int, depth: float) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        if depth > self.buffer[y][x]:
            self.buffer[y][x] = depth
            return True
        return False

    def clear(self) -> None:
        for row in self.buffer:
            for i in range(len(row)):
                row[i] = float("-inf")