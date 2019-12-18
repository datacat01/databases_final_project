from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime
from models import User
from service import Dishes, Clients, Tables, Reservations, Orders, Order_Item, Sales
from graphs import GenerateGraphs
from checks import is_number, is_phone_num

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'DM8vT6VetDLyCZVL'



@app.route('/', methods=['GET', 'POST'])
def index():
    if 'loggedin' not in session:
        return redirect(url_for('sign_in'))
    
    if request.method == 'POST' and 'logout' in request.form:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('email', None)
        session.pop('username', None)
        return redirect(url_for('sign_in'))
    
    s = Sales(session['id'])
    o = Orders(session['id'])

    gr = GenerateGraphs(session['id'])
    gr.set_sales_data(s.get_table())
    gr.sales_lineplot()
    gr.set_orders_data(o.get_table())
    gr.av_time()
    t = gr.orders_per_day()
    
    data = {
        "path_sales_stats": f"../static/images/charts/sales_statistics_overview_{session['id']}.png",
        "path_orders_per_day": f"../static/images/charts/ordrs_per_day_{session['id']}.png",
        "path_av_time": f"../static/images/charts/av_time_{session['id']}.png",
        'total_revenue': s.get_income(),
        'stats_time': t
    }

    try: 
        return render_template('index.html', usr_name=session['username'], email=session['email'], data=data)
    except KeyError:
        return redirect(url_for('sign_in'))



@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if ('name' in request.form and 'password' in request.form
            and 'organization_name' in request.form and 'email' in request.form):
                name = request.form['name']
                password = request.form['password']
                email = request.form['email']
                organization_name = request.form['organization_name']
                u = User()
                u.add_usr(email, name, organization_name, password)
                return redirect(url_for('sign_in'))
    return render_template('pages/sign_up.html')



@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    msg=''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        u = User()
        login_status, usr_id, usr_name = u.validate_password(email, password)
        if login_status is True:
            del(u)
            session['loggedin'] = True
            session['id'] = usr_id
            session['username'] = usr_name
            session['email'] = email
            return redirect(url_for('index'))
        else:
            msg = 'Failed to login. Incorrect email/password'
    return render_template('pages/sign_in.html', msg=msg)



@app.route('/sales', methods=['GET', 'POST'])
def sales():
    sales = Sales(session['id'])
    data = {
        'orders_count': sales.get_table_size(),
        'sales_tbl': sales.get_table()
    }
    if 'loggedin' not in session:
        return redirect(url_for('sign_in'))
    return render_template('pages/sales.html', usr_name=session['username'], email=session['email'], data=data)



@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if 'loggedin' not in session:
        return redirect(url_for('sign_in'))
    
    ordr = Orders(session['id'])
    ordr_item = Order_Item(session['id'])
    data = {
        'orders_count': ordr.get_table_size(),
        'orders_table': ordr.get_table(),
        'ordr_add_msg': '',
        'ordr_item_add_msg': '',
        'ord_id_ord_itm': None
    }

    if 'reserv_id' in request.form:
        prev_reserv = request.form['reserv_id']

    if request.method == 'POST' and 'ord_id_ord_itm' in request.form:
        data['ord_id_ord_itm'] = request.form['ord_id_ord_itm']
        data['ordr_item_get'] = ordr_item.get_items_for_order(request.form['ord_id_ord_itm'])
    
    if 'ord_id_ord_itm_add' in request.form and 'dish_id_ord_itm_add' in request.form and 'amount_ord_itm_add' in request.form:
        ordr_item.add_order_item(request['ord_id_ord_itm_add'], request['ord_id_ord_itm_add'], request['amount_ord_itm_add'])
    
    if (request.method == 'POST' and 'price' in request.form
            and 'ordr_time' in request.form and 'pmnt_time' in request.form):
        if 'reserv_id' in request.form and prev_reserv != request.form['reserv_id']:
            prev_reserv = request.form['reserv_id']
            return render_template('pages/sign_up.html')
            ordr_add_msg = ordr.add_order(request.form['reserv_id'], request.form['price'], request.form['ordr_time'], request.form['pmnt_time'])
        else:
            ordr_add_msg = ordr.add_order(None, request.form['price'], request.form['ordr_time'], request.form['pmnt_time'])

    return render_template('pages/orders.html', usr_name=session['username'], email=session['email'], data=data)



