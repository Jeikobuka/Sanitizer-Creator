import customtkinter as ctk
import tkinter as tk
from PIL import Image

parameterWidgets = []

def saveSanitizerConfig():
    SANITIZER_FILE = ""
    for parameterWidget in parameterWidgets:
        inputEntry = parameterWidget[0].get()
        outputEntry = parameterWidget[1].get()
        if inputEntry.strip() != "" and outputEntry.strip() != "":
            SANITIZER_FILE += inputEntry + "->" + outputEntry + "\n"
    print(SANITIZER_FILE)
    print("Sanitizer Saved")

def addParameterEntry():
    inputEntry = ctk.CTkEntry(master=leftParamFrame, font=ENTRY_BOX_FONT, width=75, height=30, justify=tk.CENTER)
    inputEntry.pack(padx=15,pady=5)
    outputEntry = ctk.CTkEntry(master=rightParamFrame, font=ENTRY_BOX_FONT, width=75, height=30, justify=tk.CENTER)
    outputEntry.pack(padx=15,pady=5)
    parameterWidgets.append((inputEntry, outputEntry))

def removeParameterEntry():
    parameterWidgets[-1][0].destroy()
    parameterWidgets[-1][1].destroy()
    parameterWidgets.pop()


WINDOW_TITLE = "Sanitizer Creator"
ENTRY_BOX_FONT = ("Roboto", 16)
LABEL_FONT = ("Roboto", 14, "bold")

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title(WINDOW_TITLE)
root.geometry("300x400")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
parametersFrame = ctk.CTkScrollableFrame(master=root, width=300, height=275, corner_radius=10)
parametersFrame.pack(pady=10, padx=15)

# PARAMETER ENTRY FRAMES
leftParamFrame = ctk.CTkFrame(master=parametersFrame, width=75)
leftParamFrame.pack(side=tk.LEFT, fill=tk.Y, expand=True)
rightParamFrame = ctk.CTkFrame(master=parametersFrame, width=75)
rightParamFrame.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

# LABEL FRAMES
inputLabelFrame = ctk.CTkFrame(master=leftParamFrame, width=75, height=50, corner_radius=10)
inputLabelFrame.pack(padx=15,pady=5)
outputLabelFrame = ctk.CTkFrame(master=rightParamFrame, width=75, height=50, corner_radius=10)
outputLabelFrame.pack(padx=15,pady=5)

# LABELS
inputLabel = ctk.CTkLabel(master=inputLabelFrame, text="Input", font=LABEL_FONT, width=75, height=30, justify=tk.CENTER).pack()
outputLabel = ctk.CTkLabel(master=outputLabelFrame, text="Output", font=LABEL_FONT, width=75, height=30, justify=tk.CENTER).pack()

# PARAMETER ENTRIES
addParameterEntry()
controlsFrame = ctk.CTkFrame(master=root, corner_radius=10)
controlsFrame.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)

addParamImg = ctk.CTkImage(dark_image=Image.open("assets/add_sign.png"), size=(12,12))
removeParamImg = ctk.CTkImage(dark_image=Image.open("assets/remove_sign.png"), size=(12,12))

paramAddRemoveFrame = ctk.CTkFrame(master=controlsFrame)
paramAddRemoveFrame.pack(padx=5,pady=5, fill=tk.Y, expand=True, side=tk.LEFT, anchor=tk.W)

addParamRowButton = ctk.CTkButton(master=paramAddRemoveFrame, text="", image=addParamImg, width=10, height=20, command=addParameterEntry)
addParamRowButton.pack(padx=2, pady=2, side=tk.TOP)
removeParamRowButton = ctk.CTkButton(master=paramAddRemoveFrame, text="", image=removeParamImg, width=10, height=20, command=removeParameterEntry)
removeParamRowButton.pack(padx=2, pady=2, side=tk.BOTTOM)

saveSanitizerButton = ctk.CTkButton(master=controlsFrame, text="Save Sanitizer", font=LABEL_FONT, width=75, height=30, command=saveSanitizerConfig)
saveSanitizerButton.pack(pady=10, padx=15, side=tk.RIGHT)

root.mainloop()