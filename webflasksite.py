from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, PostForm
from sqlalchemy import Column, String, Integer
from sqlalchemy import insert
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

admin = Admin(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    #def __init__(self, id, username, email, image_file, password):
    #    self.id = id
    #    self.username = username
    #    self.email = email
    #    self.image_file = image_file
    #    self.password = password

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit_No = db.Column(db.String(21), nullable=False)


    def __repr__(self):
        return f"Session('{self.username}', '{self.sid}')"

    #def __init__(self, username, email, password):
     # self.email = email
     # self.password = password


#    def add_user(self):
#        db.session.add(self)
#        db.session.commit()

 #   def delete_user(self):
 #       db.session.delete(self)
 #       db.session.commit()

 #   def find_by_name(cls, name):
 #       return cls.filter_by(name == name).first()

 #   def update_user(self):
  #      db.session.commit()

#    def get_all_user(cls):
 #       return cls.query.all() 

        
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False) 
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}'):"


class Product(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)

    def __init__(self, pid, title, price, image):
        self.pid = pid
        self.title = title
        self.price = price
        self.image = image

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    comment = db.Column(db.Text)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer)
    product_name = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)


posts = [
    {
        'author': 'Ccc',
        'title': 'Blog Post1',
        'content': 'First post content',
        'date_posted': 'April 21, 2020'
    },
    {
    
        'author': 'HHH',
        'title': 'Good shop',
        'content': 'it is a really good shop with different brands',
        'date_posted': 'April 29, 2021'
    }
]

@app.route('/')

@app.route('/pay')
def pay():
    return render_template("cashier.html")
