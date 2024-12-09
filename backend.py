from dotenv import load_dotenv
import os
from os.path import join, dirname
from flask import Flask, request, make_response,jsonify,send_from_directory, render_template
from flask_cors import CORS
import requests
import anthropic
from waitress import serve
#from models  import db,User
 
try:


    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
 
    API_KEY =  os.environ.get("ANTHROPIC_API_KEY")
    print("** global key ",API_KEY[:5])  #debug.
      
    # Initialize the Claude client
    client = anthropic.Anthropic()    
    
except Exception as error:  
    print("**Error:", error)

# https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
app = Flask(__name__, static_folder='client/dist',static_url_path="/")  
CORS(app,origins='*')  #accept cross site  

#db.init_app(app)
#db.create_all()

@app.route("/api/users", methods=['GET'])
def users():
    return jsonify(
        {
            "users":['joe','peter','sam']

        }
        )

# Path for our main Svelte page
@app.route("/")
def index():
    return send_from_directory(app.static_folder,'index.html')

@app.route("/ping")
def home():
    return make_response('ping,,,',200)
    #return "Ping"


@app.route('/analyze_text', methods=['POST'])
def analyze_text():

    if not request.headers.get("Content-Type") == "application/json":
        return make_response('Invalid Arguments',400)

    try:
        jdata = request.json
        sample_text=    jdata['sample_text']
        expertise = jdata['expertise']
        language= jdata['language']
        education_level=  jdata['education_level']  
        rewrite_prompt = f"Rewrite the following text in {language}. Adjust the complexity and terminology based on the user's expertise {expertise}  and education level {education_level} Text: {sample_text}"
    
        responseMessage = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[
                {"role": "user", "content":  rewrite_prompt}
            ]    
        )
        return make_response(responseMessage.content[0].text,200)
      
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080, threads=2)
    #app.run( port=8080)