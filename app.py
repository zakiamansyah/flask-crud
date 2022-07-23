from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "asdijqidkanasdawdsdsdwasqwddandiqnwwdia"

#membuat koneksi ke server db kita
userpass = "mysql+pymysql://root:1122"
basedir = "127.0.0.1"
dbname = "/company"

#konfigurasi yang ada di lib flask sqlalchemy 
app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#inisialisasi db yang udah di konekin ke server db kita
db = SQLAlchemy(app)

#ini ngebuat modelnya interaksi dari tabel di database
#harus diperhatikan nama classnya harus sama percis dangan table besar kecil hurufnya
class employes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telp = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    
    #inisialisasi penggunaan table menjadi variable
    def __ini__(self, name, email, telp, address):
        self.name = name
        self.email = email
        self.telp = telp
        self.address = address

@app.route('/')
def index():
    data_employes = db.session.query(employes)
    return render_template('index.html', data=data_employes)

@app.route('/inputData', methods=['GET', 'POST'])
def inputData():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        telp = request.form['telp']
        address = request.form['address']
        
        input_data = employes(name, email, telp, address)
        
        db.session.add(input_data)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('inputData.html')