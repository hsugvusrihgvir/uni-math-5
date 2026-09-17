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



main()