import tkinter
from PIL import Image
from tkinter import filedialog, messagebox
import cv2 as cv
from frames import *
from displayTumor import *
from predictTumor import *

import subprocess
import sys
class Gui:
    MainWindow = 0
    listOfWinFrame = list()
    FirstFrame = object()
    val = 0
    fileName = 0
    DT = object()

    wHeight = 700
    wWidth = 1180

    def __init__(self):
        global MainWindow
        MainWindow = tkinter.Tk()
        MainWindow.geometry('1200x720')
        MainWindow.resizable(width=False, height=False)
        
        self.DT = DisplayTumor()

        self.fileName = tkinter.StringVar()

        self.FirstFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, 0, 0)
        self.FirstFrame.btnView['state'] = 'disable'

        self.listOfWinFrame.append(self.FirstFrame)

        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Brain Tumor Detection", height=1, width=40)
        WindowLabel.place(x=320, y=30)
        WindowLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"))

        self.val = tkinter.IntVar()
        RB1 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="Detect Tumor", variable=self.val, value=1, command=self.check)
        RB1.place(x=250, y=200)
        RB2 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="View Tumor Region", variable=self.val, value=2, command=self.check)
        RB2.place(x=250, y=250)
        RB3 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="Classify Tumor", variable=self.val, value=3, command=self.check)
        RB3.place(x=250, y=300)
        RB3 = tkinter.Button(self.FirstFrame.getFrames(), text="Add Patient Details", width=20, command=self.open_patient_form)
        RB3.place(x=250, y=350)
       
        browseBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Browse", width=8, command=self.browseWindow)
        browseBtn.place(x=800, y=550)

        MainWindow.mainloop()

    def getListOfWinFrame(self):
        return self.listOfWinFrame

    def browseWindow(self):
        global mriImage
        FILEOPENOPTIONS = dict(defaultextension='*.*',
                               filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileName = filedialog.askopenfilename(**FILEOPENOPTIONS)
        image = Image.open(self.fileName)
        imageName = str(self.fileName)
        mriImage = cv.imread(imageName, 1)
        self.listOfWinFrame[0].readImage(image)
        self.listOfWinFrame[0].displayImage()
        self.DT.readImage(image)

    def check(self):
        global mriImage
        if self.val.get() == 1:  # Detect Tumor
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)

            res = predictTumor(mriImage)
            print(res, "tumor result")
            if res > 0.5:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Tumor Detected", height=1, width=20)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="red")
            else:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="No Tumor", height=1, width=20)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="green")

            resLabel.place(x=700, y=450)

        elif self.val.get() == 2:  # View Tumor Region
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)
            secFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, self.DT.displayTumor, self.DT)

            self.listOfWinFrame.append(secFrame)

            for i in range(len(self.listOfWinFrame)):
                if i != 0:
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()

            if len(self.listOfWinFrame) > 1:
                self.listOfWinFrame[0].btnView['state'] = 'active'

        elif self.val.get() == 3:  # Classify Tumor
            self.classify_tumor()
        elif self.val.get()==4:
            self.open_patient_form()
        else:
            print("Not Working")
    def open_patient_form(self):
        # Open the patient details form
        subprocess.Popen([sys.executable, 'patient_form.py'])  # This will open the patientform.py

    # Automatic tumor classification logic
    def classify_tumor(self):
        global mriImage
        # First, check if a tumor is detected
        tumor_detected = predictTumor(mriImage)  # Assuming this returns a probability of tumor presence
        
        if tumor_detected <= 0.5:  # No tumor detected
            messagebox.showinfo("Tumor Classification", "No tumor detected, classification not applicable.")
            return  # Exit the function since there's no tumor to classify
        
        # If tumor is detected, classify it
        classification_result = self.get_tumor_type(mriImage)

        if classification_result:
            messagebox.showinfo("Tumor Classification", f"Tumor classified as: {classification_result}")
        else:
            messagebox.showwarning("Classification Error", "Unable to classify tumor type")

# Mock function for classifying tumor type (replace with real model)
    def get_tumor_type(self, image):
        # Replace this logic with actual tumor classification (e.g., ML model or heuristics)
        res = predictTumor(image)  # Assume this returns a probability
        if res > 0.8:
            return "Malignant"
        elif res > 0.5:
            return "Benign"
        else:
            return "Pre-cancerous"
            # Replace this logic with actual tumor classification (e.g., ML model or heuristics)
            # For now, we're just returning a dummy classification.
            res = predictTumor(image)  # Assume this returns a probability
            if res > 0.8:
                return "Malignant"
            elif res > 0.5:
                return "Benign"
            else:
                return "Pre-cancerous"


mainObj = Gui()
