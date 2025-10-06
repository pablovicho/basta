import os

from flask import Flask, request, redirect, url_for, render_template
from werkzeug.exceptions import abort


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'basta.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/', methods=['GET'])
    def intro():
        return render_template('welcome.html')
        # input("\n ¡Juguemos basta! \n \n Si deseas crear un juego, presiona Enter. \n Si deseas unirte a un juego, pega aquí el código: ")

    @app.route('/welcome-form', methods=['POST'])
    def welcome_form():
        data = request.form
        # Extract the necessary information from the form data and save it to the database
        game_id = data.get('game_id')
        if not game_id or game_id.strip() == "":
            return redirect(url_for('create_game'))
        return redirect(url_for('join_game', game_id=game_id))
        
        # Here you would typically save the data to the database


    ## Create game and join game routes

    @app.route('/create-game', methods=['GET', 'POST'])
    def create_game():
        return 'thank you'
    
    @app.route('/join-game/<game_id>', methods=['GET', 'POST'])
    def join_game(game_id):
        return f'Joining game {game_id}'

    return app