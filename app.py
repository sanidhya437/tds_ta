import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

   # Load the discourse posts from the JSON file
with open('discourse_posts.json', 'r') as f:
       discourse_posts = json.load(f)

@app.route('/api/', methods=['POST'])
def answer_question():
       data = request.json
       question = data.get('question', '').lower()  # Normalize the question
       answer = "I'm sorry, I don't have an answer for that."  # Default answer

       relevant_posts = []  # List to hold relevant posts
       keywords = question.split()  # Split the question into words

       # Search for relevant posts based on keywords
       for post in discourse_posts:
           title = post['title'].lower()
           content = post.get('content', '').lower()

           # Check if any keyword is in the title or content
           if any(keyword in title or keyword in content for keyword in keywords):
               relevant_posts.append(post)

       # Generate a response based on found posts
       if relevant_posts:
           answer = "Here are some relevant posts that might help you:"
       else:
           answer = "No relevant posts found."

       # Create links to relevant posts
       links = [{"url": post['link'], "text": post['title']} for post in relevant_posts]

       response = {
           "answer": answer,
           "links": links
       }
       return jsonify(response)

if __name__ == '__main__':
       app.run(debug=True)