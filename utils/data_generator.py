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
    def generate_random_genreId(exclude_genre_id=None):
        genre_ids = list(range(1, 10))

        if exclude_genre_id is not None and exclude_genre_id in genre_ids:
            genre_ids.remove(exclude_genre_id)
        return random.choice(genre_ids)

    @staticmethod
    def generate_movie_data(exclude_genre_id=None):
        return {
            "name": DataGenerator.generate_random_movie_name(),
            "imageUrl": DataGenerator.generate_random_image_url(),
            "price": DataGenerator.generate_random_price(),
            "description": DataGenerator.generate_random_description(),
            "location": DataGenerator.generate_random_location(),
            "published": DataGenerator.generate_random_published(),
            "genreId": DataGenerator.generate_random_genreId(exclude_genre_id)
        }

    @staticmethod
    def generate_movie_filter_params():
        return {
            "pageSize": random.choice([5, 10, 20]),
            "page": random.randint(1, 3),
            "minPrice": random.randint(1, 300),
            "maxPrice": random.randint(500, 1000),
            "locations": random.choice(["MSK","SPB"]),
            "published": random.choice(["true", "false"]),
            "genreId": random.randint(1,10),
            "createdAt": random.choice(["asc", "desc"])
        }

    @staticmethod
    def generate_reviews_data():
        return {
            "rating": random.randint(1, 10),
            "text": faker.catch_phrase()
        }