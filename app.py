from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "12345"

def init_db():
    conn = sqlite3.connect("firmalar.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS firmalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    
    if "giris" not in session:
      return redirect("/login")

    conn = sqlite3.connect("firmalar.db")
    cursor = conn.cursor()

    if request.method == "POST":
        firma = request.form["firma"]
        cursor.execute("INSERT INTO firmalar (isim) VALUES (?)", (firma,))
        conn.commit()
        conn.close()
        return redirect("/")

    arama = request.args.get("arama")

    if arama:
        cursor.execute("SELECT * FROM firmalar WHERE isim LIKE ?", ('%' + arama + '%',))
    else:
        cursor.execute("SELECT * FROM firmalar")

    firmalar = cursor.fetchall()
    conn.close()

    return render_template("index.html", firmalar=firmalar)

@app.route("/sil/<int:id>")
def sil(id):
    conn = sqlite3.connect("firmalar.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM firmalar WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/duzenle/<int:id>", methods=["GET", "POST"])
def duzenle(id):
    conn = sqlite3.connect("firmalar.db")
    cursor = conn.cursor()

    if request.method == "POST":
        yeni_isim = request.form["firma"]
        cursor.execute("UPDATE firmalar SET isim=? WHERE id=?", (yeni_isim, id))
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM firmalar WHERE id=?", (id,))
    firma = cursor.fetchone()
    conn.close()

    return render_template("duzenle.html", firma=firma)

@app.route("/login", methods=["GET", "POST"])
def login():
    hata = ""

    if request.method == "POST":
        kullanici = request.form["kullanici"]
        sifre = request.form["sifre"]

        if kullanici == "admin" and sifre == "1234":
            session["giris"] = True
            return redirect("/")
        else:
            hata = "Hatalı giriş"

    return render_template("login.html", hata=hata)

@app.route("/logout")
def logout():
    session.pop("giris", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)