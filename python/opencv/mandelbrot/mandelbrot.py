from random import randint

from plot import Plot
import colours

MAX_ITERATIONS = 100
ITER_COL_MAP = [colours.random().rgb for x in range(0, MAX_ITERATIONS)]

def next_z_orbit(z: complex, c: complex):
    return complex(z) * complex(z) + complex(c)

# z_next = z^2 +c; where z is a complex number
# if |z| > 2, point is not in mandelbrot set
def find_when_point_leaves_mandelbrot_set(x, y, max_iterations=10):
    '''
    Returns the iteration the point (x, y) leaves the madelbrot set
    Returns None if point in mandelbrot set after max_iterations
    '''

    if max_iterations > MAX_ITERATIONS:
        raise AttributeError(f'max_iterations cannot be larger than {MAX_ITERATIONS}')

    z = complex(0, 0)
    c = complex(x, y)

    for i in range(0, max_iterations):
        if (z.real * z.real) + (z.imag * z.imag) > 4:
            return i

        z = next_z_orbit(z, c)

    return None


def transform_point(x, y, rgb, x_max, y_max, max_iterations):
    x_norm = (4*x/x_max) - 2
    y_norm = (4*y/y_max) - 2

    iter_out = find_when_point_leaves_mandelbrot_set(y_norm, x_norm, max_iterations)
    return ITER_COL_MAP[iter_out or 0]

def main():
    plot = Plot(height=1000, width=1000, name='mandelbrot')

    plot.map(transform_point, plot.width, plot.height, 100)

    plot.show()


if __name__ == '__main__':
    main()