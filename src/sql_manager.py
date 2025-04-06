import mysql.connector

def get_query_results(query):
    try:
        database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="test",
            database="insight_database"
            )
        cursor = database.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        database.close()
        return result
    except:
        return "Failed"