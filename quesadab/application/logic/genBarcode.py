from datetime import date

def genBarcode(lstBcode):
    """Takes a barcode and creates and returns the next one
        Input: Str in the form '16100024'
        Output: Str in the form '16100025"""
    year = str(date.today().year)[2:4] #Gets the current year
    month = str(date.today().month) #Gets the current date

    if len(month) < 2:
	#if month is less then 10 add a 0 to the front to make it match in len
	month = '0' + month

    if lstBcode[0:2] == year: #If the last barcode was made in current year
        #The year is correct
	if lstBcode[2:4] == month: #If the last barcode was made in current month
	    #The month is also correct so we increment the count
            newbar = year + month + increment(lstBcode[4:8])
        else:
	    newbar = year + month + "0000"
    else:
        newbar = year + month +"0000"
    return newbar

def increment(lstFour):
    """Takes a four digit string and increments it by 1
        Input: Str of len(4) ex: 0024
        Output: Str of the len(4) ex: 0025"""
    #Declares Variables
    incrementedNum = ""
    incremented = False
    #Iterate over number given in reverse order
    for num in reversed(lstFour):
        if num != '9' and incremented == False:
            #If number can be incremented and has not been incremented yet
            incrementedNum = str(int(num)+1) + incrementedNum
            incremented = True
        elif num == '9' and incremented == False:
            #If number is 9 and next number needs to be incremented
            incrementedNum = '0' + incrementedNum
        else:
            #Number already incremented
            incrementedNum = num + incrementedNum
    return incrementedNum
