from sqlalchemy.orm import Session
from db_models.user import UserDBModel
from db_models.movies import MoviesDBModel

class DBHelper:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_test_user(self, user_data: dict) -> UserDBModel:
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_id(self, user_id: str):
        """Получает пользователя по ID"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    def get_user_email(self, email: str):
        """Получает пользователя по email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).first()

    def get_movie_by_name(self, name: str):
        """Получает фильм по названию"""
        return self.db_session.query(MoviesDBModel).filter(MoviesDBModel.name == name).first()

    def user_exists_by_email(self, email: str):
        """Проверяет существование пользователя по email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).count() > 0

    def delete_user(self, user: UserDBModel):
        self.db_session.delete(user)
        self.db_session.commit()

    def cleanup_test_data(self, object_to_delete: list):
        """Очищает тестовые данные"""
        for obj in object_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    def create_test_movie(self, movie_data: dict) -> MoviesDBModel:
        """Создает тестовый фильм"""
        movie = MoviesDBModel(**movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return movie

    def delete_test_movie(self, movie: MoviesDBModel):
        """Удаляет фильм"""
        self.db_session.delete(movie)
        self.db_session.commit()