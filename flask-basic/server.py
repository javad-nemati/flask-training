from flask import Flask, jsonify, request, url_for, redirect, session, render_template
import mariadb
import sys


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret!'


try:
    conn = mariadb.connect(
    host='127.0.0.1',
    port=3306,
    user="test",
    password='123')
except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)
    # conn.close()
cur = conn.cursor()
# cur.execute('select id,name,location from test.test1')
# results = cur.fetchall()
# print(results)
# exit()
@app.route('/viewresults')
def viewresults():
    cur.execute("SELECT * FROM test.test1")
    results = cur.fetchall()
    
    response = ""
    for (id, name, location) in results:
        response += f"The ID is : {id}, The full name is:  {name},The location is:  {location}\n"
    return response




@app.route('/')
def index():
    session.pop('name', None)
    return '<h1>Hello, World!</h1>'

@app.route('/home', methods=['POST', 'GET'], defaults={'name' : 'Default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    cur.execute('select id,name,location from test.test1')
    results = cur.fetchall()
    return render_template('home.html', name=name, DISPLAY=False, list=['one', 'two', 'three'], dict=[{'name' : 'javad'}, {'name' : 'ali'}], results=results)
    #return render_template('home2.html', results = results)

@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotinSession!'
    return jsonify({'key' : 'value', 'listkey' : [1,2,3], 'name' : name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are on the query page!</h1>'.format(name, location)

@app.route('/theform', methods=['GET', 'POST'])
def theform():

    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']
        cur.execute('insert into test.test1 (name,location) values(?, ?)', [name, location])
        conn.commit()

        #return '<h1>Hello {}. You are from {}. You have submitted the form successfully!<h1>'.format(name, location)
        return redirect(url_for('home', name=name, location=location))

'''
@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']

    return '<h1>Hello {}. You are from {}. You have submitted the form successfully!<h1>'.format(name, location)
'''
@app.route('/processjson', methods=['POST'])
def processjson():

    data = request.get_json()

    name = data['name']
    location = data['location']

    randomlist = data['randomlist']

    return jsonify({'result' : 'Success!', 'name' : name, 'location' : location, 'randomkeyinlist' : randomlist[1]})


if __name__ == "__main__":
    app.run(debug=True)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret!'