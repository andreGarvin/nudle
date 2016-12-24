from flask import Flask, session, render_template, redirect, request, g, url_for, jsonify
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)
#  the cookie encrytion
app.secret_key = os.urandom(24)

# connection to monogodb 
client = MongoClient('localhost', 27017)
db = client.nudle_db

# checks to see if the user is logged in or is on a session
@app.before_request
def before_request():
	
	# makes a global variable	
	g.user = None

	# the checks to see if a user is in session
	if 'user' in session:

		# if not makes the session avriable to gloabl user variable
		g.user = session['user']



def collect_dbData( arg ):
	
	
	resp_data = {
		'req': arg,
		'header': '',
		'results': [],
		'len': 0,
		'status': None,
		'acc': g.user
	}
	
	# getting all nudles in db
	if arg['req'] == 'get-all':

		for i in db.nudles.find():
			resp_data['results'].append({ 'title': i['title'], 'forks': int( i['article']['data']['forks'] ), 'comments': int( i['article']['data']['comments'] ), 'shares': int( i['article']['data']['shares'] ), 'pic': i['article']['data']['pic'], 'info': i['info'], 'nudle-url': '/nudle/search?q=' + i['title'], 'nudle-tags': i['nudle-tags'] })
			resp_data['len']+=1
		
		resp_data['header'] = 'Global'
		
		return resp_data
 	
 	# getting a groups of ndules with certain tag in db
	elif arg['req'] == 'get-tag':

		for i in db.nudles.find({ 'nudle-tags': arg['tag'] }):
			resp_data['results'].append({ 'title': i['title'], 'forks': int( i['article']['data']['forks'] ), 'comments': int( i['article']['data']['comments'] ), 'shares': int( i['article']['data']['shares'] ), 'pic': i['article']['data']['pic'], 'info': i['info'], 'nudle-url': '/nudle/search?q=' + i['title'], 'nudle-tags': i['nudle-tags'] })
			resp_data['len']+=1
		
		return resp_data

	# searching for a nudle in the db with the title
	elif arg['req'] == 'get-title':

		for j in db.nudles.find({'title': arg['title']}):
			# if j['title'].lower()[0:len(arg['title'])] == arg['title'].lower():
			return render_template('nudle.html', nudle=j)

		return render_template('nudle_error.html', error_message="nudle post not found for '" + arg['title'] + "'.", req=arg['title'])
    
    # elif arg['req'] == 'grab':
    	# results = {
		#  		'nudles': [],
		#  		'tags': []
		#  	}
    	
		#  	for ns, nt in zip( db.nudles.find({'title': arg['req-data']}), db.nudles.find({'tag': arg['req-data']}) ) :
		# 	results.append({ 'type': 'story', 'title': ns['title'], 'forks': int( ns['article']['data']['forks'] ), 'comments': int( ns['article']['data']['comments'] ), 'shares': int( ns['article']['data']['shares'] ), 'pic': ns['article']['data']['pic'], 'info': ns['info'], 'nudle-url': '/nudle/search?q=' + ns['title'], 'nudle-tags': ns['nudle-tags'] })
		# 	results.append({ 'type': 'tag', 'title': nt['title'], 'forks': int( nt['article']['data']['forks'] ), 'comments': int( nt['article']['data']['comments'] ), 'shares': int( nt['article']['data']['shares'] ), 'pic': nt['article']['data']['pic'], 'info': nt['info'], 'nudle-url': '/nudle/search?q=' + nt['title'], 'nudle-tags': i['nudle-tags'] })
		
		
		# return jsonify({ 'results': results, 'req-data': arg['req-data'], 'len': int( results )  })


# posting new nudle in db
def POST_to_db( arg ):

	if arg['req'] == 'insert-new_nudle':
		db.nudles.insert_one( arg['data'] )

		return jsonify({ 'url_path': '/nudle/search?q=' + arg['nudle-tag'] })


# gets newsfeed
@app.route('/nudle')
def newsfeed():
	
	return render_template('newsfeed.html', header='Global', resp=collect_dbData({ 'req': 'get-all' }) )


# gets tags
@app.route('/nudle/<tag>')
def GET_tags( tag ):

	meta_data = request.args.get('i')

	if meta_data == 'form-box':
		return jsonify({ 'url_path': '/nudle/'+tag })

	results = collect_dbData({ 'req': 'get-tag', 'tag': tag })
	
	if results['len'] == 0:
		return render_template('nudle_error.html', error_message="nudle tag not found for '" + tag + "'.", req=tag )
		
	return render_template('newsfeed.html', header=tag, resp=results )	

# gets nudle
@app.route('/nudle/search')
def search_for_nudelpost():
	title = request.args.get('q')
	
	return collect_dbData({ 'req': 'get-title', 'title': title })


@app.route('/nudle/search/advanced')
def advancedSearch():
	
	req = request.args.get('q')
	
	return collect_dbData({ 'req': 'grab', 'req-data': req })


# posts nudle
@app.route('/nudle/post_nudle/')
def POST_nudle():
	today = datetime.date.today()

	new_nudle = {
		'title': request.args.get('ttl'),
		'info': request.args.get('info'),
		'article': {
			'nudler': '@jane_deo',
			'text': request.args.get('text'),
			'data': {
				'pic': request.args.get('coverPhoto'),
				'date': str( today.ctime() ).split(' ')[0] +' '+ str( today.ctime() ).split(' ')[1] +': '+ int( str( today ).split('-')[1] ) - 1 +' , '+ str( today.ctime() ).split(' ')[4] ,
				'time': str( datetime.time() ),
				'forks': 0,
				'comments': 0,
				'shares': 0
			}
		},
		'nudle-tags': [ request.args.get('tag') ]
	}
	
	POST_to_db({ 'data': new_nudle, 'req': 'insert-new_nudle', 'nudle-tag': str( new_nudle['nudle-tags'] ) })
	
	return jsonify({ 'url_path': '/nudle/search/' + new_nudle['title'] })


# login/Oauth page
@app.route('/nudle/Oauth/join', methods=['GET', 'POST'])
def nudleOauth():
	
	# checking if the duser is logged in 
	if g.user:
		return redirect( url_for('newsfeed') )

	# getting the user username and password
	elif request.method == 'POST':
		

		username = request.form['username']
		password = request.form['password']

		# # takes thhe user off the session
		session.pop('user', None)

		# iterating over user accounts
		for i in db.nudlers.find():
			print( i )
			# checking id the username exist
			if i['username'] == username:

				# checking if password exist
				if i['password'] == password:

					# making a session for the user
					session['user'] = username
					
					# redireccting to the user to newsfeed.html
					return redirect( url_for('newsfeed') )
	
	# else if anythonggoes go wrong then redircet them aback to the sigin/ login page
	return render_template('Oauth.html')

# drops sessions made by the user or logout of the account
@app.route('/nudle/Oauth/drop')
def dropsession():
		
	# drops session 
	session.pop('user', None)
	
	# redirects the to the home page
	return redirect( url_for('newsfeed') )

app.run(host=os.getenv('IP', 'localhost'), port=int(os.getenv('PORT', 3000)),debug=True)