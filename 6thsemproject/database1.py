import pymysql


def user_info_database(uname, email, pw):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Vijay@123',
            database='jarvis_database',
            port=3567        
        )
        print("Connection successful!")
        
        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Define the SQL query to insert data into the 'users' table
        insert_query = "INSERT INTO user_info (name, email, password) VALUES (%s, %s, %s) "

        # User data to insert
        user_data = (uname, email, pw)

        # Execute the query
        cursor.execute(insert_query, user_data)

        # Commit the changes to the database
        conn.commit()

        # Confirm the data was inserted
        print(f"User {user_data[0]} inserted successfully!")
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()

import pymysql

def check_pw(uname):
    try:
        # Connect to MySQL Database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Vijay@123',
            database='jarvis_database',
            port=3567
        )
        
        cursor = conn.cursor()
        
        # SQL query to select the password based on the username (name)
        query = "SELECT password FROM user_info WHERE name = %s"
        cursor.execute(query, (uname,))  # Pass the username as a tuple
        
        # Fetch the result and extract the password
        result = cursor.fetchone()  # fetchone() returns a single record (tuple)
        
        # Check if the result is None (no user found)
        if result:
            password = result[0]  # The password is the first column in the result
            return password
        else:
            print("User not found.")
            return None
        
    except pymysql.MySQLError as err:
        print(f"Error: {err}")

    finally:
        # Close the connection if it's open
        if 'conn' in locals() and conn.open:
            conn.close()
        

def check_user(uname):
    try:
        # Connect to MySQL Database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Vijay@123',
            database='jarvis_database',
            port=3567
            )
        cursor = conn.cursor()
        query = "SELECT name, pw FROM user_info WHERE name = %s"
        cursor.execute(query, (uname))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
        
    except pymysql.MySQLError as err:
        print(f"Error: {err}")

    finally:
        if 'conn' in locals() and conn.open:
            conn.close()
            
def getemail(uname):
    try:
        # Connect to MySQL Database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Vijay@123',
            database='jarvis_database',
            port=3567
            )
        cursor = conn.cursor()
        query = "SELECT email FROM user_info WHERE name = %s"
        cursor.execute(query, (uname))
        result = cursor.fetchone()
        if result:
            email = result[0]  # The password is the first column in the result
            return email
        else:
            print("User not found.")
            return None
        
        
    except pymysql.MySQLError as err:
        print(f"Error: {err}")

    finally:
        if 'conn' in locals() and conn.open:
            conn.close()
            
def update_password(uname, pw):
    try:
        # Connect to MySQL Database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Vijay@123',
            database='jarvis_database',
            port=3567
            )
        cursor = conn.cursor()
        query = "UPDATE user_info SET password = %s WHERE name = %s"
        cursor.execute(query, (uname, pw))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Password for {uname} updated successfully.")
        else:
            print(f"User {uname} not found.")
        
    except pymysql.MySQLError as err:
        print(f"Error: {err}")

    finally:
        if 'conn' in locals() and conn.open:
            conn.close()
            

if __name__ == "__main__":
    check_pw()
    user_info_database()
    check_user()
    getemail()
    update_password()
    
