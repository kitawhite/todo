import datetime
import sqlite3

conn = sqlite3.connect("todo.db")
cur = conn.cursor()

# A task should have
# 0. Task ID (INTEGER)
# 1. Task date (TEXT)
# 2. Task details (TEXT)
# 3. Task isDone (TEXT)
# 4. Task timeAdded, in 24h clock (string, but we're gonna use the datetime lib to help us here)
# 5. Task lastUpdated, in date (string, also using datetime lib)

cur.execute("""CREATE TABLE if NOT EXISTS todotable(ID INT, Date TEXT, Details TEXT, isDone TEXT, timeAdded TEXT, lastUpdated TEXT)""")
conn.commit()

# res = cur.execute("""SELECT name FROM sqlite_master""")
# print(res.fetchone())

# res = cur.execute("""SELECT * FROM todotable""")
# print(res.fetchall())
# conn.commit()

# A todo list should have a few functions.

# 1. The ability to log in new entries
# 2. The ability to update entries
# 3. The ability to find entries
# Basially CRUD. Create, Read, Update, Delete

month_dict = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

id_array = []

class Entry:

    def __init__(self, id = 0, date = "", details = "", isDone = "", timeAdded = "", lastUpdated = ""):
        self.id = id
        self.date = date
        self.details = details
        self.isDone = isDone
        self.timeAdded = timeAdded
        self.lastUpdated = lastUpdated

def greeting():
    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    date = datetime.date.today()
    day = weekday[datetime.date.weekday(date)]
    print(f"\nToday is {date}, {day}")

def presentChoices():
    print(f"What would you like to do today?\n")
    while True:
        try:
            print("1. Create a task")
            print("2. View tasks")
            print("3. Update tasks")
            print("4. Exit")
            choice = int(input(f"Please type in the number corresponding to your choice: "))
            print("\n")
            if choice > 0 and choice < 5:
                return choice
            else:
                print("Please pick a number from 1 to 4\n")

        except ValueError:
            print("\n")
            print("Please pick a number from 1 to 4\n")
            
def createTask():
    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    id = getID()
    updateID(id)
    date = f"{datetime.date.today()}, {weekday[datetime.date.weekday(datetime.date.today())]}"
    details =  str(input(f"Please enter task details: \n >"))
    isDone = "False"
    timeAdded = str(datetime.datetime.now().strftime("%H:%M:%S"))
    lastUpdated = "NULL"
    task = Entry(id, date, details, isDone, timeAdded, lastUpdated)

    data = (task.id, task.date, task.details, task.isDone, task.timeAdded, task.lastUpdated)

    cur.execute(f"""INSERT INTO todotable(ID, Date, Details, isDone, timeAdded, lastUpdated) VALUES (?, ?, ?, ?, ?, ?)""", data)
    conn.commit()

    print()

    main_menu()

def viewTask():
    for row in cur.execute("SELECT * FROM todotable"):
        print(row)

def updateTask():
    # Find task by date
    # Find task by ID
    # Find task by description
    # Show all tasks
    find_task(find_task_option())

def findYear():

     while True:
    # Find task by date
        try:
            year = int(input("Please enter the year. Type '0' to skip\n"))
            if year < 0:
                print("Please key in a valid year")
            else:
                return year
        except ValueError:
            print("Please key in a valid year")

def findMonth():

    while True:
        try:
            month = int(input("Please enter the month in numbers (January is 1, February is 2, etc...). Type '0' to skip\n"))
            if month > 12:
                print("Please enter an integer from 1 to 12")
            else:
                return month
        except ValueError:
            print("Please key in a valid month")

def findDay(month):

    while True:
        try:
            day = int(input("Please enter the day in numbers (1st of the month is 1, 2nd is 2, etc...). Type '0' to skip\n"))
            if month ==  0:
                return day
            
            if day > month_dict[month] and month > 0 and month < 13:
                    print(f"There are only at most {month_dict[month]} days in that month!")
            else:
                return day
        except ValueError:
            print("Please key in a valid day")

def findID():
        
    while True:
        try:
            id_picked = int(input("Please choose the task ID\n"))
            #if id_picked not in id_array:
            #    print(f"Task ID = {id_picked} does not exist\n")
            #else:
            return id_picked
        except ValueError:
            print("Invalid ID")

def editOptions(id):

    while True:
        print("1. Update details")
        print(f"2. Delete task ID = {id}")
        print("3. exit")
        print()
        try:
            choice_chosen = int(input("Please key in the option number:\n"))
            if choice_chosen < 1 or choice_chosen > 3:
                print("Please enter a number from 1 to 3\n")
            else:
                return choice_chosen
        except ValueError:
            print("Please enter a number from 1 to 3\n")

