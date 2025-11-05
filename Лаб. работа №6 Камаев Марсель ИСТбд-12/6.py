import timeit
import matplotlib.pyplot as plt

# 6. F(1) = 1; G(1) = 1; F(n) = (-1)n*(3*F(n–1)–2*G(n–1)), G(n) = F(n–1) /(2n)! + 2*G(n–1), при n >=2

def F_recursive(n):
    if n == 1:
        return 1
    return (-1 if n % 2 else 1) * (3 * F_recursive(n - 1) - 2 * G_recursive(n - 1))


def G_recursive(n):
    if n == 1:
        return 1
    return F_recursive(n - 1) / factorial(2 * n) + 2 * G_recursive(n - 1)


def factorial(k):
    res = 1
    for i in range(2, k + 1):
        res *= i
    return res


def F_iterative(n):
    F_last = 1
    G_last = 1
    fact = 2
    for i in range(2, n + 1):
        fact = fact * (2 * i - 1) * (2 * i)
        sign = -1 if i % 2 else 1
        F = sign * (3 * F_last - 2 * G_last)
        G = F_last / fact + 2 * G_last
        F_last, G_last = F, G

    return F_last

n_values = []
time_rec_values = []
time_itr_values = []
f_rec_values = []
f_itr_values = []

print("n\tВремя рекурсивно (с)\tВремя итеративно (с)\tF(n) рекурс.\tF(n) итерат.")
print("--------------------------------------------------------------------------------")

for n in range(2, 21):
    t_rec = timeit.timeit(lambda n=n: F_recursive(n), number=1)
    t_itr = timeit.timeit(lambda n=n: F_iterative(n), number=1)
    f_rec = F_recursive(n)
    f_itr = F_iterative(n)

    n_values.append(n)
    time_rec_values.append(t_rec)
    time_itr_values.append(t_itr)
    f_rec_values.append(f_rec)
    f_itr_values.append(f_itr)

    print(f"{n}\t{t_rec:.6f}\t\t\t\t{t_itr:.6f}\t\t\t\t{f_rec:.3f}\t\t\t{f_itr:.3f}")

plt.figure(figsize=(10, 6))
plt.plot(n_values, time_rec_values, '--o', label='Рекурсивно')
plt.plot(n_values, time_itr_values, '-o', label='Итеративно')
plt.xlabel('n')
plt.ylabel('Время (с)')
plt.title('Сравнение времени вычисления F(n)')
plt.legend()
plt.grid(True)
plt.show()
