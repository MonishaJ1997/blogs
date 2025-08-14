from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages

# PostgreSQL connection URI from Render environment variable
# Example: postgres://user:pass@host:port/dbname
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

# Database model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Home - List posts
@app.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)

# Add post
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]
        if not title or not content or not author:
            flash("All fields are required!", "error")
            return redirect(url_for("add"))
        post = Post(title=title, content=content, author=author)
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for("index"))
    return render_template("add.html")

# Edit post
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    post = Post.query.get_or_404(id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        post.author = request.form["author"]
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("index"))
    return render_template("edit.html", post=post)

# Delete post
@app.route("/delete/<int:id>")
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Only for local testing
    with app.app_context():
        db.create_all()
    app.run(debug=True)

