from flask import Flask, render_template, request, redirect
import models, db
from sqlalchemy import select
from datetime import datetime

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user/login/')
def user_login():
    pass
    return render_template("index.html")

@app.route('/user/signup/', methods=["POST"])
def user_signup(db = db.db_session()): #db is filename, db_session is defined funtion to start a session
    try:
        form_data = dict(request.form)

        db_user = select(models.Users).where(models.Users.Email == form_data["email"])
        if db_user != []:
            db.close()
            return render_template ("index.html", err_msg = f"User with {form_data['email']} already exists")

        new_user = models.Users()
        new_user.First_name = form_data["f_name"]
        new_user.Last_name = form_data["l_name"]
        new_user.Email = form_data["email"]
        new_user.Ph_no = form_data["contact"]
        new_user.Pass = form_data["password"]
        new_user.Created_at = datetime.now()
        new_user.Updated_at = datetime.now()
        new_user.Username = form_data["username"]
        db.add(new_user)
        db.commit()
        db.close()

        return redirect('/')
    
    except Exception as err:
        db.close()
        return {"details": str(err)}

    
    




if __name__=="__main__":
    app.run(debug=True)