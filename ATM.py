import pandas as pd
import numpy as np
import time
import pickle

df = pd.read_csv("C:/Users/Matt/Documents/Python/CSV/Accounts.csv", index_col='Account_Holderi')
print(df)

def end():
    name = pickle.load(open("name.dat","rb"))[0]
    print("Do you require anymore services today? (Y/N)")
    endchoice = input().capitalize()
    if endchoice == "Y":
        service()
    elif endchoice == "N":
        print("Thank you for using Bank of Python " + name + ", your final balance is £" + str(df.loc[name,'Account_Balance']) + ".")
        df.to_csv('C:/Users/Matt/Documents/Python/CSV/Accounts.csv')
    else:
        print("Wrong press detected, please try again.")
        end()

def withdraw():
    name = pickle.load(open("name.dat","rb"))[0]
    print("Hello " + name + ", much do you want to withdraw?")
    withdraw = int(input())
    print("Are you sure you want to withdraw £" + str(withdraw) + "? (Y/N)")
    choice1 = input().capitalize()
    if choice1 == "Y" and withdraw > 0 and withdraw <= df.loc[name,'Account_Balance']:
        print("Here's £" + str(withdraw))
        df.loc[name,'Account_Balance'] = df.loc[name,'Account_Balance'] - withdraw
        print("You have £" +str(df.loc[name,'Account_Balance']) + " left.")
        time.sleep(1)
        end()
    elif choice1 == "N":
        end()
    elif choice1 == "Y" and withdraw <= 0:
        print("Please submit a suitable figure! One that is greater than 0.")
        reset()
    elif choice1 == "Y" and withdraw > df.loc[name,'Account_Balance']: 
        print("You have insufficient funds! Please enter an amount you can actually afford.")
        end()
    else:
        print("Invalid output detected, please try again.")
        time.sleep(1)
        reset()

def reset():
    withdraw()

def pinchange():
    name = pickle.load(open("name.dat","rb"))[0]
    print("What would you like to change your pin number to? (Must be 4 digits)")
    newpin = input()
    if newpin.isnumeric() == True and len(newpin) == 4:
        print("Please confirm the number you want to change your pin to:")
        conf_newpin = input()
        if conf_newpin == newpin:
            print("Pin successfully changed")
            df.loc[name,'Pin_Number'] = newpin
            end()
        else: 
            print("Pins didn't match, please try again.")
            pinchange()
    else:
        print("Please submit a suitable pin number.")
        pinchange()

def checkbal():
    name = pickle.load(open("name.dat","rb"))[0]
    print("Hello " + name + ", your account balance is £" + str(df.loc[name,'Account_Balance']) + ".")
    end()


def service():
    name = pickle.load(open("name.dat","rb"))[0]
    print("Hi " + name + ", what service do you require today?")
    print("Do you want to withdraw funds (1), change your pin (2) or check your balance (3)?")
    service_option = int(input())
    try:
        if service_option == 1: 
            withdraw()
        elif service_option == 2:
            pinchange()
        elif service_option == 3:
            checkbal()
        else:
            print("Invalid number submitted, please try again.")
            time.sleep(2)
            service()
    except ValueError:
        print("Oops! Looks like you tried submitting an unrecognised input.")
        time.sleep(2)
        print("Please try again.")
        service()

def atm():
    print("Welcome to the Python Bank")
    time.sleep(1)
    print("What is your name?")
    name = input().capitalize()
    named = [name]
    pickle.dump(named, open("name.dat", "wb"))
    if np.any(df['Account_Holder'] == name) == False:
        print(name + " is not recognised, please start again.")
        time.sleep(2)
        atm()
    else:
        print("Please enter your pin number")
        inputs = 0
        while inputs < 3:
            try:
                pintry = int(input())
                if pintry == df.loc[name,'Pin_Number']:
                    service()
                else:
                    print("Pin enterred is incorrect, please try again.")
                    inputs += 1
            except ValueError:
                print("Oops! Looks like you tried submitting an invalid pin number!")
                time.sleep(1)
                print("Please try a different pin number.")
        else:
            print("Too many tries, your account has been locked")

print(atm())
df.to_csv('C:/Users/Matt/Documents/Python/CSV/Accounts.csv')