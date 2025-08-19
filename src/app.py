"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# Este es nuestro primer endpoint


@app.route('/people', methods=['GET'])
def get_all_people():
    # get todos los log de tab people
    all_people = People.query.all()

    # 2. convetir formato para envio
    serialized_people = [person.serialize() for person in all_people]

    # 3. respuesta
    return jsonify(serialized_people), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"msg": "Person not found"}), 404
    else:
        return jsonify(person.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in all_planets]
    return jsonify(serialized_planets), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "planet not found"}), 404
    else:
        return jsonify(planet.serialize()), 200


@app.route('/users', methods=['GET'])
def users():
    all_user = User.query.all()

    serialized_user = [user.serialize() for user in all_user]

    return jsonify(serialized_user), 200


@app.route('/users/favorites')
def get_user_favorite():
    # el user sera 1 como ejemplo
    user = User.query.get(1)
    if user is None:
        return jsonify({"msg": "favorites not found"}), 404
    else:
        serialized_favorites = [favorite.serialize() for favorite in user.favorites]
        return jsonify(serialized_favorites), 200
    

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    # lee JSON que recibo
    data = request.get_json()
    # tira user_id de JSON
    user_id = data['user_id']
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if user is None or planet is None:
        return jsonify({"msg": "404 Not Found"}), 404
    
    new_favorite = Favorite(user_id=user_id, planet_id=planet_id) # This line was moved outside the if-else block
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "favorite added"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    # busca el user_id del cuerpo de la petición
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"msg": "Missing user_id in request body"}), 400
    user_id = data['user_id']

    # verifica que el usuario y el people_id existan
    user = User.query.get(user_id)
    people = People.query.get(people_id)

    if user is None or people is None:
        return jsonify({"msg": "User or people not found"}), 404

    # crea y save el nuevo favorito
    new_favorite = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite people added successfully"}), 201
    
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
        data = request.get_json()
        user_id = data['user_id']
        favorite_detele = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if favorite_detele is None:
            return jsonify({"msg": "favorite not found"}), 404
        else:
            db.session.delete(favorite_detele)
            db.session.commit()
            return jsonify({"msg": "favorite deleted"}), 200
        
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
        data = request.get_json()
        user_id = data['user_id']
        favorite_detele = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
        if favorite_detele is None:
            return jsonify({"msg": "favorite not found"}), 404
        else:
            db.session.delete(favorite_detele)
            db.session.commit()
            return jsonify({"msg": "favorite deleted"}), 200



# @app.route('/id/<int:user_id>', methods=['GET'])
# def get_single_user(user_id):
#     user = User.query.get(user_id)
#     if user is None:
#         return jsonify({"msg": "user not found"}), 404
#     else:
#         return jsonify(user.serialize()), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
