from flask import Flask, render_template
import MySQLdb
app = Flask(__name__)


# Open database connection
db = MySQLdb.connect("localhost","root","0684","moshouse" )

# prepare a cursor object using cursor() method
cursor = db.cursor()
sql = "SELECT * FROM dog" 
try:
   # Execute the SQL command
   cursor.execute(sql)
   resultset = list(cursor.fetchall());
except:
   print ("Error: unable to fecth data")

occupancy = len(resultset);
homeval = 'home';

@app.route('/')
@app.route('/' + homeval)

def hello():
    return render_template('index.html', posts=resultset,ocp=occupancy)


@app.route('/about')
def about():
    return '<h1>Information Page!</h1>'


if __name__ == '__main__':
    app.run(debug=True)

