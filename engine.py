from RandomForest.random_forest import RandomForest
import os, json

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "heroes.json")
with open(json_url, 'r') as fp:
	heroes = json.load(fp)
	hero_ids = [hero['id'] for hero in heroes]


def get_hero_human_readable(hero_id):
	for hero in heroes:
		if hero['id'] == hero_id:
			return hero['localized_name']
	return 'Unknown hero: %d' % hero_id

def main():
	# Fill these out using hero IDs (see web API)
	my_team = [76, 54]
	their_team = [5, 15, 46, 91, 13]

	print 'My Team: %s' % [get_hero_human_readable(hero_id) for hero_id in my_team]
	print 'Their Team: %s' % [get_hero_human_readable(hero_id) for hero_id in their_team]
	print 'Recommend:'

	engine = Engine(RandomForest())
	recommendations = engine.recommend(my_team, their_team)
	print [(prob, get_hero_human_readable(hero)) for prob, hero in recommendations]



class Engine:
	def __init__(self, algorithm):
		self.algorithm = algorithm

	def get_candidates(self, my_team, their_team):
		''' 
			Returns a list of hero IDs to consider for recommending.
		'''
		ids = [i for i in hero_ids if i not in my_team and i not in their_team and i not in [24, 104, 105, 108]]
		return ids

	def recommend(self, my_team, their_team, human_readable=False):
		'''
			Returns a list of (hero, probability of winning with hero added)
			recommended to complete my_team.
		'''
		assert len(my_team) <= 5
		assert len(their_team) <= 5

		hero_candidates = self.get_candidates(my_team, their_team)
		return self.algorithm.recommend(my_team, their_team, hero_candidates)

	def predict(self, dream_team, their_team):
		'''
			Returns the probability of the dream_team winning against their_team.
		'''
		return self.algorithm.predict(dream_team, their_team)


if __name__ == "__main__":
	main()
