import pygame
import pygame_gui

class ControlPanel:
    def __init__(self, screen_size: tuple[int, int], modes: dict, models: dict):
        self.manager = pygame_gui.UIManager(screen_size)

        # Dropdowns cũ
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

        # --- THÊM TÍNH NĂNG CONFIG ---
        
        # 1. Slider Tốc độ xoay
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 50), (160, 20)),
            text="Rotation Speed",
            manager=self.manager
        )
        self.rot_speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 70), (160, 20)),
            start_value=0.02, 
            value_range=(0.0, 0.1),
            manager=self.manager
        )

        # 2. Slider Khoảng cách Camera (Eye Distance)
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 100), (160, 20)),
            text="Camera Distance",
            manager=self.manager
        )
        self.eye_dist_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 120), (160, 20)),
            start_value=5.0, 
            value_range=(2.0, 15.0),
            manager=self.manager
        )

        # Biến trạng thái để Application đọc
        self.selected_mode = list(modes.keys())[0]
        self.selected_model = list(models.keys())[0]
        self.rotation_speed = 0.007
        self.eye_distance = 5.0

    def process_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)
        
        # Xử lý Dropdown
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.mode_dropdown:
                self.selected_mode = event.text
            elif event.ui_element == self.model_dropdown:
                self.selected_model = event.text
                
        # Xử lý kéo Slider
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.rot_speed_slider:
                self.rotation_speed = event.value
            elif event.ui_element == self.eye_dist_slider:
                self.eye_distance = event.value

    def update(self, dt: float) -> None:
        self.manager.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        self.manager.draw_ui(surface)