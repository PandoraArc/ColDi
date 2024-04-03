#!/usr/bin/env conda run -n pyimagej python
# - *- coding: utf- 8 - *-

from tkinter import filedialog
from tkinter import messagebox as mbox
import tkinter as tk
import imagej as ij
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ColDi
import ColDiTargetimage
import os

# crearte object
tarImage = ColDiTargetimage.targetimage()
global pyimageJ
global pyimageJ_Result
global pyimageJ_Diameter


def imageJ_initialize():
    print("initialize")
    global pyimageJ
    pyimageJ = ij.init()


def program_initialize():
    massagebox = tk.Toplevel(root_Gui)
    massagebox.title("ColDi")
    massagebox.geometry("250x100")
    massagebox_lable = tk.Label(massagebox, text="initializing ImageJ")
    massagebox_lable.pack(pady=10)
    massagebox_botton = tk.Button(massagebox, text="OK", state=tk.DISABLED, command=massagebox.destroy)
    massagebox_botton.pack(pady=10)
    initialize_Button.configure(state=tk.DISABLED)
    imageJ_initialize()
    massagebox_lable.configure(text="ImageJ is completely initialized")
    massagebox_botton.configure(state=tk.NORMAL)
    fileLocarion_button.configure(state=tk.NORMAL)
    saveLocation_button.configure(state=tk.NORMAL)
    analyze_Button.configure(state=tk.NORMAL)
    resultGraph_Button.configure(state=tk.NORMAL)
    clear_button.configure(state=tk.NORMAL)


def get_Filename_Fileloacation():
    tarImage.filelocation = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("PNG file", "*.png"),
                                                                                                         ("JPEG file", "*.jpeg"),
                                                                                                         ("JPG file", "*.jpg")))
    fileLocation_result.configure(text=tarImage.filelocation)
    tarImage.filename = ColDi.capture_Filename(tarImage.filelocation)
    savenameFileinfo_entry.delete(0, tk.END)
    savenameFileinfo_entry.insert(tk.END, tarImage.filename)


def get_Savelocation():
    tarImage.savelocation = filedialog.askdirectory(initialdir="/", title="Select a folder", )
    saveLocation_result.configure(text=tarImage.savelocation)
    # print(tarImage.savelocation)
    # print(ColDi.SaveAs(1, savelocation=tarImage.savelocation, savename="test_pic"))


def image_Analyze():
    if not os.path.exists(tarImage.filelocation):
        mbox.showerror("Error", "Can not open file or Save directory does not not exist")
        return 1
    else:
        if not os.path.exists(tarImage.savelocation):
            mbox.showerror("Error", "Can not open file or Save directory does not not exist")
            return 1
        else:
            tarImage.savename = str(savenameFileinfo_entry.get()).strip()
            tarImage.refObj = str(refObj_entry.get()).strip()
            tarImage.pixelrefObj = str(pixelrefObj_entry.get()).strip()
            tarImage.cropZoneX = str(cropXParameter_entry.get()).strip()
            tarImage.cropZoneY = str(cropYParameter_entry.get()).strip()
            tarImage.cropZoneHW = str(cropHWParameter_entry.get()).strip()
            tarImage.threshold_front = str(thresholdParameter_entry_front.get()).strip()
            tarImage.threshold_back = str(thresholdParameter_entry_back.get()).strip()
            tarImage.circularity_start = str(circularityParameter_entry_start.get()).strip()
            tarImage.circularity_end = str(circularityParameter_entry_end.get()).strip()
            tarImage.size_start = str(sizePrameter_entry_start.get()).strip()
            tarImage.size_end = str(sizePrameter_entry_end.get()).strip()
            list_all_parameters = [tarImage.savename, tarImage.refObj, tarImage.pixelrefObj, tarImage.cropZoneX, tarImage.cropZoneY,
                                   tarImage.cropZoneHW, tarImage.threshold_front, tarImage.threshold_back, tarImage.circularity_start,
                                   tarImage.circularity_end, tarImage.size_start, tarImage.size_end]
            for parameter in list_all_parameters:
                if parameter == "":
                    mbox.showerror("Error", "Some parameter is missing")
                    return 1
                else:
                    continue
            Run_macro_state = True

            if Run_macro_state:

                macro_script = ColDi.macro_generate(filelocation=tarImage.filelocation, pixelrefObj=tarImage.pixelrefObj, refObj=tarImage.refObj,
                                                    cropZoneX=tarImage.cropZoneX, cropZoneY=tarImage.cropZoneY, cropZoneHW=tarImage.cropZoneHW,
                                                    threshold_front=tarImage.threshold_front, theshold_back=tarImage.threshold_back,
                                                    size_start=tarImage.size_start, size_end=tarImage.size_end,
                                                    circularity_start=tarImage.circularity_start, circularity_end=tarImage.circularity_end,
                                                    savename=tarImage.savename, savelocation=tarImage.savelocation)

                print(macro_script)
                global pyimageJ_Result
                pyimageJ_Result = pyimageJ.py.run_macro(macro_script)
                excel_generate(tarImage.savelocation, tarImage.savename)
                return 0


