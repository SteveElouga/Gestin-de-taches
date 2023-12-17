from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/gestiondetache'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"Todo: {self.name}"
    

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        new_task = Task(name=name, description=description)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception:
            return new_task
    else:    
        tasks = Task.query.order_by(Task.createdAt)
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>/")
def delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "Une erreur s'est produite lors de la suppression de tache."
    
@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id): 
    task = Task.query.get_or_404(id)   
    if request.method == "POST":
        task.description = request.form['description']
        task.name = request.form["name"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception:
            return "Nous ne pouvons pas modifier la tache"
    else:
        title = "Mise a jour"    
        return render_template("update.html", title=title, task=task)

@app.route('/about/')
def method_name():
    return render_template("about.html")



if __name__ == '__main__':
    app.run(debug=True)



# ====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================


