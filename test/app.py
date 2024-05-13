from flask import Flask, render_template

app = Flask(__name__)

# Route pour afficher le template HTML
@app.route('/')
def index():

    elements = ['élément 1', 'élément 2', 'élément 3', 'élément 4']

    # Rendre le template HTML avec la liste d'éléments
    return render_template('index.html', elements=elements)


if __name__ == '__main__':
    app.run(debug=True)
