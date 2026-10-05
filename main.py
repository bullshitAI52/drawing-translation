import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path  # 导入 Path
import tkinter.messagebox as messagebox
import threading
import f  # 确保 f.py 在同一目录下
import t  # 确保 t.py 在同一目录下
import registration  # 引入新的注册模块

class DXFApp:
    def __init__(self, root):
        self.root = root
        root.title("DXF处理工具")
        self.root.geometry("600x400")  # 设置窗口初始大小

        self.tab_control = ttk.Notebook(root)

        # 翻译功能的选项卡
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="翻译功能")
        self.create_translate_tab(self.tab1)

        # 提取文本功能的选项卡
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text="提取文本功能")
        self.create_extract_tab(self.tab2)

        # 翻译参数设定的选项卡
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab3, text="翻译参数设定")
        self.create_settings_tab(self.tab3)

        # 注册功能的选项卡
        self.tab4 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab4, text="注册")
        self.create_registration_tab(self.tab4)

        self.tab_control.pack(expand=1, fill="both")

        # 检查是否已注册
        if not registration.is_registered():
            self.disable_tabs()
        else:
            self.enable_tabs()

    def disable_tabs(self):
        # 禁用除注册选项卡之外的所有选项卡
        for index in range(1, self.tab_control.index("end")):
            self.tab_control.tab(index, state="disabled")

    def enable_tabs(self):
        # 启用所有选项卡
        for index in range(1, self.tab_control.index("end")):
            self.tab_control.tab(index, state="normal")


    def create_registration_tab(self, tab):
        frame = ttk.Frame(tab, padding="10")
        frame.pack(fill='x', expand=True)

        self.machine_code_label = ttk.Label(frame, text="机器码:")
        self.machine_code_label.grid(column=0, row=0, sticky='w')
        self.machine_code_entry = ttk.Entry(frame, width=40, state='readonly')
        self.machine_code_entry.grid(column=1, row=0, sticky='ew')
        self.machine_code_entry.insert(0, registration.get_machine_code())

        self.registration_code_label = ttk.Label(frame, text="注册码:")
        self.registration_code_label.grid(column=0, row=1, sticky='w')
        self.registration_code_entry = ttk.Entry(frame, width=40)
        self.registration_code_entry.grid(column=1, row=1, sticky='ew')

        self.register_button = ttk.Button(frame, text="注册", command=self.register)
        self.register_button.grid(column=1, row=2)
                # 此处设置机器码
        self.machine_code_entry.config(state='normal')  # 允许写入
        self.machine_code_entry.delete(0, tk.END)  # 清空输入框
        self.machine_code_entry.insert(0, registration.get_machine_code())  # 插入机器码
        self.machine_code_entry.config(state='readonly')  # 设置为只读

    def register(self):
        registration_code = self.registration_code_entry.get()
        if registration.register(registration_code):
            messagebox.showinfo("注册", "注册成功！")
            self.enable_tabs()
        else:
            messagebox.showerror("注册", "注册码无效。")
 # 新增翻译参数设定的方法
    def create_settings_tab(self, tab):
       
        frame = ttk.Frame(tab, padding="10")
        frame.pack(fill='x', expand=True)

        # 字体大小设置
        self.text_height_label = ttk.Label(frame, text="译文字体大小:")
        self.text_height_label.grid(column=0, row=0, sticky='w')
        self.text_height_entry = ttk.Entry(frame, width=10)
        self.text_height_entry.grid(column=1, row=0, sticky='w')
        self.text_height_entry.insert(0, "1")  # 默认值

        # 字体颜色设置（下拉框）
        self.text_color_label = ttk.Label(frame, text="译文字体颜色:")
        self.text_color_label.grid(column=0, row=1, sticky='w')
        self.text_color_combobox = ttk.Combobox(frame, width=8, state="readonly")
        self.text_color_combobox['values'] = ("使用原文颜色", "黑色", "红色", "黄色", "绿色", "蓝色", "品红", "青色", "白色")
        self.text_color_combobox.grid(column=1, row=1, sticky='w')
        self.text_color_combobox.current(0)  # 默认选择

        # 是否使用原文大小
        self.use_original_size_check = ttk.Checkbutton(frame, text="使用原文字体大小")
        self.use_original_size_check.grid(column=0, row=2, sticky='w')

        # 是否替换原文
        self.replace_original_label = ttk.Label(frame, text="译文是否替换原文:")
        self.replace_original_label.grid(column=0, row=4, sticky='w')
        self.replace_original_check = ttk.Checkbutton(frame)
        self.replace_original_check.grid(column=1, row=4, sticky='w')

        # X 偏移量设置
        self.x_offset_label = ttk.Label(frame, text="X 偏移量:")
        self.x_offset_label.grid(column=0, row=5, sticky='w')
        self.x_offset_entry = ttk.Entry(frame, width=10)
        self.x_offset_entry.grid(column=1, row=5, sticky='w')
        self.x_offset_entry.insert(0, "0")  # 默认值

        # Y 偏移量设置
        self.y_offset_label = ttk.Label(frame, text="Y 偏移量:")
        self.y_offset_label.grid(column=0, row=6, sticky='w')
        self.y_offset_entry = ttk.Entry(frame, width=10)
        self.y_offset_entry.grid(column=1, row=6, sticky='w')
        self.y_offset_entry.insert(0, "-0.75")  # 默认值

    def create_translate_tab(self, tab):
        frame = ttk.Frame(tab, padding="10")
        frame.pack(fill='x', expand=True)

        self.directory_label = ttk.Label(frame, text="操作文件夹:")
        self.directory_label.grid(column=0, row=0, sticky='w')
        self.directory_entry = ttk.Entry(frame, width=40)
        self.directory_entry.grid(column=1, row=0, sticky='ew')
        self.directory_button = ttk.Button(frame, text="浏览", command=self.browse_directory)
        self.directory_button.grid(column=2, row=0)

        self.translation_excel_label = ttk.Label(frame, text="翻译映射Excel:")
        self.translation_excel_label.grid(column=0, row=1, sticky='w')
        self.translation_excel_entry = ttk.Entry(frame, width=40)
        self.translation_excel_entry.grid(column=1, row=1, sticky='ew')
        self.translation_excel_button = ttk.Button(frame, text="浏览", command=self.browse_translation_excel)
        self.translation_excel_button.grid(column=2, row=1)

        self.output_directory_label = ttk.Label(frame, text="输出文件夹:")
        self.output_directory_label.grid(column=0, row=2, sticky='w')
        self.output_directory_entry = ttk.Entry(frame, width=40)
        self.output_directory_entry.grid(column=1, row=2, sticky='ew')
        self.output_directory_button = ttk.Button(frame, text="浏览", command=self.browse_output_directory)
        self.output_directory_button.grid(column=2, row=2)

        self.translate_button = ttk.Button(frame, text="开始翻译", command=self.start_translate_thread)
        self.translate_button.grid(column=0, row=3, columnspan=3)

        self.file_status_tree = ttk.Treeview(tab, columns=('file', 'status'), show='headings')
        self.file_status_tree.heading('file', text='文件')
        self.file_status_tree.heading('status', text='状态')
        self.file_status_tree.pack(fill='both', expand=True)

    def create_extract_tab(self, tab):
        frame = ttk.Frame(tab, padding="10")
        frame.pack(fill='x', expand=True)

        # 操作文件夹
        self.extract_directory_label = ttk.Label(frame, text="操作文件夹:")
        self.extract_directory_label.grid(column=0, row=0, sticky='w')
        self.extract_directory_entry = ttk.Entry(frame, width=40)
        self.extract_directory_entry.grid(column=1, row=0, sticky='ew')
        self.extract_directory_button = ttk.Button(frame, text="浏览", command=self.browse_extract_directory)
        self.extract_directory_button.grid(column=2, row=0)

        # 输出Excel文件夹
        self.output_excel_directory_label = ttk.Label(frame, text="输出Excel文件夹:")
        self.output_excel_directory_label.grid(column=0, row=1, sticky='w')
        self.output_excel_directory_entry = ttk.Entry(frame, width=40)
        self.output_excel_directory_entry.grid(column=1, row=1, sticky='ew')
        self.output_excel_directory_button = ttk.Button(frame, text="浏览", command=self.browse_output_excel_directory)
        self.output_excel_directory_button.grid(column=2, row=1)

        # 开始提取按钮
        self.extract_button = ttk.Button(frame, text="开始提取", command=self.start_extract_thread)
        self.extract_button.grid(column=0, row=2, columnspan=3)

        # 提取进度表格
        self.extract_status_tree = ttk.Treeview(tab, columns=('file', 'status'), show='headings')
        self.extract_status_tree.heading('file', text='文件')
        self.extract_status_tree.heading('status', text='状态')
        self.extract_status_tree.pack(fill='both', expand=True)

    def browse_output_excel_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_excel_directory_entry.delete(0, tk.END)
            self.output_excel_directory_entry.insert(0, directory)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, directory)

    def browse_translation_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        self.translation_excel_entry.delete(0, tk.END)
        self.translation_excel_entry.insert(0, file_path)

    def browse_output_directory(self):
        directory = filedialog.askdirectory()
        self.output_directory_entry.delete(0, tk.END)
        self.output_directory_entry.insert(0, directory)

    def browse_extract_directory(self):
        directory = filedialog.askdirectory()
        self.extract_directory_entry.delete(0, tk.END)
        self.extract_directory_entry.insert(0, directory)

    def start_translate_thread(self):
        if not registration.is_registered():
            messagebox.showwarning("警告", "用户未注册，无法使用！")
            return
        directory = self.directory_entry.get()
        output_directory = self.output_directory_entry.get()
        translation_excel = self.translation_excel_entry.get()
        if directory and output_directory and translation_excel:
            threading.Thread(target=self.translate_texts, args=(directory, translation_excel, output_directory)).start()
        else:
            messagebox.showwarning("警告", "请确保所有路径都已正确设置")

    def update_file_status(self, file_path, status):
        print(f"Updating file status: {file_path} - {status}")
        self.root.after(0, lambda: self.file_status_tree.insert('', 'end', values=(file_path, status)))

    def translate_texts(self, directory, translation_excel, output_directory):
        # 获取界面中设置的参数
        text_color = self.text_color_combobox.get()
        x_offset = self.x_offset_entry.get()
        y_offset = self.y_offset_entry.get()

        # 将参数转换为正确的类型，例如，将字符串转换为数字
        try:
            x_offset = float(x_offset)
            y_offset = float(y_offset)
            text_height = float(self.text_height_entry.get())  # 从界面获取文本高度并转换为浮点数
        except ValueError:
            messagebox.showerror("错误", "偏移量和文本高度必须是数字")
            return

        # 将文本颜色参数映射到整数值
        color_map = {
            "使用原文颜色": 256,  # 默认使用原文颜色
            "黑色": 1,
            "红色": 2,
            "黄色": 3,
            "绿色": 4,
            "蓝色": 5,
            "品红": 6,
            "青色": 7,
            "白色": 8
        }
        text_color_value = color_map.get(text_color, 256)  # 默认使用原文颜色

        translation_map = t.load_translation_map(translation_excel)
        # 确保将新参数传递给 process_directory 函数
        total, translated, failed = t.process_directory(directory, translation_map, Path(output_directory), self.update_file_status, text_color_value, x_offset, y_offset, text_height)
        messagebox.showinfo("完成", f"翻译完成。总计：{total}, 成功：{translated}, 失败：{failed}")

    def start_extract_thread(self):
        if not registration.is_registered():
            messagebox.showwarning("警告", "用户未注册，无法使用！")
            return
        directory = self.extract_directory_entry.get()
        output_directory = self.output_excel_directory_entry.get()  # 使用正确的属性
        output_excel = Path(output_directory, "extracted_texts.xlsx")  # 默认文件名
        if directory and output_directory:
            threading.Thread(target=self.extract_texts, args=(directory, str(output_excel))).start()
        else:
            messagebox.showwarning("警告", "请确保所有路径都已正确设置")

    def extract_texts(self, directory, output_excel):
        try:
            f.main(directory, output_excel, self.update_extraction_progress)
            messagebox.showinfo("完成", "文本提取完成")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def update_extraction_progress(self, processed, total):
        # 更新进度表格
        self.extract_status_tree.insert('', 'end', values=(f"Processed {processed} of {total}", "进行中"))
if __name__ == "__main__":
    root = tk.Tk()
    app = DXFApp(root)
    root.mainloop()
