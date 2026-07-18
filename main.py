"""Shading Models — Software Renderer (Python thuần, không OpenGL).

Đồ án cuối kỳ Computer Graphics: so sánh Flat, Gouraud, Phong, Blinn-Phong.
"""

from app.application import Application


def main() -> None:
    """Entry point: khởi tạo Application và gọi run()."""
    app = Application(width=800, height=600)
    app.run()


if __name__ == "__main__":
    main()