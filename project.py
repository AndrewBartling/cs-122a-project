import sys
import mysql.connector
import csv
import os


def connect_to_database():
    try:
        # Connect to the MySQL server
        # connect to gradescope autograder down below

        connection = mysql.connector.connect(user='test', password='password', database="cs122a")


        # connection = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="zippy",
        #     database ="cs122a",
         
        # )
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)


def add_user(UCINetID, First, Middle, Last,connection):
    user_query = "INSERT INTO Users (UCINetID, Firstname, Middlename, Lastname) VALUES (%s, %s, %s, %s);"
    cursor = connection.cursor()

    cursor.execute(user_query, (UCINetID, First, Middle, Last))

    # Committing the changes
    connection.commit()
    cursor.close()

def add_email(UCINetID, Email,connection):
    email_query = "INSERT INTO UserEmail (UCINetID, Email) VALUES (%s, %s);"
    
    cursor = connection.cursor()

    cursor.execute(email_query, (UCINetID, Email))

    # Committing the changes
    connection.commit()
    cursor.close()

def add_student(UCINetID,connection):
    student_query = "INSERT INTO Students (UCINetID) VALUES (%s);"
    cursor = connection.cursor()

    cursor.execute(student_query, (UCINetID,))

    # Committing the changes
    connection.commit()
    cursor.close()
   
def add_admins(UCINetID, connection):
    admins_query = "INSERT INTO Administrators (UCINetID) VALUES (%s);"
    cursor = connection.cursor()

    cursor.execute(admins_query, (UCINetID,))

    # Committing the changes
    connection.commit()
    cursor.close()

def add_course(CourseID,Title,Quarter,connection):
    course_query = "INSERT INTO Courses (CourseID, Title, Quarter) VALUES (%s, %s, %s);"
    cursor = connection.cursor()

    cursor.execute(course_query, (CourseID, Title, Quarter))

    # Committing the changes
    connection.commit()
    cursor.close()

def add_project(ProjectID,Name,Description,CourseID,connection):
    
    course_query = "INSERT INTO Projects (ProjectID, Name, Description, CourseID) VALUES (%s, %s, %s, %s);"
    cursor = connection.cursor()

    cursor.execute(course_query, (ProjectID, Name, Description, CourseID))

    # Committing the changes
    connection.commit()
    cursor.close()

def add_machine(MachineID ,Hostname, IPAddress ,OperationalStatus,Location,connection):
    machine_query = "INSERT INTO Machines (MachineID, Hostname, IPAddress, OperationalStatus, Location) VALUES (%s, %s, %s, %s, %s);"
    cursor = connection.cursor()

    cursor.execute(machine_query, (MachineID, Hostname, IPAddress, OperationalStatus, Location))

    # Committing the changes
    connection.commit()
    cursor.close()

def add_use(ProjectID,StudentUCINetID,MachineID,StartDate,EndDate,connection):
    use_query = "INSERT INTO StudentUseMachinesInProject (ProjectID ,StudentUCINetID ,MachineID ,StartDate ,EndDate) VALUES (%s, %s, %s, %s, %s)"
    cursor = connection.cursor()

    cursor.execute(use_query, (ProjectID, StudentUCINetID, MachineID, StartDate, EndDate))

    # Committing the changes
    connection.commit()
    cursor.close()

def add_mange(UCINetID,MachineID,connection):
    manage_query = "INSERT INTO AdministratorManageMachines (AdministratorUCINetID, MachineID) VALUES (%s, %s);"
    cursor = connection.cursor()

    cursor.execute(manage_query, (UCINetID, MachineID))

    # Committing the changes
    connection.commit()
    cursor.close()

def get_table_size(table_name,connection):

    cursor = connection.cursor()

    cursor.execute("SELECT count(*) FROM {}".format(table_name))

    size = cursor.fetchone()[0]

    cursor.close()

    return size

def get_table_contents(table_name, connection):
    cursor = connection.cursor()
 
    query = "SELECT * FROM {}".format(table_name)
    
    cursor.execute(query)
    
    rows = cursor.fetchall()
    # it seems liken when fetchall(), csv entries atre grouped when imported;
    cursor.close()
    
    return rows

