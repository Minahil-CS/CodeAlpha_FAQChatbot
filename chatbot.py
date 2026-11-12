"""CodeAlpha Task 2 - FAQ Chatbot
NLP: NLTK preprocessing (tokenize, stopwords, lemmatize) + TF-IDF (char n-grams for typos)
+ cosine similarity. Each FAQ has multiple question variants.
"""
import json
import re
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack

for pkg, path in [("stopwords", "corpora/stopwords"), ("wordnet", "corpora/wordnet")]:
    try:
        nltk.data.find(path)
    except LookupError:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass

STOP = set(stopwords.words("english"))
LEM = WordNetLemmatizer()
THRESHOLD = 0.45
SUGGEST = 0.25
GREET = {"hi", "hello", "hey", "salam", "assalamualaikum", "aoa", "hola"}
ABOUT = {"who are you", "what can you do", "help", "help me", "what are you", "your name"}
BYE = {"bye", "goodbye", "thanks", "thank you", "shukriya", "ok thanks"}


def preprocess(text: str) -> str:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return " ".join(LEM.lemmatize(w) for w in words if w not in STOP)


class FAQBot:
    def __init__(self, path="faqs.json"):
        with open(path, encoding="utf-8") as f:
            self.faqs = json.load(f)
        self.texts, self.owner = [], []
        for idx, item in enumerate(self.faqs):
            for q in item["q"]:
                self.texts.append(preprocess(q))
                self.owner.append(idx)
        self.word = TfidfVectorizer(ngram_range=(1, 2))
        self.char = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 4))
        self.matrix = hstack([self.word.fit_transform(self.texts),
                              self.char.fit_transform(self.texts)]).tocsr()

    def _scores(self, query):
        p = preprocess(query)
        q = hstack([self.word.transform([p]), self.char.transform([p])]).tocsr()
        s = cosine_similarity(q, self.matrix)[0]
        best = np.zeros(len(self.faqs))
        for sc, o in zip(s, self.owner):
            best[o] = max(best[o], sc)
        return best

    def ask(self, query: str):
        clean = query.lower().strip()
        if clean in GREET:
            return "Hello! 👋 How can I help you today?", 1.0
        if clean in BYE:
            return "You're welcome! Have a great day 😊", 1.0
        if clean in ABOUT:
            return self.faqs[-1]["a"], 1.0
        scores = self._scores(query)
        i = int(scores.argmax())
        if scores[i] >= THRESHOLD:
            return self.faqs[i]["a"], float(scores[i])
        if scores[i] >= SUGGEST:
            top = np.argsort(scores)[::-1][:2]
            opts = " or ".join(f"'{self.faqs[j]['q'][0]}'" for j in top)
            return f"I'm not sure I understood. Did you mean {opts}?", float(scores[i])
        return "Sorry, I couldn't find an answer. Please email support@example.com.", float(scores[i])


if __name__ == "__main__":
    bot = FAQBot()
    print("FAQ Chatbot ready. Type 'quit' to exit.")
    while True:
        user = input("You: ").strip()
        if user.lower() in {"quit", "exit"}:
            print("Bot: Goodbye!")
            break
        if user:
            ans, score = bot.ask(user)
            print(f"Bot: {ans}  (confidence {score:.2f})")