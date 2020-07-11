import os
import flask
import pickle
import pandas as pd
import numpy as np
from collections import defaultdict
from surprise import Dataset
from surprise import Reader

os.chdir(r'C:\FCD\Projetos\Recomendacao\dataset')
app = flask.Flask(__name__)

# Carregando dataset contendo as recomendações des filmes
arquivo = "predictions.csv"
predictions = pd.read_csv(arquivo)

# Carregando dataset contendo os filmes
arquivo2 = "movies.csv"
movies = pd.read_csv(arquivo2)

# Carregando dataset contendo a capa dos filmes
arquivo2 = "movie_poster.csv"
poster = pd.read_csv(arquivo2)

# Mesclando os 2 datasets em um único, associado pela variável movieId
data = predictions.merge(movies, on='title')
data = data.merge(poster, on='movieId')

data = data.drop(['genres', 'movieId'], axis = 1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
    
    if flask.request.method == 'POST':
        user = int(flask.request.form['userId'])
        if user not in data['userId']:
            return(flask.render_template('negative.html',name=user))
        else:
            results = data[data['userId']==user]
            titles = []
            images = []
            for i in range(len(results)):
                titles.append(results.iloc[i][1])
                images.append(results.iloc[i][2])

            return flask.render_template('positive.html', movie_names=titles, images_url=images, search_name=user)

@app.route('/sobre', methods=['GET', 'POST'])
def sobre():
    if flask.request.method == 'GET':
        return(flask.render_template('sobre.html'))
    

app.run()