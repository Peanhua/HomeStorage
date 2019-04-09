from flask       import render_template
from application import app, login_required

@app.route("/")
@login_required()
def index():
    return render_template("index.html")

@app.route("/docs/")
def docs_index():
    with open("application/static/docs/index.css") as fp:
        css = fp.read()
    with open("application/static/docs/index.md") as fp:
        content = fp.read()
    return render_template("doc.html", css=css, content=content)


@app.route("/docs/<name>.png")
def docs_png(name):
    return app.send_static_file("docs/" + name + ".png")
