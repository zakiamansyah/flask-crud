from flask import Flask, flash, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#setiap menggunakan sqlalchemy inisialisasi secret key dari random str
app.secret_key = "E0wf9V5EK+0zO3QXuH7iKiAakj2ZndhMRKj7i+AbK+E="

#membuat koneksi ke server db kita
#setiap akhiran dari password dikasih @
userpass = "mysql+pymysql://root:1122@"
basedir = "127.0.0.1"
dbname = "/company"

#konfigurasi yang ada di lib flask sqlalchemy 
app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#inisialisasi db yang udah di konekin ke server db kita
db = SQLAlchemy(app)

#ini ngebuat modelnya interaksi dari tabel di database
#harus diperhatikan nama classnya harus sama percis dangan table besar kecil hurufnya
class Employes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telp = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    
    #inisialisasi penggunaan table menjadi variable
    def __init__(self, name, email, telp, address):
        self.name = name
        self.email = email
        self.telp = telp
        self.address = address
    
@app.route('/')
def index():
    #db.session.query(nama_class_dari_table_di_database) -> fungsinya untuk get datanya
    data_employes = db.session.query(Employes)
    return render_template('index.html', data=data_employes)

@app.route('/inputData', methods=['GET', 'POST'])
def inputData():
    #jika methode post yang terpenuhi maka langsung ke proses request data dari field dalam table database
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        telp = request.form['telp']
        address = request.form['address']
        
        #proses input datanya ke table database
        input_data = Employes(name, email, telp, address)
        
        #db.session.add(variable input data) -> berfungsi sebagai INSERT untuk database 
        db.session.add(input_data)
        #db.session.commit() -> setiap melakukan INSERT di sqlalchemy selalu harus memanggil commit agar proses insert bisa terupdate
        db.session.commit()
        
        flash("Input Data Success")
        
        return redirect(url_for('index'))
    
    return render_template('inputData.html')

#inisialisasi parameter di routenya pake gituan
@app.route('/edit/<int:id>')
def getDataEdit(id):
    data_employes = Employes.query.get(id)
    return render_template('editData.html', data=data_employes)

@app.route('/postEdit', methods=['POST', 'GET'])
def postDataEdit():
    data_employes = Employes.query.get(request.form.get('id'))
    
    data_employes.name = request.form['name']
    data_employes.email = request.form['email']
    data_employes.telp = request.form['telp']
    data_employes.address = request.form['address']
    
    db.session.commit()
    
    flash('Edit Data Success')
    
    return redirect(url_for('index'))

@app.route('/deleteData/<int:id>')
def deleteData(id):
    data_employe = Employes.query.get(id)
    db.session.delete(data_employe)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('index'))