import os
import smtplib
import tempfile
from tkinter import *
from tkinter import messagebox

# Constants
errorText = "Error"
zeroRupeesText = "0.00"
rupeeText = "₹"
minusSymbol = "-"
percentageSymbol = "%"
successText = "Success"
headingLabelTitle = "Billing System"
fontStyle = "Arial"
fontSize = 12
boldFont = "bold"
fieldFontColor = "black"
backgroundColor = "lightgray"
fontColor = "black"
labelBorderSize = 2
billPath = "/path/to/bills/"
billSavingExtension = ".txt"
billFileName = "bill"
printCommandText = "print"
emailSmtp = "smtp.gmail.com"
emailSmtpPort = 587
emailSubject = "Bill Details"
emailReceiverLabelTitle = "Receiver Details"
messageText = "Message"
sendButtonText = "Send Email"
searchFieldEmptyMessage = "Search field is empty"
printValidation = "Unable to print the bill"
searchBillNotFoundMessage = "Bill not found"
somethingWentWrongMessage = "Something went wrong"
senderEmailIdTextEmptyMessage = "Sender email ID is empty"
senderEmailKeyTextEmptyMessage = "Sender email key is empty"
receiverEmailIdTextEmptyMessage = "Receiver email ID is empty"
emailContentEmptyMessage = "Email content is empty"
billNumberTitle = "Bill Number"
starLine = "************************************"
columnNamesInBill = "Product Name\tPrice\tQuantity\tTotal"
cosmeticsNamesList = ["Cosmetic 1", "Cosmetic 2"]
groceryNamesList = ["Grocery 1", "Grocery 2"]
coolDrinksNamesList = ["Cool Drink 1", "Cool Drink 2"]
cosmeticsPriceList = [100, 200]
groceryPriceList = [50, 150]
coolDrinksPriceList = [30, 60]
cosmeticsEntryList = [Entry() for _ in cosmeticsNamesList]
groceryEntryList = [Entry() for _ in groceryNamesList]
coolDrinksEntryList = [Entry() for _ in coolDrinksNamesList]
customerDetailsEntryList = [Entry() for _ in range(3)]
billMenuEntryList = [Entry() for _ in range(7)]
textarea = Text()
billNumber = 123
globalTotal = 0
cosmeticTaxPercentage = 18
groceryTaxPercentage = 12
coldDrinksTaxPercentage = 8
billMenuTitlesList = ["Cosmetic Tax", "Grocery Tax", "Cold Drink Tax", "Other Taxes", "Discount", "Total", "Final Amount"]
productsSelected = True
searchBillStatus = False

# Bill generation function
def generateBill():
    global globalTotal
    globalTotal = 0
    textarea.delete(1.0, END)

    # Check for empty fields
    if (billMenuEntryList[0].get() == zeroRupeesText and billMenuEntryList[2].get() == zeroRupeesText and billMenuEntryList[3].get() == zeroRupeesText):
        if (productsSelected):
            messagebox.showerror(errorText, "Total not calculated")
        else:
            messagebox.showerror(errorText, "No products selected")
    else:
        textarea.insert(END, "Welcome to the Billing System\n")
        textarea.insert(END, billNumberTitle + " - " + str(billNumber) + '\n')
        
        # Customer details
        name = customerDetailsEntryList[0].get()
        textarea.insert(END, "Customer Name - " + str(name) + "\n")
        
        phone = customerDetailsEntryList[1].get()
        textarea.insert(END, "Phone - " + str(phone))
        
        textarea.insert(END, starLine)
        textarea.insert(END, columnNamesInBill)
        textarea.insert(END, starLine)

        # Cosmetics
        for index in range(0, len(cosmeticsEntryList)):
            try:
                if (cosmeticsEntryList[index].get() != '' and int(cosmeticsEntryList[index].get()) > 0):
                    textarea.insert(END, cosmeticsNamesList[index] + '\t\t' + str(cosmeticsPriceList[index]) + '\t' +
                                    cosmeticsEntryList[index].get() + '\t' + str(cosmeticsPriceList[index] * int(cosmeticsEntryList[index].get())) + rupeeText + "\n")
                    globalTotal += cosmeticsPriceList[index] * int(cosmeticsEntryList[index].get())
            except:
                print("Bill exception for productName - " + cosmeticsNamesList[index])

        # Groceries
        for index in range(0, len(groceryEntryList)):
            try:
                if (groceryEntryList[index].get() != '' and int(groceryEntryList[index].get()) > 0):
                    textarea.insert(END, groceryNamesList[index] + '\t\t' + str(groceryPriceList[index]) + '\t' +
                                    groceryEntryList[index].get() + '\t' + str(groceryPriceList[index] * int(groceryEntryList[index].get())) + rupeeText + "\n")
                    globalTotal += groceryPriceList[index] * int(groceryEntryList[index].get())
            except:
                print("Bill exception for productName - " + groceryNamesList[index])

        # Cool Drinks
        for index in range(0, len(coolDrinksEntryList)):
            try:
                if (coolDrinksEntryList[index].get() != '' and int(coolDrinksEntryList[index].get()) > 0):
                    textarea.insert(END, coolDrinksNamesList[index] + '\t\t' + str(coolDrinksPriceList[index]) + '\t' +
                                    coolDrinksEntryList[index].get() + '\t' + str(coolDrinksPriceList[index] * int(coolDrinksEntryList[index].get())) + rupeeText + "\n")
                    globalTotal += coolDrinksPriceList[index] * int(coolDrinksEntryList[index].get())
            except:
                print("Bill exception for productName - " + coolDrinksNamesList[index])

        textarea.insert(END, starLine)

        # Taxes and Final Amount
        if (billMenuEntryList[3].get() != '' and billMenuEntryList[3].get() != zeroRupeesText):
            textarea.insert(END, '\t' + billMenuTitlesList[3] + minusSymbol + str(cosmeticTaxPercentage) + percentageSymbol + ' -\t' +
                            billMenuEntryList[3].get() + '\n')
        if (billMenuEntryList[4].get() != '' and billMenuEntryList[4].get() != zeroRupeesText):
            textarea.insert(END, '\t' + billMenuTitlesList[4] + minusSymbol + str(groceryTaxPercentage) + percentageSymbol + ' -\t' +
                            billMenuEntryList[4].get() + '\n')
        if (billMenuEntryList[5].get() != '' and billMenuEntryList[5].get() != zeroRupeesText):
            textarea.insert(END, '\t' + billMenuTitlesList[5] + minusSymbol + str(coldDrinksTaxPercentage) + percentageSymbol + ' -\t' +
                            billMenuEntryList[5].get() + '\n')

        textarea.insert(END, '\n')

        if (globalTotal > 0 and billMenuEntryList[6].get() != ''):
            textarea.insert(END, billMenuTitlesList[6] + ' -\t' + billMenuEntryList[6].get() + '\n')

        textarea.insert(END, starLine)

        saveBill()

