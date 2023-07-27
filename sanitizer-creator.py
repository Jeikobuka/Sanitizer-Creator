#!/usr/bin/env python 

import customtkinter as ctk
import tkinter as tk
from tktooltip import ToolTip
from tkinter import filedialog, messagebox
from PIL import Image
import webbrowser, os, json

settingsTemplate = {
    "sanitizerScriptsLocation": "",
    "selectedSanitizerScript": ""
}
parameterWidgets = []

# GETTERS & SETTERS
def getSaveData():
    try:
        with open('settings.json', 'r') as f:
            data = json.load(f)
        return data
    except (KeyError, json.JSONDecodeError) as e:
        print("Caught a JSON Exception, resetting settings...\n"+e)

def setSaveData(k, v):
    saveData = getSaveData()
    saveData[k] = v
    with open('settings.json', 'w') as f:
        data = json.dump(saveData, f, indent=4)
    print(f'Key: {k}\nValue: {v}\nSaved!')

def setSanitizerParams(fp):
    if not os.path.exists(fp): return
    filenameLabel.configure(text=fp.split('/')[-1])
    clearParameterEntries()
    with open(fp, 'r') as f:
        for line in f.readlines():
            addParameterEntry(line.split('->')[0].strip(), line.split('->')[1].strip())
    addParameterEntry("","")

def getSanitizerParams():
    SANITIZER_FILE_CONTENT = ""
    for parameterWidget in parameterWidgets:
        inputEntry = parameterWidget[0].get()
        outputEntry = parameterWidget[1].get()
        if inputEntry.strip() != "" and outputEntry.strip() != "":
            SANITIZER_FILE_CONTENT += inputEntry + "->" + outputEntry + "\n"
    return SANITIZER_FILE_CONTENT

# SANITIZER -----
def saveSanitizerScript(saveType="save"):
    saveData = getSaveData()
    initDir = saveData["sanitizerScriptsLocation"].strip()
    selectedScript = saveData["selectedSanitizerScript"].strip()
    if selectedScript == "" or saveType=="saveAs":
        if initDir == "": messagebox.showinfo(title="No Scripts Folder Location Found!", message="Set your preferred scripts folder location in 'Edit > Preferences'"); return
        sanitizerScriptFilepath = filedialog.asksaveasfilename(initialdir = initDir, title = "Save Sanitizer as Filename",
            defaultextension=".txt",filetypes=[("Text Documents","*.txt")])
        if sanitizerScriptFilepath.strip() == "": return
        setSaveData("selectedSanitizerScript", sanitizerScriptFilepath)
        with open(sanitizerScriptFilepath, 'w') as f:
            f.write("")
    saveData = getSaveData()
    SANITIZER_FILE_CONTENT = getSanitizerParams()
    with open(saveData["selectedSanitizerScript"], 'w') as f:
        f.write(SANITIZER_FILE_CONTENT.strip())
    filenameLabel.configure(text=saveData["selectedSanitizerScript"].split('/')[-1])
    filenameLabel.configure(state=tk.ACTIVE)
    print("Sanitizer Saved")

def createNewSanitizerScript():
    saveData = getSaveData()
    initDir = saveData["sanitizerScriptsLocation"].strip()
    if initDir == "": messagebox.showinfo(title="No Scripts Folder Location Found!", message="Set your preferred scripts folder location in 'Edit > Preferences'"); return
    sanitizerScriptFilepath = filedialog.asksaveasfilename(initialdir = initDir, title = "Create a File to Generate the Sanitizer in",
        defaultextension=".txt",filetypes=[("Text Documents","*.txt")])
    if sanitizerScriptFilepath.strip() == "": return
    setSaveData("selectedSanitizerScript", sanitizerScriptFilepath)
    filenameLabel.configure(text=sanitizerScriptFilepath.split('/')[-1])
    with open(sanitizerScriptFilepath, 'w') as f:
        f.write("")
    clearParameterEntries()
    addParameterEntry("","")

def openSanitizerScript():
    saveData = getSaveData()
    initDir = saveData["sanitizerScriptsLocation"].strip()
    if initDir == "": messagebox.showinfo(title="No Scripts Folder Location Found!", message="Set your preferred scripts folder location in 'Edit > Preferences'"); return
    sanitizerScriptFilepath = filedialog.askopenfilename(initialdir = initDir, title = "Open a Sanitizer Script File",
        defaultextension=".txt",filetypes=[("Text Documents","*.txt")])
    setSaveData("selectedSanitizerScript", sanitizerScriptFilepath)
    setSanitizerParams(sanitizerScriptFilepath)

