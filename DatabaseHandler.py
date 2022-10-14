import pymysql
import pymysql.cursors
from datetime import date


# Lengths Convention For Database
# Email = 50
# Password = 50
# Name = 50
# Address = 150
# Phone = 20
# Gender = 10
# Color = 20
# Model = 50
# Date Time = 50


def get_connection():
    return pymysql.connect(host='LocalHost',
                           user='root',
                           password='mughal',
                           database='ticket_booking_app',
                           cursorclass=pymysql.cursors.DictCursor)


def create_database():
    try:
        my_connection = get_connection()
        my_cursor = my_connection.cursor()
        my_cursor.execute('CREATE DATABASE IF NOT EXISTS TICKET_BOOKING_APP')

        my_connection = get_connection()
        my_cursor = my_connection.cursor()

        my_cursor.execute('CREATE TABLE IF NOT EXISTS ADMINS_LOGIN '
                          '(ADMIN_EMAIL VARCHAR(50) PRIMARY KEY,'
                          'ADMIN_PASSWORD VARCHAR(50) NOT NULL)')

        my_cursor.execute('CREATE TABLE IF NOT EXISTS USERS_LOGIN '
                          '(USER_EMAIL VARCHAR(50) PRIMARY KEY,'
                          'FIRSTNAME VARCHAR(50),'
                          'LASTNAME VARCHAR(50),'
                          'PHONE VARCHAR(20),'
                          'ADDRESS VARCHAR(150),'
                          'PASSWORD VARCHAR(50) NOT NULL,'
                          'GENDER VARCHAR(10),'
                          'CREDITS INT DEFAULT 0)')

        my_cursor.execute('CREATE TABLE IF NOT EXISTS BUSES '
                          '(BUS_ID INT AUTO_INCREMENT PRIMARY KEY,'
                          'COLOR VARCHAR(20),'
                          'MODEL VARCHAR(50),'
                          'TICKET_PRICE INT NOT NULL)')

        my_cursor.execute('CREATE TABLE IF NOT EXISTS ROUTES '
                          '(ROUTE_ID INT AUTO_INCREMENT,'
                          'SOURCE VARCHAR(50),'
                          'DESTINATION VARCHAR(50),'
                          'CONSTRAINT ROUTE_PK PRIMARY KEY(ROUTE_ID, SOURCE, DESTINATION))')

        my_cursor.execute('CREATE TABLE IF NOT EXISTS SCHEDULES '
                          '(BUS_ID INT,'
                          'DEPARTURE_DATE_TIME VARCHAR(50),'
                          'ARRIVAL_DATE_TIME VARCHAR(50),'
                          'ROUTE_ID INT,'
                          'FOREIGN KEY (BUS_ID) REFERENCES BUSES(BUS_ID) ON DELETE CASCADE,'
                          'FOREIGN KEY (ROUTE_ID) REFERENCES ROUTES(ROUTE_ID) ON DELETE CASCADE,'
                          'CONSTRAINT SCHEDULE_PK PRIMARY KEY(BUS_ID, DEPARTURE_DATE_TIME))')

        my_cursor.execute('CREATE TABLE IF NOT EXISTS BOOKINGS '
                          '(BOOKING_ID INT AUTO_INCREMENT PRIMARY KEY,'
                          'USER_EMAIL VARCHAR(50),'
                          'BUS_ID INT,'
                          'ROUTE_ID INT,'
                          'BOOKING_DATE VARCHAR(50),'
                          'DEPARTURE_DATE VARCHAR(50),'
                          'SEAT_NUMBER INT,'
                          'PRICE INT DEFAULT 0,'
                          'FOREIGN KEY (USER_EMAIL) REFERENCES USERS_LOGIN(USER_EMAIL) ON DELETE CASCADE,'
                          'FOREIGN KEY (BUS_ID) REFERENCES BUSES(BUS_ID) ON DELETE CASCADE,'
                          'FOREIGN KEY (ROUTE_ID) REFERENCES ROUTES(ROUTE_ID) ON DELETE CASCADE)')

        my_cursor.execute('CREATE TABLE IF NOT EXISTS OCCUPIED'
                          '(USER_EMAIL VARCHAR(50),'
                          'BOOKING_ID INT,'
                          'BUS_ID INT,'
                          'SEAT_NUMBER INT,'
                          'FOREIGN KEY (USER_EMAIL) REFERENCES USERS_LOGIN(USER_EMAIL) ON DELETE CASCADE,'
                          'FOREIGN KEY (BOOKING_ID) REFERENCES BOOKINGS(BOOKING_ID) ON DELETE CASCADE,'
                          'FOREIGN KEY (BUS_ID) REFERENCES BUSES(BUS_ID) ON DELETE CASCADE,'
                          'CONSTRAINT BOOKINGS_PK PRIMARY KEY(BOOKING_ID, BUS_ID, SEAT_NUMBER))')

        print("DATABASE ESTABLISHED SUCCESSFULLY!!!")

    except pymysql.Connection.Error as E:
        print("FAILED TO MAKE CONNECTION DURING CREATING DATABASE!!!\n"
              "Hint: Please Check Your SQL Server or Password!!!")


