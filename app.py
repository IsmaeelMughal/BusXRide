import MySQLdb
from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_mysqldb import MySQL
from flask_session import Session
import json
import DatabaseHandler

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mughal'
app.config['MYSQL_DB'] = 'ticket_booking_app'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'Its a secret'

Session(app)

mysql = MySQL(app)

busInfo = {"BusId": 0, "DepartureTime": 0, "ArrivalTime": 0, "RouteId": 0}

# session['email']
# session['username']
# session['credits']
# session['permission']


# HOME PAGE
@app.route('/')
def home_page():
    return render_template("Home.html")


# ABOUT PAGE
@app.route('/about')
def about():
    return render_template("About.html")


# CONTACT PAGE
@app.route('/contact')
def contact():
    return render_template("contact.html")


# SIGNUP PAGE
@app.route('/signup/', defaults={'error': ''})
@app.route('/signup/<error>')
def display_signup(error):
    return render_template("signup.html", error=error)


# PROCESSING FOR SIGNUP VALIDATIONS
@app.route('/signup_processing', methods=['POST', 'GET'])
def signup_process():
    if request.method == 'POST':
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        ph = request.form.get('phone')
        address = request.form.get('Address')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        credit = 0
        try:
            cursor = mysql.connection.cursor()
            count = cursor.execute("SELECT * FROM ADMINS_LOGIN WHERE ADMIN_EMAIL = %s", (email,))
            if count > 0:
                return redirect(url_for('display_signup', error="E-Mail is Already In Use!!!!"))
            cursor.execute('INSERT INTO USERS_LOGIN VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                           (email, first_name, last_name, ph, address, password, gender, credit))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('display_login'))

        except MySQLdb.Error as e:
            print(e)
            return redirect(url_for('display_signup', error="E-Mail is Already In Use!!!!"))


# LOGIN PAGE
@app.route('/login', defaults={'error': ''})
@app.route('/login/<error>')
def display_login(error):
    return render_template("login.html", error=error)


# PROCESSING FOR LOGIN PAGE VALIDATIONS
@app.route('/login_processing', methods=['POST'])
def login_processing():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session["email"] = email
        try:
            cursor = mysql.connection.cursor()
            count = cursor.execute('select * from admins_login where admin_email = %s and admin_password = %s',
                                   (email, password))
            if count > 0:
                session['permission'] = 'admin'
                return redirect(url_for('admin_dashboard'))
            else:
                count = cursor.execute('select * from users_login where user_email = %s and password = %s',
                                       (email, password))
                if count > 0:
                    session['permission'] = 'user'
                    return redirect(url_for('user_dashboard'))

                return redirect(url_for('display_login', error="Please Check Your Email and Password!!!!"))

        except MySQLdb.Error as e:
            print(e)
            return redirect(url_for('display_login', error="Server Busy!!!"))


# ADMIN DASHBOARD PAGE
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'email' in session and 'permission' in session:
        if session['permission'] == 'admin':
            return render_template('Admin.html')
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


# BUS CRUD FOR ADMIN
@app.route('/admin_dashboard/bus_crud/')
def busCrud():
    if 'email' in session and 'permission' in session:
        if session['permission'] == 'admin':
            l1 = DatabaseHandler.fetch_all_table_info('BUSES')
            l_id = DatabaseHandler.fetch_latest_id_of_buses()
            return render_template("busCrud.html", BusesRecords=l1, latestBusID=l_id)
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


# REMOVE BUS FOR ADMIN CRUD
@app.route('/admin_dashboard/bus_crud/remove_bus', methods=['POST', 'GET'])
def bus_crud_remove_bus():
    if request.method == 'POST':
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'admin':
                li = request.data.decode('UTF-8')
                li = json.loads(li)
                if DatabaseHandler.delete_record_of_bus_with_id(int(li['BUS_ID'])):
                    return redirect(url_for('busCrud'))
                else:
                    # Make Error Visible
                    return redirect(url_for('busCrud'))
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


# ADD NEW BUS FOR ADMIN CRUD
@app.route('/admin_dashboard/bus_crud/add_bus', methods=['POST', 'GET'])
def bus_crud_add_bus():
    if request.method == 'POST':
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'admin':
                li = request.data.decode('UTF-8')
                li = json.loads(li)
                if DatabaseHandler.add_bus_info(li['BUS_ID'], li['MODEL'], li['COLOR'], int(li['TICKET_PRICE'])):
                    return redirect(url_for('busCrud'))
                else:
                    # Make Error Visible
                    return redirect(url_for('busCrud'))
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


# UPDATE EXISTING BUS FOR ADMIN CRUD
@app.route('/admin_dashboard/bus_crud/update_bus', methods=['POST', 'GET'])
def bus_crud_update_bus():
    if request.method == 'POST':
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'admin':
                li = request.data.decode('UTF-8')
                li = json.loads(li)
                if DatabaseHandler.update_bus_info(li['BUS_ID'], li['MODEL'], li['COLOR'], li['TICKET_PRICE']):
                    return redirect(url_for('busCrud'))
                else:
                    # Make Error Visible
                    return redirect(url_for('busCrud'))
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


@app.route('/admin_dashboard/route_crud', defaults={'error': ''})
@app.route('/admin_dashboard/route_crud/<error>')
def routeCrud(error):
    if 'email' in session and 'permission' in session:
        if session['permission'] == 'admin':
            l1 = DatabaseHandler.fetch_all_table_info('ROUTES')
            l_id = DatabaseHandler.fetch_latest_id_of_routes()
            return render_template("routeCrud.html", routesRecords=l1, latestRouteID=l_id, error=error)
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


@app.route('/admin_dashboard/route_crud/add_route', methods=['POST', 'GET'])
def route_crud_add_route():
    if 'email' in session and 'permission' in session:
        if session['permission'] == 'admin':
            li = request.data.decode('UTF-8')
            li = json.loads(li)
            if DatabaseHandler.add_routes_info(li['ROUTE_ID'], li['SOURCE'], li['DESTINATION']):
                return redirect(url_for('routeCrud', error="Route Added Successfully!!!"))
            else:
                # make Error Visible
                return redirect(url_for('routeCrud'))
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


# REMOVE ROUTE FOR ADMIN CRUD
@app.route('/admin_dashboard/route_crud/remove_route', methods=['POST', 'GET'])
def route_crud_remove_route():

    if 'email' in session and 'permission' in session:
        if session['permission'] == 'admin':
            li = request.data.decode('UTF-8')
            li = json.loads(li)
            if DatabaseHandler.delete_record_of_route_with_id(li['ROUTE_ID']):
                return redirect(url_for('routeCrud'))
            else:
                # make Error Visible
                return redirect(url_for('routeCrud'))
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


# UPDATE EXISTING BUS FOR ADMIN CRUD
@app.route('/admin_dashboard/route_crud/update_route', methods=['POST', 'GET'])
def route_crud_update_route():
    if request.method == 'POST':
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'admin':
                li = request.data.decode('UTF-8')
                li = json.loads(li)
                if DatabaseHandler.update_route_info(li['ROUTE_ID'], li['SOURCE'], li['DESTINATION']):
                    return redirect(url_for('routeCrud'))
                else:
                    # Make Error Visible
                    return redirect(url_for('routeCrud'))
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


# SCHEDULE CRUD FOR ADMIN
@app.route('/admin_dashboard/schedule_crud/', defaults={'error': ''})
@app.route('/admin_dashboard/schedule_crud/<error>', methods=['GET'])
def schedule_crud(error):
    if 'email' in session and 'permission' in session:
        if session['permission'] == 'admin':
            connection = DatabaseHandler.get_connection()
            cursor = connection.cursor()
            l1 = DatabaseHandler.fetch_all_table_info('SCHEDULES')
            cursor.execute('SELECT BUS_ID FROM BUSES')
            buses = cursor.fetchall()
            cursor.execute('SELECT ROUTE_ID FROM ROUTES')
            routes = cursor.fetchall()
            cursor.close()
            connection.close()
            l_id = DatabaseHandler.fetch_latest_id_of_buses()
            return render_template("scheduleCrud.html", scheduleRecords=l1, latestBusID=l_id,
                                   buses=buses, routes=routes, error=error)
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


# ADD SCHEDULE CRUD FOR ADMIN
@app.route('/admin_dashboard/schedule_crud/add_schedule', methods=['POST', 'GET'])
def schedule_crud_add_schedule():
    if request.method == 'POST':
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'admin':
                li = request.data.decode('UTF-8')
                li = json.loads(li)
                if DatabaseHandler.add_schedule_info(li['BUS_ID'], li['DEPARTURE_DATE_TIME'],
                                                     li['ARRIVAL_DATE_TIME'], li['ROUTE_ID']):
                    return redirect(url_for('schedule_crud', error="Route Added Successfully!!!"))
                else:
                    # make Error Visible
                    return redirect(url_for('schedule_crud'))

            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


# DELETE SCHEDULE CRUD FOR ADMIN
@app.route('/admin_dashboard/schedule_crud/delete_schedule', methods=['POST', 'GET'])
def schedule_crud_delete_schedule():
    if request.method == 'POST':
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'admin':
                li = request.data.decode('UTF-8')
                li = json.loads(li)
                if DatabaseHandler.delete_record_of_schedule(li['ROUTE_ID'], li['DEPARTURE_DATE_TIME'],
                                                             li['BUS_ID']):
                    flash("Schedule Deleted Successfully")
                    return redirect(url_for('schedule_crud', error="Route DELETED Successfully!!!"))
                else:
                    # make Error Visible
                    return redirect(url_for('schedule_crud', error="FAILED To Delete Route!!!"))
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


# UPDATE SCHEDULE CRUD FOR ADMIN
@app.route('/admin_dashboard/schedule_crud/update_schedule', methods=['POST', 'GET'])
def schedule_crud_update_schedule():
    if request.method == 'POST':
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'admin':
                li = request.data.decode('UTF-8')
                li = json.loads(li)
                if DatabaseHandler.update_schedule_info(li['BUS_ID'], li['DEPARTURE_DATE_TIME'],
                                                        li['ARRIVAL_DATE_TIME'], li['ROUTE_ID'], li['old_busId'],
                                                        li['oldD-dt'], li['oldRoute_id']):
                    return redirect(url_for('schedule_crud', error="Route Updated Successfully!!!"))
                else:
                    # make Error Visible
                    return redirect(url_for('schedule_crud', error="FAILED To Update Route!!!"))
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


#################################################################################
# USER DASHBOARD PAGE
@app.route('/user_dashboard')
def user_dashboard():
    if 'email' in session and 'permission' in session:
        if session['permission'] == 'user':
            u_data = DatabaseHandler.fetch_username_from_user_email(session['email'])
            fullname = u_data['FIRSTNAME'] + ' ' + u_data['LASTNAME']
            credit = u_data['CREDITS']
            session['username'] = fullname
            session['credits'] = credit
            return render_template('User.html', loginUserName=fullname, credit=credit)
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


@app.route('/user_dashboard/buy_ticket')
def display_buy_ticket():
    if 'email' in session and 'permission' in session:
        if session['permission'] == 'user':
            connection = DatabaseHandler.get_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM ROUTES')
            result = cursor.fetchall()
            l1 = result
            sources = []
            destination = []
            for d in l1:
                sources.append(d['SOURCE'])
                destination.append(d['DESTINATION'])
            routes = {
                "sources": sources,
                "destination": destination
            }
            with open('static/BuyTicket.js', 'w') as out_file:
                with open('static/jscode.js', 'r') as firstfile:
                    out_file.write('var graph = %s;' % json.dumps(routes))
                    lines = firstfile.readlines()
                    out_file.writelines(lines)
                    firstfile.close()
                    out_file.close()
            return render_template("BuyTicket1.html")
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


@app.route("/user_dashboard/buy_ticket/schedules", methods=["GET", "POST"])
def user_buy_ticket_schedule():
    if request.method == "POST":
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'user':
                source = request.form["source"]
                des = request.form["destination"]
                date = request.form["date"]
                r_id = DatabaseHandler.get_route_id(source, des)
                l1 = DatabaseHandler.get_schedules_for_user(date, r_id)
                return render_template("BuyTicket2.html", d1=l1, source=source, destination=des)
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


@app.route("/user_dashboard/buy_ticket/schedules/tickets", methods=["GET", "POST"])
def select_tickets_to_buy():
    if request.method == "POST":
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'user':
                res = request.get_data("data")
                RowInfo = json.loads(res)
                global busInfo
                busInfo['BusId'] = RowInfo['BusID']
                busInfo['DepartureTime'] = RowInfo['DepartureTime']
                busInfo['ArrivalTime'] = RowInfo['ArrivalTime']
                busInfo['RouteId'] = RowInfo['RouteID']
                t_price = DatabaseHandler.get_ticket_price(busInfo['BusId'])
                occupied_seats = DatabaseHandler.fetch_booked_seats(busInfo['BusId'],
                                                                    busInfo['RouteId'], busInfo['DepartureTime'])
                return render_template("bus.html", ticketPrice=t_price,
                                       seatArray=occupied_seats, userAccountBalance=session['credits'])
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))

    else:
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'user':
                t_price = DatabaseHandler.get_ticket_price(busInfo['BusId'])
                occupied_seats = DatabaseHandler.fetch_booked_seats(busInfo['BusId'],
                                                                    busInfo['RouteId'], busInfo['DepartureTime'])
                return render_template("bus.html", ticketPrice=t_price,
                                       seatArray=occupied_seats, userAccountBalance=session['credits'])
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


