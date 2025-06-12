import tkinter as tk

def compare_sources():
    source1 = text1.get("1.0", tk.END).splitlines()
    source2 = text2.get("1.0", tk.END).splitlines()

    output.delete("1.0", tk.END)
    status_label.config(text="")  # Xóa thông báo cũ

    output.insert(tk.END, f"{'Line':<6} | {'Source 1':<40} | {'Source 2'}\n")
    output.insert(tk.END, "-" * 90 + "\n")

    max_lines = max(len(source1), len(source2))
    difference_count = 0

    for i in range(max_lines):
        line1 = source1[i] if i < len(source1) else ''
        line2 = source2[i] if i < len(source2) else ''
        tag = ""
        if line1 != line2:
            tag = "diff"
            difference_count += 1
        output.insert(tk.END, f"{i+1:<6} | {line1:<40} | {line2}\n", tag)

    # Hiển thị thông báo tùy theo kết quả
    if difference_count == 0:
        status_label.config(text="✅ Hai đoạn mã giống nhau hoàn toàn!", fg="green")
    else:
        status_label.config(text=f"❌ Có {difference_count} dòng khác nhau.", fg="red")

# Giao diện chính
root = tk.Tk()
root.title("So sánh Source Code - Dán vào ô nhập")

tk.Label(root, text="Source Code 1").grid(row=0, column=0)
tk.Label(root, text="Source Code 2").grid(row=0, column=1)

text1 = tk.Text(root, width=60, height=20, font=("Courier New", 10))
text1.grid(row=1, column=0, padx=5, pady=5)

text2 = tk.Text(root, width=60, height=20, font=("Courier New", 10))
text2.grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="So sánh", command=compare_sources).grid(row=2, column=0, columnspan=2, pady=(10, 0))

# 🔔 Nhãn hiển thị trạng thái so sánh (thêm vào đây)
status_label = tk.Label(root, text="", font=("Arial", 10, "bold"))
status_label.grid(row=3, column=0, columnspan=2, pady=(5, 10))

output = tk.Text(root, height=20, width=130, font=("Courier New", 10))
output.tag_config("diff", background="misty rose")
output.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
