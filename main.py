import random

balance = 10
companies = []
lucklevel = 1
luckmin = (lucklevel/50) + .5
luckmax = lucklevel * 1.5

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
        if add > balance or add < 0:
            print("ERROR: Invalid Amount")
            edit_company(compnum)
        companies[compnum - 1][1] += add
        balance -= add
    elif pick == 2:
        sub = int(input("Balance: $" + str(balance) + "\nWithdraw Amount: "))
        if sub > investment or sub < 0:
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
        print("MAX: " + str(lucklevel * 1.5) + " MIN: " + str((lucklevel/50) + .5))

    upgrades()


def end_day():
    global balance
    global companies
    global luckmin
    global luckmax

    for company in range(len(companies)):
        name = companies[company][0]
        investment = companies[company][1]

        newinvestment = round(investment*random.uniform(luckmin, luckmax), 2)
        print(name + ": " + str(newinvestment))
        companies[company][1] = newinvestment

def gameloop():
    global balance
    global companies

    pick = input("1: Start Business\n2: Check Balance\n3: See Companies\n4: Edit Company\n5: Upgrades\n6: End Day\n")
    if pick =="1":
        create_company()
    elif pick == "2":
        print("Balance: $" + str(balance))
    elif pick == "3":
        for info in range(len(companies)):
            print(str(companies[info][0]) + " with $" + str(companies[info][1]) + " invested")
    elif pick == "4":
        print("Select Company to Edit")
        for company in range(len(companies)):
            print(str(company + 1) + ": " + companies[company][0])
        comppick = int(input())
        edit_company(comppick)
    elif pick == "5":
        upgrades()
    elif pick == "6":
        end_day()
    else:
        print("ERROR: Invalid Selection")
    
    gameloop()

gameloop()