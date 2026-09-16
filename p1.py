def inp(name):
    while True:
        value = input(f"Введите {name} и нажмите Enter: ").strip().replace(",", ".")
        if value == "-0" or value == "+0":
            print("Нужно ввести число")
            continue
        try:
            return float(value)
        except ValueError:
            print("Нужно ввести число")


eps = 1e-9


class SVG:
    def __init__(self, w, h, x_min, x_max, y_min, y_max, K):
        self.w = w
        self.h = h

        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        self.K = K
        self.finished = False

        self.svg = f"""
    <svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">

    <rect width="{w}" height="{h}" fill="white"/>
    """

        self.add_coordinate_plane()


    def to_svg(self, x, y):
        svg_x = (x - self.x_min) / (self.x_max - self.x_min) * self.w
        # так как в картинках координаты по y перевернуты
        svg_y = (self.y_max - y) / (self.y_max - self.y_min) * self.h

        return svg_x, svg_y


    def add_svg_line(self, x1, y1, x2, y2, color="blue", width=2):
        self.svg += f"""
    <line
    x1="{x1}"
    y1="{y1}"
    x2="{x2}"
    y2="{y2}"
    stroke="{color}"
    stroke-width="{width}"
    />
    """


    def add_line(self, x1, y1, x2, y2, color="blue", width=2):
        point1 = self.to_svg(x1, y1)
        point2 = self.to_svg(x2, y2)

        self.add_svg_line(point1[0], point1[1], point2[0], point2[1], color, width)


    def add_text(self, x, y, text, size=12):
        self.svg += f"""
    <text
    x="{x}"
    y="{y}"
    font-size="{size}"
    fill="black"
    >{text}</text>
    """

    # через сколько целых чисел рисовать клетку чтобы не сливалось. не менее 30 пиксеоей между
    def get_step(self):
        step = 1

        while step * self.K < 30:
            step *= 2

        return step


    # первая линия сетки, коот. попадет в картинку
    def first_value(self, min_value, step):
        value = int(min_value / step) * step

        # для положительных чисел
        if value < min_value - eps:
            value += step

        return value


    def add_grid(self):
        step = self.get_step()

        x = self.first_value(self.x_min, step)

        while x <= self.x_max + eps:
            if abs(x) > eps: # в 0 не рисуем
                self.add_line(
                    x,
                    self.y_min,
                    x,
                    self.y_max,
                    "#eeeeee",
                    1
                )

            x += step


        y = self.first_value(self.y_min, step)

        while y <= self.y_max + eps:
            if abs(y) > eps: # в 0 не рисуем
                self.add_line(
                    self.x_min,
                    y,
                    self.x_max,
                    y,
                    "#eeeeee",
                    1
                )

            y += step


    def add_axes(self):
        step = self.get_step()

        # ось X
        if self.y_min - eps <= 0 <= self.y_max + eps: # если ось внутри картинки
            self.add_line(
                self.x_min,
                0,
                self.x_max,
                0,
                "black",
                1
            )

            x = self.first_value(self.x_min, step)

            while x <= self.x_max + eps:
                point = self.to_svg(x, 0)

                # рисуем деления
                self.add_svg_line(
                    point[0],
                    point[1] - 4,
                    point[0],
                    point[1] + 4,
                    "black",
                    1
                )

                if abs(x) > eps:
                    self.add_text(
                        point[0] + 3,
                        point[1] + 16,
                        x
                    )

                x += step


        # ось Y
        if self.x_min - eps <= 0 <= self.x_max + eps: # если ось внутри картинки
            self.add_line(
                0,
                self.y_min,
                0,
                self.y_max,
                "black",
                1
            )

            y = self.first_value(self.y_min, step)

            while y <= self.y_max + eps:
                point = self.to_svg(0, y)

                self.add_svg_line(
                    point[0] - 4,
                    point[1],
                    point[0] + 4,
                    point[1],
                    "black",
                    1
                )

                if abs(y) > eps:
                    self.add_text(
                        point[0] + 7,
                        point[1] - 4,
                        y
                    )

                y += step


    def add_coordinate_plane(self):
        self.add_grid()
        self.add_axes()


    def finish(self):
        if not self.finished:
            self.svg += """
    </svg>
    """
            self.finished = True

        return self.svg


    def save(self, filename):
        result = self.finish()

        file = open(filename, "w", encoding="utf-8")
        file.write(result)
        file.close()


