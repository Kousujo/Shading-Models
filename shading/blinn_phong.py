"""Blinn-Phong Shading — nội suy pháp tuyến, tính màu từng pixel với half-vector (N·H)."""

import numpy as np
from shading.base import ShadingStrategy, RGB
from core.vector import Vector3


class BlinnPhongShading(ShadingStrategy):
    """Blinn-Phong shading: nội suy pháp tuyến trong tam giác, tính màu per-pixel.
    Dùng half-vector H = normalize(L+V) thay vì reflect vector R (rẻ hơn, xấp xỉ tốt)."""

    per_pixel = True
    per_vertex = False

    def __init__(self, base_color: RGB = (200, 120, 60), ambient: float = 0.15,
                 specular_color: RGB = (255, 255, 255), shininess: float = 32.0):
        self.base_color = np.array(base_color, dtype=np.float64)
        self.ambient = ambient
        self.specular_color = np.array(specular_color, dtype=np.float64)
        self.shininess = shininess  # Độ tụ của điểm sáng (càng cao điểm sáng càng nhỏ và gắt)

    def shade(self, position: Vector3, normal: Vector3, light, eye: Vector3) -> RGB:
        """Không dùng tính đơn lẻ — BlinnPhong dùng shade_array để tính hàng loạt."""
        raise NotImplementedError("BlinnPhongShading dùng shade_array, không shade() đơn lẻ")

    def shade_array(self, positions: np.ndarray, normals: np.ndarray, light, eye: Vector3) -> np.ndarray:
        """Tính ánh sáng Blinn-Phong cho mảng K pixel vượt qua Z-buffer cùng lúc.

        Args:
            positions: (K, 3) — toạ độ world-space của từng pixel
            normals:   (K, 3) — pháp tuyến đã nội suy (cần chuẩn hoá lại)
            light:     Light object
            eye:       Vector3 — vị trí camera/mắt

        Returns:
            np.ndarray shape (K, 3) dtype uint8 — màu RGB cho từng pixel
        """
        # 1. Chuẩn hoá lại pháp tuyến (do quá trình nội suy làm mất độ dài = 1)
        norms = np.linalg.norm(normals, axis=1, keepdims=True)
        norms[norms == 0] = 1  # Tránh chia cho 0
        N = normals / norms

        # 2. Vector hướng đèn (L)
        light_pos = np.array([light.position.x, light.position.y, light.position.z])
        L = light_pos - positions
        L_norms = np.linalg.norm(L, axis=1, keepdims=True)
        L_norms[L_norms == 0] = 1
        L = L / L_norms

        # 3. Vector hướng nhìn (V)
        eye_pos = np.array([eye.x, eye.y, eye.z])
        V = eye_pos - positions
        V_norms = np.linalg.norm(V, axis=1, keepdims=True)
        V_norms[V_norms == 0] = 1
        V = V / V_norms

        # 4. Vector phân giác Half-way (H) cho Blinn-Phong
        H = L + V
        H_norms = np.linalg.norm(H, axis=1, keepdims=True)
        H_norms[H_norms == 0] = 1
        H = H / H_norms

        # --- TÍNH TOÁN 3 THÀNH PHẦN ÁNH SÁNG ---
        # A. Diffuse (N·L)
        diffuse_factor = np.clip(np.sum(N * L, axis=1, keepdims=True), 0.0, 1.0)

        # B. Specular (N·H)^shininess — chỉ hiển thị đốm sáng nếu mặt đang hướng về đèn
        spec_dot = np.clip(np.sum(N * H, axis=1, keepdims=True), 0.0, 1.0)
        specular_factor = np.where(diffuse_factor > 0, spec_dot ** self.shininess, 0.0)

        # C. Ambient
        ambient_color = self.base_color * self.ambient
        diffuse_color = self.base_color * (1 - self.ambient) * diffuse_factor * light.intensity
        specular_color = self.specular_color * specular_factor * light.intensity

        final_color = ambient_color + diffuse_color + specular_color
        return np.clip(final_color, 0, 255).astype(np.uint8)