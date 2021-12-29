import tkinter as tk
from tkinter import ttk
from googletrans import Translator
class Translate:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('翻译器')
        self.menu = ttk.Combobox(self.window, width=11)
        self.input = tk.Entry(self.window, width=80)
        self.info = tk.Text(self.window, height=20)

        self.menu['value'] = ('转成简体中文', '转成英文', '转成越南文')
        self.menu.current(0)

        self.translate_button = tk.Button(self.window, text='翻译', relief=tk.RAISED, width=8,
                                          height=1, command=self)
        self.clear_button = tk.Button(self.window, text='清空输入', relief=tk.RAISED, width=8,
                                      height=1, command=self)
        self.clear2_button = tk.Button(self.window, text='清空输出', relief=tk.RAISED, width=8,
                                       height=1, command=self)
        self.img_file = tk.PhotoImage(file='python_logo.png')
        self.label_image = tk.Label(self.window, image=self.img_file)

    def gui_arrange(self):
        self.input.grid(row=0, column=0, padx=5, pady=5)
        self.info.grid(row=1, rowspan=2, column=0, padx=5, pady=5)
        self.menu.grid(row=1, column=1, padx=5, pady=5, rowspan=2, columnspan=2, sticky=tk.NW)

        self.translate_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.clear_button.grid(row=0, column=2, padx=0, pady=5, sticky=tk.W)
        self.clear2_button.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        self.label_image.grid(row=1, column=1, columnspan=3, padx=50, pady=80, sticky=tk.W)


if __name__ == '__main__':
    t = Translate()
    t.gui_arrange()
    translator = Translator()
    str = translator.detect('Ẩm thực, làm đẹp, deal sốc, hoàn tiền')
    print(str)
    tk.mainloop()