def excel_generate(savelocation, savename):
    csv_path = savelocation + '/' + savename + "-5.csv"
    result_excel_df = pd.read_csv(csv_path)
    result_excel_df['Diameter'] = result_excel_df['Area'] / 3.14
    result_excel_df['Diameter'] = result_excel_df['Diameter'].transform(np.sqrt)
    result_excel_df['Diameter'] = 2 * (result_excel_df['Diameter'])
    max_value = result_excel_df['Diameter'].max()
    indexNames = result_excel_df[result_excel_df['Diameter'] == max_value].index
    result_excel_df.drop(indexNames, inplace=True)
    np.set_printoptions(precision=2)
    tarImage.average = np.average(result_excel_df['Diameter'])
    tarImage.median = np.median(result_excel_df['Diameter'])
    newDataframe = pd.DataFrame({"average": [tarImage.average], "median": [tarImage.median]})
    Final_excel = [result_excel_df, newDataframe]
    Final_excel_df = pd.concat(Final_excel, axis=1)
    xlsx_path = savelocation + '/' + savename + "-5.xlsx"
    writer = pd.ExcelWriter(xlsx_path, engine='xlsxwriter')
    Final_excel_df.to_excel(writer, sheet_name='Sheet1')
    writer.close()
    global pyimageJ_Diameter
    pyimageJ_Diameter = Final_excel_df['Diameter']
    # histogram = Final_excel_df.hist(column=""Diameter")
    resultAverage_result_lable.configure(text=np.around(tarImage.average, decimals=2))
    resultMedian_result_lable.configure(text=np.around(tarImage.median, decimals=2))


def graph():
    plt.hist(pyimageJ_Diameter)
    plt.show()


def clear_data():
    fileLocation_result.configure(text="None")
    tarImage.filelocation = ""
    tarImage.filename = ""
    tarImage.savelocation = ""
    saveLocation_result.configure(text="None")
    savenameFileinfo_entry.delete(0, tk.END)
    savenameFileinfo_entry.insert(tk.END, "Default  is file name")
    refObj_entry.delete(0, tk.END)
    pixelrefObj_entry.delete(0, tk.END)
    cropXParameter_entry.delete(0, tk.END)
    cropYParameter_entry.delete(0, tk.END)
    cropHWParameter_entry.delete(0, tk.END)
    thresholdParameter_entry_front.delete(0, tk.END)
    thresholdParameter_entry_front.insert(tk.END, "188")
    thresholdParameter_entry_back.delete(0, tk.END)
    thresholdParameter_entry_back.insert(tk.END, "255")
    circularityParameter_entry_start.delete(0, tk.END)
    circularityParameter_entry_start.insert(tk.END, "0.5")
    circularityParameter_entry_end.delete(0, tk.END)
    circularityParameter_entry_end.insert(tk.END, "1")
    sizePrameter_entry_start.delete(0, tk.END)
    sizePrameter_entry_start.insert(tk.END, "0.5")
    sizePrameter_entry_end.delete(0, tk.END)
    sizePrameter_entry_end.insert(tk.END, "Infinity")
    resultAverage_result_lable.configure(text="None")
    resultMedian_result_lable.configure(text="None")


