from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Land for Sale Scraper is running and sending updates to LINE Notify!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
