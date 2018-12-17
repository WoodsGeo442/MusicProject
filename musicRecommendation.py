#Aaron Parks
#Partner: Geoffrey
#11/28/18
#CST 205 Project
#run with this export OAUTHLIB_INSECURE_TRANSPORT=1

from flask import Flask, render_template, request, redirect, url_for
from flask_dance.contrib.spotify import make_spotify_blueprint, spotify
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError, OAuth2Error
import requests, json, urllib.parse

#Initializes the flask app, sets the static folder in order to use our styles and adds the secret key to be used with spotify.
app = Flask(__name__, static_folder="static")
app.secret_key = 'development'

#Creates the spotify blueprint in order to give the API our developer account credentials.
blueprint = make_spotify_blueprint(
	client_id='9d09c92238a545bcb83abf4b3427c7d5',
	client_secret='889faecbb3ee4e1196a76e5e617e802c',
	scope='playlist-modify-public streaming user-library-read',
)

#Sets the questions that will be included in the survey.
questions = ["I am a very sociable person.", "I like to party.", "I am energetic.", "I enjoy dancing.", "I enjoy happy songs.", "I enjoy instrumental songs." ]

#Registers the bluepring in order to connect to the Spotify API
app.register_blueprint(blueprint, url_prefix='/login')

#The landing page in which the user takes the survey. In the render_template function the questions are also passed.
@app.route('/')
def index():
	return render_template('musicRecommendation_home.html', questions=questions)
    
#The route to the stream page
@app.route('/stream', methods = ['POST', 'GET'])
def stream():
	#Makes sure the user is signed into spotify and if they are not takes them to the log in page.
	if not spotify.authorized:
		return redirect(url_for('spotify.login'))
	try:
		#Retrieves the data from the survey
		if request.method == 'POST':
			answers = request.form.to_dict()
			#Based on the answer sets the mode or key to major (1) or minor (0)
			if answers["4"] == "1" or answers["4"] == "2":
				mode = "0"
			else:
				mode = "1"
			#Creates the string containing the data that will be included in the Spotify get request
			search_string = ('seed_genres=' + answers["genre"] + '&target_danceability=' + answers["3"] + '&target_energy=' + answers["2"] + '&target_instrumentalness=' + answers["5"] + '&target_loudness=' + answers["0"] + '&target_mode=' + mode + '&target_popularity=' + answers["1"] )
			resp = spotify.get(f'v1/recommendations?limit=1&{search_string}')

			return render_template('musicRecommendation_stream.html', data=(resp.json()["tracks"][0]))
	except(InvalidGrantError, TokenExpiredError) as e:
		return redirect(url_for('spotify.login'))
