import os
import connexion
from flask import Flask, render_template, request,jsonify

print(os.getcwd())
app = connexion.App(__name__, specification_dir="./")

app.add_api("master.yaml")

@app.route("/")
def home():
    msg = {"msg": "It's working!"}
    return jsonify(msg)


if __name__ == "__main__":
    app.run(port=8080, debug=False)

