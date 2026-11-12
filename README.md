# CodeAlpha_FAQChatbot

FAQ chatbot built for the CodeAlpha AI Internship (Task 2).

## Features
- NLP preprocessing with NLTK (stopwords removal, lemmatization)
- TF-IDF (word + character n-grams) with cosine similarity for matching
- Handles typos, paraphrased questions, greetings, and out-of-scope queries
- "Did you mean...?" suggestions when confidence is low
- Terminal and Flask web interface

## Setup
```
pip install -r requirements.txt
python chatbot.py        # terminal chatbot
python app_flask.py      # web UI at http://127.0.0.1:5000
```

## Customize
Edit `faqs.json`: each entry has a list of question variants (`q`) and one answer (`a`).

## Tech
Python, NLTK, scikit-learn, Flask