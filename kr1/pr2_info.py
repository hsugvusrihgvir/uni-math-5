def show_reference():
    print()
    print("Справочник:")
    print()
    print("СЛАУ - система линейных алгебраических уравнений.")
    print()
    print("Для решения системы в данном случае используется правило Крамера.")
    print()
    print("Для системы второго порядка:")
    print("a11*x1 + a12*x2 = b1")
    print("a21*x1 + a22*x2 = b2")
    print()
    print("Сначала находится главный определитель:")
    print("D = |a11  a12|")
    print("    |a21  a22|")
    print()
    print("Затем находятся дополнительные определители:")
    print("D1 - первый столбец заменяется столбцом свободных членов.")
    print("D2 - второй столбец заменяется столбцом свободных членов.")
    print()
    print("Если D != 0:")
    print("x1 = D1 / D")
    print("x2 = D2 / D")
    print()
    print("Если D = 0:")
    print("если D1 = 0 и D2 = 0 — бесконечно много решений;")
    print("иначе - решений нет.")
    print()
    print("Для системы третьего порядка используется тот же принцип:")
    print("x1 = D1 / D")
    print("x2 = D2 / D")
    print("x3 = D3 / D")
    print()
    print("Если D = 0, система не имеет единственного решения.")
    print()


def show_explanation(A, B, x, opr):
    n = len(A)

    print()
    print("Ход решения:")
    print()

    print("1. Находим главный определитель:")
    D = opr(n, A)
    print("D =", D)
    print()

    print("2. Находим дополнительные определители:")

    determinants = []

    for j in range(n):
        a = [row[:] for row in A]

        for i in range(n):
            a[i][j] = B[i]

        Dj = opr(n, a)
        determinants.append(Dj)

        print(f"D{j + 1} =", Dj)

    print()

    print("3. Находим неизвестные по правилу Крамера:")

    for i in range(n):
        print(
            f"x{i + 1} = D{i + 1} / D = "
            f"{determinants[i]} / {D} = {x[i]}"
        )

    print()
    print("Ответ:")

    for i in range(n):
        print(f"x{i + 1} =", x[i])

    print()