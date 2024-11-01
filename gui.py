#!/usr/bin/env python
# encoding=utf-8
"""
this gui based on Tkinter framework.
"""

import os
import sys
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pdf_white_cut import worker
from pdf_white_cut.logger import logger


class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PDF Cut White")
        self.geometry("700x500")

        self.create_widgets()

    def create_widgets(self):
        self.browse_in_button = self.create_button("Browse...", self.browse_in_dir)
        self.browse_out_button = self.create_button("Browse...", self.browse_out_dir)
        self.find_button = self.create_button("Find PDF", self.find)
        self.action_button = self.create_button("Cut White", self.do_action)
        self.select_all_button = self.create_button("Select All", self.select_all)
        self.unselect_all_button = self.create_button("Unselect All", self.unselect_all)

        self.file_combobox = self.create_combobox("*.pdf")
        self.text_combobox = self.create_combobox()
        self.directory_combobox = self.create_combobox(os.getcwd())
        self.directory2_combobox = self.create_combobox(os.path.join(os.getcwd(), "cases/output"))

        self.files_found_label = tk.Label(self)

        self.create_files_table()

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.find_button.pack(in_=buttons_frame, side=tk.LEFT)
        self.action_button.pack(in_=buttons_frame, side=tk.LEFT)
        self.select_all_button.pack(in_=buttons_frame, side=tk.LEFT)
        self.unselect_all_button.pack(in_=buttons_frame, side=tk.LEFT)

        self.file_combobox.pack(fill=tk.X)
        self.directory_combobox.pack(fill=tk.X)
        self.browse_in_button.pack(fill=tk.X)
        self.directory2_combobox.pack(fill=tk.X)
        self.browse_out_button.pack(fill=tk.X)
        self.files_table.pack(fill=tk.BOTH, expand=True)
        self.files_found_label.pack(fill=tk.X)

    def browse_in_dir(self):
        directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Input Dir")
        if directory:
            self.directory_combobox.set(directory)

    def browse_out_dir(self):
        directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Output Dir")
        if directory:
            self.directory2_combobox.set(directory)

    def set_check(self, flag):
        for row in self.files_table.get_children():
            self.files_table.item(row, tags=(flag,))

    def select_all(self):
        self.set_check("checked")

    def unselect_all(self):
        self.set_check("unchecked")

    def do_action(self):
        indir = self.directory_combobox.get()
        outdir = self.directory2_combobox.get()

        success = True
        msg = ""
        for row in self.files_table.get_children():
            if "unchecked" in self.files_table.item(row, "tags"):
                continue
            name = self.files_table.item(row, "values")[0]
            input = os.path.join(indir, name)
            output = os.path.join(outdir, name)

            try:
                worker.cut_pdf(str(input), str(output))
            except Exception as e:
                print("error while cut white")
                traceback.print_exc()
                msg = traceback.format_exc()
                success = False
                break
        if success:
            messagebox.showinfo("Info", "Completed!")
        else:
            messagebox.showwarning("Error", f"Error while process: \n{msg}")

    def find(self):
        self.files_table.delete(*self.files_table.get_children())

        file_name = self.file_combobox.get()
        text = self.text_combobox.get()
        path = self.directory_combobox.get()

        if not file_name:
            file_name = "*"
        files = [f for f in os.listdir(path) if f.endswith(".pdf")]

        self.show_files(files)

    def show_files(self, files):
        for fn in files:
            size = os.path.getsize(fn)
            self.files_table.insert("", "end", values=(fn, f"{size // 1024} KB"), tags=("checked",))

        self.files_found_label.config(text=f"{len(files)} file(s) found")

    def create_button(self, text, command):
        return tk.Button(self, text=text, command=command)

    def create_combobox(self, text=""):
        combobox = ttk.Combobox(self)
        combobox.set(text)
        return combobox

    def create_files_table(self):
        self.files_table = ttk.Treeview(self, columns=("File Name", "Size"), show="headings")
        self.files_table.heading("File Name", text="File Name")
        self.files_table.heading("Size", text="Size")
        self.files_table.tag_configure("checked", background="lightgreen")
        self.files_table.tag_configure("unchecked", background="lightcoral")


if __name__ == "__main__":
    app = Window()
    app.mainloop()
