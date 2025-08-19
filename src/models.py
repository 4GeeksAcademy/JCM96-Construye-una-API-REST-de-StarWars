from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites =db.relationship('Favorite', backref='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    mass: Mapped[int] = mapped_column(Integer)
    hair_color: Mapped[str] = mapped_column(String(120), )
    skin_color: Mapped[str] = mapped_column(String(120), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(120))
    gender: Mapped[str] = mapped_column(String(120), nullable=False)
    homeworld: Mapped[str] = mapped_column(String(120), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld
        }


class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    rotation_period: Mapped[int] = mapped_column(Integer)
    orbital_period: Mapped[int] = mapped_column(Integer)
    diameter: Mapped[int] = mapped_column(Integer)
    climate: Mapped[str] = mapped_column(String(120))
    gravity: Mapped[int] = mapped_column(Integer)
    terrain: Mapped[str] = mapped_column(String)
    surface_water: Mapped[int] = mapped_column(Integer)
    population: Mapped[int] = mapped_column(Integer)
    url: Mapped[str] = mapped_column(String(120), unique=True)
    created: Mapped[int] = mapped_column(Integer)
    edited: Mapped[int] = mapped_column(Integer)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id
        }
    