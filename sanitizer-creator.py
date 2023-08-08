#!/usr/bin/env python 

import customtkinter as ctk
import tkinter as tk
from tktooltip import ToolTip
from tkinter import filedialog, messagebox
from PIL import Image
import webbrowser, os, json

settingsTemplate = {
    "darkmode": True,
    "sanitizerScriptsLocation": "",
    "selectedSanitizerScript": ""
}
parameterWidgets = []
settingsWin = None
previewWin = None

# GETTERS & SETTERS
def log(msg):
    with open('log.txt', 'a') as f:
        f.write(msg)

def compareFile():
    saveData = getSaveData()
    with open(saveData["selectedSanitizerScript"], 'r') as f:
        scriptContents = f.read().strip()
    return scriptContents == getSanitizerParams().strip()

def getSaveData():
    def createTemplate():
        with open('settings.json', 'w') as f:
            json.dump(settingsTemplate, f, indent=4)
        data = getSaveData()
        return data
    if not os.path.exists('settings.json'):
        createTemplate()
    try:
        with open('settings.json', 'r') as f:
            data = json.load(f)
        return data
    except (KeyError, json.JSONDecodeError) as e:
        log("Caught a JSON Exception, resetting settings...\n"+str(e))
        saveData = createTemplate()
        return saveData

def setSaveData(k, v):
    saveData = getSaveData()
    saveData[k] = v
    with open('settings.json', 'w') as f:
        data = json.dump(saveData, f, indent=4)
    log(f'Key: {k}\nValue: {v}\nJSON Saved!\n')

def setSanitizerParams(fp):
    if not os.path.exists(fp): return
    filenameLabelButton.configure(text=fp.split('/')[-1])
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
        if inputEntry.strip() != "":
            SANITIZER_FILE_CONTENT += inputEntry + "->" + outputEntry + "\n"
    return SANITIZER_FILE_CONTENT.strip()
# GETTERS & SETTERS

# SANITIZER -----
def saveSanitizerScript(saveType="save"):
    saveData = getSaveData()
    initDir = saveData["sanitizerScriptsLocation"].strip()
    selectedScript = saveData["selectedSanitizerScript"].strip()
    if not os.path.exists(selectedScript) or saveType=="saveAs":
        if initDir.strip() == "": messagebox.showinfo(title="No Scripts Folder Location Found!", message="Set your preferred scripts folder location in 'Edit > Preferences'"); return
        sanitizerScriptFilepath = filedialog.asksaveasfilename(initialdir = initDir, title = "Save Sanitizer as Filename",
            defaultextension=".txt",filetypes=[("Text Documents","*.txt")])
        if sanitizerScriptFilepath.strip() == "": return
        setSaveData("selectedSanitizerScript", sanitizerScriptFilepath)
        with open(sanitizerScriptFilepath, 'w') as f:
            f.write("")
    saveData = getSaveData()
    SANITIZER_FILE_CONTENT = getSanitizerParams()
    with open(saveData["selectedSanitizerScript"], 'w') as f:
        f.write(SANITIZER_FILE_CONTENT)
    filenameText = saveData["selectedSanitizerScript"].split('/')[-1]
    if filenameLabelButton.cget("text") != filenameText:
        filenameLabelButton.configure(text=filenameText)

def createNewSanitizerScript():
    saveClose = saveOnClose()
    if saveClose == None: return
    saveData = getSaveData()
    initDir = saveData["sanitizerScriptsLocation"].strip()
    if initDir == "": messagebox.showinfo(title="No Scripts Folder Location Found!", message="Set your preferred scripts folder location in 'Edit > Preferences'"); return
    sanitizerScriptFilepath = filedialog.asksaveasfilename(initialdir = initDir, title = "Create a File to Generate the Sanitizer in",
        defaultextension=".txt",filetypes=[("Text Documents","*.txt")])
    if sanitizerScriptFilepath.strip() == "": return
    setSaveData("selectedSanitizerScript", sanitizerScriptFilepath)
    filenameLabelButton.configure(text=sanitizerScriptFilepath.split('/')[-1])
    with open(sanitizerScriptFilepath, 'w') as f:
        f.write("")
    clearParameterEntries()
    addParameterEntry("","")

def openSanitizerScript():
    saveClose = saveOnClose()
    if saveClose == None: return
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
# SANITIZER -----

