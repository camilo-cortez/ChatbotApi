import faker
from flask import jsonify
from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest, NotFound
import random

class GetIncidentSolutions(BaseCommand):
    def __init__(self, json):
        self.json = json

    def execute(self):
        try:
            responses = []
            num_responses = random.randrange(2, 4)
            for _ in range(num_responses):
                text: str = faker.Faker().text(max_nb_chars=200)
                responses.append({"text": text})
            return responses

        except Exception as e:
            raise NotFound