def get_table_contents_machineID(table_name, connection):
    cursor = connection.cursor()
 
    query = "SELECT DISTINCT MachineID FROM {}".format(table_name)
    
    cursor.execute(query)
    
    rows = cursor.fetchall()
    # it seems liken when fetchall(), csv entries atre grouped when imported;
    cursor.close()
    
    return rows

def get_table_contents_funct_11(table_name, connection):
    cursor = connection.cursor()
 
    query = "SELECT * FROM {} ORDER BY MachineID, StudentUCINetID".format(table_name)
    
    cursor.execute(query)
    
    rows = cursor.fetchall()
    # it seems liken when fetchall(), csv entries atre grouped when imported;
    cursor.close()
    
    return rows

def deleteStudent(UCINetID,connection):
    delete = "DELETE FROM Students WHERE UCINetID = '{}'".format(UCINetID)
    cursor = connection.cursor()

    cursor.execute(delete)

    # Committing the changes
    connection.commit()
    cursor.close()

def deleteUser(UCINetID,connection):
    delete = "DELETE FROM Users WHERE UCINetID = '{}'".format(UCINetID)
    cursor = connection.cursor()

    cursor.execute(delete)

    # Committing the changes
    connection.commit()
    cursor.close()

def update_Course(cid, title, connection):

    cursor = connection.cursor()
    
    # Check if the CourseID exists
    cursor.execute("SELECT 1 FROM Courses WHERE CourseID = %s", (cid,))
    exists = cursor.fetchone()
    
    if not exists:
        cursor.close()
        raise ValueError()

    query = "UPDATE Courses SET Title = '{}' WHERE CourseID = '{}'".format(title, cid)

    cursor.execute(query)

    #committing the changes
    connection.commit()
    cursor.close()


def courses_attended(uid, connection):
    query = "SELECT DISTINCT C.CourseID, C.Title, C.Quarter FROM Students S, StudentUseMachinesInProject U, Projects P, Courses C WHERE C.CourseID = P.CourseID AND P.ProjectID = U.ProjectID AND U.StudentUCINetID = S.UCINetID AND S.UCINetID = '{}' ORDER BY C.CourseID ASC".format(uid)

    cursor = connection.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        print(row[0],",", row[1],",", row[2], sep="")

    cursor.close()


def emails_of_admin(machineID,connection):
        
    query = """
        SELECT A.UCINetID, U.Firstname, U.Middlename, U.Lastname, GROUP_CONCAT(UE.Email, ';') AS EmailList
        FROM Administrators A
        INNER JOIN Users U ON A.UCINetID = U.UCINetID
        INNER JOIN UserEmail UE ON A.UCINetID = UE.UCINetID
        INNER JOIN AdministratorManageMachines AMM ON A.UCINetID = AMM.AdministratorUCINetID
        WHERE AMM.MachineID = {}
        GROUP BY A.UCINetID, U.Firstname, U.Middlename, U.Lastname
        ORDER BY A.UCINetID ASC;
    """.format(machineID)

    cursor = connection.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        email_list = row[4].replace(';,', ';')
        if email_list.endswith(';'):
            email_list = email_list[:-1]  # Remove the last semicolon
        print(','.join(str(cell) for cell in row[:4]) + ',' + email_list)



def max_course(num, connection):
    query = """
    SELECT C.CourseID, C.Title, Count(DISTINCT S.UCINetID)
    FROM Students S, Courses C, StudentUseMachinesInProject U, Projects P
    WHERE C.CourseID = P.CourseID AND P.ProjectID = U.ProjectID AND U.StudentUCINetID = S.UCINetID
    GROUP BY C.CourseID
    ORDER BY Count(S.UCINETID) DESC
    LIMIT {}
    """.format(num)

    #print(query)

    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        print(row[0],",", row[1],",", row[2], sep="")

    cursor.close()


