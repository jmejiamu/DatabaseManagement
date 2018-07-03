import pymysql.cursors
import time

try:
    userName = input(">>>User Name : ")
    password = input(">>>Password : ")

    connection = pymysql.connect(host="192.000.0.00",     #any IP or localhost
                                     user= userName,      #username
                                     password = password, #password
                                     db="employee",
                                     charset='utf8',
                                     cursorclass= pymysql.cursors.DictCursor
                                    )
    print("Connected....")
except pymysql.err.OperationalError as error:
    print("User name or password are incorrect!")
    print("Try again!")
    exit()

def menu ():

    menu = """
            * What would you like to do next *
            
            Enter the word 'QUIT' to get out
            0. Show menu            4. Choose a database
            1. Show data            5. To delete database
            2. Create a database    6. To add a new record
            3. Show databases       7. Update a table
    """

    print(menu)

menu()

def create():
    dbName = input("Database name : ")
    cursor = connection.cursor()
    sql = ("create database {}".format(dbName))
    cursor.execute(sql)
    data = cursor.fetchall()
    print(dbName," database created")

def showDatabase():

    cursor = connection.cursor()
    sql = ("show databases")
    cursor.execute(sql)
    data = cursor.fetchall()
    print(" -DATABASES- ")
    for row in data:
        print(row["Database"],"\n")

def useDataBase():
    try:
        cursor = connection.cursor()
        usedb = input("Choose a database you want to use : ")
        sql = ("use {}".format(usedb))
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)

        print("- Database Tables - ")
        sqltables = ("show tables")
        cursor.execute(sqltables)
        d = cursor.fetchall()
        print(d)
    except pymysql.err.InternalError as e:
        print(usedb," database does not exist!")
        print("Try the option 3 on the main 'menu',")
        print("to see the valid databases")
        time.sleep(5)
        menu()


def showDatabaseInfo():
    try:
        cursor = connection.cursor()
        whatDb = input("What table you want to take a look : ")
        # sql = ("select * from registration")
        sql = ("select * from {}".format(whatDb))
        cursor.execute(sql)
        data = cursor.fetchall()
        print("Id\tName\tE-mail\t\tDate Hired\tSalary ")
        for d in data:

            print(d["employee_id"],d["employee_name"],"\t",
                  d["email"],d["hire_date"],d["salary"])

    except pymysql.err.ProgrammingError as err:
        print(whatDb, " table is not on the database")
        print("Try the option 4 to choose a database")
    # update()
def addingRecord():
    try:
        while True:
            add = input("Do you want to add a new record [y/n]: ")
            if add.lower() == 'y':
                cursor = connection.cursor()
                empId= int(input("Employe Id : "))
                empName = input("Employee Name : ")
                email = input("E-mail : ")
                hireDate = input("Hired Date: (yyyy-dd-mm) ")
                salary = int(input("Employee Salary : "))
                sql = ("INSERT INTO info VALUES('{}' ,'{}', '{}', '{}', '{}')".format(empId, empName, email, hireDate, salary))
                cursor.execute(sql)
                #data = cursor.fetchall()
                connection.commit()
                #print(data)

            else:
                break
    except ValueError:
        print(empId,"Must be an integer")

def deleteDatabase():
    try:
        cursor = connection.cursor()
        delete = input("What database you want to delete: ")
        sql = ("drop database {}".format(delete))
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        print(delete, " was deleted.")
    except pymysql.err.InternalError as err:
        print(delete, " is not a valid database")
        print("Use option 3 to see valid database")

def update():
    try:
        tableName= input("table name : ")
        cursor = connection.cursor()
        sql = ('update {} set employee_name = "newRecord" '
               'where employee_id=124'.format(tableName))
        cursor.execute(sql)
        #data = cursor.fetchall()
        connection.commit()
        print(tableName," table updated!")
    except pymysql.err.ProgrammingError as error:
        print(tableName," table's does not exist!")
while True:
    option = input(">>")

    if option.lower() == "quit":
        break
    elif option =='0':
        menu()
    elif option == '1':
        showDatabaseInfo()
        continue
    elif option == '2':
        create()
        continue
    elif option == '3':
        showDatabase()
        continue
    elif option == '4':
        useDataBase()
        continue
    elif option == '5':
        deleteDatabase()
        continue
    elif option == '6':
        addingRecord()
        continue
    elif option == '7':
        update()
        continue
    else:
        print("{} is  not an option".format(option))
        print("Here is the Menu.")
        menu()