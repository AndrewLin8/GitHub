from flask import Flask, render_template
import requests

app = Flask(__name__)

MEME_URL = "https://meme-api.com/gimme/wholesomememes"


@app.route("/")
def home():
    meme_title = "Unable to load meme"
    meme_image = ""
    meme_source = "unknown"

    try:
        response = requests.request("GET", MEME_URL)
        response.raise_for_status()
        meme_data = response.json()
        meme_title = meme_data.get("title", meme_title)
        meme_image = meme_data.get("url", meme_image)
        meme_source = meme_data.get("subreddit", meme_source)
    except requests.RequestException:
        pass

    return render_template(
        "meme.html",
        meme_title=meme_title,
        meme_image=meme_image,
        meme_source=meme_source,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)