def active_Student(mid, N, startDate, endDate, connection):
    query = """
    SELECT U.UCINetID, U.Firstname, U.Middlename, U.Lastname
    FROM Users U, Students S, StudentUseMachinesInProject P
    WHERE U.UCINetID = S.UCINetID AND S.UCINetID = P.StudentUCINetID AND P.MachineID = '{}' 
    AND P.StartDate >= '{}' AND P.EndDate <= '{}'
    GROUP BY U.UCINetID
    HAVING COUNT(*) >= {}
    ORDER BY U.UCINetID ASC
    """.format(mid, startDate, endDate, N)


    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        print(row[0],",", row[1],",", row[2], ",", row[3], sep="")

    cursor.close()


def machine_Usage(cid, connection):

    query = """
    SELECT M.MachineID, M.Hostname, M.IPAddress, COALESCE(COUNT(U.ProjectID), 0) 
    FROM Machines M
    LEFT JOIN StudentUseMachinesInProject U ON M.MachineID = U.MachineID
    AND U.ProjectID IN (SELECT ProjectID FROM Projects WHERE CourseID = {})
    GROUP BY M.MachineID
    ORDER BY M.MachineID DESC;
    """.format(cid)

    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        print(row[0],",", row[1],",", row[2], ",", row[3], sep="")


def drop_table(connection):
# input standard sql DROP TABLE commands into connection.cursor().execute()
    create_table_query = "DROP TABLE administratormanagemachines"     
    connect = connection.cursor()
    connect.execute(create_table_query) 
    connection.commit()

    create_table_query = "DROP TABLE studentusemachinesinproject"     
    connect = connection.cursor()
    connect.execute(create_table_query) 
    connection.commit()
      
    create_table_query = "DROP TABLE projects"     
    connect = connection.cursor()
    connect.execute(create_table_query) 
    connection.commit()

    create_table_query = "DROP Table useremail"     
    connect = connection.cursor()
    connect.execute(create_table_query) 
    connection.commit()

    create_table_query = "DROP TABLE students"     
    connect = connection.cursor()
    connect.execute(create_table_query) 
    connection.commit()

    create_table_query = "DROP TABLE administrators"     
    connect = connection.cursor()
    connect.execute(create_table_query) 
    connection.commit()

    create_table_query = "DROP TABLE courses"     
    connect = connection.cursor()
    connect.execute(create_table_query) 
    connection.commit()

    create_table_query = "DROP TABLE machines"     
    connect = connection.cursor()
    connect.execute(create_table_query) 
    connection.commit()

    create_table_query = "DROP TABLE Users"     
    connect = connection.cursor()
    connect.execute(create_table_query) 
    connection.commit()

    connect.close()
 
