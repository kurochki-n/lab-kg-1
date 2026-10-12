import numpy as np
from PIL import Image
from math import floor


def line(img_mat, x0: float, y0: float, x1: float, y1: float) -> None:
    d_max = max(abs(floor(x0) - floor(x1)), abs(floor(y0) - floor(y1)))
    L = d_max + 1

    if L == 1:
        dot(img_mat, get_color(y0+500), x0, y0)
        return

    d_x = (x1 - x0) / (L - 1)
    d_y = (y1 - y0) / (L - 1)

    x, y = x0, y0

    for _ in range(L):
        dot(img_mat, get_color(y+500), x, y)
        x += d_x
        y += d_y


def dot(img_mat, color, x: float, y: float) -> None:
    img_mat[-floor(x) + 500, -floor(y) + 500] = color


def parse(filename: str) -> tuple[list, list]:
    v = []
    f = []
    with open(filename, "r") as file:
        for s in file:
            spl = s.split()
            if spl[0] == "v":
                v.append([float(spl[1]), float(spl[2]), float(spl[3])])
            elif spl[0] == "f":
                f.append(
                    [
                        int(spl[1].split("/")[0]),
                        int(spl[2].split("/")[0]),
                        int(spl[3].split("/")[0]),
                    ]
                )
    return v, f


def get_color(y) -> list[int, int, int]:
    d = (y // 20) % 10
    if d % 2 == 0:
        return [255, 255, 255]
    else:
        return [255, 0, 255]


def draw(v, f, img_mat) -> None:
    for obj in f:
        line(
            img_mat,
            v[obj[0] - 1][1],
            v[obj[0] - 1][0],
            v[obj[1] - 1][1],
            v[obj[1] - 1][0],
        )
        line(
            img_mat,
            v[obj[1] - 1][1],
            v[obj[1] - 1][0],
            v[obj[2] - 1][1],
            v[obj[2] - 1][0],
        )
        line(
            img_mat,
            v[obj[2] - 1][1],
            v[obj[2] - 1][0],
            v[obj[0] - 1][1],
            v[obj[0] - 1][0],
        )
        # dot(img_mat, color, -obj[1]+500, -obj[0]+500


if __name__ == "__main__":
    # изображения - интовый беззнаковый восьмибитный массив
    img_mat = np.zeros((1000, 1000, 3), dtype=np.uint8)
    # dda(img_mat, [0, 200, 185], 12.34, 43.21, 123.45, 987.65)
    v, f = parse("feline.obj")
    draw(v, f, img_mat)
    img = Image.fromarray(img_mat)
    img.save("img.png")
