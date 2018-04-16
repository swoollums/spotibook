import json
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import urllib


app = Flask(__name__)

CLIENT_ID = "7191b80ce0364e7e96e282f04131013c"
CLIENT_SECRET = "1ae0231f8bc14553ad736266be5aae80"

SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback".format(CLIENT_SIDE_URL, PORT)
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

authorization_header = ""

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID
}

@app.route("/")
def index():
    auth_url = "https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri={}&scope=playlist-modify-private user-read-private user-top-read".format(CLIENT_ID, REDIRECT_URI)
    return redirect(auth_url)


@app.route("/callback")
def callback():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    post_request = requests.post("https://accounts.spotify.com/api/token", data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    
    top_response = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=3", headers=authorization_header)
    top_data = json.loads(top_response.text)
    lst = []
    for i in range(3):
        lst.append(top_data["items"][i]["name"] + " by " + top_data["items"][i]["artists"][0]["name"])

    return render_template("index.html", sorted_array=lst)

if __name__ == "__main__":
    app.run(debug=True,port=PORT)