def addParameterEntry(inputText, outputText):
    inputEntry = ctk.CTkEntry(master=leftParamFrame, font=ENTRY_BOX_FONT, width=100, height=30, justify=tk.CENTER)
    inputEntry.pack(padx=15,pady=5)
    inputEntry.insert(0, inputText)
    outputEntry = ctk.CTkEntry(master=rightParamFrame, font=ENTRY_BOX_FONT, width=100, height=30, justify=tk.CENTER)
    outputEntry.pack(padx=15,pady=5)
    outputEntry.insert(0, outputText)
    parameterWidgets.append((inputEntry, outputEntry))

def removeParameterEntry():
    if (len(parameterWidgets) <= 1) or (parameterWidgets[-1][0].get().strip() != "" or parameterWidgets[-1][1].get().strip() != ""): return
    parameterWidgets[-1][0].destroy()
    parameterWidgets[-1][1].destroy()
    parameterWidgets.pop()

def clearParameterEntries():
    global parameterWidgets
    for widget in parameterWidgets:
        widget[0].destroy()
        widget[1].destroy()
    parameterWidgets = []
    print(parameterWidgets)

def checkIfSaved(event:tk.Event=None):
    saveData = getSaveData()
    if not os.path.exists(saveData["selectedSanitizerScript"]): return
    with open(saveData["selectedSanitizerScript"], 'r') as f:
        if f.read().strip() != getSanitizerParams().strip():
            filenameLabel.configure(state=tk.DISABLED)
        else:
            filenameLabel.configure(state=tk.ACTIVE)

# SANITIZER -----


# SETTINGS -----
def setScriptsFolder():
    saveData = getSaveData()
    initDir = saveData["sanitizerScriptsLocation"].strip()
    if initDir == "": initDir = os.getcwd()
    folderLocation = filedialog.askdirectory(initialdir = initDir, title = "Select a Folder to Store Your Generated Scripts")
    if folderLocation.strip() == "": return
    setSaveData("sanitizerScriptsLocation", folderLocation)
    messagebox.showinfo(title="Script Location Set!", message=f"Sanitizer Script Location Set To: {folderLocation}")
    return folderLocation

def openSettingsWindow():
    settingsWin = ctk.CTk()
    settingsWin.title("Sanitizer Creator - Settings")
    settingsWin.geometry("350x300")
    settingsWin.grab_set()
    settingsFrame = ctk.CTkScrollableFrame(master=settingsWin, width=300, height=200, corner_radius=10)
    settingsFrame.pack(pady=5, padx=5, side=tk.TOP, fill=tk.X, expand=True)
    buttonFrame = ctk.CTkFrame(master=settingsWin)
    buttonFrame.pack(pady=5, padx=5, side=tk.BOTTOM, fill=tk.X, expand=True)

    # SETTINGS
    scriptLocationFrame = ctk.CTkFrame(master=settingsFrame)
    scriptLocationFrame.pack(pady=5, padx=5, side=tk.TOP, fill=tk.X, expand=True)
    scriptLocationLabel = ctk.CTkLabel(master=scriptLocationFrame, text="Script Location:", font=SETTINGS_FONT)
    scriptLocationLabel.grid(row=0,column=0, padx=5, pady=5)
    scriptLocationButton = ctk.CTkButton(master=scriptLocationFrame, text="Browse Folder Locations...", font=SETTINGS_FONT, command=setScriptsFolder)
    scriptLocationButton.grid(row=0,column=1, padx=5, pady=5)
    # CLOSE
    closeButton = ctk.CTkButton(master=buttonFrame, text="Close", font=LABEL_FONT, width=40, command=settingsWin.destroy)
    closeButton.pack(padx=10, pady=10, anchor=tk.E, side=tk.RIGHT)
    settingsWin.mainloop()
# SETTINGS -----

saveData = getSaveData()
filenameText = "?"
if saveData["selectedSanitizerScript"].strip() != "" and os.path.exists(saveData["selectedSanitizerScript"]):
    filenameText = saveData["selectedSanitizerScript"].split('/')[-1]
if not os.path.exists(saveData["selectedSanitizerScript"]):
    setSaveData("selectedSanitizerScript", "")

