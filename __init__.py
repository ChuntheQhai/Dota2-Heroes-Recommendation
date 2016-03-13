from flask import Flask, session, render_template,request
from RandomForest.random_forest import RandomForest
from engine import Engine
import json


app = Flask(__name__)

engine = Engine(RandomForest())

#URL_PREFIX = 'http://127.0.0.1:5000'


with open('heroes.json', 'r') as fp:
	heroesData = json.load(fp)

def get_api_string(recommendations, prob):
	hero_objects = []
	for hero_id in recommendations:
	    for heroData in heroesData:
	        if heroData["id"] == hero_id:
	            hero_objects.append(heroData);
	            
	return json.dumps({'x':hero_objects,'prob_x': prob})

@app.route("/")
def index():
	return render_template('index.html', heroes=heroesData)

@app.route("/api/recommend/")
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
	app.debug = True
	app.run('0.0.0.0')
