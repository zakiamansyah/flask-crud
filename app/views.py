from app import app, db
from app.models import Users, Employes
from flask import flash, render_template, redirect, url_for, request, session, jsonify

@app.route('/')
def index():
    if 'users' in session.keys():
        #db.session.query(nama_class_dari_table_di_database) -> fungsinya untuk get datanya
        data_employes = db.session.query(Employes)
        return render_template('index.html', data=data_employes)
    else:
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
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        
        form = request.form
        users = Users.query.filter_by(email=form['email']).first()

        if users and users.check_password(form['password']):
            session['users'] = users.id
            return redirect(url_for('index'))
        else:
            flash("Password was incorrect or user doesn't exist.")
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('users', None)
    return redirect(url_for('index'))

@app.route('/inputData', methods=['GET', 'POST'])
def inputData():
    if 'users' in session.keys():
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
        return render_template('login.html')

#inisialisasi parameter di routenya pake gituan
@app.route('/edit/<int:id>')
def getDataEdit(id):
    if 'users' in session.keys():
        data_employes = Employes.query.get(id)
        
        return render_template('editData.html', data=data_employes)
    else:
        return render_template('login.html')
    
@app.route('/postEdit', methods=['POST', 'GET'])
def postDataEdit():
    if 'users' in session.keys():
        data_employes = Employes.query.get(request.form.get('id'))

        data_employes.name = request.form['name']
        data_employes.email = request.form['email']
        data_employes.telp = request.form['telp']
        data_employes.address = request.form['address']
        
        db.session.commit()
        
        flash('Edit Data Success')
        
        return redirect(url_for('index'))
    else:
        return render_template('login.html')    
    
@app.route('/deleteData/<int:id>')
def deleteData(id):
    if 'users' in session.keys():
        data_employe = Employes.query.get(id)
        db.session.delete(data_employe)
        db.session.commit()

        flash('Delete Data Success')

        return redirect(url_for('index'))
    else:
        return render_template('login.html')