import re


def to_words(n):
    words = "ноль один два три четыре пять шесть семь восемь девять".split()
    return " ".join(words[int(c)] for c in str(n))

with open("1lab.txt") as f:
    content = f.read()
    m = re.findall(r'\b([0-1]{0,2}1[0-7]|[0-7]{0,1}1[0-7])\b', content)
    nums = list(map(lambda x: int(x, 8), m))
    print("\n".join(map(lambda a: a[:-2], m)))
    if nums:
        print(to_words((min(nums) + max(nums)) // 2))
