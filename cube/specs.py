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

    texture_coords = np.array([0.25, 0,
                               0.50, 0,
                               0.50, 1,
                               0.25, 1,
                               0.25, 1/3,
                               0.50, 1/3,
                               0.50, 2/3,
                               0.25, 2/3], dtype=np.float32)
    spec.append(texture_coords)
    return spec

def get_textured_cube_spec():
    spec = []
    vertex_positions = np.array([-0.5, -0.5, -0.5, 1, #0
                                  0.5, -0.5, -0.5, 1, #1
                                  0.5,  0.5, -0.5, 1, #2
                                 -0.5,  0.5, -0.5, 1, #3
                                 -0.5, -0.5,  0.5, 1, #4
                                  0.5, -0.5,  0.5, 1, #5
                                  0.5,  0.5,  0.5, 1, #6
                                 -0.5,  0.5,  0.5, 1, #7
                                 -0.5, -0.5, -0.5, 1, #8  -> 0
                                 -0.5, -0.5, -0.5, 1, #9  -> 0
                                  0.5, -0.5, -0.5, 1, #10 -> 1
                                  0.5,  0.5, -0.5, 1, #11 -> 2
                                 -0.5,  0.5, -0.5, 1, #12 -> 3
                                 -0.5,  0.5, -0.5, 1, #13 -> 3
                                 ], dtype=np.float32)
    spec.append(vertex_positions)

    vertex_colors = np.array([1, 0, 0, 1,
                              1, 0, 0, 1,
                              1, 0, 0, 1,
                              1, 0, 0, 1,
                              0, 1, 0, 1,
                              0, 1, 0, 1,
                              0, 1, 0, 1,
                              0, 1, 0, 1,
                              1, 0, 0, 1,
                              1, 0, 0, 1,
                              1, 0, 0, 1,
                              1, 0, 0, 1,
                              1, 0, 0, 1,
                              1, 0, 0, 1,
                              ], dtype=np.float32)
    spec.append(vertex_colors)

    texture_coords = np.array([1,    1/3,
                               0.75, 1/3,
                               0.75, 2/3,
                               1,    2/3,
                               0.25, 1/3,
                               0.50, 1/3,
                               0.50, 2/3,
                               0.25, 2/3,
                               0.25, 0,
                               0,    1/3,
                               0.50, 0,
                               0.50, 1,
                               0,    2/3,
                               0.25, 1,
                               ], dtype=np.float32)
    spec.append(texture_coords)
    return spec