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