from flask import Flask, render_template, request
from model import parse_website

app = Flask(__name__)

# Главная страница с формой
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")  # Получаем введенный URL
        if url:
            products = parse_website(url)  # Парсим сайт и извлекаем сущности
            if products:
                return render_template("index.html", products=products)
            else:
                return render_template("index.html", no_products=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)