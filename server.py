import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from flask_cors import CORS

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

CORS(app, supports_credentials=True)

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/api/session")
def get_session():
    user = session.get("user")
    if user:
        return user
    return {"error": "Not logged in"}, 401

@app.route("/login")
def login():
    print(url_for("callback", _external=True))
    # return oauth.auth0.authorize_redirect("http://192.168.0.100:3000/")
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True, prompt="none")
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    print(session)
    print(token)
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

def mask_pii(data):
    data['userinfo']['email']="***email-Masked***"
    data['userinfo']['iss']="***iss-Masked***"
    data['userinfo']['name']="***name-Masked***"
    data['userinfo']['sid']="***sid-Masked***"
    data['userinfo']['picture']="***picture-Masked***"
    data['userinfo']['sub']="***sub-Masked***"
    data['userinfo']['aud']="***aud-Masked***"
    data['userinfo']['nonce']="***nonce-Masked***"
    return data

@app.route("/")
def home():
    if session:
        print(json.dumps(session.get('user')))
        pretty=mask_pii(session.get('user'))
        return render_template("home.html", session=session.get('user'), pretty=json.dumps(pretty, indent=4))
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    # if session:
    #     masked_session = sanitize_session_data(session)
    #     pretty = json.dumps(masked_session, indent=2)
    #     return render_template('home.html', session=session, pretty=pretty)
    # return render_template('home.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))


