from app.db import get_connection

def create_complaint(user_id, title, description, category, location, co_ordinates, image):
    conn = get_connection()
    cursor = conn.cursor()

    lat = None
    long = None

    if co_ordinates:
        try:
            parts = co_ordinates.split(",")
            lat = float(parts[0].strip())
            long = float(parts[1].strip())
        except:
            lat = None
            long = None

    cursor.execute('''
    INSERT INTO complaints
    (user_id, title, description, category, location, latitude, longitude, image)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (user_id, title, description, category, location, lat, long, image))

    conn.commit()
    cursor.close()
    conn.close()


def get_report_by_id(comp_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
    SELECT * FROM complaints
    WHERE id = %s
    ''', (comp_id,))

    complaint = cursor.fetchone()

    return complaint

def get_reports_info(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    info = {}
    cursor.execute('''
    SELECT COUNT(id) FROM complaints
    WHERE user_id = %s;
    ''', (user_id,))
    info['total'] = cursor.fetchone()[0]

    cursor.execute('''
    SELECT COUNT(id) FROM complaints
    WHERE user_id = %s AND status = 'pending';
    ''', (user_id,))
    info['pending'] = cursor.fetchone()[0]

    cursor.execute('''
    SELECT COUNT(id) FROM complaints
    WHERE user_id = %s AND status = 'in progress';
    ''', (user_id,))
    info['in_progress'] = cursor.fetchone()[0]

    cursor.execute('''
    SELECT COUNT(id) FROM complaints
    WHERE user_id = %s AND status = 'resolved';
    ''', (user_id,))
    info['resolved'] = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return info


def get_recent_reports(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
    SELECT title, status FROM complaints
    WHERE user_id = %s
    ORDER BY id DESC
    LIMIT 3;
    ''', (user_id,))

    reports = cursor.fetchall()

    cursor.close()
    conn.close()

    return reports

def get_all_reports_by_id(user_id, status=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = f"SELECT  * FROM complaints WHERE user_id = {user_id}"
    params = []

    if status:
        sql += " AND status = %s"
        params.append(status)

    sql += " ORDER BY created_at DESC"

    cursor.execute(sql, params)
    reports = cursor.fetchall()

    cursor.close()
    conn.close()

    return reports


# Admin----------------

def get_all_reports(status=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    if status:
        cursor.execute('''
        SELECT * FROM complaints
        WHERE status = %s
        ORDER BY created_at DESC;
        ''', (status,))
    else:
        cursor.execute('''
        SELECT * FROM complaints
        ORDER BY created_at DESC;
        ''')

    reports = cursor.fetchall()
    cursor.close()
    conn.close()
    return reports


def get_admin_stats():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
    SELECT COUNT(*) AS total,
    SUM(status = 'pending') AS pending,
    SUM(status = 'in progress') AS in_progress,
    SUM(status = 'resolved') AS resolved
    FROM complaints;
    ''')

    stats = cursor.fetchone()
    cursor.close()
    conn.close()

    return stats

def updateStatus(complaint_id, status):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
    UPDATE complaints
    SET status = %s
    WHERE id = %s;
    ''', (status, complaint_id))

    conn.commit()
    cursor.close()
    conn.close()


def search_reports(query=None, status=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT  * FROM complaints WHERE 1=1"
    params = []

    if query:
        sql += " AND (title LIKE %s OR category LIKE %s OR location LIKE %s)"
        like_query = f"%{query}%"
        params.extend([like_query, like_query, like_query])

    if status:
        sql += " AND status = %s"
        params.append(status)

    sql += " ORDER BY created_at DESC"

    cursor.execute(sql, params)
    reports = cursor.fetchall()

    cursor.close()
    conn.close()

    return reports


def get_category_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, COUNT(*) 
        FROM complaints
        GROUP BY category
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {row[0]: row[1] for row in data}



def get_monthly_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MONTH(created_at), COUNT(*)
        FROM complaints
        GROUP BY MONTH(created_at)
        ORDER BY MONTH(created_at)
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Initialize all 12 months
    monthly_counts = [0] * 12

    for month, count in data:
        monthly_counts[month - 1] = count

    return monthly_counts

