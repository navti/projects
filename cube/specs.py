import numpy as np

def get_cube_spec():
    spec = []
    vertex_positions = np.array([-0.5, -0.5, -0.5, 1,
                                  0.5, -0.5, -0.5, 1,
                                  0.5,  0.5, -0.5, 1,
                                 -0.5,  0.5, -0.5, 1,
                                 -0.5, -0.5,  0.5, 1,
                                  0.5, -0.5,  0.5, 1,
                                  0.5,  0.5,  0.5, 1,
                                 -0.5,  0.5,  0.5, 1,], dtype=np.float32)
    spec.append(vertex_positions)

    vertex_colors = np.array([1, 0, 0, 1,
                              1, 0, 0, 1,
                              1, 0, 0, 1,
                              1, 0, 0, 1,
                              0, 1, 0, 1,
                              0, 1, 0, 1,
                              0, 1, 0, 1,
                              0, 1, 0, 1], dtype=np.float32)
    spec.append(vertex_colors)

    return spec