# WINDOWS -----
def openSettingsWindow():
    global settingsWin
    if settingsWin: settingsWin.focus_force(); return
    def closeSettings():
        global settingsWin
        settingsWin.destroy()
        settingsWin = None
    def setScriptsFolder():
        saveData = getSaveData()
        initDir = saveData["sanitizerScriptsLocation"].strip()
        if initDir == "": initDir = os.getcwd()
        folderLocation = filedialog.askdirectory(initialdir = initDir, title = "Select a Folder to Store Your Generated Scripts")
        if folderLocation.strip() == "": return
        setSaveData("sanitizerScriptsLocation", folderLocation)
        messagebox.showinfo(title="Script Location Set!", message=f"Sanitizer Script Location Set To: {folderLocation}")
        scriptLocationTT.msg = "'"+folderLocation+"'"
        return folderLocation
    def setDarkmode():
        darkmode = darkModeCheckmark.get()
        appearanceMode = "dark" if darkmode else "light"
        ctk.set_appearance_mode(appearanceMode)
        setSaveData("darkmode", darkmode)
    saveData = getSaveData()
    settingsWin = ctk.CTkToplevel()
    settingsWin.title("Sanitizer Creator - Settings")
    settingsWin.geometry(f"350x300+{root.winfo_x()+int(rootW)}+{root.winfo_y()}")
    settingsWin.focus_force()
    settingsFrame = ctk.CTkScrollableFrame(master=settingsWin, width=300, height=200, corner_radius=10)
    settingsFrame.pack(pady=5, padx=5, side=tk.TOP, fill=tk.X, expand=True)
    buttonFrame = ctk.CTkFrame(master=settingsWin)
    buttonFrame.pack(pady=5, padx=5, side=tk.BOTTOM, fill=tk.X, expand=True)

    # SETTINGS
    scriptLocationFrame = ctk.CTkFrame(master=settingsFrame)
    scriptLocationFrame.pack(pady=5, padx=5, side=tk.TOP, fill=tk.X, expand=True)
    scriptLocationLabel = ctk.CTkLabel(master=scriptLocationFrame, text="Script Location:", font=SETTINGS_FONT)
    scriptLocationLabel.grid(row=0,column=0, padx=5, pady=5)
    scriptLocationButton = ctk.CTkButton(master=scriptLocationFrame, text="Browse For Folder Location...", font=SETTINGS_FONT, command=setScriptsFolder)
    scriptLocationButton.grid(row=0,column=1, padx=5, pady=5)
    scriptLocationTT = ToolTip(scriptLocationButton, msg='"'+saveData['sanitizerScriptsLocation']+'"', delay=0.15, )

    darkModeFrame = ctk.CTkFrame(master=settingsFrame)
    darkModeFrame.pack(pady=5, padx=5, side=tk.TOP, fill=tk.X, expand=True)
    darkModeLabel = ctk.CTkLabel(master=darkModeFrame, text="Dark Mode:", font=SETTINGS_FONT)
    darkModeLabel.grid(row=1,column=0, padx=5, pady=5)
    darkModeCheckmark = ctk.CTkCheckBox(master=darkModeFrame, text="", onvalue=True, offvalue=False, command=setDarkmode)
    darkModeCheckmark.grid(row=1,column=1, padx=5, pady=5)
    darkModeCheckmark.select() if saveData["darkmode"] else darkModeCheckmark.deselect()
    # CLOSE
    closeButton = ctk.CTkButton(master=buttonFrame, text="Close", font=LABEL_FONT, width=40, command=closeSettings)
    closeButton.pack(padx=10, pady=10, anchor=tk.E, side=tk.RIGHT)

def openPreviewWindow():
    global scriptPreviewLabel
    global previewWin
    def closePreview():
        global previewWin
        previewWin.destroy()
        previewWin = None
    if previewWin: closePreview(); return
    previewWin = ctk.CTkToplevel()
    previewWin.title("Script Preview")
    previewWin.geometry(f"200x280+{root.winfo_x()+int(rootW)}+{root.winfo_y()}")
    previewWin.resizable(False, False)
    previewWin.focus_force()
    previewFrame = ctk.CTkScrollableFrame(master=previewWin, width=300, height=200, corner_radius=10)
    previewFrame.pack(pady=5, padx=5, side=tk.TOP, fill=tk.X, expand=True)
    buttonFrame = ctk.CTkFrame(master=previewWin)
    buttonFrame.pack(pady=5, padx=5, side=tk.BOTTOM, fill=tk.X, expand=True)
    # SETTINGS
    scriptPreviewLabel = ctk.CTkLabel(master=previewFrame, text=getSanitizerParams(), font=LABEL_FONT, justify=tk.LEFT)
    scriptPreviewLabel.grid(row=0,column=0, padx=5, pady=5)
    # CLOSE
    closeButton = ctk.CTkButton(master=buttonFrame, text="Close", font=LABEL_FONT, width=40, command=closePreview)
    closeButton.pack(padx=5, pady=5, anchor=tk.E, side=tk.RIGHT)
    previewWin.mainloop()
# SETTINGS -----

