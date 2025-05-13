def read_matrix(filename):
    with open(filename, 'r') as file:
        return [list(map(int, line.split())) for line in file]


def print_matrix(matrix, name):
    print(f"\n{name}:")
    for row in matrix:
        print(" ".join(f"{x:4}" for x in row))


def get_regions(n):
    r1, r2, r3, r4 = [], [], [], []
    for i in range(n):
        for j in range(n):
            if i < j and i + j < n - 1:
                r1.append((i, j))
            elif i < j and i + j > n - 1:
                r2.append((i, j))
            elif i > j and i + j > n - 1:
                r3.append((i, j))
            elif i > j and i + j < n - 1:
                r4.append((i, j))
    return r1, r2, r3, r4


def swap_symmetric(F, region1, region2):
    for (i1, j1), (i2, j2) in zip(region1, region2):
        F[i1][j1], F[i2][j2] = F[i2][j2], F[i1][j1]
    return F


def swap_asymmetric(F, region1, region2):
    for (i1, j1), (i2, j2) in zip(region1, region2):
        F[i1][j1], F[i2][j2] = F[i2][j2], F[i1][j1]
    return F


def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix))]


def multiply_matrices(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def scalar_multiply(K, M):
    return [[K * M[i][j] for j in range(len(M))] for i in range(len(M))]


def subtract_matrices(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]


def build_F(A):
    n = len(A)
    F = [row[:] for row in A]
    r1, r2, r3, r4 = get_regions(n)

    zeros_odd_r4 = sum(1 for (i, j) in r4 if j % 2 == 1 and A[i][j] == 0)
    zeros_even_r1 = sum(1 for (i, j) in r1 if j % 2 == 0 and A[i][j] == 0)

    print(f"\nКоличество нулей в нечетных столбцах области 4: {zeros_odd_r4}")
    print(f"Количество нулей в четных столбцах области 1: {zeros_even_r1}")

    if zeros_odd_r4 > zeros_even_r1:
        print("Меняем симметрично области 2 и 3")
        F = swap_symmetric(F, r2, r3)
    else:
        print("Меняем несимметрично области 1 и 2")
        F = swap_asymmetric(F, r1, r2)

    return F


def main():
    K = int(input("Введите K: "))
    A = read_matrix('matrix.txt')
    print_matrix(A, "Матрица A")

    F = build_F(A)
    print_matrix(F, "Матрица F")

    AT = transpose(A)
    print_matrix(AT, "Транспонированная A")

    FA = multiply_matrices(F, A)
    KAT = scalar_multiply(K, AT)

    print_matrix(FA, "F * A")
    print_matrix(KAT, "K * AT")

    result = subtract_matrices(FA, KAT)
    print_matrix(result, "Результат (F * A) - (K * AT)")


main()