@app.route('/user_dashboard/buy_ticket/schedules/tickets/buy_tickets', methods=['POST', 'GET'])
def buy_bus_tickets():
    if request.method == "POST":
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'user':
                output = request.get_json()
                seats = json.loads(output)
                t_price = DatabaseHandler.get_ticket_price(busInfo['BusId'])
                DatabaseHandler.add_bookings(session['email'], busInfo['BusId'], busInfo['RouteId'],
                                             busInfo['DepartureTime'], seats, t_price)
                session['credits'] = session['credits'] - (t_price * len(seats))
                return render_template("User.html")
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))
    else:

        if 'email' in session and 'permission' in session:
            if session['permission'] == 'user':
                t_price = DatabaseHandler.get_ticket_price(busInfo['BusId'])
                occupied_seats = DatabaseHandler.fetch_booked_seats(busInfo['BusId'],
                                                                    busInfo['RouteId'], busInfo['DepartureTime'])
                return render_template("bus.html", ticketPrice=t_price, seatArray=occupied_seats,
                                       userAccountBalance=session['credits'])
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


@app.route('/user_dashboard/refund_schedule')
def display_refund_schedule():
    if 'email' in session and 'permission' in session:
        if session['permission'] == 'user':
            l1 = DatabaseHandler.fetch_all_table_info('ROUTES')
            sources = []
            destination = []
            for d in l1:
                sources.append(d['SOURCE'])
                destination.append(d['DESTINATION'])
            routes = {
                "sources": sources,
                "destination": destination
            }
            with open('static/BuyTicket.js', 'w') as out_file:
                with open('static/jscode.js', 'r') as firstfile:
                    out_file.write('var graph = %s;' % json.dumps(routes))
                    lines = firstfile.readlines()
                    out_file.writelines(lines)
                    firstfile.close()
                    out_file.close()
            return render_template("refund1.html")
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


