import os
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from Conversions.Excel2md import ExcelToMarkdownConverter
from Conversions.mht2md import MHTToMarkdownConverter
from Conversions.pdf2md import PdfToMarkdownConverter


# GUI Application
class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Converter")
        self.root.geometry("500x300")

        self.selected_file = None
        self.converter = None

        self.create_widgets()

    def create_widgets(self):
        # File selection
        self.file_label = ttk.Label(self.root, text="请选择一个文件", font=("Helvetica", 12))
        self.file_label.pack(pady=10)

        self.file_button = ttk.Button(self.root, text="选择文件", command=self.select_file)
        self.file_button.pack(pady=10)

        # Conversion options
        self.conversion_type = ttk.StringVar()
        self.option_menu = ttk.Combobox(
            self.root,
            textvariable=self.conversion_type,
            values=["MHT to Markdown", "Excel to Markdown","PDF to Markdown"],
            state="readonly",
        )
        self.option_menu.set("选择转换类型")
        self.option_menu.pack(pady=10)

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.root, style="info.Horizontal.TProgressbar", length=400, mode="determinate"
        )
        self.progress_bar.pack(pady=20)

        # Convert button
        self.convert_button = ttk.Button(
            self.root, text="开始转换", command=self.start_conversion
        )
        self.convert_button.pack(pady=10)

    def select_file(self):
        self.selected_file = filedialog.askopenfilename(
            filetypes=[("All Supported Files", "*.mht;*.xlsx;*.pdf"),
                       ("MHT files", "*.mht"),
                       ("Excel files", "*.xlsx"),
                       ("PDF files", "*.pdf")
                       ]
        )
        if self.selected_file:
            self.file_label["text"] = f"已选择文件: {os.path.basename(self.selected_file)}"

    def start_conversion(self):
        if not self.selected_file:
            messagebox.showerror("错误", "请先选择一个文件！")
            return

        output_dir = os.path.dirname(self.selected_file)
        conversion_type = self.conversion_type.get()

        if conversion_type == "MHT to Markdown":
            self.converter = MHTToMarkdownConverter(self.selected_file, output_dir)
        elif conversion_type == "Excel to Markdown":
            self.converter = ExcelToMarkdownConverter(self.selected_file, output_dir)
        elif conversion_type == "PDF to Markdown":
            self.converter = PdfToMarkdownConverter(self.selected_file, output_dir)
        else:
            messagebox.showerror("错误", "请选择转换类型！")
            return

        self.progress_bar["value"] = 0
        self.root.update_idletasks()

        try:
            result = self.converter.convert(self.update_progress)
            messagebox.showinfo("完成", result)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def update_progress(self, value):
        self.progress_bar["value"] = value
        self.root.update_idletasks()

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = ConverterApp(root)
    root.mainloop()
