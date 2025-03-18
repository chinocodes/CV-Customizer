from flask import Flask, render_template, request
from openai import OpenAI
import fitz
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=api_key)


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")

def index():
    return render_template("index.html")



@app.route("/submit", methods=["POST"])
def scrape_qualifications() :
    user_URL = request.form.get('user-url')
    user_CV = request.files.get('user-cv')
    def extract_from_file(file):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text= ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text
    extracted_cv = extract_from_file(user_CV)
    
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Expert CV writer"},
        {"role": "user", "content": f'Here is my CV:\n\n{extracted_cv}'},
        {"role": "user", "content": f'Here are the job requirements:\n\n{user_URL}'},
        {"role": "user", "content": "Tailor my CV to match the job requirements."}

        
        ]
    )
    new_cv = completion.choices[0].message.content
    return render_template("index.html", new_cv=new_cv)








if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)