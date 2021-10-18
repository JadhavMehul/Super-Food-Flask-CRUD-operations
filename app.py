from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///superfoods.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Superfoods(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    cnumber = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    food =  db.Column(db.String(20), nullable=False)
    ordered_at = db.Column(db.DateTime(20), default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.fname} - {self.lname} - {self.email} - {self.cnumber} - {self.address} - {self.food}"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/order", methods=['GET','POST'])
def order():
    if request.method=='POST':
        fnmae = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        add = request.form['address']
        food = request.form['food']
        superFoods = Superfoods(fname=fnmae, lname=lname, email=email, cnumber=phone, address=add, food=food)
        db.session.add(superFoods)
        db.session.commit()
    return render_template("order.html")

# @app.route("/booktable")
# def booktable():
#     return render_template("table.html")

@app.route("/admin")
def admin():
    allData = Superfoods.query.all()
    print(allData)
    return render_template("admin.html", allData=allData)

@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        add = request.form['address']
        food = request.form['food']
        newData = Superfoods.query.filter_by(sno=sno).first()
        newData.fname = fname
        newData.lname = lname
        newData.email = email
        newData.cnumber = phone
        newData.address = add
        newData.food = food
        db.session.add(newData)
        db.session.commit()
        return redirect("/admin")
    selectedData = Superfoods.query.filter_by(sno=sno).first()
    return render_template("update.html", selectedData=selectedData)

@app.route("/delete/<int:sno>")
def delete(sno):
    allData = Superfoods.query.filter_by(sno=sno).first()
    db.session.delete(allData)
    db.session.commit()

    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True, port=3000)