# ищем середину между прямыми
def center(a11, a12, b1, a21, a22, b2, res):
    # прямые пересекаются
    if res == 0:
        o = a11 * a22 - a12 * a21
        o1 = b1 * a22 - a12 * b2
        o2 = a11 * b2 - b1 * a21

        cx = o1 / o
        cy = o2 / o

        return cx, cy

    # прямые совпадают
    if res == 1:
        # выбираем уравнение которое действительно задаёт прямую
        if abs(a11) > eps or abs(a12) > eps:
            A = a11
            B = a12
            C = b1
        elif abs(a21) > eps or abs(a22) > eps:
            A = a21
            B = a22
            C = b2
        else:
            return 0, 0

        # ищем ближайшую к 0 0 точку
        # знаменатель
        d = A ** 2 + B ** 2

        cx = A * C / d
        cy = B * C / d

        return cx, cy

    # прямые параллельны
    if res == -1:
        n1 = (a11 ** 2 + a12 ** 2) ** 0.5
        n2 = (a21 ** 2 + a22 ** 2) ** 0.5

        # нормализуем
        A1 = a11 / n1
        B1 = a12 / n1
        C1 = b1 / n1

        A2 = a21 / n2
        B2 = a22 / n2
        C2 = b2 / n2

        # чтобы нормали смотрели в одну сторону
        if A1 * A2 + B1 * B2 < -eps:
            A2 = -A2
            B2 = -B2
            C2 = -C2

        # средняя прямая между двумя
        Cmid = (C1 + C2) / 2

        # ближайшая к (0, 0) точка этой средней прямой
        cx = A1 * Cmid
        cy = B1 * Cmid

        return cx, cy


# ищем, где прямые пересекаются с границами картинки
def points_img(A, B, C, x_min, x_max, y_min, y_max):
    points = set()

    if abs(B) > eps:
        # левая граница
        y = (C - A * x_min) / B
        if y_min - eps <= y <= y_max + eps:
            points.add((x_min, y))
        # правая граница
        y = (C - A * x_max) / B
        if y_min - eps <= y <= y_max + eps:
            points.add((x_max, y))

    if abs(A) > eps:
        # нижняя граница
        x = (C - B * y_min) / A
        if x_min - eps <= x <= x_max + eps:
            points.add((x, y_min))
        # верхняя граница
        x = (C - B * y_max) / A
        if x_min - eps <= x <= x_max + eps:
            points.add((x, y_max))

    points = list(points)

    if len(points) != 2:
        raise Exception("Точек пересечение больше 2. Что то не так считалось")

    return points


# расстояние между параллельными прямыми (чтобы уместить обе прямые, если они не пересекаются)
def distance(a11, a12, b1, a21, a22, b2):
    # нрмализуем прямые
    # длины нормалей
    n1 = (a11 ** 2 + a12 ** 2) ** 0.5
    n2 = (a21 ** 2 + a22 ** 2) ** 0.5

    # нам нужны только оменять b1 и b2 ля результата
    c1 = b1 / n1
    c2 = b2 / n2

    # если напрвлены в разные стороны
    if a11 * a21 + a12 * a22 < -eps:
        c2 = -c2

    return abs(c2 - c1)



def gr(a11, a12, b1, a21, a22, b2, r, filename="graph.svg"):
    K = 30
    w = 600
    h = 600

    if r == -1:
        dist = distance(a11, a12, b1, a21, a22, b2)

        if dist > eps and dist / 2 * K > 250:
            K = 500 / dist

    cx, cy = center(a11, a12, b1, a21, a22, b2, r)
    ox, oy = 0, 0

    # ищем границы на коорд. прямой
    x_min = cx - w / (2 * K)
    x_max = cx + w / (2 * K)

    y_min = cy - h / (2 * K)
    y_max = cy + h / (2 * K)

    # точки пересечения границ картинки и прямых
    points1 = points_img(a11, a12, b1, x_min, x_max, y_min, y_max)
    points2 = points_img(a21, a22, b2, x_min, x_max, y_min, y_max)

    svg = SVG(
        w,
        h,
        x_min,
        x_max,
        y_min,
        y_max,
        K
    )

    svg.add_line(
        points1[0][0],
        points1[0][1],
        points1[1][0],
        points1[1][1],
        "red"
    )

    svg.add_line(
        points2[0][0],
        points2[0][1],
        points2[1][0],
        points2[1][1],
        "green"
    )

    svg.save(filename)



