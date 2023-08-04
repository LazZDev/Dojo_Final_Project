import pymysql.cursors


class MySQLConnection:
    def __init__(self, db):
        # Initialize a connection to the MySQL database
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            db=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        # Store the connection in an instance variable
        self.connection = connection

    def query_db(self, query, data=None):
        # Execute a query on the database
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # If the query is an INSERT statement, return the ID of the inserted row
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # If the query is a SELECT statement, return the resulting data as a list of dictionaries
                    result = cursor.fetchall()
                    return result
                else:
                    # If the query is an UPDATE or DELETE statement, return nothing
                    self.connection.commit()
            except Exception as e:
                # If the query fails, return False
                return False
            finally:
                # Close the database connection
                self.connection.close()


def connectToMySQL(db):
    # Create and return a MySQLConnection object
    return MySQLConnection(db)