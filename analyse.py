from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np


class analyseWindow():
    counter = 0

    def display_pie_chart(self, wedge_sizes, labels):
        figure = Figure(figsize=(5, 5), dpi=100)
        plot1 = figure.add_subplot(111)
        plot1.pie(wedge_sizes, autopct='%.2f')
        plot1.legend(loc=1, labels=labels)
        # creating a tkinter canvas containing the matplotlib figure
        canvas = FigureCanvasTkAgg(figure, master=self.graph_frame)
        canvas.draw()
        # placing the window in tkinter window
        canvas.get_tk_widget().pack()
        # creating a matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.graph_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def validate(self, value):
        try:
            value = float(value)
            if value > 10 or value < 0:
                raise ValueError('Enter a value between 1 to 10')
        except ValueError:
            print('Invalid input error value')
            self.filter_cgpa_entry.delete(0, END)
            self.filter_cgpa_entry.insert(0, '0')
            return 0

        return value

    def enter_records_from_df(self, df):
        for i in range(len(df)):
            self.records_treeView.insert(parent='', index='end', iid=self.counter,
                                         values=(' '.join(df.loc[i, 'Roll No \nName'].split(" ")[1:]), df.loc[i, 'DIV'], df.loc[i, 'GR. CGPA']))
            self.counter += 1

    def delete_all_records(self):
        records = self.records_treeView.get_children()
        for record in records:
            self.records_treeView.delete(record)

    def delete_children(self, frame):
        for child in frame.winfo_children():
            child.pack_forget()

    def sort_records(self, treeView, col, reverse):
        positions_and_elements = [(treeView.set(i, col), i)
                                  for i in treeView.get_children()]
        positions_and_elements.sort(reverse=reverse)

        for idx, (values, element) in enumerate(positions_and_elements):
            treeView.move(element, "", idx)

    def display_cgpa_graph(self):
        self.records_frame.pack_forget()
        self.delete_children(self.graph_frame)
        self.graph_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        labels = ['below 4', 'above 4 and below 7', 'above 7 and below 9',
                  'above 9 or equal to 10 ', 'result not declared']
        below7 = len(self.df[(pd.to_numeric(self.df['GR. CGPA']) > 4) & (
            pd.to_numeric(self.df['GR. CGPA']) < 7)])
        above7 = len(self.df[(pd.to_numeric(self.df['GR. CGPA']) > 7) & (
            pd.to_numeric(self.df['GR. CGPA']) < 9)])
        above9orequalto10 = len(
            self.df[pd.to_numeric(self.df['GR. CGPA']) > 9])
        below4 = len(self.df[pd.to_numeric(self.df['GR. CGPA']) < 4])
        result_not_declared = len(self.df[self.df['DIV'] == ''])
        wedge_sizes = [below4, below7, above7,
                       above9orequalto10, result_not_declared]
        self.display_pie_chart(wedge_sizes, labels)

    def back_to_records(self):
        self.graph_frame.pack_forget()
        self.records_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    def display_div_graph(self):
        self.records_frame.pack_forget()
        self.delete_children(self.graph_frame)
        self.img_back_button = Image.open(
            'res\\buttons\\back_button.png')
        self.img_back_button = self.img_back_button.resize((40, 40))
        self.final_img_back = ImageTk.PhotoImage(self.img_back_button)
        self.back_button = Button(self.graph_frame, image=self.final_img_back, command=self.back_to_records,
                                  bg='#4E4E50', borderwidth=0)
        self.back_button.pack(anchor=NW, pady=5, padx=10)
        self.graph_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        labels = ['I Division', 'II Division',
                  'III Division', 'result not declared']
        i_div = len(self.df[self.df['DIV'] == 'I'])
        ii_div = len(self.df[self.df['DIV'] == 'II'])
        iii_div = len(self.df[self.df['DIV'] == 'III'])
        result_not_declared = len(self.df[self.df['DIV'] == ''])
        wedge_sizes = [i_div, ii_div, iii_div, result_not_declared]
        self.display_pie_chart(wedge_sizes, labels)

    def first_div_records(self):
        self.back_to_records()
        self.delete_all_records()
        temp_df = self.df[self.df['DIV'] == 'I']
        temp_df.index = np.arange(len(temp_df))
        self.enter_records_from_df(temp_df)

    def first_and_second_div_records(self):
        self.back_to_records()
        self.delete_all_records()
        temp_df = self.df[(self.df['DIV'] == 'I') | (self.df['DIV'] == 'II')]
        temp_df.index = np.arange(len(temp_df))
        self.enter_records_from_df(temp_df)

    def move_record_up(self):
        rows = self.records_treeView.selection()
        for row in rows:
            self.records_treeView.move(row, self.records_treeView.parent(
                row), self.records_treeView.index(row) - 1)

    def move_record_down(self):
        rows = self.records_treeView.selection()
        for row in reversed(rows):
            self.records_treeView.move(row, self.records_treeView.parent(
                row), self.records_treeView.index(row)+1)

    def filter(self, cgpa):
        self.delete_all_records()
        desired_records = list()
        for i in range(len(self.df)):
            try:
                desired_records.append(pd.to_numeric(
                    self.df.loc[i, 'GR. CGPA']) > cgpa)

            except TypeError:
                desired_records.append(False)
                continue

        temp_df = self.df[desired_records]
        temp_df.index = np.arange(len(temp_df))
        self.enter_records_from_df(temp_df)

    def remove_record(self):
        self.records_treeView.delete(self.records_treeView.selection())

    def default_records(self):
        self.records_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.delete_all_records()
        self.enter_records_from_df(self.df)

    def __init__(self, master, df):
        self.df = df
        window = Toplevel(master)
        window.geometry('800x600')
        window.title('Analyse Window')
        left_half_frame = Frame(window, bg='#1A1A1D')
        right_half_frame = Frame(window, bg='#4E4E50')
        left_half_frame.pack_propagate(0)
        right_half_frame.pack_propagate(0)
        left_half_frame.pack(side=LEFT, fill=BOTH, expand=True)
        right_half_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        sort_frame = LabelFrame(
            left_half_frame, text='Sort Records', bg='#1A1A1D', fg='#C3073F')
        sort_frame.pack(padx=20, pady=7, fill='x')
        self.img_sort = Image.open(
            'res\\buttons\\button_sort_records.png')
        self.img_sort = self.img_sort.resize((120, 40))
        self.final_img_sort = ImageTk.PhotoImage(self.img_sort)
        sort_button = Button(sort_frame, image=self.final_img_sort,
                             command=lambda: self.sort_records(
                                 self.records_treeView, self.sort_variable.get(), self.sort_order.get()),
                             bg='#1A1A1D', borderwidth=0)
        sort_button.grid(row=0, column=0, columnspan=2,
                         pady=(14, 7), sticky=W, padx=20)
        self.sort_variable = StringVar()
        self.sort_order = BooleanVar()
        div_radio_button = Radiobutton(
            sort_frame, text='DIV', variable=self.sort_variable, value='Division', bg='#1A1A1D', fg='#C3073F')
        cgpa_radio_button = Radiobutton(
            sort_frame, text='CGPA', var=self.sort_variable, value='C.G.P.A', bg='#1A1A1D', fg='#C3073F')
        ascending_radio_button = Radiobutton(
            sort_frame, text='Ascending Order', variable=self.sort_order, value=False, bg='#1A1A1D', fg='#C3073F')
        descending_radio_button = Radiobutton(
            sort_frame, text='Descending Order', variable=self.sort_order, value=True, bg='#1A1A1D', fg='#C3073F')
        div_radio_button.grid(row=1, column=0, sticky=W, padx=10, pady=7)
        cgpa_radio_button.grid(row=1, column=1, sticky=W, padx=(0, 10), pady=7)
        ascending_radio_button.grid(row=2, column=0, sticky=W, padx=10, pady=7)
        descending_radio_button.grid(
            row=2, column=1, sticky=W, padx=(0, 10), pady=7)
        self.sort_variable.set('C.G.P.A')
        self.sort_order.set(False)
        segregate_frame = Frame(left_half_frame, bg='#1A1A1D')
        segregate_frame.pack(fill=X)
        self.img_cgpa = Image.open(
            'res\\buttons\\button_cgpa_distribution.png')
        self.img_cgpa = self.img_cgpa.resize((140, 40))
        self.final_img_cgpa = ImageTk.PhotoImage(self.img_cgpa)
        cgpa_button = Button(segregate_frame, image=self.final_img_cgpa, command=self.display_cgpa_graph,
                             bg='#1A1A1D', borderwidth=0)
        cgpa_button.grid(row=0, column=0, stick=W, pady=(14, 7), padx=20)
        self.img_div = Image.open(
            'res\\buttons\\button_division_distribution.png')
        self.img_div = self.img_div.resize((140, 40))
        self.final_img_div = ImageTk.PhotoImage(self.img_div)
        div_button = Button(segregate_frame, image=self.final_img_div, command=self.display_div_graph,
                            bg='#1A1A1D', borderwidth=0)
        div_button.grid(row=0, column=1, sticky=W, padx=20, pady=7)
        self.img_i_div = Image.open(
            'res\\buttons\\button_i_div.png')
        self.img_i_div = self.img_i_div.resize((140, 40))
        self.final_img_i_div = ImageTk.PhotoImage(self.img_i_div)
        first_div_button = Button(segregate_frame, image=self.final_img_i_div, command=self.first_div_records,
                                  bg='#1A1A1D', borderwidth=0)
        first_div_button.grid(row=1, column=0, sticky=W, padx=20, pady=(7, 14))
        self.img_i_ii_div = Image.open(
            'res\\buttons\\button_i_ii_div.png')
        self.img_i_ii_div = self.img_i_ii_div.resize((140, 40))
        self.final_img_i_ii_div = ImageTk.PhotoImage(self.img_i_ii_div)
        first_and_second_div_button = Button(segregate_frame, image=self.final_img_i_ii_div, command=self.first_and_second_div_records,
                                             bg='#1A1A1D', borderwidth=0)
        first_and_second_div_button.grid(
            row=1, column=1, sticky=W, padx=20, pady=(7, 14))
        # customize records table
        customize_records_frame = LabelFrame(
            left_half_frame, text='Customize records table', bg='#1A1A1D', fg='#C3073F')
        customize_records_frame.pack(padx=20, fill='x', anchor=W)
        self.img_up = Image.open('res\\buttons\\button_move_up.png')
        self.img_up = self.img_up.resize((120, 40))
        self.final_img_up = ImageTk.PhotoImage(self.img_up)
        move_up_button = Button(customize_records_frame, image=self.final_img_up, command=self.move_record_up,
                                bg='#1A1A1D', borderwidth=0)
        move_up_button.grid(row=0, column=0, stick=W, pady=(14, 7), padx=20)
        self.img_down = Image.open(
            'res\\buttons\\button_move_down.png')
        self.img_down = self.img_down.resize((120, 40))
        self.final_img_down = ImageTk.PhotoImage(self.img_down)
        move_down_button = Button(customize_records_frame, image=self.final_img_down, command=self.move_record_down,
                                  bg='#1A1A1D', borderwidth=0)
        move_down_button.grid(row=0, column=1, stick=W, pady=(14, 7), padx=20)
        self.img_remove = Image.open(
            'res\\buttons\\button_remove_record.png')
        self.img_remove = self.img_remove.resize((120, 40))
        self.final_img_remove = ImageTk.PhotoImage(self.img_remove)
        remove_button = Button(customize_records_frame, image=self.final_img_remove, command=self.remove_record,
                               bg='#1A1A1D', borderwidth=0)
        remove_button.grid(row=1, column=0, stick=W, pady=(14, 7), padx=20)
        self.img_default = Image.open(
            'res\\buttons\\button_default_records.png')
        self.img_default = self.img_default.resize((120, 40))
        self.final_img_default = ImageTk.PhotoImage(self.img_default)
        default_button = Button(customize_records_frame, image=self.final_img_default, command=self.default_records,
                                bg='#1A1A1D', borderwidth=0)
        default_button.grid(row=1, column=1, stick=W, pady=(14, 7), padx=20)
        # filter frame
        filter_frame = LabelFrame(
            left_half_frame, text='Filter with C.G.P.A', bg='#1A1A1D', fg='#C3073F')
        filter_frame.pack(padx=20, pady=7, fill='x')
        self.filter_cgpa_entry = Entry(filter_frame, width=50)
        self.filter_cgpa_entry.pack(pady=7)
        self.img_filter = Image.open(
            'res\\buttons\\button_search.png')
        self.img_filter = self.img_filter.resize((120, 40))
        self.final_img_filter = ImageTk.PhotoImage(self.img_filter)
        filter_search_button = Button(filter_frame, image=self.final_img_filter, command=lambda: self.filter(self.validate(self.filter_cgpa_entry.get())),
                                      bg='#1A1A1D', borderwidth=0)
        filter_search_button.pack(pady=7, padx=20)

        self.graph_frame = Frame(right_half_frame, bg='#4E4E50')
        self.records_frame = Frame(right_half_frame, bg='#4E4E50')
        self.records_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        # creating a scrollbar
        tree_scroll = Scrollbar(self.records_frame)
        tree_scroll.pack(side=RIGHT, fill=Y, pady=10, padx=(0, 10))
        self.records_treeView = ttk.Treeview(
            self.records_frame, yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.records_treeView.yview)

        self.records_treeView.pack(
            fill=BOTH, expand=True, padx=(10, 0), pady=10)
        record_columns = ['Name', 'Division', 'C.G.P.A']
        self.records_treeView['columns'] = record_columns

        # formatting the columns
        self.records_treeView.column('#0', width=0, stretch=NO)
        self.records_treeView.column('Name', width=180, anchor=W)
        self.records_treeView.column('Division', width=90, anchor=CENTER)
        self.records_treeView.column('C.G.P.A', width=90, anchor=CENTER)

        # Assigning the heading names to the respective columns
        self.records_treeView.heading('Name', text='Name', anchor=W)
        self.records_treeView.heading(
            'Division', text='Division', anchor=CENTER)
        self.records_treeView.heading('C.G.P.A', text='C.G.P.A', anchor=CENTER)

        self.enter_records_from_df(df)