# EVENTS
def close():
    saveClose = saveOnClose()
    if saveClose != None:
        root.destroy()

def saveOnClose():
    saveData = getSaveData()
    if not os.path.exists(saveData["selectedSanitizerScript"]): return True
    filenameText = saveData["selectedSanitizerScript"].split('/')[-1]
    fileIsOrig = compareFile()
    if fileIsOrig==False:
        yesNoCancel = messagebox.askyesnocancel("You have unsaved changes", f'Do you want to save the changes made to "{filenameText}"?')
        if yesNoCancel == True: # CLICKED YES
            saveSanitizerScript()
            return True
        elif yesNoCancel == False: # CLICKED NO
            return False
        else: # CLICKED CANCEL
            return None
    elif fileIsOrig==True:
        return True

def checkIfFileChanged(event:tk.Event=None):
    try:
        scriptPreviewLabel.configure(text=getSanitizerParams())
    except:
        pass
    saveData = getSaveData()
    if not os.path.exists(saveData["selectedSanitizerScript"]): return
    filenameText = saveData["selectedSanitizerScript"].split('/')[-1]
    fileIsOrig = compareFile()
    if fileIsOrig == True and filenameLabelButton.cget("text") == filenameText+' *': 
        filenameLabelButton.configure(text=filenameText)
    elif fileIsOrig == False and filenameLabelButton.cget("text") == filenameText:
        filenameLabelButton.configure(text=f"{filenameText} *")
        
# EVENTS

def Start():
    global saveData, filenameText
    saveData = getSaveData()
    filenameText = "?"
    if saveData["selectedSanitizerScript"].strip() != "" and os.path.exists(saveData["selectedSanitizerScript"]):
        filenameText = saveData["selectedSanitizerScript"].split('/')[-1]
    if not os.path.exists(saveData["selectedSanitizerScript"]):
        setSaveData("selectedSanitizerScript", "")
    saveData = getSaveData()

def Main():
    Start()
    # WINDOW
    global ENTRY_BOX_FONT, LABEL_FONT, SETTINGS_FONT, root, rootW, rootH, filenameLabelButton, leftParamFrame, rightParamFrame
    WINDOW_TITLE = "Sanitizer Creator"
    ENTRY_BOX_FONT = ("Roboto", 16)
    LABEL_FONT = ("Roboto", 15)
    SETTINGS_FONT = ("Roboto", 13)

    rootW = "325"
    rootH = "425"
    saveData = getSaveData()
    appearanceMode = "dark" if saveData["darkmode"] else "light"
    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode(appearanceMode)
    root = ctk.CTk()
    root.title(WINDOW_TITLE)
    root.geometry(rootW+"x"+rootH)
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
    fileMenu.add_command(label="Exit", command=close)
    editMenu = tk.Menu(menubar, tearoff=0)
    editMenu.add_command(label="Preferences", command=openSettingsWindow)
    helpMenu = tk.Menu(menubar, tearoff=0)
    helpMenu.add_command(label="Help Index")
    helpMenu.add_command(label="About...", command= lambda: webbrowser.open("https://github.com/Jeikobuka/Sanitizer-Creator"))
    menubar.add_cascade(label="File", menu=fileMenu)
    menubar.add_cascade(label="Edit", menu=editMenu)
    menubar.add_cascade(label="Help", menu=helpMenu)
    root.config(menu=menubar)
    root.bind("<KeyRelease>", checkIfFileChanged)

    filenameFrame = ctk.CTkFrame(master=root, corner_radius=5)
    filenameFrame.pack(pady=5, padx=10)

    filenameLabelButton = ctk.CTkButton(master=filenameFrame, text=filenameText, width=20, font=("Roboto", 15, "bold"), corner_radius=5, command=openPreviewWindow)
    filenameLabelButton.pack(pady=2, padx=2)
    ToolTip(filenameLabelButton, msg="Show preview of file...", delay=0.1)

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
    inputLabel = ctk.CTkLabel(master=inputLabelFrame, text="Replace", font=LABEL_FONT, width=75, height=30, justify=tk.CENTER).pack()
    outputLabel = ctk.CTkLabel(master=outputLabelFrame, text="With", font=LABEL_FONT, width=75, height=30, justify=tk.CENTER).pack()

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
    ToolTip(addParamRowButton, msg="Add Row of Parameters", delay=0.15)
    ToolTip(removeParamRowButton, msg="Remove Row of Parameters", delay=0.15)
    saveSanitizerButton = ctk.CTkButton(master=controlsFrame, text="Save Sanitizer", font=LABEL_FONT, width=75, height=30, command=saveSanitizerScript)
    saveSanitizerButton.pack(pady=10, padx=10, side=tk.RIGHT, anchor=tk.SE)

    root.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()

Main()
