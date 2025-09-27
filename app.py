from flask import Flask, request, render_template
import os


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
	# GET: show form; POST: read name from form
	name = ""
	if request.method == "POST":
		name = (request.form.get("name") or "").strip()
	else:
		# Also allow query string ?name=...
		name = (request.args.get("name") or "").strip()

	greeting = "こんにちは！" if name == "" else f"こんにちは、{name}さん！"
	return render_template("index.html", title="Hello Flask on AWS", greeting=greeting, name=name)


@app.get("/healthz")
def healthz():
	return {"status": "ok"}


if __name__ == "__main__":
	# Local run: respect PORT like on Fly/App Runner; default 8501 to match previous config
	port = int(os.environ.get("PORT", "8501"))
	app.run(host="0.0.0.0", port=port)
