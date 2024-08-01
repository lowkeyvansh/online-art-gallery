from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///art_gallery.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(100), nullable=False)

db.create_all()

@app.route('/')
def index():
    artworks = Artwork.query.all()
    return render_template('index.html', artworks=artworks)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        image_file = request.files['image_file']

        if image_file:
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename))
            new_artwork = Artwork(title=title, description=description, price=price, image_file=image_file.filename)
            db.session.add(new_artwork)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
