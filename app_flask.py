from flask import Flask, request, jsonify, render_template_string
from chatbot import FAQBot

app = Flask(__name__)
bot = FAQBot()

PAGE = """
<!doctype html><html><head><meta charset="utf-8"><title>FAQ Chatbot</title>
<style>
body{font-family:Segoe UI,Arial;background:#f0f2f5;display:flex;justify-content:center;padding:30px}
#box{width:420px;background:#fff;border-radius:12px;box-shadow:0 2px 12px #0002;overflow:hidden}
h2{margin:0;padding:16px;background:#4f46e5;color:#fff;font-size:18px}
#chat{height:380px;overflow-y:auto;padding:14px}
.m{margin:8px 0;padding:9px 12px;border-radius:10px;max-width:80%;clear:both}
.u{background:#4f46e5;color:#fff;float:right}.b{background:#e5e7eb;float:left}
#bar{display:flex;border-top:1px solid #ddd}
input{flex:1;padding:14px;border:0;outline:0;font-size:15px}
button{border:0;background:#4f46e5;color:#fff;padding:0 20px;cursor:pointer}
</style></head><body><div id="box">
<h2>💬 FAQ Chatbot - CodeAlpha Task 2</h2><div id="chat"></div>
<div id="bar"><input id="q" placeholder="Type your question..." autofocus><button onclick="send()">Send</button></div></div>
<script>
const chat=document.getElementById('chat'),q=document.getElementById('q');
function add(t,c){const d=document.createElement('div');d.className='m '+c;d.textContent=t;chat.appendChild(d);chat.scrollTop=chat.scrollHeight}
add('Hi! Ask me anything about orders, shipping or payments.','b');
q.addEventListener('keydown',e=>{if(e.key==='Enter')send()});
async function send(){const t=q.value.trim();if(!t)return;add(t,'u');q.value='';
const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q:t})});
add((await r.json()).answer,'b')}
</script></body></html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

@app.route("/ask", methods=["POST"])
def ask():
    ans, score = bot.ask(request.json.get("q", ""))
    return jsonify(answer=ans, score=score)

if __name__ == "__main__":
    app.run(debug=False)