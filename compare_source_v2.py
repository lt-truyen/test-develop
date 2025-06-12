import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime

# === Khởi tạo file lịch sử nếu chưa có ===
history_file = "history.json"
if not os.path.exists(history_file):
    with open(history_file, "w") as f:
        json.dump([], f)

# === Các hàm xử lý lịch sử ===
def load_history():
    with open(history_file, "r") as f:
        return json.load(f)

def save_history(entry):
    history = load_history()
    history.append(entry)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)

def update_dropdown():
    dropdown["values"] = [h["timestamp"] for h in load_history()]

def load_selected_history(event):
    index = dropdown.current()
    if index >= 0:
        selected = load_history()[index]
        text1.delete("1.0", tk.END)
        text1.insert("1.0", selected["source1"])
        text2.delete("1.0", tk.END)
        text2.insert("1.0", selected["source2"])

# === Hàm so sánh source ===
def compare_sources():
    source1 = text1.get("1.0", tk.END).splitlines()
    source2 = text2.get("1.0", tk.END).splitlines()

    output.delete("1.0", tk.END)
    status_label.config(text="")

    output.insert(tk.END, f"{'Line':<6} | {'Source 1':<40} | {'Source 2'}\n")
    output.insert(tk.END, "-" * 120 + "\n")

    max_lines = max(len(source1), len(source2))
    difference_count = 0

    for i in range(max_lines):
        line1 = source1[i] if i < len(source1) else ''
        line2 = source2[i] if i < len(source2) else ''

        line_start = output.index(tk.INSERT)
        output_line = f"{i+1:<6} | "
        output.insert(tk.END, output_line)

        max_len = max(len(line1), len(line2))
        for j in range(max_len):
            c1 = line1[j] if j < len(line1) else ''
            c2 = line2[j] if j < len(line2) else ''

            if c1 != c2:
                output.insert(tk.END, c1, "diff")
                difference_count += 1
            else:
                output.insert(tk.END, c1)

        output.insert(tk.END, " " * max(0, 40 - len(line1)))
        output.insert(tk.END, " | ")

        for j in range(max_len):
            c1 = line1[j] if j < len(line1) else ''
            c2 = line2[j] if j < len(line2) else ''

            if c1 != c2:
                output.insert(tk.END, c2, "diff")
            else:
                output.insert(tk.END, c2)

        output.insert(tk.END, "\n")

        if line1 != line2:
            line_end = output.index(tk.INSERT)
            output.tag_add("line_diff", line_start, line_end)

    if difference_count == 0:
        status_label.config(text="✅ Hai đoạn mã giống nhau hoàn toàn!", fg="green")
    else:
        status_label.config(text=f"❌ Có {difference_count} ký tự khác nhau.", fg="red")

    # Lưu vào lịch sử
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source1": "\n".join(source1),
        "source2": "\n".join(source2)
    }
    save_history(entry)
    update_dropdown()

# === Làm mới input/output ===
def clear_all():
    text1.delete("1.0", tk.END)
    text2.delete("1.0", tk.END)
    output.delete("1.0", tk.END)
    status_label.config(text="")

# === Giao diện chính ===
root = tk.Tk()
root.title("So sánh Source Code - Đánh dấu ký tự & dòng khác")
root.geometry("1200x700")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(4, weight=2)

# Ô nhập liệu
tk.Label(root, text="Source Code 1").grid(row=0, column=0, sticky="w", padx=5)
tk.Label(root, text="Source Code 2").grid(row=0, column=1, sticky="w", padx=5)

text1 = tk.Text(root, font=("Courier New", 10), wrap="none")
text1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

text2 = tk.Text(root, font=("Courier New", 10), wrap="none")
text2.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

# Nút thao tác
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=2)
tk.Button(button_frame, text="So sánh", command=compare_sources).pack(side="left", padx=10, pady=10)
tk.Button(button_frame, text="Làm mới", command=clear_all).pack(side="left", padx=10, pady=10)

# Hiển thị kết quả
status_label = tk.Label(root, text="", font=("Arial", 10, "bold"))
status_label.grid(row=3, column=0, columnspan=2)

# Dropdown lịch sử
history_frame = tk.Frame(root)
history_frame.grid(row=3, column=0, columnspan=2, sticky="e")
tk.Label(history_frame, text="🔽 Lịch sử so sánh:").pack(side="left", padx=5)
dropdown = ttk.Combobox(history_frame, state="readonly", width=30)
dropdown.pack(side="left")
dropdown.bind("<<ComboboxSelected>>", load_selected_history)
update_dropdown()

# Ô kết quả
output = tk.Text(root, font=("Courier New", 10), wrap="none")
output.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
#Format chữ khác nhau
output.tag_config("diff", background="red", foreground="red")
#Format line khác nhau
output.tag_config("line_diff", background="misty rose")

# Scroll
scroll = tk.Scrollbar(root, command=output.yview)
output.config(yscrollcommand=scroll.set)
scroll.grid(row=4, column=2, sticky="ns")

root.mainloop()
