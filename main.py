import random
import pyfiglet

balance = 10
companies = []
lucklevel = 1
luckmin = (lucklevel/50) + .5
luckmax = lucklevel * 1.5
maxlucklevel = 10
luckcost = (lucklevel**3) * lucklevel
daycount = 0
loans = []
loanlevel = 0
maxloanlevel = 5
loancost = 25
loanoptions = ["1: Tiny Loan    $50      15 days",
               "2: Small Loan   $100     30 days",
               "3: Mid Loan     $200     45 days",
               "4: Big Loan     $500     60 days", 
               "5: Huge Loan    $1,000   75 days"]

result = pyfiglet.figlet_format("DAY " + str(daycount))
print(result)

def create_company():
    global balance
    global companies

    name = input("\nCompany Name: ")
    if any(name in sublist for sublist in companies):
        print("ERROR: Company Name Already Taken")
        create_company()

    if name == "e" or name == "esc" or name == "escape":
        gameloop()

    investment = input(f"Balance: ${balance:,} \nInvest Amount: ")
    if investment == "e" or investment == "esc" or investment == "escape":
        gameloop()
    else:
        investment = int(investment)

    if investment > balance:
        print("ERROR: Investment Bigger than Balance")
        create_company()
    if investment <= 0:
        print("ERROR: Invalid Investment Amount")
        create_company()
    
    balance -= investment
    companies.append([name, investment])
    print(name + " Company Created!\n")

def edit_company(compnum):
    global balance
    global companies
    name = companies[compnum - 1][0]
    investment = companies[compnum - 1][1]

    print("Editing " + name + "\nInvestment: " + str(investment))
    pick = input("1: Deposit\n2: Withdraw\n3: Delete\n")
    if pick == "e" or pick == "esc" or pick == "escape":
        print("")
        gameloop()

    elif pick == "1":
        add = input(f"Balance: ${balance:,} \nDeposist Amount: ")
        if add == "e" or add == "esc" or add == "escape":
            print("")
            gameloop()
        elif int(add) > balance or int(add) < 0:
            print("ERROR: Invalid Amount")
            edit_company(compnum)
        companies[compnum - 1][1] += int(add)
        balance -= int(add)
    elif pick == "2":
        sub = input(f"Balance: ${balance:,}\nWithdraw Amount: ")
        if sub == "e" or sub == "esc" or sub == "escape":
            print("")
            gameloop()
        elif int(sub) > investment or int(sub) < 0:
            print("ERROR: Invalid Amount")
            edit_company(compnum)
        companies[compnum - 1][1] -= int(sub)
        balance += int(sub)
    elif pick == "3":
        confirm = input("Do you want to permanently delete " + name + "? You will lose $" + str(investment) + ". (Y/N): ")
        if confirm == "Y" or confirm == "y":
            del companies[compnum - 1]
            print(name + " Deleted\n")

def upgrades():
    global balance
    global luckmin
    global luckmax
    global lucklevel
    global loanlevel
    global maxlucklevel
    global luckcost
    global maxloanlevel
    global loancost
    
    print(f"\nBalance: ${balance:,}")
    pick = input("Upgrades: \n1: Luck - " + str(lucklevel) + " - $" + str(luckcost) + "\n2: Loans - " + str(loanlevel) + " - $" + str(loancost) + "\n")
    if pick == "e" or pick == "esc" or pick == "escape":
        print("")
        gameloop()
    elif pick == "1":
        if lucklevel == "MAX" or lucklevel >= maxlucklevel:
            print("ERROR: Max Luck Level Reached")
            upgrades()
        elif balance < luckcost:
            print("ERROR: Insufficient Funds")
            upgrades()

        lucklevel += 1
        balance -= luckcost
        luckcost = (lucklevel**3) * lucklevel
        if lucklevel == maxlucklevel:
            lucklevel = "MAX"
            luckcost = "N/A"
    
    elif pick == "2":
        if loanlevel == "MAX" or loanlevel >= maxloanlevel:
            print("ERROR: Max Loan Level Reached")
            upgrades()
        elif balance < loancost:
            print("ERROR: Insufficient Funds")
            upgrades()
        
        loanlevel += 1
        balance -= loancost
        loancost = (loanlevel * 100)
        if loanlevel == maxloanlevel:
            loanlevel = "MAX"
            loancost = "N/A"

    upgrades()

