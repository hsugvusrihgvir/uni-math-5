eps = 1e-9
PI = 3.141592653589793


def inp_number(name):
    while True:
        value = input(f"Введите {name}: ").strip().replace(",", ".")

        if value == "-0" or value == "+0":
            print("Нужно ввести число без знака у нуля.")
            continue

        try:
            return float(value)
        except ValueError:
            print("Нужно ввести вещественное число.")


def arctg(x):
    # для |x| <= 1 используем ряд:
    # arctg(x) = x - x^3/3 + x^5/5 - x^7/7 + ...

    # если |x| > 1, сначала уменьшаем аргумент

    # arctg(x) = pi/2 - arctg(1/x) если x > 1
    if x > 1:
        return PI / 2 - arctg(1 / x)

    # arctg(x) = -pi/2 - arctg(1/x) если x < -1
    if x < -1:
        return -PI / 2 - arctg(1 / x)

    result = 0
    k = 0

    while True:
        part = ((-1) ** k) * (x ** (2 * k + 1)) / (2 * k + 1)

        if abs(part) < eps:
            break

        result += part
        k += 1

    return result


def get_quadrant(x, y):
    if abs(x) < eps and abs(y) < eps:
        return "Начало координат"

    if abs(y) < eps:
        if x > 0:
            return "Положительная полуось Ox"
        else:
            return "Отрицательная полуось Ox"

    if abs(x) < eps:
        if y > 0:
            return "Положительная полуось Oy"
        else:
            return "Отрицательная полуось Oy"

    if x > 0 and y > 0:
        return "I четверть"

    if x < 0 and y > 0:
        return "II четверть"

    if x < 0 and y < 0:
        return "III четверть"

    return "IV четверть"


def show_quadrants():
    print()
    print("                Im")
    print("                 ^")
    print("                 |")
    print("          II     |     I")
    print("                 |")
    print("    -------------+-------------> Re")
    print("                 |")
    print("          III    |     IV")
    print("                 |")
    print()


def get_argument(x, y):
    if abs(x) < eps and abs(y) < eps:
        return None

    # I четверть
    if x > eps and y > eps:
        return arctg(y / x)

    # II четверть
    if x < -eps and y > eps:
        return PI + arctg(y / x)

    # III четверть
    if x < -eps and y < -eps:
        return PI + arctg(y / x)

    # IV четверть
    if x > eps and y < -eps:
        return 2 * PI + arctg(y / x)

    # положительная полуось Ox
    if x > eps and abs(y) < eps:
        return 0

    # положительная полуось Oy
    if abs(x) < eps and y > eps:
        return PI / 2

    # отрицательная полуось Ox
    if x < -eps and abs(y) < eps:
        return PI

    # отрицательная полуось Oy
    if abs(x) < eps and y < -eps:
        return 3 * PI / 2


def format_number(value):
    if abs(value) < eps:
        return "0"

    if abs(value - round(value)) < eps:
        return str(int(round(value)))

    return str(round(value, 6))


def show_reference():
    print()
    print("Справочник:")
    print()

    print("Комплексное число в алгебраической форме:")
    print("z = x + yi")
    print()
    print("x - вещественная часть")
    print("y - коэффициент при мнимой части")
    print()

    print("Тригонометрическая форма:")
    print("z = r * (cos(phi) + i*sin(phi))")
    print()

    print("Модуль комплексного числа вычисляется по формуле:")
    print("r = sqrt(x^2 + y^2)")
    print()

    print("Аргумент phi - угол комплексного числа.")
    print("В программе он выбирается из промежутка [0; 2*pi).")
    print()

    print("Определение аргумента:")
    print()
    print("1) x > 0")
    print("   phi = arctg(y / x)")
    print()

    print("2) x < 0 и y >= 0")
    print("   phi = pi + arctg(y / x)")
    print()

    print("3) x < 0 и y < 0")
    print("   phi = -pi + arctg(y / x)")
    print()

    print("4) x = 0 и y > 0")
    print("   phi = pi / 2")
    print()

    print("5) x = 0 и y < 0")
    print("   phi = -pi / 2")
    print()

    print("6) x > 0 и y = 0")
    print("   phi = 0")
    print()

    print("7) x < 0 и y = 0")
    print("   phi = pi")
    print()

    print("Таблица четвертей:")
    show_quadrants()

    print("I четверть:   x > 0, y > 0")
    print("II четверть:  x < 0, y > 0")
    print("III четверть: x < 0, y < 0")
    print("IV четверть:  x > 0, y < 0")
    print()


