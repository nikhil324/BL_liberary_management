from flask import Flask,render_template,request,flash,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,login_required,logout_user,UserMixin,current_user
from datetime import datetime
import sqlite3
app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///liberaries.db'
app.secret_key="nikhil@1234" 
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)


class Accounts(UserMixin,db.Model):
    id_no=db.Column(db.TEXT(50),primary_key=True)
    password=db.Column(db.TEXT(50))
    fees=db.Column(db.INTEGER)
    date=db.Column(db.TEXT(10),index = True,default=datetime.now)

    def get_id(self):
      return self.id_no

@login_manager.user_loader
def user_loader(id_no):
  return Accounts.query.get(id_no)      
  
         
  def __repr__(self):
    return self.id_no   
class Visit(UserMixin,db.Model):
    name=db.Column(db.TEXT(50),primary_key=True)
    add=db.Column(db.TEXT(50))
    date=db.Column(db.TEXT(10),index = True,default=datetime.now)

    def get_id(self):
      return self.name
     
@app.route("/")
def home():
	return render_template("index.html")
@app.route("/login")	
def login():
	return render_template("login.html")
@app.route("/choice",methods=['GET', 'POST'])
def choice():
    if request.method=='POST':
        ids = request.form.get('ids_no')
        pas = request.form.get('password')
        if ids and pas:
          user = Accounts.query.filter_by(id_no=ids,password=pas).first()    
          if user:
            login_user(user, remember=True)
            return render_template("offered.html")
          else:
            flash('PLEASE ENTER VALID USERID OR PASSWORD','danger')
            return redirect(url_for('login'))
        else:
          flash('PLEASE FILL ALL REQUIRED','danger')
          return redirect(url_for('login'))
              
class Books(db.Model):
    books = db.Column(db.TEXT(50), primary_key=True)            
@app.route("/read",methods=['GET', 'POST'])
def read():
    if request.method=='POST':
        book = request.form.get('book1')
        if book:
            user= Books.query.filter_by(books=book).first()    
            if user:
                return render_template("read.html")
            else:
             flash('THIS BOOK IS NOT AVAILIABLE IN MY LIBERARY PLEASE CHOOSE ANOTHER BOOK!!!','danger')
             return render_template('offered.html')
        else:
          flash('PLEASE ENTER BOOK NAME','danger')
          return render_template('offered.html')
class lib(UserMixin,db.Model):
    id_no = db.Column(db.TEXT(50), primary_key=True)
    books = db.Column(db.TEXT(50))
    Return_book = db.Column(db.TEXT(50))
    date=db.Column(db.TEXT(10),index = True,default=datetime.now)
@login_required
@app.route("/withdraw",methods=['GET', 'POST'])
def withdraw():
    if request.method=='POST':
        book = request.form.get('book2')
        id=current_user.id_no
        if book:
            user= Books.query.filter_by(books=book).first()    
            if user:
                sob = lib(books=book,id_no=id)
                db.session.add(sob)
                db.session.commit()
                return render_template("read.html")
            else:
             flash('THIS BOOK IS NOT AVAILIABLE IN MY LIBERARY PLEASE CHOOSE ANOTHER BOOK!!!','danger')
             return render_template('offered.html')
        else:
          flash('PLEASE ENTER BOOK NAME','danger')
          return render_template('offered.html')
@app.route("/return",methods=['GET', 'POST'])          
def returned():
    if request.method=='POST':
        book = request.form.get('book3')
        id=current_user.id_no
        if book:
            user= Books.query.filter_by(books=book).first()    
            if user:
                sob = lib(books=book,id_no=id,Return_book=book)
                db.session.add(sob)
                db.session.commit()
                flash('YOUR BOOK RETURNED SUCCESSFULLY!!!','success')
                return render_template("offered.html")
             
            else:
             flash('THIS BOOK IS NOT FROM MY LIBERARY!!!','danger')
             return render_template('offered.html')
        else:
          flash('PLEASE ENTER BOOK NAME','danger')
          return render_template('offered.html')          
@app.route("/new_acc")
def new_acc():
     return render_template('new_account.html')          
