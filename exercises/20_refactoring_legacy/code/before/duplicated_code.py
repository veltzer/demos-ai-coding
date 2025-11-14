def get_active_users():
    connection = mysql.connect(host='localhost', user='root', password='pass')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE active = 1")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_premium_users():
    connection = mysql.connect(host='localhost', user='root', password='pass')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE premium = 1")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_verified_users():
    connection = mysql.connect(host='localhost', user='root', password='pass')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE verified = 1")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
