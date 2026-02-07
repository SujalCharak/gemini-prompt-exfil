"""
Research-only scenario runner.

Used for controlled evaluation under owned accounts.
Not an exploit. Not for third-party systems.
"""



from flask import Flask, request, jsonify
app = Flask(__name__)

PUBLIC_INDEX = {"doc1":"This is public doc content."}
PRIVATE_INDEX = {"secret_doc":"VICTIM_CANARY_TOKEN_PLACEHOLDER"}  

APP_TOKENS = {"attacker_token": ["public"], "trusted_token": ["public","private"]}
@app.route('/query', methods=['POST'])
def query():
    payload = request.json or {}
    q = payload.get('q','')
    app_token = request.headers.get('X-APP-TOKEN','')
    results = []

    if 'private' in APP_TOKENS.get(app_token,[]):
        results.append({"source":"private","text": PRIVATE_INDEX.get("secret_doc")})

    results.append({"source":"public","text": PUBLIC_INDEX.get("doc1")})
    return jsonify({"query": q, "hits": results})
if __name__ == '__main__':
    app.run(port=7865)