@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    if 'loggedin' not in session:
        return redirect(url_for('sign_in'))
    
    tbl = Tables(session['id'])
    rsrv = Reservations(session['id'])
    data = {
        'tables_count': tbl.get_table_size(),
        'table': tbl.get_table(),
        'tbl_add_msg': '',
        'tbl_rm_msg': '',
        'rsrv_add_msg': '',
        'reserv_tbl': rsrv.get_table(),
        'rsrv_count': tbl.get_table_size()
    }

    if request.method == 'POST' and 'tbl_add' in request.form:
        data['tbl_add_msg'] = tbl.add_table(request.form['tbl_add'])
    
    if request.method == 'POST' and 'tbl_id_rm' in request.form:
        data['tbl_rm_msg'] = tbl.rm_table(request.form['tbl_id_rm'])
    
    if (request.method == 'POST' and 'rsrv_cli_name' in request.form and 'rsrv_cli_phone' in request.form and
            'rsrv_pers_count' in request.form and 'rsrv_time_from' in request.form and 'rsrv_time_to' in request.form):
        try:
            time_from = datetime.strptime(request.form['rsrv_time_from'][2:], '%y-%m-%d %H:%M')
            time_to = datetime.strptime(request.form['rsrv_time_to'][2:], '%y-%m-%d %H:%M')
            data['rsrv_add_msg'] = rsrv.add_reservation(request.form['rsrv_cli_name'], request.form['rsrv_cli_phone'], request.form['rsrv_pers_count'], time_from, request.form['rsrv_time_to'])
        except ValueError:
            data['rsrv_add_msg'] = 'Error. Invalid dates '

    return render_template(
        'pages/reservations.html',
        usr_name=session['username'],
        email=session['email'],
        data=data)



@app.route('/clients', methods=['GET', 'POST'])
def clients():
    if 'loggedin' not in session:
        return redirect(url_for('sign_in'))
    requested_data = {}
    cl = Clients(session['id'])
    if request.method == 'POST' and 'phone' in request.form:
        requested_data['client_info'] = cl.get_client_info(request.form['phone'])
    if request.method == 'POST' and 'cli_id' in request.form and is_number(request.form['cli_id']) is not False:
        cli_id = is_number(request.form['cli_id'])
        requested_data['client_info'] = cl.get_client_info(cli_id)
    if request.method == 'POST' and 'new_client_name' in request.form and 'new_client_phone' in request.form:
        if is_phone_num(request.form['new_client_phone']) is True:
            cl.add_client(request.form['new_client_name'], request.form['new_client_phone'])
            requested_data['client_add'] = (request.form['new_client_name'], 'Success')
        else:
            requested_data['client_add'] = (request.form['new_client_name'], 'Invalid phone num')
    return render_template(
        'pages/clients.html',
        usr_name=session['username'],
        email=session['email'],
        data=requested_data)



@app.route('/dishes', methods=['GET', 'POST'])
def dishes():
    if 'loggedin' not in session:
        return redirect(url_for('sign_in'))
    requested_data = {}
    d = Dishes(session['id'])
    if request.method == 'POST' and 'dish_name' in request.form:
        requested_data['dish_name'] = request.form['dish_name']
        requested_data['dish_info'] = d.get_dish_info(request.form['dish_name'])
    if request.method == 'POST' and 'new_dish_name' in request.form and 'new_dish_price' in request.form:
        if is_number(request.form['new_dish_price']) is not False:
            d.add_dish(request.form['new_dish_name'], request.form['new_dish_price'])
            requested_data['dish_add'] = (request.form['new_dish_name'], 'Success!')
        else:
            requested_data['dish_add'] = (request.form['new_dish_name'], f"{request.form['new_dish_price']} is not a number.")
    return render_template(
        'pages/dishes.html',
        usr_name=session['username'],
        email=session['email'],
        data=requested_data)




if __name__ == "__main__":
    app.run(debug=True)