def create_tables(connection):
    create_table_query = "CREATE TABLE Users( UCINetID VARCHAR(255) PRIMARY KEY, Firstname VARCHAR(255), Middlename VARCHAR(255), Lastname VARCHAR(255) );"     
    connect = connection.cursor()
    connect.execute(create_table_query)
    connection.commit()

    create_table_query = "CREATE TABLE UserEmail( UCINetID VARCHAR(255) NOT NULL, Email VARCHAR(255), PRIMARY KEY (UCINetID, Email), FOREIGN KEY (UCINetID) REFERENCES Users (UCINetID) ON DELETE CASCADE );"
    connect = connection.cursor()
    connect.execute(create_table_query)
    connection.commit()

    create_table_query = "CREATE TABLE Students( UCINetID VARCHAR(20) PRIMARY KEY NOT NULL, FOREIGN KEY (UCINetID) REFERENCES Users(UCINetID) ON DELETE CASCADE );"
    connect = connection.cursor()
    connect.execute(create_table_query)
    connection.commit()

    create_table_query = "CREATE TABLE Administrators( UCINetID VARCHAR(20) PRIMARY KEY NOT NULL, FOREIGN KEY (UCINetID) REFERENCES Users(UCINetID) ON DELETE CASCADE );"
    connect = connection.cursor()
    connect.execute(create_table_query)
    connection.commit()

    create_table_query = "CREATE TABLE Courses( CourseID INT PRIMARY KEY NOT NULL, Title VARCHAR(100), Quarter VARCHAR(20) );"
    connect = connection.cursor()
    connect.execute(create_table_query)
    connection.commit()
    
    create_table_query = "CREATE TABLE Projects( ProjectID INT PRIMARY KEY NOT NULL, Name VARCHAR(100), Description TEXT, CourseID INT NOT NULL, FOREIGN KEY (CourseID) REFERENCES Courses(CourseID) ON DELETE CASCADE );"
    connect = connection.cursor()
    connect.execute(create_table_query)
    connection.commit()


    create_table_query = "CREATE TABLE Machines( MachineID INT PRIMARY KEY NOT NULL, Hostname VARCHAR(255), IPAddress VARCHAR(15), OperationalStatus VARCHAR(50), Location VARCHAR(255) );"
    connect = connection.cursor()
    connect.execute(create_table_query)
    connection.commit()
    #add managae and use rel tables

    create_table_query =" CREATE TABLE StudentUseMachinesInProject( ProjectID INT,StudentUCINetID VARCHAR(20), MachineID INT, StartDate DATE, EndDate DATE, PRIMARY KEY (ProjectID, StudentUCINetID, MachineID), FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID), FOREIGN KEY (StudentUCINetID) REFERENCES Students(UCINetID) ON DELETE NO ACTION, FOREIGN KEY (MachineID) REFERENCES Machines(MachineID) ON DELETE NO ACTION );"
    connect = connection.cursor()
    connect.execute(create_table_query)
    connection.commit()

    create_table_query = "CREATE TABLE AdministratorManageMachines( AdministratorUCINetID VARCHAR(20), MachineID INT, PRIMARY KEY (AdministratorUCINetID, MachineID), FOREIGN KEY (AdministratorUCINetID) REFERENCES Administrators(UCINetID) ON DELETE NO ACTION, FOREIGN KEY (MachineID) REFERENCES Machines(MachineID) ON DELETE NO ACTION );"
    connect = connection.cursor()
    connect.execute(create_table_query)
    connection.commit()




def import_data(folderName:str, connection):
    try:
        drop_table(connection)
    except:
        pass
    
    # read folder files, add tables and return (Table - (Number of users,Number of machine, Number of Course))
    file_name = "admins.csv"
    file_path = os.path.join(folderName, file_name)
    # Hu: is this necessary?

    create_tables(connection)

    # *** begin adding to tables ***
    with open(f"{folderName}/users.csv","r") as f:
        csv_reader = csv.reader(f)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Process each row
            add_user(row[0],row[1],row[2],row[3],connection)
            # 'INSERT INTO' returns error if attempting to insert entries with same primary key.
            
    with open(f"{folderName}/emails.csv","r") as f:
        csv_reader = csv.reader(f)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Process each row
            add_email(row[0],row[1],connection)
            
    with open(f"{folderName}/students.csv","r") as f:
        csv_reader = csv.reader(f)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Process each row
            add_student(row[0],connection)
            
    with open(f"{folderName}/admins.csv","r") as f:
        csv_reader = csv.reader(f)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Process each row
            add_admins(row[0],connection)
            
    with open(f"{folderName}/courses.csv","r") as f:
        csv_reader = csv.reader(f)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Process each row
            add_course(row[0],row[1],row[2],connection)


    with open(f"{folderName}/projects.csv","r") as f:
        csv_reader = csv.reader(f)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Process each row
            add_project(row[0],row[1],row[2],row[3],connection)

    with open(f"{folderName}/machines.csv","r") as f:
        csv_reader = csv.reader(f)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Process each row
            add_machine(row[0],row[1],row[2],row[3],row[4],connection)

    with open(f"{folderName}/use.csv","r") as f:
        csv_reader = csv.reader(f)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Process each row
            add_use(row[0],row[1],row[2],row[3],row[4],connection)


    with open(f"{folderName}/manage.csv","r") as f:
        csv_reader = csv.reader(f)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Process each row
            add_mange(row[0],row[1],connection)

def courses_machines_distinct_use(connection):
    query = """
    SELECT DISTINCT C.CourseID, P.ProjectID, SM.StudentUCINetID, SM.MachineID
    FROM Courses C
    JOIN Projects P ON C.CourseID = P.CourseID
    JOIN StudentUseMachinesInProject SM ON P.ProjectID = SM.ProjectID;
    """ 

    cursor = connection.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()