root_Gui = tk.Tk()
root_Gui.title("ColDi")
root_Gui.geometry("500x700")
icon = tk.PhotoImage(file="ColDi_logo.png")
root_Gui.iconphoto(False, icon)

# program_initialize
initialize_Button = tk.Button(root_Gui, text="ImageJ initialize", width=50, command=program_initialize)
initialize_Button.pack()

# location frame
location_Frame = tk.LabelFrame(root_Gui, text="Locarion")
location_Frame.pack(ipady=5, pady=5, padx=10, fill="x")

# filelocation
fileLocarion_lable = tk.Label(location_Frame, text="File location")
fileLocarion_lable.grid(column=0, row=0, sticky="W", padx=5)
fileLocarion_button = tk.Button(location_Frame, text="Browse", command=get_Filename_Fileloacation, state=tk.DISABLED)
fileLocarion_button.grid(column=1, row=0, sticky="W", padx=5)
fileLocation_result = tk.Label(location_Frame, text="None", fg="blue")
fileLocation_result.grid(column=2, row=0, sticky="W")

# savelocation
saveLocation_lable = tk.Label(location_Frame, text="Save location").grid(column=0, row=1, sticky="W", padx=5)
saveLocation_button = tk.Button(location_Frame, text="Browse", command=get_Savelocation, state=tk.DISABLED)
saveLocation_button.grid(column=1, row=1, sticky="W", padx=5)
saveLocation_result = tk.Label(location_Frame, text="None", fg="blue")
saveLocation_result.grid(column=2, row=1, sticky="W")

# save option frame
fileinfo_Frame = tk.LabelFrame(root_Gui, text="Save option")
fileinfo_Frame.pack(ipady=5, pady=5, padx=10, fill="x")

# save name
savenameFileinfo_lable = tk.Label(fileinfo_Frame, text="Save name").grid(column=0, row=1, sticky="W", padx=5)
savenameFileinfo_entry = tk.Entry(fileinfo_Frame)
savenameFileinfo_entry.grid(column=1, row=1, sticky="W", padx=5)
savenameFileinfo_entry.insert(tk.END, "Default  is file name")

# Measurement parameter frame
parameters_Frame = tk.LabelFrame(root_Gui, text="Measurement parameters")
parameters_Frame.pack(ipady=5, pady=5, padx=10, fill="x")

# reference object
refObj_lable = tk.Label(parameters_Frame, text="Size of reference object").grid(column=0, row=0, sticky="W", padx=5)
refObj_entry = tk.Entry(parameters_Frame, width=10)
refObj_entry.grid(column=1, row=0)
refObj_unitlable = tk.Label(parameters_Frame, text="mm").grid(column=3, row=0, sticky="W")

# pixel reference object
pixelrefObj_lable = tk.Label(parameters_Frame, text="Pixel size of reference object").grid(column=0, row=1, sticky="W", padx=5)
pixelrefObj_entry = tk.Entry(parameters_Frame, width=10)
pixelrefObj_entry.grid(column=1, row=1)
pixelrefObj_unitlable = tk.Label(parameters_Frame, text="px").grid(column=3, row=1, sticky="W")

# crop zone
cropParameter_lable = tk.Label(parameters_Frame, text="\nCrop Zone").grid(column=0, row=2, sticky="W", padx=5)
cropXParameter_lable = tk.Label(parameters_Frame, text="X:").grid(column=0, row=3, sticky="W", padx=5)
cropXParameter_entry = tk.Entry(parameters_Frame, width=10)
cropXParameter_entry.grid(column=1, row=3)
cropYParameter_lable = tk.Label(parameters_Frame, text="Y:").grid(column=0, row=4, sticky="W", padx=5)
cropYParameter_entry = tk.Entry(parameters_Frame, width=10)
cropYParameter_entry.grid(column=1, row=4)
cropHWParameter_lable = tk.Label(parameters_Frame, text="Hight and width(H/W)").grid(column=0, row=5, sticky="W", padx=5)
cropHWParameter_entry = tk.Entry(parameters_Frame, width=10)
cropHWParameter_entry.grid(column=1, row=5)