# WINDOW
saveData = getSaveData()
WINDOW_TITLE = "Sanitizer Creator"
ENTRY_BOX_FONT = ("Roboto", 16)
LABEL_FONT = ("Roboto", 15)
SETTINGS_FONT = ("Roboto", 13)

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title(WINDOW_TITLE)
root.geometry("325x425")
root.resizable(False, False)

# MENUBARS
menubar = tk.Menu(root)
fileMenu = tk.Menu(menubar, tearoff=0)
fileMenu.add_command(label="New"+" "*21+"Ctrl+N", command=createNewSanitizerScript)
root.bind('<Control-n>', createNewSanitizerScript)
fileMenu.add_command(label="Open"+" "*20+"Ctrl+O", command=openSanitizerScript)
root.bind('<Control-o>', openSanitizerScript)
fileMenu.add_command(label="Save"+" "*22+"Ctrl+S", command=saveSanitizerScript)
root.bind('<Control-s>', saveSanitizerScript)
fileMenu.add_command(label="Save As...", command=lambda:saveSanitizerScript("saveAs"))
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)
editMenu = tk.Menu(menubar, tearoff=0)
editMenu.add_command(label="Preferences", command=openSettingsWindow)
helpMenu = tk.Menu(menubar, tearoff=0)
helpMenu.add_command(label="Help Index")
helpMenu.add_command(label="About...", command= lambda: webbrowser.open("https://github.com/Jeikobuka/Sanitizer-Creator"))
menubar.add_cascade(label="File", menu=fileMenu)
menubar.add_cascade(label="Edit", menu=editMenu)
menubar.add_cascade(label="Help", menu=helpMenu)
root.config(menu=menubar)
root.bind("<KeyRelease>", checkIfSaved)

filenameFrame = ctk.CTkFrame(master=root, corner_radius=10)
filenameFrame.pack(pady=5, padx=10)

filenameLabel = ctk.CTkButton(master=filenameFrame, text=filenameText, width=5, font=LABEL_FONT)
filenameLabel.pack(pady=2, padx=2)
filenameLabel.configure(state=tk.NORMAL)
ToolTip(filenameLabel, msg="Currently opened file...", delay=0.1)

parametersFrame = ctk.CTkScrollableFrame(master=root, width=300, height=275, corner_radius=10)
parametersFrame.pack(pady=5, padx=15)

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
setSanitizerParams(saveData["selectedSanitizerScript"])
if not os.path.exists(saveData["selectedSanitizerScript"]):
    addParameterEntry("","")
inputLabel = ctk.CTkLabel(master=inputLabelFrame, text="Input", font=LABEL_FONT, width=75, height=30, justify=tk.CENTER).pack()
outputLabel = ctk.CTkLabel(master=outputLabelFrame, text="Output", font=LABEL_FONT, width=75, height=30, justify=tk.CENTER).pack()

# PARAMETER ENTRIES
controlsFrame = ctk.CTkFrame(master=root, height=20, corner_radius=10)
controlsFrame.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)

addParamImg = ctk.CTkImage(dark_image=Image.open("assets/add_sign.png"), size=(12,12))
removeParamImg = ctk.CTkImage(dark_image=Image.open("assets/remove_sign.png"), size=(12,12))

paramAddRemoveFrame = ctk.CTkFrame(master=controlsFrame)
paramAddRemoveFrame.pack(padx=5,pady=5, fill=tk.Y, expand=True, side=tk.LEFT, anchor=tk.W)

addParamRowButton = ctk.CTkButton(master=paramAddRemoveFrame, text="", image=addParamImg, width=10, height=20, command=lambda:addParameterEntry("",""))
addParamRowButton.pack(padx=2, pady=2, side=tk.TOP)
removeParamRowButton = ctk.CTkButton(master=paramAddRemoveFrame, text="", image=removeParamImg, width=10, height=20, command=removeParameterEntry)
removeParamRowButton.pack(padx=2, pady=2, side=tk.BOTTOM)
ToolTip(addParamRowButton, msg="Add Row of Parameters", delay=0.2)
ToolTip(removeParamRowButton, msg="Remove Row of Parameters", delay=0.2)

saveSanitizerButton = ctk.CTkButton(master=controlsFrame, text="Save Sanitizer", font=LABEL_FONT, width=75, height=30, command=saveSanitizerScript)
saveSanitizerButton.pack(pady=10, padx=10, side=tk.RIGHT, anchor=tk.SE)

root.mainloop()