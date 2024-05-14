import pyrr
import numpy as np

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
        self.view_transform = self._get_view_transform()

    def _get_view_transform(self):
        """
        calculate the view transform
        """
        return pyrr.matrix44.create_look_at(np.array(self.position),
                                           np.array(self.target),
                                           np.array(self.up),
                                           dtype=np.float32)

    def _get_dp(self):
        scale = 0.1
        return scale * pyrr.vector.normalise(self.target - self.position)

    # move in the direction of -z
    def step_forward(self):
        self.dp = self._get_dp()
        self.position += self.dp
        self.view_transform = self._get_view_transform()
        return self.view_transform

    # move in the direction of +z
    def step_back(self):
        self.dp = self._get_dp()
        self.position -= self.dp
        self.view_transform = self._get_view_transform()
        return self.view_transform
