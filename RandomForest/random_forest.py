import numpy as np
import pickle, os

NUM_HEROES = 108
NUM_FEATURES = NUM_HEROES * 2

class RandomForest:
	def __init__(self, model_root='RandomForest'):
		model_path = os.path.join(model_root, 'model.pkl')
		with open(model_path, 'r') as input_file:
			self.model = pickle.load(input_file)

	def transform(self, my_team, their_team):
		X = np.zeros(NUM_FEATURES, dtype=np.int8)
		for hero_id in my_team:
			X[hero_id - 1] = 1
		for hero_id in their_team:
			X[hero_id - 1 + NUM_HEROES] = 1
		return X


	def recommend(self, my_team, their_team, hero_candidates):
		''' Returns a list of (hero, probability of wining with hero added) recommended to complete my_team.'''
		
		team_possibilities = [(candidate, my_team + [candidate]) for candidate in hero_candidates]

		prob_candidate_pairs = []
		for candidate, team in team_possibilities:
			query = self.transform(team, their_team)
			prob = self.score(query)
			prob_candidate_pairs.append((prob, candidate))
		prob_candidate_pairs = sorted(prob_candidate_pairs, reverse=True)[0:5 - len(my_team)]
		return prob_candidate_pairs

	def score(self,query):
		radiant_query = query
		dire_query = np.concatenate((radiant_query[NUM_HEROES:NUM_FEATURES], radiant_query[0:NUM_HEROES]))
		rad_prob = self.model.predict_proba(radiant_query)[0][1]
		dire_prob = self.model.predict_proba(dire_query)[0][0]
		return (rad_prob + dire_prob) / 2

	def predict(self, dream_team, their_team):
		dream_team_query = self.transform(dream_team, their_team)
		return self.score(dream_team_query)


