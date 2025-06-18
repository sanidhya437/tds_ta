import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

   # Load the discourse posts from the JSON file with UTF-8 encoding
try:
       with open('discourse_posts.json', 'r', encoding='utf-8-sig') as f:
           discourse_posts = json.load(f)
except UnicodeDecodeError as e:
       print(f"Error reading the JSON file: {e}")
       discourse_posts = []  # Fallback to an empty list or handle as needed

@app.route('/api/', methods=['POST'])
def answer_question():
       data = request.json
       question = data.get('question', '').lower()
       answer = "I'm sorry, I don't have an answer for that."

       relevant_posts = []
       keywords = question.split()

       for post in discourse_posts:
           title = post['title'].lower()
           content = post.get('content', '').lower()

           if any(keyword in title or keyword in content for keyword in keywords):
               relevant_posts.append(post)

       if relevant_posts:
           answer = "Here are some relevant posts that might help you:"
       else:
           answer = "No relevant posts found."

       links = [{"url": post['link'], "text": post['title']} for post in relevant_posts]

       response = {
           "answer": answer,
           "links": links
       }
       return jsonify(response)

if __name__ == '__main__':
       app.run()
   
