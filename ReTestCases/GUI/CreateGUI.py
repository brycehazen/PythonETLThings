import os
import glob
import tkinter as tk
from tkinter import filedialog
from RETestCases_original_v8 import process_csv

def select_input_directory():
    input_dir.set(filedialog.askdirectory())

def select_output_directory():
    output_dir.set(filedialog.askdirectory())

def process_input_files():
    try:
        input_directory = input_dir.get()
        output_directory = output_dir.get()

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        os.chdir(input_directory)
        csv_files = glob.glob('*.csv')

        print(f'Processing {len(csv_files)} CSV files...')

        for file in csv_files:
            input_file_path = os.path.join(input_directory, file)
            print(f'Processing file: {input_file_path}')
            process_csv(input_file_path, output_directory)
            print(f'Finished processing file: {input_file_path}')

        print(f'Finished processing all CSV files.')

    except Exception as e:
        print(f'An error occurred: {e}')

root = tk.Tk()
root.title('CSV Processor')

input_dir = tk.StringVar()
output_dir = tk.StringVar()

input_label = tk.Label(root, text='Input directory:')
input_label.grid(row=0, column=0, sticky='e')
input_entry = tk.Entry(root, textvariable=input_dir)
input_entry.grid(row=0, column=1)
input_button = tk.Button(root, text='Browse', command=select_input_directory)
input_button.grid(row=0, column=2)

output_label = tk.Label(root, text='Output directory:')
output_label.grid(row=1, column=0, sticky='e')
output_entry = tk.Entry(root, textvariable=output_dir)
output_entry.grid(row=1, column=1)
output_button = tk.Button(root, text='Browse', command=select_output_directory)
output_button.grid(row=1, column=2)

process_button = tk.Button(root, text='Process CSV Files', command=process_input_files)
process_button.grid(row=2, column=1, pady=10)

root.mainloop()
