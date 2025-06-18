from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
app = Flask(__name__)
CORS(app)


   # Load scraped data
with open('discourse_posts.json') as f:
       discourse_posts = json.load(f)

@app.route('/api/', methods=['POST'])
def answer_question():
       data = request.json
       question = data.get('question')
       # Placeholder logic for answering questions
       answer = "This is a placeholder answer."  # Replace with actual logic
       links = [{"url": post['link'], "text": post['title']} for post in discourse_posts]

       response = {
           "answer": answer,
           "links": links
       }
       return jsonify(response)

if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   