# Save bill function
def saveBill():
    billFileName = str(billNumber) + billSavingExtension
    with open(billPath + billFileName, 'w') as billFile:
        billFile.write(textarea.get(1.0, END))
    messagebox.showinfo(successText, "Bill Saved Successfully")

# Search bill function
def searchBill():
    billId = customerDetailsEntryList[2].get()
    billFound = False
    if (billId == ''):
        error = searchFieldEmptyMessage
        if (searchBillStatus == True):
            error = searchFieldEmptyMessage + " or " + printValidation
        messagebox.showerror(errorText, error)
    else:
        billFileName = billId + billSavingExtension
        for fileName in os.listdir(billPath):
            if (fileName == billFileName):
                billFound = True
                with open(billPath + billFileName, 'r') as file:
                    textarea.delete(1.0, END)
                    for data in file:
                        textarea.insert(END, data)
                break
        if (not billFound):
            messagebox.showerror(errorText, customerDetailsTitlesList[2] + billId + searchBillNotFoundMessage)
    searchBillStatus = False
    return billFound

# Print bill function
def printBill():
    searchBillStatus = True
    textareaContent = textarea.get(1.0, END)
    if (textareaContent == '' or textareaContent == '\n'):
        billFound = searchBill()
        if (billFound == True):
            billContent = textarea.get(1.0, END)
            if (billContent != ""):
                fileName = tempfile.mktemp()
                with open(fileName, 'w') as billFile:
                    billFile.write(billContent)
                os.startfile(fileName, printCommandText)

# Send email function
def createSendEmailWindow():
    sendEmailWindow = Toplevel()
    sendEmailWindow.geometry("600x400")
    sendEmailWindow.config(bg=backgroundColor)
    sendEmailWindow.title(emailReceiverLabelTitle)
    
    Label(sendEmailWindow, text=sendButtonText, font=(fontStyle, fontSize, boldFont), fg=fieldFontColor, bg=backgroundColor).grid(row=1, column=0)
    receiverEmailEntry = Entry(sendEmailWindow, font=(fontStyle, fontSize), fg=fontColor)
    receiverEmailEntry.grid(row=2, column=0)

    emailMessageLabel = Label(sendEmailWindow, text=messageText, font=(fontStyle, fontSize, boldFont), fg=fieldFontColor, bg=backgroundColor)
    emailMessageLabel.grid(row=3, column=0)

    emailMessageEntry = Text(sendEmailWindow, font=(fontStyle, fontSize), fg=fontColor, height=5)
    emailMessageEntry.grid(row=4, column=0)

    def sendEmail():
        receiverEmail = receiverEmailEntry.get()
        message = emailMessageEntry.get(1.0, END)
        senderEmail = customerDetailsEntryList[2].get()
        senderPassword = billMenuEntryList[6].get()
        
        if senderEmail == '':
            messagebox.showerror(errorText, senderEmailIdTextEmptyMessage)
        elif senderPassword == '':
            messagebox.showerror(errorText, senderEmailKeyTextEmptyMessage)
        elif receiverEmail == '':
            messagebox.showerror(errorText, receiverEmailIdTextEmptyMessage)
        elif message == '':
            messagebox.showerror(errorText, emailContentEmptyMessage)
        else:
            try:
                server = smtplib.SMTP(emailSmtp, emailSmtpPort)
                server.starttls()
                server.login(senderEmail, senderPassword)
                server.sendmail(senderEmail, receiverEmail, message)
                server.quit()
                messagebox.showinfo(successText, "Email sent successfully")
                sendEmailWindow.destroy()
            except Exception as e:
                messagebox.showerror(errorText, somethingWentWrongMessage)
                print(e)

    sendButton = Button(sendEmailWindow, text="Send", font=(fontStyle, fontSize, boldFont), fg=fieldFontColor, bg=backgroundColor, command=sendEmail)
    sendButton.grid(row=5, column=0)
    
# Run the app
root = Tk()
root.title(headingLabelTitle)
root.geometry("800x600")
root.config(bg=backgroundColor)
root.mainloop()
