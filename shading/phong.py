"""Phong Shading (cổ điển) — nội suy pháp tuyến, specular dùng reflect vector R."""

import numpy as np
from shading.base import ShadingStrategy, RGB
from core.vector import Vector3


class PhongShading(ShadingStrategy):
    """Phong reflection model cổ điển: specular = (R·V)^shininess,
    R = phản xạ của hướng TỚI đèn (L) qua pháp tuyến N — khác Blinn-Phong
    (dùng half-vector H = normalize(L+V), rẻ hơn nhưng là xấp xỉ của R·V)."""

    per_pixel = True
    per_vertex = False

    def __init__(self, base_color: RGB = (200, 120, 60), ambient: float = 0.15,
                 specular_color: RGB = (255, 255, 255), shininess: float = 32.0):
        self.base_color = np.array(base_color, dtype=np.float64)
        self.ambient = ambient
        self.specular_color = np.array(specular_color, dtype=np.float64)
        self.shininess = shininess

    def shade(self, position: Vector3, normal: Vector3, light, eye: Vector3) -> RGB:
        raise NotImplementedError("PhongShading dùng shade_array, không shade() đơn lẻ")

    def shade_array(self, positions: np.ndarray, normals: np.ndarray, light, eye: Vector3) -> np.ndarray:
        norms = np.linalg.norm(normals, axis=1, keepdims=True)
        norms[norms == 0] = 1
        N = normals / norms

        light_pos = np.array([light.position.x, light.position.y, light.position.z])
        L = light_pos - positions
        L_norms = np.linalg.norm(L, axis=1, keepdims=True)
        L_norms[L_norms == 0] = 1
        L = L / L_norms

        eye_pos = np.array([eye.x, eye.y, eye.z])
        V = eye_pos - positions
        V_norms = np.linalg.norm(V, axis=1, keepdims=True)
        V_norms[V_norms == 0] = 1
        V = V / V_norms

        # Vector phản xạ R = 2(N·L)N - L — đây là điểm khác Blinn-Phong
        n_dot_l = np.sum(N * L, axis=1, keepdims=True)
        R = 2 * n_dot_l * N - L
        R_norms = np.linalg.norm(R, axis=1, keepdims=True)
        R_norms[R_norms == 0] = 1
        R = R / R_norms

        diffuse_factor = np.clip(n_dot_l, 0.0, 1.0)
        spec_dot = np.clip(np.sum(R * V, axis=1, keepdims=True), 0.0, 1.0)
        specular_factor = np.where(diffuse_factor > 0, spec_dot ** self.shininess, 0.0)

        ambient_color = self.base_color * self.ambient
        diffuse_color = self.base_color * (1 - self.ambient) * diffuse_factor * light.intensity
        specular_color = self.specular_color * specular_factor * light.intensity

        final_color = ambient_color + diffuse_color + specular_color
        return np.clip(final_color, 0, 255).astype(np.uint8)