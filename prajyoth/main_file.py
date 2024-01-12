import sqlite3
import datetime

conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

while True:
  print("Select an choice:")
  print("1.Enter a new item")
  print("2.View expenses")
  choice = int(input())
  if choice == 1:
    date = input("Enter the date of expenses (DD_MM_YYYY): ")
    description = input("Enter the category of the expense: ")
    cur.execute("SELECT DISTINCT category FROM expenses")
    categories = cur.fetchall()
    print("Select a option by number:")
    for idx,category in enumerate(categories):
       print(f"{idx +1},{category[0]}")
    print(f"{len(categories) +1}.Create a new item")
    category_choice=int(input())
    if category_choice==len(categories)+1:
       category=input("enter the new item name: ")
    else:
       category=categories[category_choice-1][0]
    price=input("enter the price of item: ")
    cur.execute("INSERT INTO expenses (Date,description,category,price) VALUES (?,?,?,?)",(date,description,category,price))
    conn.commit()
  elif choice==2:
    print("Select an choice:")
    print("1.View all expenses")
    print("2.View monthly expenses")
    view_choice=int(input())
    if view_choice==1:
       cur.execute("SELECT*FROM expenses")
       expenses=cur.fetchall()
       for expense in expenses:
          print(expense)
    elif view_choice==2:
       month=input("enter the month (MM): ")
       year=input("enter the year (YYYY): ")
       cur.execute("""SELECT category,SUM(price) FROM expenses"
                   WHERE strftime('%m',Date)=? AND strftime('%Y',Date)=?
                   GROUP BY category""",(month,year))
       expenses=cur.fetchall()
       for expense in expenses:
          print(f"item:{expense[0]},Total:{expense[1]}")
    else:
       exit()
  else:
    exit()
  repeat = input("Would you like to do something else (yes/no)?\n")
  if repeat.lower() !="yes":
    break
conn.close()
bill=int(input("enter the amount of bill: "))
tip=int(input("enter the percentage of tip? 10,12,15: "))
people=int(input("number of people to split the bill in between1: "))
tip_as_percentage=tip/100
total_tip=bill*tip_as_percentage
total_bill=bill+total_tip
bill_per_person=total_bill/people
final_amount=round(bill_per_person,2)
print(f"each person has to pay:Rs {final_amount}")