def main():
    while True:
        print("Введите 0, чтобы выйти, или что-либо другое, чтобы начать новое решение, и нажмите Enter:")

        if input() == "0":
            break

        print("a11*x1 + a12*x2 = b1")
        print("a21*x1 + a22*x2 = b2")
        print()

        while True:
            a11 = inp("a11")
            a12 = inp("a12")
            b1 = inp("b1")

            if abs(a11) < eps and abs(a12) < eps:
                print("уравнение не задаёт прямую. Введите корректные данные")
            else:
                break

        print()

        while True:
            a21 = inp("a21")
            a22 = inp("a22")
            b2 = inp("b2")

            if abs(a21) < eps and abs(a22) < eps:
                print("уравнение не задаёт прямую. Введите корректные данные")
            else:
                break

        o = a11 * a22 - a12 * a21
        o1 = b1 * a22 - a12 * b2
        o2 = a11 * b2 - b1 * a21

        print()

        res = 0

        if abs(o) < eps:
            print("Определитель = 0")

            if abs(a11) < eps and abs(a12) < eps and abs(a21) < eps and abs(a22) < eps:
                if abs(b1) < eps and abs(b2) < eps:
                    print("Система имеет бесконечно много решений")
                    res = 1
                else:
                    print("Система не имеет решений")
                    res = -1

            elif abs(o1) < eps and abs(o2) < eps:
                print("Система имеет бесконечно много решений")
                res = 1

            else:
                print("Система не имеет решений")
                res = -1

        else:
            x1 = o1 / o
            x2 = o2 / o

            print("Система имеет единственное решение:")
            print("x1 =", x1)
            print("x2 =", x2)

        print()
        filename = input("Введите название картинки или 0, чтобы оставить название graph.svg: ").strip()

        if filename == "0" or filename == "":
            filename = "graph.svg"
        elif not filename.lower().endswith(".svg"):
            filename += ".svg"

        gr(a11, a12, b1, a21, a22, b2, res, filename)

        print(f"График сохранён в {filename}")
        print()


def get_res(a11, a12, b1, a21, a22, b2):
    o = a11 * a22 - a12 * a21
    o1 = b1 * a22 - a12 * b2
    o2 = a11 * b2 - b1 * a21

    if abs(o) < eps:
        if abs(a11) < eps and abs(a12) < eps and abs(a21) < eps and abs(a22) < eps:
            if abs(b1) < eps and abs(b2) < eps:
                return 1
            else:
                return -1

        elif abs(o1) < eps and abs(o2) < eps:
            return 1
        else:
            return -1

    return 0

def test_gr():
    tests = [
        ("pr1_test_img/test_1_cross.svg", 1, 1, 4, 1, -1, 0),
        ("pr1_test_img/test_2_parallel.svg", 0, 1, 2, 0, 1, 5),
        ("pr1_test_img/test_3_same.svg", 1, 1, 4, 2, 2, 8),
        ("pr1_test_img/test_4_vertical_horizontal.svg", 1, 0, 3, 0, 1, 2),
        ("pr1_test_img/test_5_vertical_parallel.svg", 1, 0, 2, 1, 0, 5),
        ("pr1_test_img/test_6_float.svg", 1.5, 2.5, 7.2, -0.5, 3.0, 1.1),
    ]

    for filename, a11, a12, b1, a21, a22, b2 in tests:
        r = get_res(a11, a12, b1, a21, a22, b2)
        gr(a11, a12, b1, a21, a22, b2, r, filename)
        print(f"{filename} создан")

test_gr()
main()