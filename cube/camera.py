import pyrr
import numpy as np
import math

class Camera:
    """
    set up camera object to get view transform and for easy camera motion
    """
    # initialize camera vectors to defaults
    def __init__(self):
        self.position = pyrr.Vector3(np.array([0, 1, 1], dtype=np.float32))
        self.up = pyrr.Vector3(np.array([0, 1, 0], dtype=np.float32))
        self.target = pyrr.Vector3(np.array([0, 0, 0], dtype=np.float32))
        self.dp = pyrr.Vector3(np.array([0, 0, 0.1], dtype=np.float32))
        self._update_view_transform()

    def _update_view_transform(self):
        """
        calculate the view transform
        """
        self.view_transform = pyrr.matrix44.create_look_at(np.array(self.position),
                                           np.array(self.target),
                                           np.array(self.up),
                                           dtype=np.float32)

    def _get_dp(self):
        """
        calculate delta position
        calculate unit vector in direction of camera -> target
        scale unit vector to get delta p
        """
        scale = 0.1
        return scale * pyrr.vector.normalise(self.target - self.position)

    # move in the direction of -z
    def step_forward(self):
        """
        move towards the target and update camera view transform
        """
        self.dp = self._get_dp()
        self.position += self.dp
        self._update_view_transform()

    # move in the direction of +z
    def step_back(self):
        """
        move away from the target and update camera view transform
        """
        self.dp = self._get_dp()
        self.position -= self.dp
        self._update_view_transform()

    def rotate(self, x_offset, y_offset):
        """
        rotate camera about x and y axis based on x and y offsets
        update camera position, up and transform data
        :param x_offset: x offset from scroll action
        :param y_offset: y offset from scroll action
        """
        factor = 5.0
        x_axis = np.array([1, 0, 0], dtype=np.float32)
        y_axis = np.array([0, 1, 0], dtype=np.float32)
        z_axis = np.array([0, 0, 1], dtype=np.float32)
        # about y axis, in xz plane
        yaw_degrees = x_offset / factor
        # about x axis, yz plane
        pitch_degrees = y_offset / factor
        yaw_tr = pyrr.matrix33.create_from_axis_rotation(axis=y_axis, theta=math.radians(yaw_degrees))
        pitch_tr = pyrr.matrix33.create_from_axis_rotation(axis=x_axis, theta=math.radians(pitch_degrees))
        rotate_tr = yaw_tr @ pitch_tr
        self.position = self.position @ rotate_tr
        self.up = self.up @ rotate_tr
        self._update_view_transform()