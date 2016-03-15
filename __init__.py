from flask import Flask, render_template,request
from RandomForest.random_forest import RandomForest
from engine import Engine
import json, os, time
from pymongo import MongoClient
import logging

#client = MongoClient(os.getenv('DOTABOT_DB_SERVER', 'localhost'), 27017)
#db = client[os.getenv('DOTABOT_DB_NAME', 'dota2')]
client = MongoClient("127.0.0.1", 27017)
db = client["dota2"]
match_collection = db.matches

logger = logging.getLogger(__name__)
#logger.log(match_collection)
#logger.log(db)
#logger.log(client)
#logger.log(os.getenv('DOTABOT_DB_SERVER','localhost'))


application = Flask(__name__)

engine = Engine(RandomForest())

#URL_PREFIX = 'http://127.0.0.1:5000'

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_path = os.path.join(SITE_ROOT,"heroes.json")

with open(json_path, 'r') as fp:
	heroesData = json.load(fp)

def get_api_string(recommendations, prob):
	hero_objects = []
	for hero_id in recommendations:
	    for heroData in heroesData:
	        if heroData["id"] == hero_id:
	            hero_objects.append(heroData);
	            
	return json.dumps({'x':hero_objects,'prob_x': prob})

@application.route("/")
def index():
	#return render_template('starter.html')
	return render_template('index.html', heroes=heroesData)

@application.route("/stats")
def stats():
	most_recent_match_id = 0
	for post in match_collection.find({}).sort('_id', direction=-1).limit(1):
		most_recent_match_id = post['match_id']
		most_recent_match_time = post['start_time']

	total_matches = match_collection.count()
	human_readable_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime(most_recent_match_time))

	disk_stats = os.statvfs('/')
	mb_remaining = disk_stats.f_bavail * disk_stats.f_frsize/1024.0/1024.0/1024.0
	return render_template('stats.html',total_matches=total_matches, most_recent_match_id=most_recent_match_id, human_readable_time=human_readable_time, mb_remaining=mb_remaining)

@application.route("/api/recommend/")
def api():
	if 'x' not in request.args or 'y' not in request.args:
		return 'Invalid request'

	my_team = request.args['x'].split(',')
	if len(my_team) == 1 and my_team[0] == '':
	 	my_team = []
	else:
	 	my_team = map(int, my_team)

	their_team = request.args['y'].split(',')
	if len(their_team) == 1 and their_team[0] == '':
		their_team = []
	else:
		their_team = map(int, their_team)

	print my_team
	print their_team

	prob_recommendation_pairs = engine.recommend(my_team, their_team)
	recommendations = [hero for prob, hero in prob_recommendation_pairs]
	prob = engine.predict(my_team, their_team)

	print prob
	return get_api_string(recommendations, prob)

if __name__ == "__main__":
	application.debug = True
	application.run(host='0.0.0.0')
