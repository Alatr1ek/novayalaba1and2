import timeit
from itertools import combinations

candidates = [f'P{i + 1}' for i in range(10)]
K = 4
candidate_stats = {
    'P1': {'skill': 9, 'cost': 10},
    'P2': {'skill': 8, 'cost': 9},
    'P3': {'skill': 7, 'cost': 8},
    'P4': {'skill': 6, 'cost': 7},
    'P5': {'skill': 5, 'cost': 6},
    'P6': {'skill': 4, 'cost': 5},
    'P7': {'skill': 3, 'cost': 4},
    'P8': {'skill': 2, 'cost': 3},
    'P9': {'skill': 1, 'cost': 2},
    'P10': {'skill': 10, 'cost': 11}
}
maxstoimost = 30
BEST_TEAM_ALGO = ([], 0)


def find_optimal_team_algo(cands, k, stats, budget):
    global BEST_TEAM_ALGO
    BEST_TEAM_ALGO = ([], 0)
    n = len(cands)

    def rec(curr_team, idx, current_cost, current_skill):
        global BEST_TEAM_ALGO
        if len(curr_team) == k:
            if current_skill > BEST_TEAM_ALGO[1]:
                BEST_TEAM_ALGO = (tuple(curr_team), current_skill)
            return
        for i in range(idx, n):
            cand_name = cands[i]
            cand_skill = stats[cand_name]['skill']
            cand_cost = stats[cand_name]['cost']
            next_cost = current_cost + cand_cost
            if next_cost <= budget:
                rec(curr_team + [cand_name],
                    i + 1,
                    next_cost,
                    current_skill + cand_skill)
    rec([], 0, 0, 0)
    return BEST_TEAM_ALGO


def find_optimal_team_python(cands, k, stats, budget):
    best_skill = -1
    best_team = tuple()
    all_teams = combinations(cands, k)
    for team in all_teams:
        total_cost = sum(stats[c]['cost'] for c in team)
        total_skill = sum(stats[c]['skill'] for c in team)

        if total_cost <= budget:
            if total_skill > best_skill:
                best_skill = total_skill
                best_team = team

    return (best_team, best_skill)


def main():
    optimal_algo = find_optimal_team_algo(candidates, K, candidate_stats, maxstoimost)
    optimal_py = find_optimal_team_python(candidates, K, candidate_stats, maxstoimost)
    print(f"Кандидаты: {candidates}, K=4")
    print(f"Ограничение (максимальный бюджет): 30")
    print(f"Целевая Функция: Максимизация суммарного навыка (Total Skill)")
    print("-" * 30)
    print(
        f"Оптимальная команда (Алгоритм): {optimal_algo[0]} (Skill: {optimal_algo[1]}, Cost: {sum(candidate_stats[p]['cost'] for p in optimal_algo[0])})")
    print(
        f"Оптимальная команда (Python):  {optimal_py[0]} (Skill: {optimal_py[1]}, Cost: {sum(candidate_stats[p]['cost'] for p in optimal_py[0])})")


    t_alg = timeit.timeit(lambda: find_optimal_team_algo(candidates, K, candidate_stats, maxstoimost), number=100)
    t_py = timeit.timeit(lambda: find_optimal_team_python(candidates, K, candidate_stats, maxstoimost), number=100)
    print("-" * 30)
    print(f"Скорость (100 повторов):")
    print(f"Алгоритмический (с отсечением) = {t_alg:.4f}s")
    print(f"Python (полный перебор + фильтр) = {t_py:.4f}s")


if __name__ == "__main__":
    main()
