import json
from flask import Flask, request, redirect, render_template
import requests
import base64

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("https://accounts.spotify.com/authorize?client_id=7191b80ce0364e7e96e282f04131013c&response_type=code&redirect_uri=https://swoollums.github.io/spotibook/callback&scope=user-read-private user-top-read")


@app.route("/callback")
def callback():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": "https://swoollums.github.io/spotibook/callback"
    }
    base64encoded = base64.b64encode(("7191b80ce0364e7e96e282f04131013c:1ae0231f8bc14553ad736266be5aae80").encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    post_request = requests.post("https://accounts.spotify.com/api/token", data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    top_response = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=3&time_range=long_term", headers=authorization_header)
    top_data = json.loads(top_response.text)
    lst = []
    for i in range(3):
        lst.append(top_data["items"][i]["name"] + " by " + top_data["items"][i]["artists"][0]["name"])

    return render_template("index.html", sorted_array=lst)

if __name__ == "__main__":
    app.run()

