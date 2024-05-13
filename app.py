import matplotlib
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import datetime

matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = Flask(__name__)

app.secret_key = 'xyzsdfg'

app.config['MYSQL_HOST'] = 'b64szssnltiaky7avzrp-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'uapmjfxp6v9ri9zk'
app.config['MYSQL_PASSWORD'] = 'FBXLEq4O6baEYiAOpft0'
app.config['MYSQL_DB'] = 'b64szssnltiaky7avzrp'

mysql = MySQL(app)

# Création du dictionnaire
mon_dictionnaire = {}

# Fonction pour ajouter une valeur à une clé existante ou créer une nouvelle clé
def ajouter_valeur(dictionnaire, cle, valeur):
    if cle in dictionnaire:
        dictionnaire[cle] += valeur
    else:
        dictionnaire[cle] = valeur

# Exemple d'utilisation




@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    ord = list()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['name'] = user['name']
            session['email'] = user['email']
            session['userid'] = int(user['id'])
            mesage = 'Logged in successfully !'

            cursor.execute('SELECT * FROM stock WHERE id = %s', (session["userid"],))
            ord = cursor.fetchall()
            ord = list(ord)


            total = 0
            for spend in ord:
                total += spend['totalSpending']

            session['totalSpending'] = total
            session['priceSales'] = 0
            session['priceStock'] = session['totalSpending'] - session['priceSales']

            cursor.execute('SELECT productName, quantity, totalSpending FROM stock WHERE id = % s ', (session["userid"],))
            oys = cursor.fetchall()
            oys = list(oys)
            quantity = 0
            productName = str()
            spendTotal = 0
            mon_dictionnaire = {}
            mon_dictionnaire2 = {}
            liste = []
            resultats = {}

            nouveau_dictionnaire = {}

            for donnee in oys:
                produit = donnee['productName']
                quantite = donnee['quantity']
                depenses = donnee['totalSpending']

                if produit in nouveau_dictionnaire:
                    nouveau_dictionnaire[produit]['quantity'] += quantite
                    nouveau_dictionnaire[produit]['totalSpending'] += depenses
                else:
                    nouveau_dictionnaire[produit] = {'quantity': quantite, 'totalSpending': depenses}

            print(nouveau_dictionnaire)
            for produit, valeurs in nouveau_dictionnaire.items():
                nom_produit = produit
                quantite = valeurs['quantity']
                depenses = valeurs['totalSpending']

            categories = list(nouveau_dictionnaire.keys())
            quantites = [data['quantity'] for data in nouveau_dictionnaire.values()]
            spending = [data['totalSpending'] for data in nouveau_dictionnaire.values()]

            plt.pie(spending, labels=categories, autopct='%1.1f%%')
            plt.title('Répartition du stock')

            # Sauvegarde du graphique dans un fichier image
            image_path = 'static/repartition_stock.png'
            plt.savefig(image_path)
            plt.close()

            return render_template('dashboard.html', ord=ord, nouveau_dictionnaire=nouveau_dictionnaire, image_path=image_path)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage=mesage)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password,))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
            return render_template('login.html')
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage=mesage)



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    nbreSpend = int()
    ord = []
    image_path = 0
    nouveau_dictionnaire = []
    nbre = 0

    if request.method == 'POST' and 'unitPrice' in request.form and 'unitMeasure' in request.form and 'quantity' in request.form and 'productName' in request.form:
        productName = request.form['productName']
        quantity = request.form['quantity']
        unitMeasure = request.form['unitMeasure']
        unitPrice = request.form['unitPrice']
        userid = session['userid']
        totalSpending = int(quantity) * int(unitPrice)
        date = datetime.datetime.now()
        date1 = date.date()
        date2 = date.strftime("%H:%M")
        date = str(date1) +  " " + str(date2)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO stock VALUES ( % s, % s, % s, % s, % s, % s, % s)', (productName, quantity, unitMeasure, unitPrice, userid, totalSpending, date))
        mysql.connection.commit()
        mesage = 'You have successfully registered !'

        session['productName'] = productName
        session['quantity'] = int(quantity)
        session['unitMeasure'] = unitMeasure
        session['unitPrice'] = unitPrice

        session['priceSales'] = 0
        cursor.execute('SELECT totalSpending FROM stock WHERE id = % s', (userid,))
        totalSpend = cursor.fetchall()
        totalSpend = list(totalSpend)
        nbreSpend = len(totalSpend)

        total = 0
        for spend in totalSpend:
            total += spend['totalSpending']

        cursor.execute('SELECT * FROM stock WHERE id = % s', (session["userid"],))
        ord = cursor.fetchall()
        ord = list(ord)
        print(ord)

        total = 0
        for spend in ord:
            total += spend['totalSpending']
            print(total)

        session['totalSpending'] = total
        if int(quantity) < 0:
            session['priceStock'] = session['totalSpending'] + session['priceSales']
        else:
            session['priceStock'] = session['totalSpending']


        cursor.execute('SELECT productName, quantity, totalSpending, unitPrice FROM stock WHERE id = % s ', (session["userid"],))
        oys = cursor.fetchall()
        oys = list(oys)
        quantity = 0
        productName = str()
        spendTotal = 0
        mon_dictionnaire = {}
        mon_dictionnaire2 = {}
        liste = []
        resultats = {}

        nouveau_dictionnaire = {}

        for donnee in oys:
            produit = donnee['productName']
            quantite = donnee['quantity']
            depenses = donnee['totalSpending']
            unitPrice = donnee['unitPrice']

            if int(quantite) < 0:
                session['priceSales'] =  session['quantity'] * unitPrice
                session['priceSales'] = -(session['priceSales'])
                session['priceStock'] = session['priceStock'] - session['priceSales']


            if produit in nouveau_dictionnaire:
                nouveau_dictionnaire[produit]['quantity'] += quantite
                nouveau_dictionnaire[produit]['totalSpending'] += depenses
            else:
                nouveau_dictionnaire[produit] = {'quantity': quantite, 'totalSpending': depenses}

        for produit, valeurs in nouveau_dictionnaire.items():
            nom_produit = produit
            quantite = valeurs['quantity']
            depenses = valeurs['totalSpending']

        categories = list(nouveau_dictionnaire.keys())
        quantites = [data['quantity'] for data in nouveau_dictionnaire.values()]
        spending = [data['totalSpending'] for data in nouveau_dictionnaire.values()]

        plt.pie(spending, labels=categories, autopct='%1.1f%%')
        plt.title('Répartition du stock')

        # Sauvegarde du graphique dans un fichier image
        image_path = 'static/repartition_stock.png'
        plt.savefig(image_path)
        plt.close()

    return render_template('dashboard.html', nbreSpend=nbreSpend, ord=ord, image_path=image_path, nouveau_dictionnaire=nouveau_dictionnaire, nbre=nbre)


@app.route('/url/<user_id>')
def ulrd(user_id):
    return f'<h1>{user_id}</h1>'

if __name__ == "__main__":
    app.run(debug=True)
