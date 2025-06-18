from flask import Flask, request, jsonify
import json

app = Flask(__name__)

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
   