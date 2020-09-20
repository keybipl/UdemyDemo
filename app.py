from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '&Oc?P7zBQZ1H}7y{k!a?7oD>q)qHa'


def connect_db():
    sql = sqlite3.connect('data.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite.db'):
        g.sqlite_db.close()


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'Przybyszu'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()

    return render_template('home.html', name=name, display=True, mylist = [1,2,3,4,5], listdict = [{'name': 'Kuba'}, \
                            {'name': 'Mati'}], results=results)


@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'zdupy'
    return jsonify({'key': 'value', 'listkey': [1,2,3,], 'name': name})


@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return f'<h1>Hi {name}, you are from {location}. You are on the query page</h1>'


@app.route('/theform', methods=['GET', 'POST'])
def theform():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values (?,?)', [name, location])
        db.commit()

        # return f'Hello {name}, you are from {location}'
        return redirect(url_for('home', name=name, location=location))



@app.route('/processjson', methods=['GET', 'POST'])
def processjson():
    response = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/eur/")
    data = response.json()
    kurs = data["rates"]
    lista = kurs[0]
    eur = lista['mid']
    kurs = float(eur)
    return f'Kurs: {kurs}'


@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1>The ID is {}. The name is {}. The location is {}.'.format(results[2]['id'], results[2]['name'], \
                                                                          results[2]['location'])


if __name__ == '__main__':
    app.run()
