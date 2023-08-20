#!/usr/bin/python3
"""
Title: Transaction tracker GUI
Author: Amanda Zacharias
Date Created: 08/14/2023
Date Modified: 08/20/2023
Version: python 3.11.4
"""

# Dependencies
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkcalendar
import pandas as pd

# Class
class TrackerGUI: 

    def __init__(self):

            self.root = tk.Tk()
            self.root.title("Transaction tracker")

            self.frame = tk.Frame(self.root)
            self.frame.pack()

            self.workingDf = pd.DataFrame(columns=["name", "category", "amount", "denomination", "date"])

            # Transaction information ---------------------------------------------
            self.tInfoFrame = tk.LabelFrame(self.frame, text="Input a transaction")
            self.tInfoFrame.grid(row=0, column=0, padx=20, pady=10)

            self.tNameLabel = tk.Label(self.tInfoFrame, text = "Transaction name")
            self.tNameLabel.grid(row=0, column=0)
            self.nameVar = tk.StringVar(value="name")
            self.tNameEntry = tk.Entry(self.tInfoFrame, textvariable=self.nameVar)
            self.tNameEntry.grid(row=1, column=0)

            self.tCategories = [
                 "Cash", "DiningOut", "Entertainment", "Shopping", "Fees", "Travel", 
                 "Health", "Home", "Education", "Groceries", "Transportation", "Utilities", 
                 "AccountTransfers", "BusinessExpenses", "Donations", "Gifts", "Income", 
                 "Payments", "Savings", "Taxes", "Uncategorized"
                ]
            self.tCategoryLabel = tk.Label(self.tInfoFrame, text = "Transaction category")
            self.tCategoryLabel.grid(row=2, column=0)
            self.tCategoryComboBox = ttk.Combobox(self.tInfoFrame, values=self.tCategories)
            self.tCategoryComboBox.current(0)
            self.tCategoryComboBox.grid(row=3, column=0)

            # Amount frame within tInfoFrame
            self.tAmountFrame = tk.Frame(self.tInfoFrame)
            self.tAmountFrame.grid(row=4, column=0)

            self.tAmountLabel = tk.Label(self.tAmountFrame, text = "Transaction amount")
            self.tAmountLabel.grid(row=0, column=0)
            self.amountVar = tk.StringVar(value="0.00")
            self.tAmountSpinBox = ttk.Spinbox(self.tAmountFrame, from_="-infinity", to="infinity", textvariable=self.amountVar)
            self.tAmountSpinBox.grid(row=1, column=0)

            self.tDenomination = tk.Label(self.tAmountFrame, text = "Denomination")
            self.tDenomination.grid(row=0, column=1)
            self.tDenomComboBox = ttk.Combobox(self.tAmountFrame, values=["CAD", "USD"], width=3)
            self.tDenomComboBox.current(0)
            self.tDenomComboBox.grid(row=1, column=1)

            # Right column, tInfoFrame
            self.tDateLabel = tk.Label(self.tInfoFrame, text = "Transaction date")
            self.tDateLabel.grid(row=0, column=1)
            self.tDateCal = tkcalendar.Calendar(self.tInfoFrame, selectmode="day", year=2023, month=8, day=1, date_pattern="yyyy-mm-dd")
            self.tDateCal.grid(row=1, column=1, rowspan=5)

            # Enter button
            button = tk.Button(self.tInfoFrame, text="Enter data", command = self.enterData)
            button.grid(row=5, column=0)

            # Format tInfoFrame widgets
            for self.widget in self.tInfoFrame.winfo_children(): 
                self.widget.grid_configure(sticky="news", padx=10, pady=5)

            # History of transactions ---------------------------------------------
            self.tHistoryFrame = tk.LabelFrame(self.frame, text="Transaction history")
            self.tHistoryFrame.grid(row=1, column=0, padx=20, pady=10, sticky="news")

            # Save new transaction
            self.saveFileLabel = tk.Label(self.tHistoryFrame, text="Save transaction history")
            self.saveFileLabel.grid(row=0, column=0)
            self.saveFileButton = tk.Button(self.tHistoryFrame, text="Save file browser", command=self.writeFile)
            self.saveFileButton.grid(row=1, column=0)

            # Load transaction history
            self.loadFileLabel = tk.Label(self.tHistoryFrame, text="Load transaction history")
            self.loadFileLabel.grid(row=0, column=1)
            self.loadFileButton = tk.Button(self.tHistoryFrame, text="Load file browser", command=self.readFile)
            self.loadFileButton.grid(row=1, column=1)
            

            # Format tHistoryFrame widgets
            for self.widget in self.tHistoryFrame.winfo_children(): 
                self.widget.grid_configure(sticky="news", padx=10, pady=5)

            self.root.mainloop()


    # Helpers
    def enterData(self):
          tName = self.tNameEntry.get()
          tCategory = self.tCategoryComboBox.get()
          tAmount = self.tAmountSpinBox.get()
          tDenom = self.tDenomComboBox.get()
          tDate = self.tDateCal.get_date()
          tList = [tName, tCategory, tAmount, tDenom, tDate]
          tDf = pd.DataFrame(tList).T.\
            rename(columns={0: "name", 1: "category", 2: "amount", 3: "denomination", 4: "date"})
          self.workingDf = pd.concat([self.workingDf, tDf])
    

    def readFile(self): 
        fTypes = [('CSV files',"*.csv")]
        inFilePath = filedialog.askopenfilename(filetypes=fTypes)
        df = pd.read_csv(inFilePath) # create DataFrame
        return(df)
    

    def writeFile(self): 
        fTypes = [('CSV files',"*.csv")]
        outFilePath = filedialog.asksaveasfilename(filetypes=fTypes, initialdir=".")  
        if (self.workingDf.shape[0] >= 1): 
            # Read in dataframe and append or, create dataframe
            if (os.path.exists(outFilePath) == True): 
                df = pd.read_csv(outFilePath)
                # Add new transaction
                saveDf = pd.concat([df, self.workingDf])
            else: 
                saveDf = self.workingDf
            # Save
            saveDf.to_csv(outFilePath, index = False)
            # Reset the working dir
            self.workingDf = pd.DataFrame(columns=["name", "category", "amount", "denomination", "date"])
        else: 
             print("No new transactions!")


TrackerGUI() 

