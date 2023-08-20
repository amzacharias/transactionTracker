#!/usr/bin/python3
"""
Title: Transaction tracker
Author: Amanda Zacharias
Date Created: 08/12/2023
Date Modified: 08/12/2023
Version: python 3.11.4
Note: 
Following this tutorial: https://www.youtube.com/watch?v=HTD86h69PtE
"""

# Dependencies =====
# External
from datetime import datetime
import numpy as np
import pandas as pd
from tabulate import tabulate
# Internal
from transaction import Transaction

# Helper functions
def getUserTransaction(): 
    """
    Title: Gets inputs from the user
    Input: No arguments, uses `input()` to get info from the user.
    Output: Returns an Transaction class object
    """
    print("Getting transaction")
    # Name
    transactionName = input("Enter transaction name: ")
    # Category
    transactionCategories = [
        "Housing", "Food", "Utilities", "Healthcare", "Education", 
        "Personal", "Recreation", "Giving", "Income", "MomIncome" "Misc"
    ]
    loop = True
    while loop: 
        print("Select a category: ")
        for idx, categoryName in enumerate(transactionCategories): 
            print(f"{idx + 1}.  {categoryName}")

        valueRange = f"[1 - {len(transactionCategories)}]"
        # get input
        selectedIdx = int(input(f"Enter a category number {valueRange}: ")) - 1
        # check input
        if selectedIdx in range(len(transactionCategories)): 
            transactionCat = transactionCategories[selectedIdx]
            loop = False
        else: 
            print("Invalid category. Please try again.")
            loop = True
    # Amount
    transactionAmount = float(input("Enter transaction amount: "))
    # Denomination
    transactionDenom = input("Enter the country denomination (ex. CAD): ") or "CAD"
    # Date of transaction
    eDateEntry = input("Enter the transaction date in YYYY-MM-DD format: ") or \
        datetime.now().strftime("%Y-%m-%d")
    transactionDate = datetime.strptime(eDateEntry, "%Y-%m-%d").strftime("%Y-%m-%d")
    # Combine and output new transaction
    newTransaction = Transaction(
                name = transactionName, 
                category = transactionCat, 
                amount = transactionAmount, 
                denom = transactionDenom, 
                date = transactionDate
                )
    return(newTransaction)


def writeUserTransaction(transaction: Transaction, transactionFilePath): 
    """
    Title: 
    Input: 
    Output: 
    """
    print(f"Writing transaction: {transaction}")
    with open(transactionFilePath, "a") as f: 
        f.write(
            f"{transaction.name},{transaction.category},{transaction.amount},{transaction.denom},{transaction.date}\n")


def summarizingTransactions(transactionFilePath, targMonth): 
    """
    Title: 
    Input: 
    Output: 
    """
    print("Getting transaction\n")
    tData = pd.read_csv(transactionFilePath)
    tData["date"] = pd.to_datetime(tData["date"])
    if targMonth != 0: 
        tData = tData.loc[(tData['date'].dt.month == targMonth)]
        tData["data"] = tData.date.astype(str)

    # Summarize amounts by category
    amountsByCatDf = tData.groupby(["category"]).amount.sum()
    print("Net transaction amounts by category")
    print(amountsByCatDf)

    # Overall summary
    netTransactions = tData.amount.sum()
    print(f"Net transactions: ${netTransactions:.2f}")
    totalIncome = tData[tData["amount"] >= 1].amount.sum()
    print(f"Total income: ${totalIncome:.2f}")
    totalCosts = tData[tData["amount"] <= 1].amount.sum()
    print(f"Total costs: ${totalCosts:.2f}")
    flexibleCosts = tData[tData["amount"] <= 1]
    flexibleCosts = flexibleCosts[
         ~flexibleCosts["category"].isin(["Education", "Housing", "Utilities"])].\
            groupby(["category"]).amount.sum()
    print("Flexible costs:")
    print(flexibleCosts)

    
# Main
def main(): 
    print("Running transaction tracker!")
    # Instantiate variables
    transactionFilePath = "transactions.csv"

    # Get user to input transaction.
    toGetT = input("Do you want to enter a transaction? y or n: ")
    if "y" in toGetT: 
        transaction = getUserTransaction()
        print(transaction)
        # Write transaction to a file.
        writeUserTransaction(transaction, transactionFilePath)

    # Read file and summarize all transactions.
    toGetM = int(input("If you have a month of interest, give its number here: ") or 0)
    summarizingTransactions(transactionFilePath, toGetM)


# Execute main
if __name__ == "__main__": 
    # main() will only run if run directly
    main()
