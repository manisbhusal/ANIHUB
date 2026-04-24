import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)


TMDB_API_KEY = os.getenv("TMDB_API_KEY")
ANILIST_URL = "https://graphql.anilist.co"
TMDB_URL = "https://api.themoviedb.org/3"

def run_query(query, variables=None):
    try:
        response = requests.post(ANILIST_URL, json={'query': query, 'variables': variables}, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

FULL_DATA = '''
    id idMal title { english romaji native }
    coverImage { extraLarge large }
    bannerImage description episodes status genres averageScore
    season seasonYear format duration
    studios(isMain: true) { nodes { name } }
    nextAiringEpisode { airingAt timeUntilAiring episode }
    rankings { rank type context year }
    popularity favourites
    characters(sort: [ROLE, RELEVANCE], perPage: 12) {
      edges {
        role
        node { name { full } image { large } }
        voiceActors(language: JAPANESE) { name { full } image { large } }
      }
    }
    recommendations(perPage: 8) {
      nodes { mediaRecommendation { id title { english romaji } coverImage { large } } }
    }
'''

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "secure": True,
        "key_detected": bool(TMDB_API_KEY)
    })

@app.route('/api/trending')
def get_trending():
    query = f'query {{ Page(perPage: 25) {{ media(type: ANIME, sort: TRENDING_DESC) {{ {FULL_DATA} }} }} }}'
    return jsonify(run_query(query))

@app.route('/api/this-season')
def get_seasonal():
    query = f'query {{ Page(perPage: 25) {{ media(type: ANIME, season: SPRING, seasonYear: 2026, sort: POPULARITY_DESC) {{ {FULL_DATA} }} }} }}'
    return jsonify(run_query(query))

@app.route('/api/all-time-popular')
def get_popular():
    query = f'query {{ Page(perPage: 25) {{ media(type: ANIME, sort: POPULARITY_DESC) {{ {FULL_DATA} }} }} }}'
    return jsonify(run_query(query))

@app.route('/api/top-rated')
def get_top_rated():
    query = f'query {{ Page(perPage: 25) {{ media(type: ANIME, sort: SCORE_DESC) {{ {FULL_DATA} }} }} }}'
    return jsonify(run_query(query))

@app.route('/api/top-upcoming')
def get_upcoming():
    query = f'query {{ Page(perPage: 25) {{ media(type: ANIME, status: NOT_YET_RELEASED, sort: POPULARITY_DESC) {{ {FULL_DATA} }} }} }}'
    return jsonify(run_query(query))

@app.route('/api/recently-updated')
def get_recent():
    query = f'query {{ Page(perPage: 25) {{ media(type: ANIME, sort: UPDATED_AT_DESC) {{ {FULL_DATA} }} }} }}'
    return jsonify(run_query(query))

@app.route('/api/search')
def search_anime():
    q = request.args.get('q')
    if not q: return jsonify({"error": "Query required"}), 400
    query = f'''query ($s: String) {{ Page(perPage: 20) {{ media(search: $s, type: ANIME) {{ {FULL_DATA} }} }} }}'''
    return jsonify(run_query(query, {'s': q}))

@app.route('/api/details/<int:anime_id>')
def get_details(anime_id):
    query = f'''query ($id: Int) {{ Media(id: $id) {{ {FULL_DATA} }} }}'''
    return jsonify(run_query(query, {'id': anime_id}))

@app.route('/api/schedule')
def get_schedule():
    now = int(datetime.now().timestamp())
    week_later = now + (7 * 24 * 60 * 60)
    query = '''
    query ($start: Int, $end: Int) {
      Page(perPage: 50) {
        airingSchedules(airingAt_greater: $start, airingAt_less: $end, sort: TIME_ASC) {
          airingAt episode
          media { id title { english romaji } coverImage { large } }
        }
      }
    }
    '''
    return jsonify(run_query(query, {'start': now, 'end': week_later}))

@app.route('/api/metadata')
def get_tmdb_metadata():
    if not TMDB_API_KEY:
        return jsonify({"error": "TMDB API Key missing"}), 500
    title = request.args.get('title')
    params = {'api_key': TMDB_API_KEY, 'query': title}
    res = requests.get(f"{TMDB_URL}/search/tv", params=params)
    return jsonify(res.json())

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)