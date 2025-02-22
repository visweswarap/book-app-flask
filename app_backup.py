from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy database (List of dictionaries)
books = [
    {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho"},
    {"id": 2, "title": "Atomic Habits", "author": "James Clear"},
]


# Home Page - Read (List)
@app.route("/")
def index():
    return render_template("index.html", books=books)

# Create (Add New Book)
@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        new_id = max([book["id"] for book in books], default=0) + 1  # Generate new ID
        books.append({"id": new_id, "title": title, "author": author})
        return redirect(url_for("index"))
    return render_template("form.html", action="Add", book={})


# Update (Edit Book)
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        return "Book not found", 404
    if request.method == "POST":
        book["title"] = request.form["title"]
        book["author"] = request.form["author"]
        return redirect(url_for("index"))
    return render_template("form.html", action="Edit", book=book)


# Delete Book
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_book(id):
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        return "Book not found", 404
    if request.method == "POST":
        books.remove(book)
        return redirect(url_for("index"))
    return render_template("delete.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)
