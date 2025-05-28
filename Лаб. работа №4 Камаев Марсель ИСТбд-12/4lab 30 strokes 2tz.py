import numpy as np

def print_matrix(matrix, name):
    print(f"\n{name}:")
    for row in matrix:
        row_str = ' '.join(f"{int(round(x)):4d}" for x in row)
        print(f"[{row_str}]")

def is_secondary_symmetric(A):
    n = A.shape[0]
    return np.all(A[::-1].T == A)

def split_blocks(A):
    n = A.shape[0] // 2
    E = A[:n, :n]
    B = A[:n, n:]
    D = A[n:, :n]
    C = A[n:, n:]
    return E, B, D, C

def build_F(A):
    F = A.copy()
    E, B, D, C = split_blocks(A)
    n = E.shape[0]
    if is_secondary_symmetric(A):
        print("\nA симметрична относительно побочной диагонали — меняем B и D симметрично")
        F[:n, n:], F[n:, :n] = D.T, B.T
    else:
        print("\nA не симметрична относительно побочной диагонали — меняем D и E несимметрично")
        F[:n, :n], F[n:, :n] = D, E
    return F
def plot_graphs(F):
    plt.figure(figsize=(15, 4))
    for i, (title, data) in enumerate([
        ("Тепловая карта F", F),
        ("Среднее по столбцам", F.mean(axis=0)),
        ("Гистограмма значений F", F.flatten())
    ]):
        plt.subplot(1, 3, i+1)
        plt.imshow(data, cmap='coolwarm') if i == 0 else plt.plot(data, 'o-') if i == 1 else plt.hist(data, bins=10, color='skyblue')
        plt.title(title)
    plt.tight_layout(); plt.show()
def main():
    K = int(input("Введите K: "))
    A = np.loadtxt('matrix_data.txt', dtype=int)
    print_matrix(A, "A")

    F = build_F(A)
    print_matrix(F, "F")

    try:
        det_A = np.linalg.det(A)
        diag_sum_F = np.trace(F)
        print(f"\nОпределитель A: {det_A:.2f}, Сумма диагонали F: {diag_sum_F:.2f}")

        if det_A > diag_sum_F:
            print("\ndet(A) > sum(diag(F)), считаем: A^-1 * A^T – K * F^-1")
            A_inv = np.linalg.inv(A)
            F_inv = np.linalg.inv(F)
            result = A_inv @ A.T - K * F_inv
        else:
            print("\ndet(A) <= sum(diag(F)), считаем: (A^T + G – F^T) * K")
            G = np.tril(A)
            result = (A.T + G - F.T) * K

        print_matrix(np.round(result).astype(int), "Результат")
    except np.linalg.LinAlgError:
        print("Ошибка: одна из матриц необратима")

main()
