import gensim
from flask import Flask
import numpy as np

app = Flask(__name__)

model = gensim.models.KeyedVectors.load_word2vec_format("jawiki.entity_vectors.300d.txt")

@app.route('/get_vector/<word>')
def get_vector(word=None):
   vector = model[word];
   string = "";
   for v in vector:
       string += np.array(v,dtype='unicode').tostring().decode('utf-8')+','
   return string

@app.route('/get_similarity/<word1>/<word2>')
def get_similarity(word1=None,word2=None):
   similarity = model.similarity(word1,word2);
   return np.array(similarity,dtype='unicode').tostring().decode('utf-8')

if __name__ == "__main__":
       app.run()