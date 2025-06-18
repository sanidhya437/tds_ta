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
       
          relevant_posts = []
       # Define keywords based on the question
       keywords = question.split()  # Split the question into words
       # Search for relevant posts based on keywords
       for post in discourse_posts:
           title = post['title'].lower()
           content = post.get('content', '').lower()  # Assuming each post has a 'content' field
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
       app.run(host='0.0.0.0', port=5000)
   
