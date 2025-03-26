def to_words(n):
    d = "ноль один два три четыре пять шесть семь восемь девять".split()
    return " ".join(d[int(c)] for c in str(n))

min_n = float('inf')
max_n = float('-inf')

with open("1lab.txt", "r") as file:
    for line in file:
        for token in line.split():
            if all(c in "01234567" for c in token):
                n = int(token, 8)
                if n <= 1023 and len(token) > 1 and token[-2] == '1':
                    print(token[:-2])
                    min_n, max_n = min(min_n, n), max(max_n, n)

if min_n != float('inf'):
    print(to_words((min_n + max_n) // 2))
