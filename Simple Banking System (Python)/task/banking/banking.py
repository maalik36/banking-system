# Write your code here
import random
import sqlite3
conn = sqlite3.connect('card.s3db')
curr = conn.cursor()
curr.execute("""Create Table If not exists card(id Integer, number Text, pin Text, balance Integer Default 0)""")


decision = "1"
income = "2"
card_check = ""
pin_check = ""
def luhn(card_number):
    number = 0
    count = 0
    sum = 0
    list = []
    #[int(i) for i in str(card_number)]
    for i in card_number:
        list.append(int(i))
    while number < len(list):
        list[number] *= 2
        number += 2
    number = 0
    #print(list[number])
    while number < len(list):
        if list[number] > 9:
            list[number] -= 9
        number += 1
    count = 0
    print(list[8])
    for i in list:
        sum = sum + list[count]
        count += 1
    remains = sum % 10
    if sum % 10 == 0:
       return True
    else:
       return False

class card:

    def __init__(self):
        self.card_number = {1: 4, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        number = 7
        self.full_card_number = ""
        sum = 0
        save = {}
        
        while number <= 15:
            
            unique = random.randint(0, 9)
            temp_dict = {number: unique}
            self.card_number.update(temp_dict)
            number += 1
        save.update(self.card_number)
        number = 1
        while number <= len(self.card_number) + 1:
            self.card_number[number]*= 2
            number+=2
        for i in self.card_number:
            if self.card_number[i] > 9:
                self.card_number[i]-= 9
        for i in self.card_number:
            sum = sum + self.card_number[i]
        remains = sum % 10
        if sum % 10 == 0:
            final = {16: 0}
            save.update(final)
        else:
            final = {16: (10 - remains)}
            save.update(final)
        self.card_number.update(save)
        for i in self.card_number:
            self.full_card_number += str(self.card_number[i])
        self.pin = random.randint(1000, 9999)
        self.id = random.randint(100, 999)
        curr.execute("""Insert into card (number, pin, balance)
         Values (?, ?, ?)""", (self.full_card_number, self.pin, 0))
        conn.commit()
        #curr.execute("""Select number, pin, balance from card""")
        #print(curr.fetchall())
        self.balance = 0

while decision != "0":
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    decision = input()
    if decision == "1":
        new_card = card()


        print("Your card has been created")
        print("Your card number:")
        print(new_card.full_card_number)
        print("Your card PIN:")
        print(new_card.pin)
    if decision == "2":
        print("Enter your card number:")
        new_card.full_card_number = input()
        print("Enter your PIN:")
        new_card.pin = input()
        curr.execute("""Select * from card where pin = ? and number = ?""", (new_card.pin, new_card.full_card_number))
        result = curr.fetchone()
        if result is None:
        #new_card.full_card_number = str(curr.fetchone())
        #new_card.full_card_number = new_card.full_card_number.strip("() , ''")
        #string_pin = str(new_card.pin)
        #curr.execute("""Select pin from card where number = ? and pin = ?""", (card_check, pin_check))
        #print(curr.fetchall())
        #string_pin = str(curr.fetchone())
        #string_pin = string_pin.strip("() , ''")
        #print(new_card.full_card_number)
        #print(string_pin)
        #if card_check != new_card.full_card_number or pin_check != string_pin:
            print("Wrong card number or PIN!")
        else:
            print("You have successfully logged in!")
            decision = "3"
            while decision != "5" or decision != "0":
                print("1. Balance")
                print("2. Add income")
                print("3. Do transfer")
                print("4. Close account")
                print("5. Log out")
                print("0. Exit")
                decision = input()
                if decision == "1":
                    print("Balance: " + str(new_card.balance))
                elif decision == "2":
                    print("Enter income:")
                    income = input()
                    new_card.balance = new_card.balance + int(income)
                    curr.execute("""Update card Set balance = balance + ? Where number = ?""", (int(income), new_card.full_card_number))
                    conn.commit()
                    print("Income was added!")
                elif decision == "3":
                    print("Transfer")
                    print("Enter card number: ")
                    other_card = input()

                    if other_card == new_card.full_card_number:
                        print("You can't transfer money to the same account!")
                    else:
                        check = luhn(other_card)
                        if check == False:
                            print("Probably you made a mistake in the card number. Please try again!")
                        else:
                            curr.execute("""Select * from card Where number = ?""", (other_card,))
                            check = curr.fetchone()
                            if check is None:
                                print("Such a card does not exist.")
                            else:
                                print("Enter how much money you want to transfer:")
                                transfer =int(input())
                                if transfer > new_card.balance:
                                    print("Not enough money!")
                                else:
                                    curr.execute("""Update card Set balance = balance - ? Where number = ?""", (transfer, new_card.full_card_number))
                                    curr.execute("""Update card Set balance = balance + ? Where number = ?""", (transfer, other_card))
                                    conn.commit()
                                    print("Success!")
                elif decision == "4":
                    curr.execute("""Delete from card where number = ?""", (new_card.full_card_number,))
                    conn.commit()
                    print("The account has been closed!")
                    break
                elif decision == "5":
                    print("You have successfully logged out!")
                elif decision == "0":
                    break
print("Bye!")
conn.close()