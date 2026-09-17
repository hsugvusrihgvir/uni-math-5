from pr1_gr import gr
eps = 1e-9



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


def opr(n, a):
    if n == 1:
        return a[0][0]

    if n == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]

    s = 0

    for i in range(n):
        minor = []

        for row in a[1:]:
            minor.append(row[:i] + row[i + 1:])

        if i % 2 == 0:
            s += a[0][i] * opr(n - 1, minor)
        else:
            s -= a[0][i] * opr(n - 1, minor)

    return s

def solve(A, B):
    n = len(A)

    o = opr(n, A)

    if abs(o) < eps:
        return None

    x = []

    for j in range(n):
        a = [row[:] for row in A]

        for i in range(n):
            a[i][j] = B[i]

        oi = opr(n, a)
        x.append(oi / o)

    return x


def print_system(n):
    for i in range(n):
        eq = ""

        for j in range(n):
            if j > 0:
                eq += " + "

            eq += f"a{i + 1}{j + 1}*x{j + 1}"

        eq += f" = b{i + 1}"

        print(eq)

    print()


def input_system(n):
    A = []
    B = []

    for i in range(n):
        while True:
            row = []

            for j in range(n):
                row.append(inp(f"a{i + 1}{j + 1}"))

            b = inp(f"b{i + 1}")

            if all(abs(value) < eps for value in row):
                print("Уравнение не задаёт прямую илм плоскость. Введите корректные данные")
            else:
                A.append(row)
                B.append(b)
                break

        print()

    return A, B


def print_solution(x):
    print("Система имеет единственное решение:")

    for i in range(len(x)):
        print(f"x{i + 1} =", x[i])


def graph_name():
    filename = input(
        "Введите название картинки или 0, чтобы оставить название graph.svg: "
    ).strip()

    if filename == "0" or filename == "":
        return "graph.svg"

    if not filename.lower().endswith(".svg"):
        filename += ".svg"

    return filename


def main():
    while True:
        print()
        print()
        print("Меню:")
        print("0 - выйти")
        print("2 - решить СЛАУ второго порядка")
        print("3 - решить СЛАУ третьего порядка")

        choice = input("Выберите пункт меню: ").strip()

        match choice:
            case "0":
                break

            case "2" | "3":
                n = int(choice)

                print_system(n)

                A, B = input_system(n)

                x = solve(A, B)

                if x is None:
                    print("Определитель = 0")

                    if n == 2:
                        a11 = A[0][0]
                        a12 = A[0][1]
                        a21 = A[1][0]
                        a22 = A[1][1]

                        b1 = B[0]
                        b2 = B[1]

                        o1 = b1 * a22 - a12 * b2
                        o2 = a11 * b2 - b1 * a21

                        if abs(o1) < eps and abs(o2) < eps:
                            print("Система имеет бесконечно много решений")
                            res = 1
                        else:
                            print("Система не имеет решений")
                            res = -1

                    else:
                        print("Система не имеет единственного решения")

                else:
                    print_solution(x)
                    if n == 2:
                        res = 0

                if n == 2:
                    filename = graph_name()

                    gr(
                        A[0][0],
                        A[0][1],
                        B[0],
                        A[1][0],
                        A[1][1],
                        B[1],
                        res,
                        filename
                    )

                    print(f"График сохранён в {filename}")

                print()

            case _:
                print("Такого пункта меню нет")
                print()

main()