from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.nudle_db


def collect_dbData( arg ):
	resp_data = {
		'req': arg,
		'results': [],
		'len': 0,
		'status': None
	}
	
	if arg['req'] == 'get-all':

		for i in db.nudles.find():
			resp_data['results'].append({ 'title': i['title'], 'forks': i['article']['data']['forks'], 'comments': i['article']['data']['comments'], 'shares': i['article']['data']['shares'], 'pic': i['article']['data']['pic'], 'info': i['info'], 'nudle-url': '/nudle/search?q=' + i['title'], 'nudle-tags': i['nudle-tags'] })
			resp_data['len']+=1

		return render_template('index.html', n_act='newsFeed', header='Global', resp=resp_data )
 	
	elif arg['req'] == 'get-tag':

		for i in db.nudles.find({ 'nudle-tags': arg['tag'] }):
			resp_data['results'].append({ 'title': i['title'], 'forks': i['article']['data']['forks'], 'comments': i['article']['data']['comments'], 'shares': i['article']['data']['shares'], 'pic': i['article']['data']['pic'], 'info': i['info'], 'nudle-url': '/nudle/search?q=' + i['title'], 'nudle-tags': i['nudle-tags'] })
			resp_data['len']+=1
		
		if resp_data['len'] == 0:
			return render_template('index.html', n_act='no_nudle', error_message="nudle tag not found for '" + arg['tag'] + "'.", req=arg['tag'])
		
		return render_template('index.html', n_act='newsFeed', header=arg['tag'], resp=resp_data )	

	elif arg['req'] == 'get-title':

		for j in db.nudles.find({'title': arg['title']}):
			return render_template('index.html', n_act='article', nudle=j)

		return render_template('index.html', n_act='no_nudle', error_message="nudle post not found for '" + arg['title'] + "'.", req=arg['title'])



def POST_to_db( arg ):

	if arg['req'] == 'insert-new_nudle':
		db.nudles.insert_one( arg['data'] )

		return jsonify({ 'url_path': '/nudle/search?q=' + arg['nudle-tag'] })


# <!-- col-sm-3 col-sm-offset-1 blog-sidebar -->


@app.route('/nudle')
def home():
	return collect_dbData({ 'req': 'get-all' })


@app.route('/nudle/<tag>')
def GET_tags( tag ):

	meta_data = request.args.get('i')

	if meta_data == 'form-box':
		return jsonify({ 'url_path': '/nudle/'+tag })

	return collect_dbData({ 'req': 'get-tag', 'tag': tag })


@app.route('/nudle/search')
def search_for_nudelpost():
	title = request.args.get('q')
	
	return collect_dbData({ 'req': 'get-title', 'title': title })


@app.route('/nudle/post_nudle/')
def POST_nudle():


	new_nudle = {
		'title': request.args.get('ttl'),
		'info': request.args.get('info'),
		'article': {
			'nudler': '@jane_deo',
			'text': request.args.get('text'),
			'data': {
				'pic': request.args.get('coverPhoto'),
				'date': '12/5/2016',
				'time': '7:40 pm',
				'forks': 0,
				'comments': 0,
				'shares': 0
			}
		},
		'nudle-tags': [ request.args.get('tag') ]
	}

	POST_to_db({ 'data': new_nudle, 'req': 'insert-new_nudle', 'nudle-tag': str( new_nudle['nudle-tags'] ) })
	
	return jsonify({ 'url_path': '/nudle/search/' + new_nudle['title'] })


app.run(host=os.getenv('IP', 'localhost'), port=int(os.getenv('PORT', 3000)),debug=True)