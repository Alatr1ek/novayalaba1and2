import timeit
from itertools import combinations
candidates = [f'P{i + 1}' for i in range(10)]
K = 4


def generate_algo(cands, k):
    result = []
    n = len(cands)

    def rec(curr, idx):
        if len(curr) == k:
            result.append(tuple(curr))
            return
        for i in range(idx, n):
            rec(curr + [cands[i]], i + 1)

    rec([], 0)
    return result


def generate_python(cands, k):
    return list(combinations(cands, k))


def main():
    print(generate_algo(candidates,K))

    t_alg = timeit.timeit(lambda: generate_algo(candidates, K), number=10)
    t_py = timeit.timeit(lambda: generate_python(candidates, K), number=10)
    print(f"Скорость (10 повторов): алгоритмический = {t_alg:.4f}s, python = {t_py:.4f}s\n")

if __name__ == "__main__":
    main()
