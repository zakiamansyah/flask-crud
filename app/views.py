from app import app, db
from app.models import Users, Employes
from flask import flash, render_template, redirect, url_for, request, session

@app.route('/')
def index():
    if 'email' in session:
        #db.session.query(nama_class_dari_table_di_database) -> fungsinya untuk get datanya
        data_employes = db.session.query(Employes)
        return render_template('index.html', data=data_employes)
    else:
        return redirect(url_for('login'))
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        users = Users(
            username = form['username'],
            email = form['email'],)
        users.set_password(form['password'])
        db.session.add(users)
        db.session.commit()
        
        flash("Success Register Account")
        
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/inputData', methods=['GET', 'POST'])
def inputData():
    if 'email' in session:
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
    else:
        return redirect(url_for('login'))
    

#inisialisasi parameter di routenya pake gituan
@app.route('/edit/<int:id>')
def getDataEdit(id):
    if 'email' in session:
        data_employes = Employes.query.get(id)
        
        return render_template('editData.html', data=data_employes)
    else:
        return redirect(url_for('login'))

@app.route('/postEdit', methods=['POST', 'GET'])
def postDataEdit():
    if 'email' in session:
        data_employes = Employes.query.get(request.form.get('id'))
    
        data_employes.name = request.form['name']
        data_employes.email = request.form['email']
        data_employes.telp = request.form['telp']
        data_employes.address = request.form['address']
        
        db.session.commit()
        
        flash('Edit Data Success')
        
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
    
@app.route('/deleteData/<int:id>')
def deleteData(id):
    if 'email' in session:
        data_employe = Employes.query.get(id)
        db.session.delete(data_employe)
        db.session.commit()

        flash('Delete Data Success')

        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))