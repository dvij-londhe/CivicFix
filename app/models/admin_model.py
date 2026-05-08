from app.db import get_connection


def get_admin_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
    SELECT * FROM admin
    WHERE email = %s;
    ''', (email,))

    admin = cursor.fetchone()
    cursor.close()
    conn.close()
    return admin


