from flask import Flask, render_template, request
import spacy
import re

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

def generate_bullet_points(text):
    doc = nlp(text)
    bullet_points = []

    for sent in doc.sents:
        simplified_sentence = " ".join([token.text for token in sent if not token.is_stop])
        simplified_sentence = re.sub(r'\[.*?\d+.*?\]', '', simplified_sentence)  # Remove numbers inside square brackets
        simplified_sentence = simplified_sentence.strip()
        
        if simplified_sentence:
            bullet_points.append(simplified_sentence)

    return bullet_points

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        bullet_points = generate_bullet_points(user_input)
        return render_template('index.html', user_input=user_input, bullet_points=bullet_points)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