@app.route("/user_dashboard/refund_schedule/select_refund", methods=["GET", "POST"])
def select_refund_option():
    if request.method == "POST":
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'user':
                source = request.form["source"]
                des = request.form["destination"]
                date = request.form["date"]
                r_id = DatabaseHandler.get_route_id(source, des)
                l1 = DatabaseHandler.get_schedules_for_user(date, r_id)
                return render_template("refund2.html", d1=l1, source=source, destination=des)
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


@app.route("/RowInfo", methods=["GET", "POST"])
def RowInfo():
    if request.method == "POST":
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'user':
                res = request.get_data("data")
                RowInfo = json.loads(res)
                global busInfo
                busInfo['BusId'] = RowInfo['BusID']
                busInfo['DepartureTime'] = RowInfo['DepartureTime']
                busInfo['ArrivalTime'] = RowInfo['ArrivalTime']
                busInfo['RouteId'] = RowInfo['RouteID']
                return render_template("User.html", loginId="Dummy", credit="5000")
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


@app.route('/user_dashboard/refund_schedule/select_refund/seats', methods=['POST', 'GET'])
def refund():
    # /here you will get refunded seat numbers
    if request.method == "POST":
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'user':
                output = request.get_json()
                result = json.loads(output)
                t_price = DatabaseHandler.get_ticket_price(busInfo['BusId'])
                DatabaseHandler.remove_bookings(session['email'], busInfo['BusId'], busInfo['RouteId'],
                                                busInfo['DepartureTime'], result['refundList'], t_price)
                session['credits'] = session['credits'] + (t_price * len(result['refundList']))
                return render_template("User.html", credit=session['credits'])
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))
    else:
        # here by busInfo u can get selected bus data that has been selected for refund
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'user':
                t_price = DatabaseHandler.get_ticket_price(busInfo['BusId'])
                occupied_seats = DatabaseHandler.fetch_booked_seats(busInfo['BusId'],
                                                                    busInfo['RouteId'], busInfo['DepartureTime'])
                user_selected = DatabaseHandler.fetch_user_selected_seats(session['email'], busInfo['BusId'],
                                                                          busInfo['RouteId'], busInfo['DepartureTime'])
                for i in user_selected:
                    occupied_seats.remove(i)
                return render_template("refund.html", ticketPrice=t_price, selectedSeatsArray=user_selected,
                                       userAccountBalance=session['credits'], occupiedSeatsArray=occupied_seats)
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


