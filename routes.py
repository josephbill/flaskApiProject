from flask import Flask, current_app, make_response, request, jsonify, g
from models.user import User 
from models.post import Post, db
from flask_cors import CORS
import os 

def create_app():
    # define routes , request hook , define helper methods associated to routes 
    # create the flask app 
    app = Flask(__name__)
    # allow CORS for all routes 
    CORS(app)
    app.config.from_object('config.Config')
    db.init_app(app)

    # sample request hook 
    @app.before_request
    def app_path():
        g.path = os.path.abspath(os.getcwd())

    
    # define routes 
    @app.route('/',methods=['GET'])
    def index():
        # usage make_response
        host = request.headers.get('Host')
        appname = current_app.name
        responsebody = f'''Hello world'''
        statuscode = 200

        return make_response(responsebody, statuscode)
    
    # jsonify to return json 
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        users_data = [{'id': user.id, 'username' : user.username} for user in users]
        return jsonify(users_data)
    

    # create /post 
    @app.route('/users', methods=['POST'])
    def create_user():
        # we use request to get info needed by custom methods 
        # dictate the format which data comes in as 
        # json data , multipart data (cloudinary)
        # {
        #   "username" : "Joseph",
        #   "url" : "url from cloudinary"
        # }
        data  = request.get_json()
        username = data.get('username')
        # utilize the classes to create the records 
        new_user = User(username=username)  
        db.session.add(new_user)
        db.session.commit()
        # return statement 
        return jsonify({'message' : 'User created successfully'})
    

    return app

  