@app.route('/cashier', methods=['GET', 'POST'])
def cashier():
    if request.method == "POST":
        credit_No = request.values.get("credit_No")
        if credit_No != None:
            print(credit_No)
            credit = Payment(credit_No=credit_No)
            db.session.add(credit)
            db.session.commit()
            carts = session["cart"]
            user_id = session["user_id"]
            if carts != None and user_id != None:
                for x1 in carts:
                    ordersRec = Orders(user_id=user_id, product_id=x1["product"], product_name=x1["productTitle"], quantity=x1["quantity"], price=x1["unitPrice"])
                    db.session.add(ordersRec)
                    db.session.commit()
            flash(f"Thank you for your purchase!!")
            return redirect(url_for('home'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        product = request.values.get("search")
        print(product)
        #productList = Product.query.filter_by(title=product)
        productList = Product.query.filter(Product.title.like("%{}%".format(product)))
        if productList == None:
            print("cannot find the required product")
            flash("cannot find the required product")
        return render_template("Product.html", productList=productList )

    return render_template('product.html')



@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/addrec')
def addrec():
    ballGreenN = Product(1, 'ballGreenNike', 10, 'ballGreenNike.jpg')
    ballOrangeA = Product(2, 'ballOrangeAdidas', 12, 'ballOrangeAdidas.jpg')
    ballWhiteN = Product(3, 'ballWhiteNike', 23, 'ballWhiteNike.jpg')
    ballpack = Product(4, 'ballpack', 11, 'ballpack.jpg')
    db.session.add(ballGreenN)
    db.session.add(ballWhiteN)
    db.session.add(ballOrangeA)
    db.session.add(ballpack)
#    db.session.commit()
    print("db insert end")
    return render_template("assigment.html", posts=posts)

@app.route('/product')
def product():
    # This page shows all products
    productList = Product.query.all()
    return render_template("Product.html", productList=productList )

@app.route("/item/<int:id>")
def display_item(id):
    # This page show one product. Customer can add it to cart
    item = Product.query.filter_by(pid=id).first()

    # <<< debug
    print(item.pid)
    print(item.title)
    print(item.price)
    print(item.image)
    # >>> debug

    return render_template("Item.html", display_item=item)
@app.route('/add_to_cart/<int:id>',methods=["GET", "POST"])
def add_to_cart(id):
    quantity = request.values.get("quantity")
    productTitle = request.values.get("productTitle")
    unitPrice = request.values.get("unitPrice")
    print(id)
    print(quantity)
    print(productTitle)
    print(unitPrice)
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append({"product":id, "productTitle": productTitle, "quantity":quantity, "unitPrice": unitPrice})
    #print session[cart]
    flash("Successfully added to cart!")
    return redirect("/cart")

@app.route('/home')
def home():
    return render_template("assigment.html", posts=posts)

@app.route('/cart')
def cart():
    if 'user_id' in session:
        userId = session['user_id']
    else:
          flash("Please login")
          return redirect(url_for('account'))
    return render_template("Cart.html", posts=posts)
@app.route('/about' ,methods=['GET','POST'])
def about():
    if request.method == "POST":
        if 'user_id' in session:
            commentStr = request.values.get("comment")
            userId = session['user_id']
            commentRec = Comment(user_id=userId, comment=commentStr)
            db.session.add(commentRec)
            db.session.commit()
            flash("thank you for your comments")
            return redirect(url_for('about'))
        else:
            flash("Please login")
            return redirect(url_for('account'))

    form=PostForm()

    return render_template("About.html", posts=posts, form=form)

@app.route('/comment' , methods=["GET", "POST"])
def submitComment():
    if request.method == "POST":
       if  "username" in session:
        commentStr = request.values.get("comment")
        userId = session['user_id']
        commentRec = Comment(user_id=userId, comment=commentStr)
        db.session.add(commentRec)
        db.session.commit()
        flash("thank you for your comments")
        return redirect(url_for('about'))
       else:
          return redirect(url_for('account'))
    else:
        return "GET comment"

@app.route('/blog',methods=["GET", "POST"])
def writeBlog():
    if request.method == "POST":
       if  "username" in session:
        email = request.values.get("email")
        title = request.values.get("title")
        content = request.values.get("content")
        user_id = session['user_id']
        blogRec = Post(user_id=user_id, title=title, content=content, email=email)
        db.session.add(blogRec)
        db.session.commit()
        blogs = Post.query.all()
        form=PostForm()
        return render_template("About.html", blogs=blogs, form=form, posts=posts)
       else:
          return redirect(url_for('account'))
    else:
        return "GET blog"

@app.route('/account' ,methods=['GET','POST'])
def account():
    error = None
    if request.method == "POST":
        username = request.values.get("username")
        password = request.values.get("password")

        # debug
        print(username)
        print(password)

        userRec = User.query.filter_by(username=username, password=password).first()

        if userRec != None:
            print(userRec.email)
            session['username'] = request.form['username']
            session['user_id'] = userRec.id
            return redirect(url_for('home'))
        else:
            print("record not found")
            flash("Invalid username/password: " + username + "/" + password)
            error = "Username / Passord: " + username + "/" + password + " not found!!"

    if 'username' in session:
        session.pop('username', None)
        return render_template('assigment.html', post=posts)
    else:
        return render_template('Account.html', post=posts)


@app.route('/register',methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.values.get("username")
        password = request.values.get("password")
        confirm_password = request.values.get("confirm_password")
        email = request.values.get("email")

        print(password)
        print(confirm_password)
        print(email)
        
        name = User.query.filter_by(username=username).first()
        user_email =  User.query.filter_by(email=email).first()
        
        if name == None:
            if user_email == None:
                if password == confirm_password:
                    new_user = User(username=username, password=confirm_password, email=email)
                    print(new_user)
                    db.session.add(new_user)
                    db.session.commit()
                    flash(f"user created {username} !!")
                    return redirect(url_for('account'))
                else:
                    flash('wrong password')
            else:
                flash(" this email  has been taken ")
                return redirect(url_for('register'))
        else:
            flash(" this username has been taken ")
            return redirect(url_for('register'))

                
    
    return render_template("Register.html", posts=posts)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Payment, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Orders, db.session))

if not os.path.exists('site.db'):
    db.create_all()
 
else:
    app.run(debug=True)