create_database()


def insert_admin():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO ADMINS_LOGIN(ADMIN_EMAIL, ADMIN_PASSWORD) VALUES(%s, %s)',
                       ('admin@gmail.com', 'admin'))
        connection.commit()
        connection.close()
        print("ADMMIN ADDED")
        return True
    except pymysql.MySQLError as e:
        print("ADMIN ALREADY EXISTS")
        return False


insert_admin()

#################################################################################################



def fetch_all_table_info(table):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM ' + table)
    li = cursor.fetchall()
    connection.close()
    return li


def fetch_latest_id_of_buses():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(BUS_ID) FROM BUSES')
    b_id = cursor.fetchone()
    b_id = b_id['MAX(BUS_ID)']
    connection.close()
    return b_id


def delete_record_of_bus_with_id(i):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM BUSES WHERE BUS_ID = %s', (i,))
        connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        return False


def add_bus_info(i, c, m, p):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO BUSES(BUS_ID, MODEL, COLOR, TICKET_PRICE) VALUES (%s, %s, %s, %s)',
                       (i, m, c, p))
        connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        return False


def update_bus_info(i, m, c, p):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('UPDATE BUSES SET MODEL = %s, COLOR = %s, TICKET_PRICE = %s WHERE BUS_ID = %s',
                       (m, c, p, i))
        connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        return False


def fetch_latest_id_of_routes():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(ROUTE_ID) FROM ROUTES')
    r_id = cursor.fetchone()
    r_id = r_id['MAX(ROUTE_ID)']
    connection.close()
    return r_id


def add_routes_info(i, s, d):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO ROUTES(ROUTE_ID, SOURCE, DESTINATION) VALUES (%s, %s, %s)',
                       (i, s, d))
        connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        return False


def delete_record_of_route_with_id(i):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM ROUTES WHERE ROUTE_ID = %s', (i,))
        connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        return False


def update_route_info(i, s, d):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('UPDATE ROUTES SET SOURCE = %s, DESTINATION = %s WHERE ROUTE_ID = %s',
                       (s, d, i))
        connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        return False


def add_schedule_info(bi, dt, at, ri):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO SCHEDULES(BUS_ID, DEPARTURE_DATE_TIME, ARRIVAL_DATE_TIME, ROUTE_ID) '
                       'VALUES (%s, %s, %s, %s)',
                       (bi, dt, at, ri))
        connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        return False


def delete_record_of_schedule(ri, dt, bi):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM SCHEDULES WHERE ROUTE_ID = %s AND DEPARTURE_DATE_TIME = %s AND BUS_ID = %s',
                       (ri, dt, bi))
        connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        return False


def update_schedule_info(bi, dt, at, ri, obi, odt, ori):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('UPDATE SCHEDULES SET BUS_ID = %s, DEPARTURE_DATE_TIME = %s, ARRIVAL_DATE_TIME = %s,'
                       ' ROUTE_ID = %s WHERE ROUTE_ID = %s AND DEPARTURE_DATE_TIME = %s AND BUS_ID = %s',
                       (bi, dt, at, ri, ori, odt, obi))
        connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        return False


def fetch_username_from_user_email(e):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT FIRSTNAME, LASTNAME, CREDITS FROM USERS_LOGIN WHERE USER_EMAIL = %s', (e,))
        u_data = cursor.fetchone()
        connection.commit()
        connection.close()
        return u_data
    except pymysql.MySQLError as e:
        return False


def add_into_user_credits(e, c):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT CREDITS FROM USERS_LOGIN WHERE USER_EMAIL = %s', (e,))
        old_cr = cursor.fetchone()
        old_cr = old_cr['CREDITS']
        new_cr = old_cr + int(c)
        cursor = connection.cursor()
        cursor.execute('UPDATE USERS_LOGIN SET CREDITS = %s WHERE USER_EMAIL = %s', (new_cr, e))
        connection.commit()
        connection.close()
        return old_cr+1
    except pymysql.MySQLError as e:
        return False


def withdraw_user_credits(e, c):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT CREDITS FROM USERS_LOGIN WHERE USER_EMAIL = %s', (e,))
        old_cr = cursor.fetchone()
        old_cr = old_cr['CREDITS']
        new_cr = old_cr - int(c)
        cursor = connection.cursor()
        cursor.execute('UPDATE USERS_LOGIN SET CREDITS = %s WHERE USER_EMAIL = %s', (new_cr, e))
        connection.commit()
        connection.close()
        return old_cr+1
    except pymysql.MySQLError as e:
        return False