def show_explanation(x, y, r, quadrant, phi):
    print()
    print("Ход решения:")
    print()

    print("1. Исходное комплексное число:")
    print(f"z = {format_number(x)} + ({format_number(y)})i")
    print()

    print("2. Находим модуль:")
    print("r = sqrt(x^2 + y^2)")
    print(
        f"r = sqrt(({format_number(x)})^2 + "
        f"({format_number(y)})^2)"
    )
    print(f"r = {format_number(r)}")
    print()

    print("3. Определяем положение числа:")
    print(quadrant)
    show_quadrants()

    print("4. Находим аргумент:")

    if x > eps:
        print("x > 0")
        print("phi = arctg(y / x)")
        print(
            f"phi = arctg({format_number(y)} / "
            f"{format_number(x)})"
        )

    elif x < -eps and y >= -eps:
        print("x < 0 и y >= 0")
        print("phi = pi + arctg(y / x)")
        print(
            f"phi = pi + arctg({format_number(y)} / "
            f"{format_number(x)})"
        )

    elif x < -eps and y < -eps:
        print("x < 0 и y < 0")
        print("phi = -pi + arctg(y / x)")
        print(
            f"phi = -pi + arctg({format_number(y)} / "
            f"{format_number(x)})"
        )

    elif abs(x) < eps and y > eps:
        print("x = 0 и y > 0")
        print("phi = pi / 2")

    elif abs(x) < eps and y < -eps:
        print("x = 0 и y < 0")
        print("phi = -pi / 2")

    elif x > eps and abs(y) < eps:
        print("x > 0 и y = 0")
        print("phi = 0")

    elif x < -eps and abs(y) < eps:
        print("x < 0 и y = 0")
        print("phi = pi")

    print()
    print("phi =", format_number(phi), "рад")
    print()

    print("5. Записываем тригонометрическую форму:")
    print(
        f"z = {format_number(r)} * "
        f"(cos({format_number(phi)}) + "
        f"i*sin({format_number(phi)}))"
    )
    print()


def solve(x, y):
    print()

    if abs(x) < eps and abs(y) < eps:
        print("z = 0")
        print("Для нулевого комплексного числа аргумент не определён.")
        print("Тригонометрическая форма в обычном виде не записывается.")
        return

    r = (x ** 2 + y ** 2) ** 0.5
    quadrant = get_quadrant(x, y)
    phi = get_argument(x, y)


    print("Модуль r =", format_number(r))
    print("Аргумент phi =", format_number(phi), "рад")
    print()

    print("Тригонометрическая форма:")
    print(
        f"z = {format_number(r)} * "
        f"(cos({format_number(phi)}) + "
        f"i*sin({format_number(phi)}))"
    )
    print()

    while True:
        answer = input(
            "Показать ход решения? (1 - да, 0 - нет): "
        ).strip()

        if answer == "1":
            show_explanation(x, y, r, quadrant, phi)
            break

        if answer == "0":
            break

        print("Нужно ввести 1 или 0.")


def input_complex():
    print()
    print("Комплексное число имеет вид:")
    print("z = x + yi")
    print()
    print("Можно вводить целые и дробные числа.")
    print("Дробные можно писать через точку или через запятую.")
    print()

    x = inp_number("x")
    y = inp_number("y")

    return x, y


def main():
    while True:
        print()
        print()
        print("Меню:")
        print("0 - выйти")
        print("1 - перевести комплексное число в тригонометрическую форму")
        print("2 - справочник")

        choice = input("Выберите пункт меню: ").strip()

        match choice:
            case "0":
                break

            case "2":
                show_reference()

            case "1":
                x, y = input_complex()
                solve(x, y)

            case _:
                print("Такого пункта меню нет")


if __name__ == "__main__":
    main()