import tkinter as tk
from tkinter import scrolledtext
from itertools import combinations

def generate_juries():
    output.delete(1.0, tk.END)
    try:
        N = int(entry_n.get())
        K = int(entry_k.get())
        age_limit = int(entry_limit.get())
        candidates = [f"P{i+1}" for i in range(N)]
        age = {name: 20 + i for i, name in enumerate(candidates)}
        juries = list(combinations(candidates, K))
        valid = [jury for jury in juries if sum(age[name] for name in jury) <= age_limit]
        if not valid:
            output.insert(tk.END, "Нет подходящих жюри для таких условий.\n")
            return
        max_avg = max(sum(age[name] for name in jury)/K for jury in valid)
        best = [jury for jury in valid if sum(age[name] for name in jury)/K == max_avg]
        output.insert(tk.END, f"Всего подходящих жюри: {len(valid)}\n")
        output.insert(tk.END, f"Оптимальные (макс. средний возраст = {max_avg:.2f}):\n")
        for i, jury in enumerate(best, 1):
            ages = [age[name] for name in jury]
            output.insert(tk.END, f"{i}. {jury} (возрасты: {ages})\n")
    except Exception as e:
        output.insert(tk.END, f"Ошибка: {e}\n")

root = tk.Tk()
root.title("Генератор вариантов жюри")

frame_input = tk.Frame(root)
frame_input.pack(pady=5)

tk.Label(frame_input, text="Число претендентов (N):").grid(row=0, column=0)
entry_n = tk.Entry(frame_input, width=5)
entry_n.insert(0, "10")
entry_n.grid(row=0, column=1)

tk.Label(frame_input, text="Размер жюри (K):").grid(row=0, column=2)
entry_k = tk.Entry(frame_input, width=5)
entry_k.insert(0, "4")
entry_k.grid(row=0, column=3)

tk.Label(frame_input, text="Лимит по сумме возрастов:").grid(row=0, column=4)
entry_limit = tk.Entry(frame_input, width=8)
entry_limit.insert(0, "100")
entry_limit.grid(row=0, column=5)

btn = tk.Button(root, text="Сгенерировать", command=generate_juries)
btn.pack(pady=5)

output = scrolledtext.ScrolledText(root, width=80, height=20, font=("Courier", 10))
output.pack(padx=10, pady=10)

root.mainloop()
