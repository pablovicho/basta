import os

from flask import Flask, cli, request, redirect, url_for, render_template
from werkzeug.exceptions import abort

from .database.supabase import get_supabase_client, create_game, join_game

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

    @app.route('/', methods=['GET'])
    def intro():
        return render_template('welcome.html')
        # input("\n ¡Juguemos basta! \n \n Si deseas crear un juego, presiona Enter. \n Si deseas unirte a un juego, pega aquí el código: ")

    @app.route('/welcome-form', methods=['POST'])
    def welcome_form():
        data = request.form
        game_id = data.get('gameId')
        if not game_id or game_id.strip() == "":
            return redirect(url_for('create_game_form'))
        return redirect(url_for('join', game_id=game_id))

    @app.route('/create-game', methods=['GET', 'POST'])
    def create_game_form():
        return render_template('create_game.html')
    
    @app.route('/create-game-form>', methods=['GET'])
    def create():
        data = request.form
        name = data.get('name', 'Anonymous')
        categories = data.getlist('categories') or ['Animal', 'Country', 'City', 'Food', 'Movie', 'Famous Person']
        client = get_supabase_client()
        game_info = create_game(client, name=name, categories=categories)
        return f'Game {game_info} created for {name} with categories {", ".join(categories)}'    
    
    @app.route('/join-game/<game_id>', methods=['GET', 'POST'])
    def join(game_id):
        if game_id is None or game_id.strip() == "":
            abort(400, "Game ID is required to join a game.")
        client = get_supabase_client()
        join_game(client, game_id)
        return f'Joining game {game_id}'

    return app