# Threshold
space = tk.Label(parameters_Frame).grid(column=0, row=6, columnspan=True)
thresholdParameter_lable = tk.Label(parameters_Frame, text="Threshold").grid(column=0, row=7, sticky="W", padx=5)
thresholdParameter_entry_front = tk.Entry(parameters_Frame, width=10)
thresholdParameter_entry_front.grid(column=1, row=7)
thresholdParameter_entry_front.insert(tk.END, "188")
slash_lable = tk.Label(parameters_Frame, text="/").grid(column=2, row=7)
thresholdParameter_entry_back = tk.Entry(parameters_Frame, width=10)
thresholdParameter_entry_back.grid(column=3, row=7, sticky="W")
thresholdParameter_entry_back.insert(tk.END, "255")

# circularity
circularityParameter_lable = tk.Label(parameters_Frame, text="Circularity (0-1)").grid(column=0, row=8, sticky="W", padx=5)
circularityParameter_entry_start = tk.Entry(parameters_Frame, width=10)
circularityParameter_entry_start.grid(column=1, row=8, sticky="W")
circularityParameter_entry_start.insert(tk.END, "0.5")
circularity_to_symbol_lable = tk.Label(parameters_Frame, text="-").grid(column=2, row=8)
circularityParameter_entry_end = tk.Entry(parameters_Frame, width=10)
circularityParameter_entry_end.grid(column=3, row=8, sticky="W")
circularityParameter_entry_end.insert(tk.END, "1")

# size
sizePrameter_lable = tk.Label(parameters_Frame, text="Range of analyzed coloy").grid(column=0, row=9, sticky="W", padx=5)
sizePrameter_entry_start = tk.Entry(parameters_Frame, width=10)
sizePrameter_entry_start.grid(column=1, row=9)
sizePrameter_entry_start.insert(tk.END, "0.5")
sizePrameter_to_symbol_lable = tk.Label(parameters_Frame, text="-").grid(column=2, row=9)
sizePrameter_entry_end = tk.Entry(parameters_Frame, width=10)
sizePrameter_entry_end.grid(column=3, row=9, sticky="W")
sizePrameter_entry_end.insert(tk.END, "Infinity")
sizeParameter_unit_lable = tk.Label(parameters_Frame, text="mm²").grid(column=4, row=9)

# Analyze button
analyze_Button = tk.Button(root_Gui, text="Analyze", width=50, state=tk.DISABLED, command=image_Analyze)
analyze_Button.pack()

# result frame
result_Frame = tk.LabelFrame(root_Gui, text="Result")
result_Frame.pack(ipady=5, pady=5, padx=10, fill="x")
resultAverage_lable = tk.Label(result_Frame, text="Average of colony dimeter")
resultAverage_lable.grid(column=0, row=0, sticky="W", padx=5)
resultAverage_result_lable = tk.Label(result_Frame, text="None", fg="blue")
resultAverage_result_lable.grid(column=1, row=0, sticky="W", padx=5)
resultMedian_lable = tk.Label(result_Frame, text="Median of colony dimeter")
resultMedian_lable.grid(column=0, row=1, sticky="W", padx=5)
resultMedian_result_lable = tk.Label(result_Frame, text="None", fg="blue")
resultMedian_result_lable.grid(column=1, row=1, sticky="W", padx=5)
resultGraph_Button = tk.Button(result_Frame, text="Show histogram", command=graph, state=tk.DISABLED)
resultGraph_Button.grid(column=1, row=2, columnspan=True)

# clear button
clear_button = tk.Button(root_Gui, text="Clear data and result", state=tk.DISABLED, command=clear_data)
clear_button.pack()

root_Gui.mainloop()