def loanmenu():
    global balance
    global daycount
    global loans
    global loanlevel
    global loanoptions

    pick = input("\nLoan Options:\n1: Start Loan\n2: Pay a Loan\n3: See Current Loan\n")    
    if pick == "e" or pick == "esc" or pick == "escape":
        print("")
        gameloop()
    elif pick == "1":
        if len(loans) >= loanlevel:
            print("ERROR: Selection Locked")
            loanmenu()

        print("\nLoan Amounts: ")
        for option in range(loanlevel):
            print(loanoptions[option])
        pick = input()
        
        if pick == "e" or pick == "esc" or pick == "escape":
            print("")
            gameloop()
        elif pick == "1":
            loans.append(["Tiny", 50, 15])
            balance += 50
        elif pick == "2" and loanlevel >= 2:
            loans.append(["Small", 100, 30])
            balance += 100
        elif pick == "3" and loanlevel >= 3:
            loans.append(["Mid", 200, 45])
            balance += 200
        elif pick == "4" and loanlevel >= 4:
            loans.append(["Big", 500, 60])
            balance += 500
        elif pick == "5" and loanlevel == "MAX":
            loans.append(["Huge", 1000, 75])
            balance += 1000
        else:
            print("ERROR: Invalid Selection")
            loanmenu()

        loanname = loans[(len(loans) - 1)][0]
        loandebt = loans[(len(loans) - 1)][1]
        loandays = loans[(len(loans) - 1)][2]
        print(loanname + f" Loan Created!\nYou will have to pay ${loandebt:,} in " + str(loandays) + " days\n")

    elif pick == "2":
        print("Select a Loan to Pay:")
        for loannum in range(len(loans)):
            print(str(loannum + 1) + ": " + str(loans[loannum][0]))
        pick = input()
        if pick == "e" or pick == "esc" or pick == "escape":
            print("")
            gameloop()

        debt = loans[int(pick) - 1][1]
        confirm = input("Do you want to pay $" + str(debt) + "? (Y/N) ")
        if confirm == "Y" or confirm == "y":
            if balance < debt:
                print("ERROR: Insufficient Funds")
                loanmenu()
            balance -= debt
            del loans[int(pick) - 1]
            print(f"New Balance: ${balance:,}")

    elif pick == "3":
        if loans == []:
            print("No Current Loan")
        for loan in loans:
            print("Loan: " + loan[0] + " | Amount: $" + str(loan[1]) + " | Due: " + str(loan[2]) + " days")
        loanmenu()
def end_day():
    global balance
    global companies
    global luckmin
    global luckmax
    global daycount
    global loans

    multiplier = 1
    for company in companies:
        multiplier += .01
    print(multiplier)

    for company in range(len(companies)):
        name = companies[company][0]
        investment = companies[company][1]

        newinvestment = round(multiplier * (investment*random.uniform(luckmin, luckmax)), 2)
        print(name + f": {newinvestment:,}")
        companies[company][1] = newinvestment

    daycount += 1
    print(pyfiglet.figlet_format(f"DAY {daycount:,}"))

    for loannum in range(len(loans)):
        loan = loans[loannum]
        loan[2] -= 1
        if loan[2] <= 5 and loan[2] > 0:
            print("$" + str(loan[1]) + " due in " + str(loan[2]) + " days!")
        elif loan[2] == 0:
            print("ALERT: You missed your due for a " + str(loan[0]) + " Loan. You've been charged $" + str(loan[1] * 1.25))
            balance -= loan[1] * 1.25
            print(f"New Balance: ${balance:,}")
            del loans[loannum]

def gameloop():
    global balance
    global companies

    pick = input("1: End Day\n2: Start Company\n3: Check Balance\n4: See Companies\n5: Edit Company\n6: Upgrades\n7: Loans\n")
    if pick == "1":
        end_day()
    elif pick =="2":
        create_company()
    elif pick == "3":
        print(f"\nBalance: ${balance:,}\n")
    elif pick == "4":
        print("")
        for info in range(len(companies)):
            print(str(companies[info][0]) + " with $" + str(companies[info][1]) + " invested")
            print("")
    elif pick == "5":
        print("\nSelect Company to Edit")
        for company in range(len(companies)):
            print(str(company + 1) + ": " + companies[company][0])
        comppick = input()
        if comppick == "e" or comppick == "esc" or comppick == "escape":
            print("")
            gameloop()
        edit_company(int(comppick))
    elif pick == "6":
        upgrades()
    elif pick == "7":
        loanmenu()
    else:
        print("ERROR: Invalid Selection")
    
    gameloop()

gameloop()