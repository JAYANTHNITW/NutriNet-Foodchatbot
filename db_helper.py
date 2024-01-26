import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "root",
    database = "pandeyji_eatery"
)

def get_next_order_id():
    cursor = cnx.cursor()
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    #fetch the result
    result = cursor.fetchone()[0]

    # closing the cursor
    cursor.close()

    if result is None:
        return 1
    else:
        return result+1

def insert_order_item(food_item,quantity,order_id):
    try:
        cursor = cnx.cursor()

        # calling the  stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))


        # committing the changes
        cnx.commit()

        #closing the cursor
        cursor.close()

        print("Order item inserted Successfully")

        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1
    
    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1

def get_total_order_price(order_id):
    cursor = cnx.cursor()
    query = "SELECT get_total_order_price(%s)"

    cursor.execute(query, (order_id,))


    #fetch the result
    result = cursor.fetchone()[0]

    # closing the cursor
    cursor.close()
    
    return result


def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"

    cursor.execute(insert_query, (order_id, status))

    # Commiting the changes
    cnx.commit()

    # closing the cursor
    cursor.close()

def insert_order_city(city, order_id):
    try:
        cursor = cnx.cursor()

        # calling the stored procedure or executing a SQL statement
        cursor.execute('UPDATE order_tracking SET city = %s WHERE order_id = %s', (city, order_id))

        # committing the changes
        cnx.commit()

        # closing the cursor
        cursor.close()

        print("City inserted into order_tracking Successfully")

        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting city into order_tracking: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1
    
def insert_order_street(street, order_id):
    try:
        cursor = cnx.cursor()

        # calling the stored procedure or executing a SQL statement
        cursor.execute('UPDATE order_tracking SET street = %s WHERE order_id = %s', (street, order_id))

        # committing the changes
        cnx.commit()

        # closing the cursor
        cursor.close()

        print("street inserted into order_tracking Successfully")

        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting city into order_tracking: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1

def insert_order_flatno(flatno, order_id):
    try:
        cursor = cnx.cursor()

        # calling the stored procedure or executing a SQL statement
        cursor.execute('UPDATE order_tracking SET flatno = %s WHERE order_id = %s', (flatno, order_id))

        # committing the changes
        cnx.commit()

        # closing the cursor
        cursor.close()

        print("flat number inserted into order_tracking Successfully")

        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting city into order_tracking: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1

def insert_order_phono(phono, order_id):
    try:
        cursor = cnx.cursor()

        # calling the stored procedure or executing a SQL statement
        cursor.execute('UPDATE order_tracking SET phonenumber = %s WHERE order_id = %s', (str(phono), order_id))

        # committing the changes
        cnx.commit()

        # closing the cursor
        cursor.close()

        print("phonenumber inserted into order_tracking Successfully")

        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting phonenumber into order_tracking: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1

def get_order_status(order_id: int):
    # Replace the placeholders with your actual database credentials
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'pandeyji_eatery'
    }

    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(**db_config)

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Define the SQL query to retrieve the status based on order_id
        query = "SELECT status FROM order_tracking WHERE order_id = %s"

        # Execute the query with the provided order_id
        cursor.execute(query, (order_id,))

        # Fetch the result
        result = cursor.fetchone()

        if result is not None:
            return result[0]
        else:
            return None
    except mysql.connector.Error as err:
        # Handle database errors
        print(f"Error: {err}")
        return None
    finally:
        # Make sure to close the cursor and connection in the 'finally' block
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


