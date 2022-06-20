from flask import Flask, render_template, request, redirect, url_for
import dbquery

app = Flask(__name__)

seasons = range(1950,2023)

@app.route("/", methods=["GET", "POST"])
def query():
    if request.method == "POST": 
        return redirect(url_for('result', season = int(request.form["Season"]), stat = request.form["Stat"]))
    else:
        return render_template("query.html")



@app.route("/result/<season>/<stat>")
def result(season, stat):
    return render_template("result.html", result=dbquery.master(want = 'Player, Pos, Tm, PTS, AST, TRB', season = season, where = stat, order = 'PTS'))