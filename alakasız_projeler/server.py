from flask import Flask, request, render_template_string

app = Flask(__name__)

# Uygulama çalıştığı sürece saklanacak bir liste.
# (Dosyaya veya veritabanına yazmak istersen, bu listeyi kaydetmen gerekir.)
headlines = ["Test Haber 1", "Test Haber 2"]

html_template = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Test Haber Sayfası (Flask)</title>
  <style>
    body {
      font-family: sans-serif;
      margin: 20px;
      background-color: #f9f9f9;
    }
    h1 {
      font-size: 1.5rem;
      margin-bottom: 10px;
    }
    #headlines {
      margin-top: 20px;
      padding: 10px;
      background-color: #ffffff;
      border: 1px solid #ccc;
    }
    h2 {
      margin: 10px 0;
      padding: 5px;
      border-bottom: 1px dashed #aaa;
    }
    #newHeadlineInput {
      padding: 6px;
      width: 200px;
    }
    #addHeadlineBtn {
      padding: 6px 12px;
      border: none;
      background-color: #4caf50;
      color: white;
      cursor: pointer;
      margin-left: 5px;
    }
    #addHeadlineBtn:hover {
      background-color: #45a049;
    }
  </style>
</head>
<body>
  <h1>Yerel Haber Test Sayfası (Flask)</h1>
  <p>Bu sayfa, <strong>test amaçlı</strong> bir haber kaynağı gibi davranır. Aşağıdaki "Başlık Ekle" butonunu kullanarak yeni bir haber başlığı ekleyebilirsiniz. Yeni eklenen başlıklar sunucu tarafında saklanır ve sayfa yenilese de kalır.</p>

  <form action="/add" method="POST">
    <label for="newHeadlineInput">Haber Başlığı Gir:</label>
    <input type="text" name="headline" id="newHeadlineInput" placeholder="Örnek: Yeni Test Haberi" />
    <button type="submit" id="addHeadlineBtn">Başlık Ekle</button>
  </form>

  <div id="headlines">
    {% for h in headlines %}
      <h2>{{ h }}</h2>
    {% endfor %}
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html_template, headlines=headlines)

@app.route("/add", methods=["POST"])
def add_headline():
    # Formdan gelen başlığı server tarafındaki headlines listesine ekle
    new_headline = request.form.get("headline", "").strip()
    if new_headline:
        headlines.insert(0, new_headline)  # Başa ekle
    return index()  # Yeniden anasayfayı döndür

if __name__ == "__main__":
    app.run(debug=True, port=5000)