@app.route("/signin",methods=['GET','POST'])
def signin():
    if request.method=='POST':
            new_id = request.form.get('user_id')
            pas = request.form.get('password')
            fees=2000
            if new_id and pas:
              user = Accounts.query.filter_by(id_no=new_id).first()    
              if user:
                  flash("this id is already exist please enter unique id:","danger")
                  return render_template("new_account.html")
              else:
                  acc=Accounts(id_no=new_id,password=pas,fees=fees)
                  db.session.add(acc)
                  db.session.commit()
                  flash("your account has been created successfully!!!","success")
                  return render_template("new_account.html")
            else:
                return print("fill all required!!!")                                 
@app.route('/guest')
def guest():
    return render_template("guest.html")    
@app.route("/guest_load",methods=['GET','POST']) 
def guest_load():
  if request.method=='POST':
        guest_id = request.form.get('user_name')
        guest_add = request.form.get('add')
        if guest_id and guest_add:
                  gst=Visit(name=guest_id,add=guest_add)
                  db.session.add(gst)
                  db.session.commit()
                  flash("you visit in my liberary successfully!!!","success")
                  return render_template("choose.html")
        else:
         return print("fill all required!!!")                     

@app.route("/readg",methods=['GET', 'POST'])
def readg():
    if request.method=='POST':
        book = request.form.get('book1')
        if book:
            user= Books.query.filter_by(books=book).first()    
            if user:
                return render_template("read.html")
            else:
             flash('THIS BOOK IS NOT AVAILIABLE IN MY LIBERARY PLEASE CHOOSE ANOTHER BOOK!!!','danger')
             return render_template('offered.html')
        else:
          flash('PLEASE ENTER BOOK NAME','danger')
          return render_template('choose.html')
class Local(UserMixin,db.Model):
    name = db.Column(db.TEXT(50), primary_key=True)
    address = db.Column(db.TEXT(50))
    book = db.Column(db.TEXT(50))
    security_money = db.Column(db.INTEGER)
    return_money = db.Column(db.INTEGER)
    date=db.Column(db.TEXT(10),index = True,default=datetime.now)
    non_refendable= db.Column(db.INTEGER)          
@login_required          
@app.route("/withdrawg",methods=['GET', 'POST'])
def withdrawg():
    if request.method=='POST':
        book = request.form.get('book2')
        name=request.form.get('name')
        add=request.form.get('add')
        security=1000
        non=100
        if book:
            user= Books.query.filter_by(books=book).first()
            id_no=Visit.query.filter_by(name=name,add=add).first()    
            if id_no:
              if user:
                sob = Local(book=book,name=name,address=add,security_money=security,non_refendable=non)
                db.session.add(sob)
                db.session.commit()
                return render_template("read.html")
              else:
                flash('THIS BOOK IS NOT AVAILIABLE IN MY LIBERARY PLEASE CHOOSE ANOTHER BOOK!!!','danger')
                return render_template('choose.html')  
            else:
             flash('PLEASE ENTER VALID USER NAME AND ADDRESS!!!! ','danger')
             return render_template('choose.html')
        else:
          flash('PLEASE ENTER BOOK NAME','danger')
          return render_template('choose.html')          

@app.route("/returng",methods=['GET', 'POST'])
def returng():
    if request.method=='POST':
        book = request.form.get('book3')
        name=request.form.get('name')
        add=request.form.get('add')
        return_mon=900
        if book:
            user= Books.query.filter_by(books=book).first()
            id_no=Visit.query.filter_by(name=name,add=add).first()    
            if id_no:
              if user:
                sob = Local(book=book,name=name,address=add,return_money=return_mon)
                db.session.add(sob)
                db.session.commit()
                return render_template("read.html")
              else:
                flash('THIS BOOK IS NOT AVAILIABLE IN MY LIBERARY PLEASE CHOOSE ANOTHER BOOK!!!','danger')
                return render_template('choose.html')  
            else:
             flash('PLEASE ENTER VALID USER NAME AND ADDRESS!!!! ','danger')
             return render_template('choose.html')
        else:
          flash('PLEASE ENTER BOOK NAME','danger')
          return render_template('choose.html')
@app.route('/logout')
def remove():
   return render_template('login.html')           
@app.route('/remove')
def logout():
  id=current_user.id_no

  user= Accounts.query.filter_by(id_no=id).delete()    
  if user:
    
    db.session.commit()
    flash('YOUR ACCOUNT HAS BEEN REMOVED SUCCESSFULLY!!!','success')
    return render_template("index.html")         
if __name__ == '__main__':          
	app.run(debug=True)