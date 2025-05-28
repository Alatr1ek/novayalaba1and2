import timeit
import pandas as pd
import matplotlib.pyplot as plt

def F_recursive(n):
    if n == 1:
        return 1
    return (-1 if n % 2 else 1) * (3 * F_recursive(n-1) - 2 * G_recursive(n-1))

def G_recursive(n):
    if n == 1:
        return 1
    return F_recursive(n-1)/factorial(2*n) + 2 * G_recursive(n-1)

def factorial(k):
    res = 1
    for i in range(2, k+1):
        res *= i
    return res

def F_iterative(n):
    F = [0] * (n+1)
    G = [0] * (n+1)
    F[1] = 1
    G[1] = 1
    fact = 1
    for i in range(2, n+1):
        prev_fact = fact
        for j in range(2*(i-1)+1, 2*i+1):
            prev_fact *= j
        fact = prev_fact
        sign = -1 if i % 2 else 1
        F[i] = sign * (3 * F[i-1] - 2 * G[i-1])
        G[i] = F[i-1]/fact + 2 * G[i-1]
    return F[n]

results = []
for n in range(2, 21):
    t_rec = timeit.timeit(lambda n=n: F_recursive(n), number=1)
    t_itr = timeit.timeit(lambda n=n: F_iterative(n), number=10)
    f_rec = F_recursive(n)
    f_itr = F_iterative(n)
    results.append((n, t_rec, t_itr, f_rec, f_itr))

df = pd.DataFrame(results, columns=['n', 'Время рекурсивно (с)', 'Время итеративно (с)', 'F(n) рекурс.', 'F(n) итерат.'])

pd.set_option('display.float_format', '{:.3f}'.format)

print(df.to_string(index=False))

plt.figure(figsize=(10,6))
plt.plot(df['n'], df['Время рекурсивно (с)'], '--o', label='Рекурсивно')
plt.plot(df['n'], df['Время итеративно (с)'], '-o', label='Итеративно')
plt.xlabel('n')
plt.ylabel('Время (с)')
plt.title('Сравнение времени вычисления F(n)')
plt.legend()
plt.grid(True)
plt.show()