if __name__ == "__main__":

    args = sys.argv

    connection = connect_to_database()
    # credential saved in def connect_to_database();
    # def connect_to_database() returns mysql.connector.connect() as object 'connection';
    
    for i in range(len(args)):
        if args[i] == "NULL":
            args[i] = None

    if args[1] == "import":
        import_data(folderName=args[2],connection=connection)
        print(str(get_table_size("Users",connection))+","+str(get_table_size("Machines",connection))+","+str(get_table_size("Courses",connection)))
    
    elif args[1] == "getTableContent":
        rows = get_table_contents(args[2], connection)
        for row in rows:
            print(row)
            print()  # This adds a newline after printing each row
    # Hu: created for visualization
    
    elif args[1] == "getTableContentFunct11":
        rows = get_table_contents_funct_11(args[2], connection)
        for row in rows:
            print(row)
            print()  # This adds a newline after printing each row
    # Hu: created for visualization

    elif args[1]  == "insertStudent":
        try:
            add_user(args[2],args[4],args[5],args[6],connection)
            add_student(args[2],connection)
            add_email(args[2],args[3],connection)
            print("Success")
        except:
            print("Fail")     
            
    elif args[1] == "addEmail":
        try:        
            add_email(args[2],args[3],connection)
            print("Success")
        except:
            print("Fail")
            
    elif args[1] ==  "deleteStudent":
        try:
            deleteUser(args[2],connection)
            deleteStudent(args[2],connection)
            print("Success")
        # except:
        #     print("Fail")
        except:
            print("Fail")  
    
    elif args[1] ==  "deleteStudent_in_batch":
        rows = get_table_contents(args[2], connection)
        for row in rows:
            try:
                deleteUser(row[0],connection)
                deleteStudent(row[0],connection)
                print("delete " + row[0] + " Success\n")
            # except Exception as e:
            #     print("delete " + row[0] + " Fail")
            #     print(f"Fail: {str(e)}\n")
            except:
                print("Fail")  
            
    elif args[1] =="insertMachine":
        try:
            add_machine(args[2],args[3],args[4],args[5],args[6],connection)
            print("Success")
        except:
            print("Fail")
            
    elif args[1] == "insertUse":
        try:
            add_use(args[2],args[3],args[4],args[5],args[6],connection)
            print("Success")
        # except:
        #     print("Fail")
        except:
            print("Fail")  
                
    elif args[1] == "updateCourse":
        try:
            update_Course(args[2], args[3], connection)
            print("Success")
        except:
            print("Fail")

    elif args[1] ==  "updateCourse_in_batch":
        rows = get_table_contents(args[2], connection)
        for row in rows:
            try:
                update_Course(row[0], args[3], connection)
                print("update " + str(row[0]) + " Success")
            # except Exception as e:
            #     print("update " + str(row[0]) + " Fail")
            #     print(f"Fail: {str(e)}")
            except:
                print("Fail")  

    elif args[1] == "listCourse":
        courses_attended(args[2], connection)

    elif args[1] ==  "listCourse_in_batch":
        rows = get_table_contents(args[2], connection)
        for row in rows:
            try:
                print("\nlistCourse_in_batch " + row[1] + " Success")
                courses_attended(row[1], connection)
            # except Exception as e:
            #     print("listCourse " + row[1] + " Fail")
            #     print(f"Fail: {str(e)}")
            except:
                print("Fail") 
            
    elif args[1] == "popularCourse":
        max_course(args[2], connection)
    
    elif args[1] == "adminEmails":
        emails_of_admin(args[2], connection)

    elif args[1] == "adminEmails_in_batch":
        rows = get_table_contents_machineID(args[2], connection)
        for row in rows:
            print(row[0])
            emails_of_admin(row[0], connection)
            print()  # This adds a newline after printing each row
    # Hu: created for visualization

    elif args[1] == "activeStudent":
        active_Student(args[2], args[3], args[4], args[5], connection)

    elif args[1] == "machineUsage":
        machine_Usage(args[2], connection)
    
    elif args[1] == "coursesMachinesDistinctUse":
         courses_machines_distinct_use(connection)
 
