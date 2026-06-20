from flask import Flask, render_template, request
import eacal
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    selected_year = None
    selected_country = None
    country_name = None

    if request.method == "POST":
        selected_year = int(request.form.get("year", 2025))
        selected_country = request.form.get("country", "korea")

        if selected_country == "korea":
            cal = eacal.EACal(ko=True)
            country_name = "한국"
        elif selected_country == "japan":
            cal = eacal.EACal(ja=True)
            country_name = "일본"
        else:
            cal = eacal.EACal(zh_s=True)
            country_name = "중국"

        results = []
        for x in cal.get_annual_solar_terms(selected_year):
            results.append(
                {
                    "index": x[1],
                    "name": x[0],
                    "date": datetime.strftime(x[2], "%Y-%m-%d %H:%M %Z"),
                }
            )

    return render_template(
        "index.html",
        results=results,
        selected_year=selected_year,
        selected_country=selected_country,
        country_name=country_name,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
