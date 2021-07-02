from cs50 import SQL


db = SQL("sqlite:///pessoas.db")

db.execute("DELETE FROM registrados;")
