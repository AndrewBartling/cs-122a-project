


***
# funct 12

Output:
Table - machineID,hostname,ipAddr,count

python3 project.py machineUsage [courseId: int]

Courses (CourseID, Title, Quarter)
Projects (ProjectID, Name, Description, CourseID)
# MachineUse
StudentUseMachinesInProject (ProjectID ,StudentUCINetID ,MachineID ,StartDate ,EndDate)
Machines (MachineID, Hostname, IPAddress, OperationalStatus, Location)


# python3 project.py getTableContent Projects
# python3 project.py getTableContent StudentUseMachinesInProject
# python3 project.py getTableContent Machines
# MachineID 102, exist, but no student use it. thus not in StudentUseMachinesInProject record


    create_table_query =" CREATE TABLE StudentUseMachinesInProject( ProjectID INT,StudentUCINetID VARCHAR(20), MachineID INT, StartDate DATE, EndDate DATE, PRIMARY KEY (ProjectID, StudentUCINetID, MachineID), FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID), FOREIGN KEY (StudentUCINetID) REFERENCES Students(UCINetID) ON DELETE NO ACTION, FOREIGN KEY (MachineID) REFERENCES Machines(MachineID) ON DELETE NO ACTION );"
    connect = connection.cursor()
    connect.execute(create_table_query)
    connection.commit()




SELECT DISTINCT C.CourseID, P.ProjectID, SM.StudentUCINetID, SM.MachineID
FROM Courses C, Projects P, StudentUseMachinesInProject SM,
WHERE C.CourseID = P.CourseID AND P.ProjectID = SM.ProjectID




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



python3 project.py coursesMachinesDistinctUse
# DISTINCT C.CourseID, P.ProjectID, SM.StudentUCINetID, SM.MachineID
# python3 project.py machineUsage [courseId: int]
python3 project.py machineUsage 1
python3 project.py machineUsage 2
python3 project.py machineUsage 3
python3 project.py machineUsage 4
python3 project.py machineUsage 5






***
# funct 11
python3 project.py getTableContent StudentUseMachinesInProject


***
# all tables
Users (UCINetID, Firstname, Middlename, Lastname)
UserEmail (UCINetID, Email)
Students (UCINetID)
Administrators (UCINetID)
Courses (CourseID, Title, Quarter)
Projects (ProjectID, Name, Description, CourseID)
Machines (MachineID, Hostname, IPAddress, OperationalStatus, Location)
StudentUseMachinesInProject (ProjectID ,StudentUCINetID ,MachineID ,StartDate ,EndDate)
AdministratorManageMachines (AdministratorUCINetID, MachineID)


Users (UCINetID, Firstname, Middlename, Lastname)
Students (UCINetID)
StudentUseMachinesInProject (ProjectID ,StudentUCINetID ,MachineID ,StartDate ,EndDate)

MachineID

python3 project.py getTableContentFunct11 StudentUseMachinesInProject




Selection of Non-Aggregated Columns: SQL standards (and most SQL database systems) require that any column in the SELECT list that is not part of an aggregate function (like SUM(), AVG(), COUNT(), etc.) must be included in the GROUP BY clause. Your query selects * (all columns), but only groups by StudentUCINetID and MachineID. This could lead to an error in many SQL databases because it's not clear how to handle the columns that are not part of the GROUP BY clause.

Intent of Grouping: If your intention is to simply order the results by StudentUCINetID and MachineID without aggregating data, you should use ORDER BY instead of GROUP BY. If you indeed intend to perform some form of aggregation (like counting records, summing values, etc.), you'll need to specify what you want to aggregate and how.








***
# funct 11
    elif args[1] == "activeStudent":
        active_Student(args[2], args[3], args[4], args[5], connection)

