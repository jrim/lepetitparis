
#imports
from __future__ import with_statement
from contextlib import closing
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template,request,session,g,redirect,url_for,flash,abort

#configuration
DATABASE = './paris.db'
DEBUG = True
SECRET_KEY ='development key'
USERNAME = 'jrim'
PASSWORD = 'jrim'


app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def show_entries():
	cur=g.db.execute('select title,text from entries order by id desc')
	entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html',entries=entries)

@app.route('/add',methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title,text) values(?,?)',
		[request.form['title'],request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/send_next',methods=['POST'])
def send_next():
	if(request.form['score1']>0):
		if(request.form['score2']>0):
			if(request.form['score3']>0):
				trend="+++"
			else:
				trend="++-"
		else:
			if(request.form['score3']>0):
				trend="+-+"	
			else:
				trend="+--"
	else:
		if(request.form['score2']>0):
			if(request.form['score3']>0):
                                trend="-++"
                        else:
                                trend="-+-"
		else:
                        if(request.form['score3']>0):
                                trend="--+"     
                        else:
                                trend="---"

	g.db.execute('insert into userinfo (username,s1,s2,s3,trend) values(?,?,?,?,?)',
		[request.form['username'],request.form['score1'],request.form['score2'],request.form['score3'],trend])
	g.db.commit()
	
	flash('Test END')
	return redirect(url_for('taste_result'))

@app.route('/taste_result')
def taste_result():
	cur=g.db.execute('select username,s1,s2,s3,trend from userinfo order by id desc')
	userinfo = [dict(username=row[0],s1=row[1],s2=row[2],s3=row[3],trend=row[4]) for row in cur.fetchall()]
	return render_template('taste_result.html',userinfo=userinfo)

@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/login',methods=['GET','POST'])
def login():
	error=None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'livalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'wrong password'
		else:
			session['logged_in']=True
			flash('logged in , welcome')
			return redirect(url_for('show_entries'))
	return render_template('login.html',error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('logged out, Bye')
	return redirect(url_for('show_entries'))


@app.route('/direction')
def direction():
	cur=g.db.execute('select * from museum')
	museum = [dict(name=row[1],trend=row[2],latitude=row[3],longtitude=row[4],extra=row[5]) for row in cur.fetchall()]
	return render_template('direction.html',museum=museum)


@app.route('/about')
def about():
	return render_template('about.html')

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()




if __name__ == '__main__':
	init_db()
	app.run(debug=True)
    
