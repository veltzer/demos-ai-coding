# This is the "before" half of a refactoring exercise: a deliberately bad
# snippet the reader is asked to improve. It is an excerpt, not a runnable
# module, so the database driver it calls is never imported.
# ruff: noqa: F821
# pylint: disable=undefined-variable,missing-module-docstring,missing-function-docstring


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
