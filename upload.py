from tkinter import *
from TkinterDnD2 import DND_FILES, TkinterDnD
from tkinter import filedialog as fd
from tkinter import messagebox
import time
from tkinter import ttk
from PIL import Image, ImageTk
from findPages import *
import tkinter.font as font
import threading
from analyse import analyseWindow
import pandas as pd
import numpy as np
import camelot


class Upload (TkinterDnD.Tk):

    colleges = ['025- Hans Raj College',
                '029- I.P. College For Women',
                '033- Kalindi College',
                '035- Keshav Mahavidyalaya',
                '075- Shyama Prasad Mukherjee College',
                '078- Sri Guru Gobind Singh College Of Commerce',
                '001- Acharya Narendra Dev College',
                '003- Atma Ram Sanatan Dharam College',
                '009- Bhaskaracharya College of Applied Sciences',
                '013- College of Vocational Studies',
                '015- Deen Dayal Upadhaya College',
                '020- Ramanujan College',
                '053- P.G.D.A.V. College (Day)',
                '058- Ram Lal Anand College(Day)',
                '059- Aryabhatta College',
                '066- Shaheed Rajguru College of Applied Science for Women']

    def __init__(self):
        super().__init__()
        self.title('Result Analysis')
        self.geometry('800x580+400+100')
        self.menu = Menu(self, bg='#1A1A1D')
        self.config(menu=self.menu)
        # creating a menu
        file_menu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New Window', command=self.new_window)
        file_menu.add_command(label='Quit', command=self.quit)
        about_menu = Menu(self.menu)
        self.menu.add_cascade(label='About', menu=about_menu)
        about_menu.add_command(label='About', command=self.about)
        about_menu.add_command(label='Help', command=self.help)

        self.main_frame = Frame(self, bg='#1A1A1D')
        self.main_frame.pack(fill=BOTH, expand=True)
        self.my_font = font.Font(family='Calibri', size=20)
        upload_label = Label(self.main_frame, text='Drop your file here',
                             font=self.my_font, bg='#1A1A1D', fg='#C3073F')
        upload_label.pack(padx=10, pady=(20, 5))

        self.drop_frame = Frame(
            self.main_frame,  height=300, width=500, bg='#4E4E50')
        self.drop_frame.pack_propagate(0)
        self.add_img = Image.open('res\\addFile.png')
        self.add_resized_img = self.add_img.resize((100, 100))
        self.add_file_img = ImageTk.PhotoImage(self.add_resized_img)
        self.image_label = Label(
            self.drop_frame, image=self.add_file_img, bg='#4E4E50')
        self.image_label.place(in_=self.drop_frame, anchor="c", relx=.5, rely=.5)
        self.drop_frame.pack(pady=10, padx=10)
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.drop_inside_list_box)

        or_label = Label(self.main_frame, text='-------or-------',
                         bg='#1A1A1D', font=self.my_font, fg='#C3073F')
        or_label.pack(pady=(5, 10))
        self.img_upload = Image.open(
            'res\\buttons\\button_upload.png')
        self.img_upload = self.img_upload.resize((120, 40))
        self.final_img_upload = ImageTk.PhotoImage(self.img_upload)
        self.upload_button = Button(
            self.main_frame, image=self.final_img_upload, command=self.upload, borderwidth=0, bg='#1A1A1D')
        self.upload_button.pack(pady=(5, 10))

        self.progressBar = ttk.Progressbar(
            self.main_frame, orient=HORIZONTAL, length=300, mode='determinate')
        self.statusBar = Label(self, border=1, relief=SUNKEN,
                               anchor=E, padx=10, bg='#4E4E50', fg='white')
        self.statusBar.pack(anchor=S, fill='x')

        self.img_continue = Image.open(
            'res\\buttons\\button_continue.png')
        self.img_continue = self.img_continue.resize((120, 40))
        self.final_img_continue = ImageTk.PhotoImage(self.img_continue)
        self.continue_button = Button(
            self.main_frame, image=self.final_img_continue, command=self.next_frame, bg='#1A1A1D', borderwidth=0)

    def new_window(self):
        self.destroy()
        upload2 = Upload()
        upload2.mainloop()


    def about(self):
        messagebox.showinfo('About', 
        '''Result Analysis \nVersion: 1.0 \n 
        Result Analysis reads the data from the result in pdf 
        format and extracts useful data from it.
        Data can also be imported into excel and html format.''')

    def help(self):
        messagebox.showinfo('Help', 
        ''' >> Drag and drop file into file dropping area or upload the file by clicking on upload button
        >> Click on continue button after ensuring the correct 
        file is uploaded
        >> Select the college you want get the results of 
        >> Click on analyse window to analyse the result
        >> Excel and html formatted file can also be generated 
        by clicking on respective buttons
        ''')

    def drop_inside_list_box(self, event):

        global file_path
        self.statusBar.config(text='Uploading file...')

        file_path = event.data
        self.progressBar.pack(pady=10)
        for i in range(11):
            time.sleep(0.25)
            self.update_idletasks()
            self.progressBar['value'] = i * 20
        self.progressBar.destroy()
        self.continue_button.pack(pady=10)
        self.statusBar.config(text='File uploaded Sucessfully')
        Label(self.drop_frame, text='The file droppped is : ' + event.data, bg='#4E4E50', fg='white').place(
            in_=self.drop_frame, anchor=CENTER, relx=0.5, rely=0.8)

    def upload(self):
        global file_path

        file_path = fd.askopenfilename(initialdir='C:/', title='Select the PDF',
                                       filetypes=(('pdf files', '*.pdf'), ('all files', '*.*')))
        if file_path != "":
            if file_path.split('.')[1] == 'pdf':
                self.statusBar.config(text='Uploading file...')
                self.progressBar.pack()
                for i in range(11):
                    time.sleep(0.25)
                    self.update_idletasks()
                    self.progressBar['value'] = i * 20
                self.progressBar.destroy()
                Label(self.drop_frame, text='The file uploaded is : ' + file_path, bg='#4E4E50', fg='white').place(
                    in_=self.drop_frame, anchor=CENTER, relx=0.5, rely=0.8)
                self.continue_button.pack(pady=10)
                self.statusBar.config(text='File uploaded Sucessfully')
                self.upload_button.pack_forget()
            else:
                self.statusBar.config(text='Invalid file format selected')

        else:
            self.statusBar.config(text='No file selected')

    def next_frame(self):
        self.statusBar.config(text='')
        self.delete_all_children(self.main_frame)
        self.img_search = Image.open(
            'res\\buttons\\button_search.png')
        self.img_search = self.img_search.resize((120, 40))
        self.final_img_search = ImageTk.PhotoImage(self.img_search)
        code_label = Label(self.main_frame, text='Select the college',
                           bg='#1A1A1D', font=self.my_font, fg='#C3073F')
        code_label.pack(pady=10, padx=130, anchor=W)
        self.selected_college = StringVar()
        code_entry = ttk.Combobox(
            self.main_frame, textvariable=self.selected_college, values=self.colleges, width=70)
        code_entry.pack(pady=(10, 15))
        search_button = Button(self.main_frame, image=self.final_img_search,
                               command=lambda: (threading.Thread(target=self.search_college).start()), bg='#1A1A1D', borderwidth=0)
        search_button.pack(pady=(5, 10))
        self.bottom_frame = Frame(self.main_frame, bg='#1A1A1D')

    def search_college(self):
        if self.selected_college.get() == '':
            self.statusBar.config(
                text='Please select a college from the drop down list')
            self.statusBar.after(2000, lambda: self.statusBar.config(text=''))
        else:

            college = self.selected_college.get()
            college_code = college.split('-')[0]
            self.statusBar.config(text='Searching...')
            progressBar_search_college = ttk.Progressbar(
                self.main_frame, orient=HORIZONTAL, length=300, mode='indeterminate')
            progressBar_search_college.pack()
            progressBar_search_college.start(10)
            self.pages = find_pages(file_path, college_code)
            progressBar_search_college.destroy()
            self.statusBar.config(text='finished searching')

            self.bottom_frame.pack(padx=15, pady=15)
            self.delete_all_children(self.bottom_frame)
            pages_label = Label(self.bottom_frame, text='Pages containg results of interest: \n' +
                                str(self.pages), bg='#1A1A1D', fg='white')
            pages_label.pack(pady=(5, 15))
            self.img_analyse = Image.open(
                'res\\buttons\\button_analyse.png')
            self.img_analyse = self.img_analyse.resize((120, 40))
            self.final_img_analyse = ImageTk.PhotoImage(self.img_analyse)
            analyse_button = Button(self.bottom_frame, image=self.final_img_analyse, bg='#1A1A1D',
                                    borderwidth=0, command=lambda: threading.Thread(target=lambda: self.analyse_pdf()).start())
            self.img_html = Image.open(
                'res\\buttons\\button_generate_html.png')
            self.img_html = self.img_html.resize((200, 40))
            self.final_img_html = ImageTk.PhotoImage(self.img_html)
            html_button = Button(self.bottom_frame, image=self.final_img_html, bg='#1A1A1D',
                                 borderwidth=0, command=lambda: threading.Thread(target=self.generate_html).start())
            self.img_xl = Image.open(
                'res\\buttons\\button_generate_excel.png')
            self.img_xl = self.img_xl.resize((200, 40))
            self.final_img_xl = ImageTk.PhotoImage(self.img_xl)
            xl_button = Button(self.bottom_frame, image=self.final_img_xl, bg='#1A1A1D',
                               borderwidth=0, command=lambda: threading.Thread(target=self.generate_xl).start())
            analyse_button.pack(pady=(10, 15))
            html_button.pack(pady=(5, 15))
            xl_button.pack(pady=(5, 10))

    def analyse_pdf(self):

        self.statusBar.config(text='Extracting the data from PDF...')
        df = self.load_df()
        self.statusBar.config(text='opening Analysis Window...')
        self.progressBar_load_file.destroy()
        self.statusBar.config(text='')
        analyseWindow(self, df)
        

    def load_df(self):
        self.progressBar_load_file = ttk.Progressbar(
            self.bottom_frame, orient=HORIZONTAL, length=300, mode='indeterminate')
        self.progressBar_load_file.pack()
        self.progressBar_load_file.start(10)

        tables = camelot.read_pdf(file_path, ','.join(map(str, self.pages)))

        list_of_dfs = list()

        for table in tables:
            list_of_dfs.append(table.df)

        result_df = pd.concat(list_of_dfs)
        self.format_df(result_df)
        return result_df

    def format_df(self, df):
        # setting the names of columns
        columns = ["Roll No \nName",
                   "SEM \n Father's Name",
                   "Sub Credit",
                   "GR", "GP", "CRP", "Sub Credit",
                   "GR", "GP", "CRP", "Sub Credit",
                   "GR", "GP", "CRP", "Sub Credit",
                   "GR", "GP", "CRP", "Sub Credit",
                   "GR", "GP", "CRP", "Sub Credit",
                   "GR", "GP", "CRP", "Total CR",
                   "Total CRP", "SGPA", "CGPA",
                   "Result",  "GR. CGPA", "DIV"]
        df.columns = columns

        # replacing the redundant columns headers scanned from the pdf with Nan
        df.replace({"Roll No": np.nan}, inplace=True)
        # removing the  redundant headers and empty columns parsed from pdf
        df.dropna(subset=["Roll No \nName"],  axis=0, inplace=True)

        df.replace('PRMS', np.nan, regex=True, inplace=True)
        df.dropna(axis=0, inplace=True, subset=['GR. CGPA'])
        df.index = np.arange(len(df))

    def generate_html(self):
        file_name = 'Result.html'
        self.statusBar.config(text='Generating HTML File...')
        result_df = self.load_df()
        self.print_html_file(result_df, file_name)

        self.statusBar.config(text='HTML file generated')
        self.progressBar_load_file.destroy()

    def generate_xl(self):
        file_name = 'Result.xlsx'
        self.statusBar.config(text='Generating Excel File...')
        result_df = self.load_df()
        result_df.to_excel(file_name, sheet_name='Sheet No 1')
        self.statusBar.config(text='Excel file generated')
        self.progressBar_load_file.destroy()

    def print_html_file(df, page_name):
        html = df.to_html(index=False, header=True).replace(r"\n", "<br/>")

        # writing the data into the file
        with open(page_name, 'w') as f:
            f.write(html)

    def delete_all_children(self, frame):
        children = frame.winfo_children()
        for child in children:
            child.destroy()


if __name__ == '__main__':
    upload1 = Upload()
    upload1.mainloop()

