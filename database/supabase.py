from turtle import update
from supabase import create_client, Client
import os
import uuid
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env.local')

def get_supabase_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL") or "http://localhost:54321"
    key: str = os.environ.get("SUPABASE_KEY") or "your-anon-key"
    client: Client = create_client(url, key)
    return client

def create_game(client, name="Anonymous", categories=['Animal', 'Country', 'City', 'Food', 'Movie', 'Famous Person']):
    player_uuid = str(uuid.uuid4())
    # Status: ('waiting', 'playing', 'reviewing', 'finished')
    game = (client.table('games')
                .insert({'creator_id': player_uuid, 'categories': categories, 'status': 'waiting'})
                .execute())
    if game.status_code != 200:
        raise Exception(f"Error creating game: {game.json()}")

    player = (client.table('players')
              .insert({'game_id': game.json()[0]['id'], 'name': name, 'id': player_uuid})
              .execute())
    if player.status_code != 200:
        raise Exception(f"Error adding player to game: {player.json()}")

    return {'game': game.json().id, 'player': player.json()}

def join_game(client, game_id):
    user_id = str(uuid.uuid4())
    response = (client.table('games')
                .select('*')
                .eq('id', game_id)
                .limit(1)
                .execute())
    if response.status_code != 200 or len(response.json()) == 0:
        raise Exception(f"Game with id {game_id} does not exist.")
    game = response.json()[0]

    player = (client.table('players')
                .insert({'game_id': game_id, 'id': user_id})
                .execute())
    if player.status_code != 200:
        raise Exception(f"Error joining game: {player.json()}")
    
    return {'game': game.id, 'player': player.json()}

def get_game_state(client, game_id):
    response = (client.table('games')
                .select('*, status')
                .eq('id', game_id)
                .limit(1)
                .execute())
    if response.status_code != 200 or len(response.json()) == 0:
        raise Exception(f"Game with id {game_id} does not exist.")
    return response.json()[0]

def send_response(client, player_id, answers):
    response = (client.table('players')
                .update({ 'answers': answers})
                .eq('id', player_id)
                .execute())
    if response.status_code != 200:
        raise Exception(f"Error sending response: {response.json()}")
    return response.json()

def get_latest_responses(client, game_id):
    response = (client.table('players')
                .select('answers, name, id')
                .eq('game_id', game_id)
                .order('id', desc=True)
                .limit(1)
                .execute())
    # answers = response.json().get('answers', [])[-1] if response.json() else None
    if response.status_code != 200:
        raise Exception(f"Error getting responses: {response.json()}")
    return response.json()

def start_game(client, game_id):
    response = (client.table('games')
                .update({ 'status': 'playing'})
                .eq('id', game_id)
                .execute())
    if response.status_code != 200:
        raise Exception(f"Error starting game: {response.json()}")
    return response.json()