***
# funct 11
def active_Student(mid, N, startDate, endDate, connection):
    query = """
    SELECT U.UCINetID, U.Firstname, U.Middlename, U.Lastname
    FROM Users U, Students S, StudentUseMachinesInProject P
    WHERE U.UCINetID = S.UCINetID AND S.UCINetID = P.StudentUCINetID AND P.MachineID = '{}' 
    AND P.StartDate >= '{}' AND P.EndDate <= '{}'
    GROUP BY U.UCINetID
    # without this can't use HAVING COUNT(*) >= {}
    HAVING COUNT(*) >= {}
    ORDER BY U.UCINetID ASC
    """.format(mid, startDate, endDate, N)

    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        print(row[0],",", row[1],",", row[2], ",", row[3], sep="")

    cursor.close()




    # def import_data(folderName:str, connection):

    def add_use(ProjectID,StudentUCINetID,MachineID,StartDate,EndDate,connection):
        use_query = "INSERT INTO StudentUseMachinesInProject (ProjectID ,StudentUCINetID ,MachineID ,StartDate ,EndDate) VALUES (%s, %s, %s, %s, %s)"
        cursor = connection.cursor()

        cursor.execute(use_query, (ProjectID, StudentUCINetID, MachineID, StartDate, EndDate))

        # Committing the changes
        connection.commit()
        cursor.close()

    # is time range data type inserted when I use add_use() 
    add_use(row[0],row[1],row[2],row[3],row[4],connection)
    1,mchang13,1,2020-01-04,2020-01-05
    # chatgpt:: with 1, mchang13, 1, 2020-01-04, 2020-01-05 as the input values, the function will insert these values into your database as long as the StartDate and EndDate columns are of a date-compatible type (such as DATE in SQL).




***
The error message you're encountering, Fail: 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails, indicates that your attempt to delete or update a row in the parent table (students) is being blocked because there are dependent rows in the child table (studentusemachinesinproject) that reference the row you're trying to delete. This behavior is due to a foreign key constraint that enforces referential integrity between the two tables.

