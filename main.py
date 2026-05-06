import random
import pyfiglet

balance = 10
companies = []
lucklevel = 1
luckmin = (lucklevel/50) + .75
luckmax = lucklevel * 1.5
daycount = 0
loans = []

result = pyfiglet.figlet_format("DAY " + str(daycount))
print(result)

def create_company():
    global balance
    global companies

    name = input("Company Name: ")
    if any(name in sublist for sublist in companies):
        print("ERROR: Company Name Already Taken")
        create_company()

    if name == "e" or name == "esc" or name == "escape":
        gameloop()

    investment = input("Balance: $" + str(balance) + "\nInvest Amount: ")
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
    print(name + " Company Created!")

def edit_company(compnum):
    global balance
    global companies
    name = companies[compnum - 1][0]
    investment = companies[compnum - 1][1]

    print("Editing " + name + "\nInvestment: " + str(investment))
    pick = int(input("1: Deposit\n2: Withdraw\n3: Delete\n"))
    if pick == "e" or pick == "esc" or pick == "escape":
        gameloop()

    elif pick == 1:
        add = int(input("Balance: $" + str(balance) + "\nDeposist Amount: "))
        if add == "e" or add == "esc" or add == "escape":
            gameloop()
        elif add > balance or add < 0:
            print("ERROR: Invalid Amount")
            edit_company(compnum)
        companies[compnum - 1][1] += add
        balance -= add
    elif pick == 2:
        sub = int(input("Balance: $" + str(balance) + "\nWithdraw Amount: "))
        if sub == "e" or sub == "esc" or sub == "escape":
            gameloop()
        elif sub > investment or sub < 0:
            print("ERROR: Invalid Amount")
            edit_company(compnum)
        companies[compnum - 1][1] -= sub
        balance += sub
    elif pick == 3:
        confirm = input("Do you want to permanently delete " + name + "? You will lose $" + str(investment) + ". (Y/N): ")
        if confirm == "Y" or confirm == "y":
            del companies[compnum - 1]
            print(name + " Deleted")

def upgrades():
    global balance
    global luckmin
    global luckmax
    global lucklevel

    print("Balance: $" + str(balance))
    pick = input("Upgrades: \n1: Luck - " + str(lucklevel) + " - $" + str(lucklevel**2) + "\n")
    if pick == "e" or pick == "esc" or pick == "escape":
        gameloop()
    elif pick == "1":
        if balance < lucklevel**2:
            print("ERROR: Insufficient Funds")
            upgrades()
        balance -= lucklevel**2
        lucklevel += 1
        print("MAX: " + str(lucklevel * 1.5) + " MIN: " + str((lucklevel/50) + .75))

    upgrades()

def loanmenu():
    global balance
    global daycount
    global loans

    pick = input("Loan Options:\n1: Start Loan\n2: Pay a Loan\n3: See Current Loans\n")
    if pick == "e" or pick == "esc" or pick == "escape":
        gameloop()
    elif pick == "1":
        pick = input("Loan Amounts: \n1: Tiny Loan    $50    15 days\n2: Small Loan   $100   30 days\n3: Mid Loan     $200   45 days\n4: Big Loan     $500   60 days\n5: Huge Loan    $1000  75 days\n")
        if pick == "e" or pick == "esc" or pick == "escape":
            gameloop()
        elif pick == "1":
            loans.append(["Tiny", 50, 15])
            balance += 50
        elif pick == "2":
            loans.append(["Small", 100, 30])
            balance += 100
        elif pick == "3":
            loans.append(["Mid", 200, 45])
            balance += 200
        elif pick == "4":
            loans.append(["Big", 500, 60])
            balance += 500
        elif pick == "5":
            loans.append(["Huge", 1000, 75])
            balance += 1000

        loanname = loans[(len(loans) - 1)][0]
        loandebt = loans[(len(loans) - 1)][1]
        loandays = loans[(len(loans) - 1)][2]
        print(loanname + " Loan Created!\nYou will have to pay $" + str(loandebt) + " in " + str(loandays) + " days")

    elif pick == "2":
        print("Select a Loan to Pay:")
        loanamounts = []
        for loannum in range(len(loans)):
            print(str(loannum + 1) + ": " + str(loans[loannum][0]))
        pick = input()
        if pick == "e" or pick == "esc" or pick == "escape":
            gameloop()
        else:
            debt = loans[int(pick) - 1][1]
            confirm = input("Do you want to pay $" + str(debt) + "? (Y/N) ")
            if confirm == "Y" or confirm == "y":
                if balance < debt:
                    print("ERROR: Insufficient Funds")
                    loanmenu()
                balance -= debt
                del loans[int(pick) - 1]
                print("New Balance: $" + str(balance))

    elif pick == "3":
        if loans == []:
            print("No Current Loans")
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

    for company in range(len(companies)):
        name = companies[company][0]
        investment = companies[company][1]

        newinvestment = round(investment*random.uniform(luckmin, luckmax), 2)
        print(name + ": " + str(newinvestment))
        companies[company][1] = newinvestment

    daycount += 1
    result = pyfiglet.figlet_format("DAY " + str(daycount))
    print(result)

    for loannum in range(len(loans)):
        loan = loans[loannum]
        loan[2] -= 1
        if loan[2] <= 5 and loan[2] > 0:
            print("$" + str(loan[1]) + " due in " + str(loan[2]) + " days!")
        elif loan[2] == 0:
            print("ALERT: You missed your due for a " + str(loan[0]) + " Loan. You've been charged $" + str(loan[1] * 1.25))
            balance -= loan[1] * 1.25
            print("New Balance: $" + str(balance))
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
        print("Balance: $" + str(balance))
    elif pick == "4":
        for info in range(len(companies)):
            print(str(companies[info][0]) + " with $" + str(companies[info][1]) + " invested")
    elif pick == "5":
        print("Select Company to Edit")
        for company in range(len(companies)):
            print(str(company + 1) + ": " + companies[company][0])
        comppick = int(input())
        edit_company(comppick)
    elif pick == "6":
        upgrades()
    elif pick == "7":
        loanmenu()
    else:
        print("ERROR: Invalid Selection")
    
    gameloop()

gameloop()