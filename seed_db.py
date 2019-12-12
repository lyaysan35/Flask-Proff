
import json
import models


def populate_db():
	with open('./proffs.json', 'r') as f:
		professionals_data = json.load(f)
		professionals = professionals_data['data']

	for professional in professionals:
		models.Professional.create(**professional)