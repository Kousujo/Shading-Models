import pygame
import pygame_gui


class ControlPanel:
    """Thanh điều khiển tách biệt hoàn toàn khỏi phần render 3D.
    Application chỉ cần đọc self.selected_mode / self.selected_model mỗi frame.
    Mở rộng: thêm mode/model mới = thêm key vào dict `modes`/`models` khi khởi tạo,
    không cần sửa gì trong class này."""

    def __init__(self, screen_size: tuple[int, int], modes: dict, models: dict):
        self.manager = pygame_gui.UIManager(screen_size)

        self.mode_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=list(modes.keys()),
            starting_option=list(modes.keys())[0],
            relative_rect=pygame.Rect((10, 10), (160, 30)),
            manager=self.manager,
        )
        self.model_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=list(models.keys()),
            starting_option=list(models.keys())[0],
            relative_rect=pygame.Rect((180, 10), (160, 30)),
            manager=self.manager,
        )

        self.selected_mode = list(modes.keys())[0]
        self.selected_model = list(models.keys())[0]

    def process_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.mode_dropdown:
                self.selected_mode = event.text
            elif event.ui_element == self.model_dropdown:
                self.selected_model = event.text

    def update(self, dt: float) -> None:
        self.manager.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        self.manager.draw_ui(surface)