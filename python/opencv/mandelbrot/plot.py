import numpy as np
import cv2


class Plot:
    def __init__(self, width: int, height: int, name: str = ''):
        self.name = name
        self.matrix = np.ones(shape=[height, width, 3], dtype=np.uint8)

    def __iter__(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                yield (x, y, tuple(self.matrix[x][y]))

    @property
    def width(self):
        return self.matrix.shape[0]

    @property
    def height(self):
        return self.matrix.shape[1]

    def set_point(self, x: int, y: int, rgb: tuple):
        if not isinstance(x, int) or not isinstance(y, int):
            raise AttributeError('Coordinates must be integers')

        if not len(rgb) == 3:
            raise AttributeError('rgb should be a tuple of length 3')

        if x >= self.width or y >= self.height:
            raise AttributeError('Point ({x}, {y}) does not fit in plot of size {width} x {height}')

        # Reverse rgb as OpenCV uses BGR
        self.matrix[x][y] = list(rgb)[::-1]

    def map(self, func, *args, **kwargs):
        ''' Apply function to ever point in the plot
        function prototype should match:
            >>> def func(x, y, rgb, *args, **kwargs):
                ...
        Where x and y are point coordinates and rgb is the current rgb value
        at that point. Function should return a new rgb tuple.
        '''

        for x, y, rgb in self:
            self.set_point(x, y, func(x, y, rgb, *args, **kwargs))

    def show(self):
        cv2.imshow(self.name, self.matrix)
        cv2.waitKey(0)
