from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(String(120), unique=True, nullable=False)
    password = db.Column(String(100), nullable=False)
    first_name = db.Column(String(50))
    last_name = db.Column(String(50))
    subscription_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    is_active = db.Column(Boolean(), default=True)

    favorite_planets = relationship("FavoritePlanet", back_populates="user")
    favorite_characters = relationship("FavoriteCharacter", back_populates="user")

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "subscription_date": self.subscription_date.isoformat()
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String(120), nullable=False)
    population = db.Column(String(100))
    climate = db.Column(String(50))
    terrain = db.Column(String(50))

    favorite_planets = relationship("FavoritePlanet", back_populates="planet")

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String(120), nullable=False)
    gender = db.Column(String(20))
    birth_year = db.Column(String(20))
    eye_color = db.Column(String(20))

    favorite_characters = relationship("FavoriteCharacter", back_populates="character")

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, ForeignKey('planet.id'), nullable=False)

    user = relationship("User", back_populates="favorite_planets")
    planet = relationship("Planet", back_populates="favorite_planets")

    def __repr__(self):
        return f'<FavoritePlanet {self.id} - User {self.user_id} - Planet {self.planet_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize()
        }

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, ForeignKey('character.id'), nullable=False)

    user = relationship("User", back_populates="favorite_characters")
    character = relationship("Character", back_populates="favorite_characters")

    def __repr__(self):
        return f'<FavoriteCharacter {self.id} - User {self.user_id} - Character {self.character_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.serialize()
        }
