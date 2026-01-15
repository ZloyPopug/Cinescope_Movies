import random

from faker import Faker

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_movie_name():
        return f"{faker.catch_phrase()}"

    @staticmethod
    def generate_random_image_url():
        return f"{faker.url()}"

    @staticmethod
    def generate_random_price():
        return random.randint(100, 1000)

    @staticmethod
    def generate_random_description():
        return f"{faker.catch_phrase()}"

    @staticmethod
    def generate_random_location():
        return random.choice(["MSK","SPB"])

    @staticmethod
    def generate_random_published():
        return random.choice([True,False])

    @staticmethod
    def generate_random_genreId():
        return random.randint(1,10)