Understanding ON DELETE NO ACTION
The default behavior for foreign key constraints in many SQL databases, including MySQL, is ON DELETE NO ACTION. This means that if you try to delete a row in a parent table that has dependent rows in a child table (rows that reference the row you're trying to delete), the delete operation will be blocked, and you'll receive an error message.

ON DELETE NO ACTION is essentially a way to prevent orphaned records in the child table—rows that refer to a non-existent entry in the parent table. By blocking the delete operation, the database ensures that all references remain valid, thus maintaining the integrity of the relational data.

Why You Encounter an Error
When you encounter this error, it means the database is enforcing referential integrity as expected. The database is preventing you from deleting a row that other rows depend on, thereby avoiding data inconsistencies.




***
When you use cursor.fetchall() in a database programming context (such as Python with libraries like sqlite3, PyMySQL, psycopg2 for PostgreSQL, etc.), the method retrieves all rows of a query result and returns them as a list of tuples. Each tuple corresponds to a row in the result set.

Regarding the types of values it can output:

String: Yes, if the data in a column of a row is a string, the corresponding element in the tuple will be a string. For example, if a column contains text data, fetchall() will return that data in the tuple as a string.

NULL type: Yes, fetchall() can also output NULL values from the database, but how they are represented in the result depends on the programming language and the database adapter you're using. In many programming languages and their database libraries, a SQL NULL is translated to the language's equivalent of a null or none value. For instance, in Python, a SQL NULL will be returned as None in the tuple.

Example:
Consider a database table Users with some rows having NULL in the email column.

ID | Name      | Email
---|-----------|----------------
1  | Alice     | alice@example.com
2  | Bob       | NULL

cursor.execute("SELECT ID, Name, Email FROM Users")
rows = cursor.fetchall()
for row in rows:
    print(row)

Output:
(1, 'Alice', 'alice@example.com')
(2, 'Bob', None)

In this example, you can see that for the Email column of Bob, which is NULL in the database, fetchall() returns None in the tuple for Python. The exact representation of NULL values will be consistent with the conventions of the programming language you are using.










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



    elif args[1] ==  "updateCourse_in_batch":
        rows = get_table_contents(args[2], connection)
        for row in rows:
            try:
                update_Course(row[0], args[3], connection)
                print("update " + str(row[0]) + " Success")
            except Exception as e:
                print("update " + str(row[0]) + " Fail")
                print(f"Fail: {str(e)}")





***
convert all
        except Exception as e:
            print(f"Fail: {str(e)}")
to 
        except:
            print("Fail")



***
def drop_table(connection):
# input standard sql DROP TABLE commands into connection.cursor().execute()
    create_table_query = "DROP TABLE administratormanagemachines"     
    connect = connection.cursor()
    connect.execute(create_table_query) 
    connection.commit()
// hu: feel like would be better if we do 'DROP TABLE IF EXISTS tableName';



***
```
# Hu: optimal to run mysql commands directly in mysql
# mysql -u root -p
# # type password
# USE cs122a;
# SELECT * FROM employees;
# # note commands won't execute without ';'
# EXIT;
```




***
# all tables
Users (UCINetID, Firstname, Middlename, Lastname)
UserEmail (UCINetID, Email)
Students (UCINetID)
Administrators (UCINetID)
Courses (CourseID, Title, Quarter)
Projects (ProjectID, Name, Description, CourseID)
Machines (MachineID, Hostname, IPAddress, OperationalStatus, Location)
StudentUseMachinesInProject (ProjectID ,StudentUCINetID ,MachineID ,StartDate ,EndDate)
AdministratorManageMachines (AdministratorUCINetID, MachineID)



***
# funct 10
AdministratorManageMachines (AdministratorUCINetID, MachineID)
Administrators (UCINetID)
Users (UCINetID, Firstname, Middlename, Lastname)
UserEmail (UCINetID, Email)
// uhh. I think a JOIN OF all these tables.
// output 'Table - UCINETId,first name,middle name,last name,list of email'
// ouputting 'UCINETId,first name,middle name,last name' easy. but list of email
// python3 project.py adminEmails [machineId: int]
// AdministratorManageMachines -> Adminstrators -> Users -> UserEmail
// think it's gonna be like a two part query. where funct call 1 return UCINETId,first name,middle name,last name. then function call 2 return list of email.

python3 project.py getTableContent AdministratorManageMachines

emails_of_admin(args[2],connection)
args[2] == adminEmails

    elif args[1] == "adminEmails_in_batch":
        rows = get_table_contents(args[2], connection)
        for row in rows:
            emails_of_admin(row[0],connection)
            print()  # This adds a newline after printing each row
    # Hu: created for visualization

python3 project.py adminEmails_in_batch AdministratorManageMachines



***
# funct 10
python3 project.py getTableContent AdministratorManageMachines
python3 project.py adminEmails_in_batch AdministratorManageMachines



***
# funct 10
def emails_of_admin(machineID,connection):
    # AdministratorManageMachines -> Adminstrators -> Users -> UserEmail

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
    # `GROUP BY A.UCINetID, U.Firstname, U.Middlename, U.Lastname`, allow you to use aggregate funct such as `GROUP_CONCAT(`
    cursor = connection.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        email_list = row[4].replace(';,', ';')
        # `replace(';,', ';')` is this in respons to group concate??? possibly;
        if email_list.endswith(';'):
            email_list = email_list[:-1]  # Remove the last semicolon
        print(','.join(str(cell) for cell in row[:4]) + ',' + email_list)
        # `.join(` join each entry within a row




***
Hu: run
    python3 project.py getTableContent Projects
    python3 project.py getTableContent Students
    python3 project.py getTableContent Machines
to see avaiable IDs.
python3 project.py getTableContent StudentUseMachinesInProject




***
    create_table_query =" CREATE TABLE StudentUseMachinesInProject( ProjectID INT,StudentUCINetID VARCHAR(20), MachineID INT, StartDate DATE, EndDate DATE, PRIMARY KEY (ProjectID, StudentUCINetID, MachineID), FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID), FOREIGN KEY (StudentUCINetID) REFERENCES Students(UCINetID) ON DELETE CASCADE, FOREIGN KEY (MachineID) REFERENCES Machines(MachineID) ON DELETE CASCADE );"
    connect = connection.cursor()
    connect.execute(create_table_query)
    connection.commit()

Fail: 1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`cs122a`.`studentusemachinesinproject`, CONSTRAINT `studentusemachinesinproject_ibfk_1` FOREIGN KEY (`ProjectID`) REFERENCES `projects` (`ProjectID`))

    create_table_query =" CREATE TABLE StudentUseMachinesInProject( ProjectID INT,StudentUCINetID VARCHAR(20), MachineID INT, StartDate DATE, EndDate DATE, PRIMARY KEY (ProjectID, StudentUCINetID, MachineID), FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID), FOREIGN KEY (StudentUCINetID) REFERENCES Students(UCINetID) ON DELETE CASCADE, FOREIGN KEY (MachineID) REFERENCES Machines(MachineID) ON DELETE CASCADE );"

    create_table_query = "CREATE TABLE AdministratorManageMachines( AdministratorUCINetID VARCHAR(20), MachineID INT, PRIMARY KEY (AdministratorUCINetID, MachineID), FOREIGN KEY (AdministratorUCINetID) REFERENCES Administrators(UCINetID) ON DELETE CASCADE, FOREIGN KEY (MachineID) REFERENCES Machines(MachineID) ON DELETE CASCADE );"
    // do not know if ON DELETE CASADE is necessary. I mean it's not specificed