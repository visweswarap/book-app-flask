from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/vish"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Define Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)


# Create the database tables
with app.app_context():
    db.create_all()


# Home Page - Read (List Books)
@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)


# Create (Add Book)
@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        new_book = Book(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("form.html", action="Add", book={})


# Update (Edit Book)
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == "POST":
        book.title = request.form["title"]
        book.author = request.form["author"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("form.html", action="Edit", book=book)


# Delete (Remove Book)
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_book(id):
    book = Book.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("delete.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)
