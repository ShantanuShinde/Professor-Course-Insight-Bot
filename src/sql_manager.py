import mysql.connector

destructive_query_keywords = ['DELETE', 'DROP']

def get_query_results(query):
    try:
        for keyword in destructive_query_keywords:
            if keyword in query.lower():
                print("Attempted to execute destructive query!")
                return 'Failed'
        database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="test",
            database="insightdb"
            )
        cursor = database.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        database.close()
        return result
    except:
        return "Failed"