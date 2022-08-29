import tkinter as tk
from multiprocessing import Process, Queue
from tkinter import END


class Parser:
    def __init__(self, gui):
        self.gui = gui
        self.gui.title('List of integers')

        self.integer_list = []
        self.queue = Queue()

        self.integer_list_lbl = tk.Label(master=self.gui, text='List of integers:')

        self.add_list_btn = tk.Button(master=self.gui, text='Add list', command=self.add_list)

        self.integer_list_text = tk.Text(self.gui, width=60, height=1)
        self.integer_list_text.insert(tk.END, str(list(range(1, 16)))[1:-1])

        self.result_text = tk.Text(self.gui, width=60, height=10)

        self.filter_odd_btn = tk.Button(master=self.gui, text='Filter odd', command=lambda: self.filter('odd'))
        self.filter_prime_btn = tk.Button(master=self.gui, text='Filter primes', command=lambda: self.filter('prime'))
        self.sum_btn = tk.Button(master=self.gui, text='Sum numbers', command=self.sum)

        self.integer_list_lbl.grid(row=0, column=0, padx=5, pady=10)
        self.integer_list_text.grid(row=0, column=1)
        self.add_list_btn.grid(row=0, column=2)
        self.result_text.grid(row=2, column=1)
        self.filter_odd_btn.grid(row=2, column=2)
        self.filter_prime_btn.grid(row=5, column=2)
        self.sum_btn.grid(row=6, column=2, padx=5, pady=5)
        self.gui.mainloop()

    def add_list(self):
        result = self.integer_list_text.get('1.0', tk.END)
        result = result.strip().replace(' ', '')
        result = [int(item) for item in result.split(',')]
        self.integer_list = result

    def filter(self, text):
        if len(self.integer_list) != 0:
            p = Process(target=filter_fun, args=(self.queue, self.integer_list, text))
            p.start()
            p.join()
            # filter_fun(self.queue, self.integer_list, text)
            self.print_txt()
            self.result_text.insert(END, self.queue.get())
        else:
            print('Nu exista elem in lista')

    def sum(self):
        if len(self.integer_list) != 0:
            result = sum(self.integer_list)
            self.print_txt()
            self.result_text.insert(END, result)
        else:
            print('Nu exista elem in lista')

    def print_txt(self):
        self.result_text.delete('1.0', END)
        self.result_text.insert(END, 'The list is: ')
        self.result_text.insert(END, self.integer_list)
        self.result_text.insert(END, '\nResult: ')


def filter_fun(queue, _list, text):
        result = [element for element in _list if (element % 2 != 0)]
        queue.put(result)
    if text == 'prime':
        result = [element for element in _list if (is_prime(element) and element != 1)]
        queue.put(result)


def is_prime(nr):
    for i in range(2, nr):
        if nr % i == 0:
            return False
    return True


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Root title')
    root.resizable(False, False)
    app = Parser(root)
    root.mainloop()
