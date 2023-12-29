import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()

        # Configure the grid
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.file1_label = tk.Label(self, text="マップデータ")
        self.file1_label.grid(row=0, column=0, sticky=tk.E + tk.W)

        self.file1_entry = tk.Entry(self)
        self.file1_entry.grid(row=1, column=0, sticky=tk.E + tk.W)

        self.file1_button = tk.Button(self)
        self.file1_button["text"] = "マップデータを選択"
        self.file1_button["command"] = self.select_file1
        self.file1_button.grid(row=2, column=0, sticky=tk.E + tk.W)

        self.file2_label = tk.Label(self, text="購入物リスト")
        self.file2_label.grid(row=0, column=1, sticky=tk.E + tk.W)

        self.file2_entry = tk.Entry(self)
        self.file2_entry.grid(row=1, column=1, sticky=tk.E + tk.W, padx=20)

        self.file2_button = tk.Button(self)
        self.file2_button["text"] = "購入物リストを選択"
        self.file2_button["command"] = self.select_file2
        self.file2_button.grid(row=2, column=1, sticky=tk.E + tk.W, padx=20)

        self.option1 = tk.IntVar()
        self.option1_check = tk.Checkbutton(
            self, text="1日目", variable=self.option1)
        self.option1_check.grid(row=3, column=0, sticky=tk.E + tk.W)

        self.option2 = tk.IntVar()
        self.option2_check = tk.Checkbutton(
            self, text="2日目", variable=self.option2)
        self.option2_check.grid(row=3, column=1, sticky=tk.E + tk.W)

        self.output_label = tk.Label(self, text="出力ファイル名")
        self.output_label.grid(
            row=4, column=0, columnspan=2, sticky=tk.E + tk.W)

        self.output_entry = tk.Entry(self)
        self.output_entry.grid(
            row=5, column=0, columnspan=2, sticky=tk.E + tk.W)

        self.run_button = tk.Button(self)
        self.run_button["text"] = "作成"
        self.run_button["command"] = self.run
        self.run_button.config(font=("Helvetica", 24))
        self.run_button.grid(row=6, column=0, columnspan=2, sticky=tk.E + tk.W)

    def select_file1(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Excel file", "*.xlsx;*.xls;*.xlsm")])
        self.file1_entry.delete(0, tk.END)
        self.file1_entry.insert(0, filename)

    def select_file2(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Json file", "*.json")])
        self.file2_entry.delete(0, tk.END)
        self.file2_entry.insert(0, filename)

    def run(self):
        file1 = self.file1_entry.get()
        file2 = self.file2_entry.get()
        output = self.output_entry.get()

        if not file1 or not file2 or not output:
            messagebox.showerror(
                "Error", "Please select both files and specify an output file name.")
            return

        # ここでファイルを処理します
        # ...

        messagebox.showinfo("Success", "Operation completed successfully.")


root = tk.Tk()
root.geometry("400x220")
app = Application(master=root)
app.mainloop()