def get_route_id(s, d):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT ROUTE_ID FROM ROUTES WHERE SOURCE = %s AND DESTINATION = %s', (s, d))
        r_id = cursor.fetchone()
        if r_id == None:
            r_id = 0
        else:
            r_id = r_id['ROUTE_ID']
        connection.close()
        return r_id
    except pymysql.MySQLError as e:
        return False


def get_schedules_for_user(d, r_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM SCHEDULES WHERE ROUTE_ID = %s AND DEPARTURE_DATE_TIME = %s', (r_id, d))
        sch = cursor.fetchall()
        connection.close()
        return sch
    except pymysql.MySQLError as e:
        return False


def get_ticket_price(i):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT TICKET_PRICE FROM BUSES WHERE BUS_ID = %s', (i,))
        sch = cursor.fetchone()
        connection.close()
        return sch['TICKET_PRICE']
    except pymysql.MySQLError as e:
        return False


def add_bookings(email, b_id, r_id, d_date, seats, p):
    try:
        connection = get_connection()
        for i in seats:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO BOOKINGS(USER_EMAIL, BUS_ID, ROUTE_ID, BOOKING_DATE, DEPARTURE_DATE,'
                           ' SEAT_NUMBER, PRICE) '
                           'VALUES(%s, %s, %s, %s, %s, %s, %s)', (email, b_id, r_id, date.today(), d_date, i, p))
            connection.commit()
            cursor = connection.cursor()
            withdraw_user_credits(email, p)
            booking_id = fetch_latest_id_of_bookings()
            cursor.execute('INSERT INTO OCCUPIED(USER_EMAIL, BOOKING_ID, BUS_ID, SEAT_NUMBER) '
                           'VALUES(%s, %s, %s, %s)', (email, booking_id, b_id, i))
            connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        return False


def fetch_latest_id_of_bookings():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT MAX(BOOKING_ID) FROM BOOKINGS')
    r_id = cursor.fetchone()
    r_id = r_id['MAX(BOOKING_ID)']
    connection.close()
    return r_id


def fetch_booked_seats(b_id, r_id, d_date):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT SEAT_NUMBER FROM BOOKINGS WHERE BUS_ID = %s and ROUTE_ID = %s and DEPARTURE_DATE = %s",
                       (b_id, r_id, d_date))
        seats = cursor.fetchall()
        connection.commit()
        connection.close()
        arr = []
        for i in seats:
            arr.append(i['SEAT_NUMBER'])
        return arr
    except pymysql.MySQLError as e:
        return False


def fetch_user_selected_seats(e, b_id, r_id, d_date):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT SEAT_NUMBER FROM BOOKINGS WHERE USER_EMAIL = %s and BUS_ID = %s and ROUTE_ID = %s"
                       " and DEPARTURE_DATE = %s",
                       (e, b_id, r_id, d_date))
        seats = cursor.fetchall()
        connection.commit()
        connection.close()
        arr = []
        for i in seats:
            arr.append(i['SEAT_NUMBER'])
        return arr
    except pymysql.MySQLError as e:
        return False


def remove_bookings(email, b_id, r_id, d_date, seats, p):
    try:
        for i in seats:
            connection = get_connection()
            cursor = connection.cursor()
            count = cursor.execute('DELETE FROM BOOKINGS WHERE USER_EMAIL = %s and BUS_ID = %s and '
                                   'ROUTE_ID = %s and DEPARTURE_DATE = %s and SEAT_NUMBER = %s',
                                   (email, b_id, r_id, d_date, i))
            connection.commit()
            print(count)
            add_into_user_credits(email, p)
            connection.close()
        return True
    except pymysql.MySQLError as e:
        return False


def fetch_ticketing_info(email):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT b.BOOKING_ID, b.BOOKING_DATE, b.USER_EMAIL, b.ROUTE_ID, b.BUS_ID, b.SEAT_NUMBER,'
                       ' b.DEPARTURE_DATE, b.PRICE, r.SOURCE, r.DESTINATION, s.DEPARTURE_DATE_TIME,'
                       ' s.ARRIVAL_DATE_TIME FROM BOOKINGS as b, ROUTES as r, SCHEDULES as s '
                       'where b.ROUTE_ID = r.ROUTE_ID and b.BUS_ID = s.BUS_ID and '
                       'b.DEPARTURE_DATE = s.DEPARTURE_DATE_TIME and b.USER_EMAIL = %s ', (email,))
        sch = cursor.fetchall()
        connection.close()
        return sch
    except pymysql.MySQLError as e:
        return False

