import mysql.connector



# Function that uses the shared MySQL connection
def fetch_all(mydb):
    cursor = mydb.cursor()
    mydb.commit()
    cursor.execute("SELECT * FROM employees")
    sql_result = cursor.fetchall() ## gets all rows returned by above
    # NB: You must fetch all rows for the current query before executing new statements using the same connection.
    return sql_result

def fetch_emp(mydb,emp_id):
    cursor = mydb.cursor()
    mydb.commit()
    cursor.execute("SELECT * FROM employees where ID="+emp_id)
    sql_result = cursor.fetchall()
    return sql_result

def insert_emp(mydb,emp_id,emp_name,emp_age):
    cursor = mydb.cursor()
    mydb.commit()
    myvals = (emp_id,emp_name,emp_age)

    try:
        # Try executing the SQL statement
        cursor.execute("INSERT INTO employees(id,name,age) VALUES (%s, %s, %s)", myvals)
        mydb.commit()

        return "Item created successfully"

    except mysql.connector.Error as err:
        # If an error occurs, display the error message
        return {"error": f"Failed to insert item. MySQL Error: {err}"}