def find_task(choice):
    if choice == 1:
        year = findYear()
        month = findMonth()
        day = findDay(month)

        if year == 0:
            inputyear = "%"
        else:
            inputyear = f"{year}"

        if month == 0:
            inputmonth = "%"
        else:
            inputmonth = str(month).zfill(2)

        if day == 0:
            inputday = "%"
        else:
            inputday = str(day).zfill(2)    

        query = f"""SELECT * FROM todotable WHERE Date LIKE ?"""
        for row in cur.execute(query, (f"{inputyear}-{inputmonth}-{inputday}%",)):
            print(row)

        # Select by ID. I think this should be a separate function
        print()
        id_picked = findID()
        print()

        print("Would you like to\n")

        choice_chosen = editOptions(id_picked)

        if choice_chosen == 1:
            updateDetails(id_picked)
            print("Updated\n")
        elif choice_chosen == 2:
            deleteEntry(id_picked)
            print("deleted\n")
        else:
            print("Exiting\n")
            return

        

    elif choice == 2:
        # Find task by ID
        print()
        id_picked = findID()
        print()
        print("Would you like to\n")

        choice_chosen = editOptions(id_picked)

        if choice_chosen == 1:
            updateDetails(id_picked)
            print("Updated\n")
        elif choice_chosen == 2:
            deleteEntry(id_picked)
            print("deleted\n")
        else:
            print("Exiting\n")
            return
        
    elif choice == 3:
        # Find task by description
        description = findDescription()
        print()
        descriptionArray = descriptionMatcher(description)
        if not descriptionArray[0]:
            print("No entries match the provided description")
        else:
            for i in descriptionArray:
                print(i)

        print()
        id_picked = findID()
        print()
        print("Would you like to\n")

        choice_chosen = editOptions(id_picked)

        if choice_chosen == 1:
            updateDetails(id_picked)
            print("Updated\n")
        elif choice_chosen == 2:
            deleteEntry(id_picked)
            print("deleted\n")
        else:
            print("Exiting\n")
            return
        
    else:
        # Show all tasks
        for row in cur.execute("""SELECT * FROM todotable"""):
            print(row)

        print()
        id_picked = findID()
        print()
        print("Would you like to\n")

        choice_chosen = editOptions(id_picked)

        if choice_chosen == 1:
            updateDetails(id_picked)
            print("Updated\n")
        elif choice_chosen == 2:
            deleteEntry(id_picked)
            print("deleted\n")
        else:
            print("Exiting\n")
            return

def descriptionMatcher(s):
    array = []
    query = f"""SELECT * FROM todotable WHERE Details LIKE '%{s}%'"""
    for row in cur.execute(query):
        array.append(row)
    return array

def findDescription():
    while True:
        try:
            description = str(input("Please enter the description of the task in here:\n"))
            return description
        except ValueError:
            print("Invalid description")

def newDetails():
    while True:
        try:
            details = str(input("Please enter in the new updated details here:\n"))
            return details
        except ValueError:
            print("Invalid entry")

def updateDetails(id):
    new_details = newDetails()
    query = f"""UPDATE todotable SET Details = ? WHERE ID = ?"""
    cur.execute(query, (new_details, id))
    conn.commit()

def deleteEntry(id):
    query = f"""DELETE FROM todotable WHERE id = ?"""
    cur.execute(query, (id, ))
    conn.commit()

def find_task_option():
    print("How would you like to find your task?\n")
    while True:
        try:
            print("1. Find task by date")
            print("2. Find task by ID")
            print("3. Find task by description")
            print("4. Show al tasks")
            choice = int(input(f"Please type in the number corresponding to your choice: "))
            print("\n")
            if choice > 0 and choice < 5:
                return choice
            else:
                print("Please pick a number from 1 to 4\n")

        except ValueError:
            print("\n")
            print("Please pick a number from 1 to 4\n")

def getID():
    try:
        file = open('id.txt', 'r')
        try:
            content = int(file.read())
            file.close()
            return content
        except ValueError:
            file.close()
            file = open('id.txt', 'w')
            file.write('0')
            file.close()
            return 0
    except FileNotFoundError:
        file = open('id.txt', 'w')
        file.write('0')
        file.close()
        return getID()
        
def updateID(ID):
    file = open('id.txt', 'w')
    file.write(f"{ID + 1}")
    file.close()

def main_menu():
    option = presentChoices()
    print()
    if option == 1:
        createTask()
    elif option == 2:
        viewTask()
    elif option == 3:
        updateTask()
    else:
        pass
        
greeting()
main_menu()

conn.close()