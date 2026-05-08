from app.db import get_connection

def create_notification(user_id, complaint_id, message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO notifications (user_id, complaint_id, message)
    VALUES(%s, %s, %s);
    ''', (user_id, complaint_id, message))

    conn.commit()
    cursor.close()
    conn.close()