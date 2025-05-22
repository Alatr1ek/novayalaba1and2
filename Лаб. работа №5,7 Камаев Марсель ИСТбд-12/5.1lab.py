import timeit
from itertools import combinations

candidates = [f'P{i+1}' for i in range(15)]
K = 4

def generate_algo(cands, k):
    result = []
    n = len(cands)
    def rec(curr, idx):
        if len(curr) == k:
            result.append(tuple(curr))
            return
        for i in range(idx, n):
            rec(curr + [cands[i]], i+1)
    rec([], 0)
    return result

def generate_python(cands, k):
    return list(combinations(cands, k))

age = {name: 20 + (i % 15) for i, name in enumerate(candidates)}

def filter_and_optimize(juries, min_count=10, max_count=30):
    for limit in range(K * min(age.values()), K * max(age.values()) + 1):
        valid = [jury for jury in juries if sum(age[name] for name in jury) <= limit]
        if min_count <= len(valid) <= max_count:
            max_avg = max(sum(age[name] for name in jury) / K for jury in valid)
            best = [jury for jury in valid if sum(age[name] for name in jury) / K == max_avg]
            return best, max_avg, limit, len(valid)
    limit = K * max(age.values())
    valid = [jury for jury in juries if sum(age[name] for name in jury) <= limit]
    max_avg = max(sum(age[name] for name in jury) / K for jury in valid) if valid else 0
    best = [jury for jury in valid if sum(age[name] for name in jury) / K == max_avg]
    return best, max_avg, limit, len(valid)

def main():
    t_alg = timeit.timeit(lambda: generate_algo(candidates, K), number=10)
    t_py  = timeit.timeit(lambda: generate_python(candidates, K), number=10)
    print(f"Скорость (10 повторов): алгоритмический = {t_alg:.4f}s, python = {t_py:.4f}s\n")

    juries_py = generate_python(candidates, K)
    print("Первые 5 вариантов (python/itertools):")
    for j in juries_py[:5]:
        print("  ", j)
    print(f"\nВсего вариантов: {len(juries_py)}")

    best, max_avg, limit, total_valid = filter_and_optimize(juries_py, min_count=10, max_count=30)
    print(f"\nЛимит по сумме возрастов: {limit}")
    print(f"Всего подходящих жюри: {total_valid}")
    print(f"Лучший(ие) вариант(ы) (ср. возраст = {max_avg:.2f}):")
    for idx, jury in enumerate(best, 1):
        print(f"{idx}. {jury}")
    print(f"\nВсего оптимальных вариантов: {len(best)}")

if __name__ == "__main__":
    main()
