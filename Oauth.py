



def Oauth_user():

	# @app.route('/nudle/Oauth', methods=['GET', 'POST'])
	# def home():
	
	# checking if the duser is logged in 
	if g.user:
		return redirect( url_for('newsfeed') )

	# getting the user username and password
	elif request.method == 'POST':
		

		username = request.form['username']
		password = request.form['password']

		# takes thhe user off the session
		# session.pop('user', None)

		# iterating over user accounts
		for i in users:

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
	
	
	# @app.route('/newsfeed')
	# def newsfeed():
	
	# 	# checks if the user is logged in
	# 	if g.user:
	# 		return render_template('newsfeed.html', user=session['user'], profile_img=users[0]['img'])
	
	# 	# if not then redirect thm to the sigin and login page
	# 	return redirect( url_for('home') )
	
	# @app.before_request
	# def before_request():
		
	# 	# makes a global variable	
	# 	g.user = None
	
	# 	# the checks to see if a user is in session
	# 	if 'user' in session:
	
	# 		# if not makes the session avriable to gloabl user variable
	# 		g.user = session['user']
	
	# # drops sessions made by the user or logout of the account
	# @app.route('/dropsession')
	# def dropsession():
		
	# 	# drops session 
	# 	session.pop('user', None)
	
	# 	# redirects the to the home page
	# 	return redirect( url_for('home') )

if __name__ == '__main__':
	app.run(debug=True)