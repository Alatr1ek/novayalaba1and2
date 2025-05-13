import sys

def read_matrix_from_file(filename, N):
    """Чтение матрицы из файла с проверкой размера"""
    try:
        with open(filename, 'r') as file:
            matrix = []
            for _ in range(N):
                line = file.readline()
                if not line:
                    raise ValueError("Файл содержит недостаточно строк для матрицы размера N")
                row = list(map(int, line.strip().split()))
                if len(row) != N:
                    raise ValueError("Количество элементов в строке не соответствует размеру N")
                matrix.append(row)
            return matrix
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка в данных файла: {e}", file=sys.stderr)
        sys.exit(1)

def print_matrix(matrix, name):
    """Вывод матрицы с форматированием"""
    print(f"\n{name}:")
    for row in matrix:
        print(' '.join(f"{elem:5}" for elem in row))

def count_zeros_in_area(matrix, condition):
    """Подсчет нулей в области по условию"""
    return sum(1 for i in range(len(matrix)) 
               for j in range(len(matrix)) 
               if condition(i, j, len(matrix)) and matrix[i][j] == 0)

def area1(i, j, n):
    """Условие для области 1"""
    return i < j and i < n//2 and j < n//2

def area4(i, j, n):
    """Условие для области 4"""
    return i > j and i >= n//2 and j >= n//2

def swap_symmetrical(F, n):
    """Симметричный обмен областей 2 и 3"""
    for i in range(n//2):
        for j in range(n//2, n):
            if i < j:  # Область 2
                mirror_i = n - 1 - i
                mirror_j = n - 1 - j
                F[i][j], F[mirror_i][mirror_j] = F[mirror_i][mirror_j], F[i][j]

def swap_non_symmetrical(F, n):
    """Несимметричный обмен областей 1 и 2"""
    temp = [row[:] for row in F]
    for i in range(n//2):
        for j in range(n):
            if area1(i, j, n):  # Область 1
                F[i][j] = temp[i][n//2 + j] if j < n//2 else temp[i][j - n//2]
            elif i < j and j >= n//2:  # Область 2
                F[i][j] = temp[i][j - n//2]

def matrix_multiply(A, B):
    """Умножение матриц без NumPy"""
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def matrix_power(matrix, power):
    """Возведение матрицы в степень"""
    result = matrix
    for _ in range(power - 1):
        result = matrix_multiply(result, matrix)
    return result

def main():
    # Ввод параметров
    try:
        K = int(input("Введите число K: "))
        N = int(input("Введите размер матрицы N: "))
        filename = input("Введите имя файла с матрицей: ")
    except ValueError:
        print("Ошибка: введены некорректные данные", file=sys.stderr)
        sys.exit(1)
    
    # Чтение и проверка матрицы
    A = read_matrix_from_file(filename, N)
    print_matrix(A, "Исходная матрица A")
    
    # Создание матрицы F
    F = [row[:] for row in A]
    
    # Подсчет нулей в областях
    zeros_area4 = count_zeros_in_area(F, lambda i,j,n: area4(i,j,n) and j%2!=0)
    zeros_area1 = count_zeros_in_area(F, lambda i,j,n: area1(i,j,n) and j%2==0)
    
    # Выполнение условий задачи
    if zeros_area4 > zeros_area1:
        swap_symmetrical(F, N)
        print("\nВыполнен симметричный обмен областей 2 и 3")
    else:
        swap_non_symmetrical(F, N)
        print("\nВыполнен несимметричный обмен областей 1 и 2")
    print_matrix(F, "Матрица F после преобразований")
    
    # Вычисление выражений
    F_transposed = [[F[j][i] for j in range(N)] for i in range(N)]
    F_star_A = matrix_multiply(F_transposed, A)
    A_pow_n = matrix_power(A, N)
    K_A_pow_n = [[K * num for num in row] for row in A_pow_n]
    result = [[F_star_A[i][j] - K_A_pow_n[i][j] for j in range(N)] for i in range(N)]
    
    # Вывод результатов
    print_matrix(F_transposed, "Транспонированная матрица F*")
    print_matrix(F_star_A, "Результат F* * A")
    print_matrix(A_pow_n, f"Матрица A^{N}")
    print_matrix(K_A_pow_n, f"Матрица K * A^{N}")
    print_matrix(result, "Итоговый результат (F* * A) - (K * A^N)")

if __name__ == "__main__":
    main()