@app.route('/user_dashboard/generate_tickets')
def GenerateTicket():
    if 'email' in session and 'permission' in session:
        if session['permission'] == 'user':
            result = DatabaseHandler.fetch_ticketing_info(session['email'])
            return render_template("GenerateTicket.html", d1=result)
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


@app.route('/user_dashboard/generate_tickets/ticket')
def display_ticket():
    if 'email' in session and 'permission' in session:
        if session['permission'] == 'user':
            return render_template("GenerateTicket2.html")
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


@app.route('/user_dashboard/add_user_credits')
def add_user_credits():
    if 'email' in session and 'permission' in session:
        if session['permission'] == 'user':
            if 'username' in session and 'credits' in session:
                return render_template("AddCredit.html", name=session['username'], credit=session['credits'])
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))
    else:
        return redirect(url_for('display_login'))


@app.route('/user_dashboard/add_user_credits/add_credits', methods=['POST'])
def add_credits():
    if request.method == 'POST':
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'user':
                if 'email' in session:
                    cr = request.form.get('credit')
                    old_cr = DatabaseHandler.add_into_user_credits(session['email'], cr)
                    if old_cr:
                        session['credits'] = old_cr - 1 + int(cr)
                        return redirect(url_for('add_user_credits'))
                    else:
                        return redirect(url_for('add_user_credits'))
                else:
                    return redirect(url_for('display_login'))
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


@app.route('/user_dashboard/add_user_credits/withdraw_credits', methods=['POST'])
def withdraw_credits():
    if request.method == 'POST':
        if 'email' in session and 'permission' in session:
            if session['permission'] == 'user':
                if 'email' in session:
                    cr = request.form.get('E-credit')
                    old_cr = DatabaseHandler.withdraw_user_credits(session['email'], cr)
                    if old_cr:
                        session['credits'] = old_cr - 1 - int(cr)
                        return redirect(url_for('add_user_credits'))
                    else:
                        return redirect(url_for('add_user_credits'))
                else:
                    return redirect(url_for('display_login'))
            else:
                return redirect(url_for('display_login'))
        else:
            return redirect(url_for('display_login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_page'))


@app.route('/switch')
def switch_user():
    session.clear()
    return redirect(url_for('display_login'))


if __name__ == "__main__":
    app.run(debug=True)
