from flask import Flask, render_template, request, redirect
import models, db, utils
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from sqlalchemy import select
from datetime import datetime

app=Flask(__name__)

app.config["SECRET_KEY"] = "3jkshejkfhwleowjefkwe"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def loader_user(user_id, db = db.db_session()):
    user = db.get(models.Users, user_id)
    db.close()
    return user



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user/login/', methods=["POST"])
def user_login(db = db.db_session()):
    try:
        login_data = dict(request.form)
        user_name = login_data['Email']
        password = login_data["Password"]

        db_user = select(models.Users).where(models.Users.Email == user_name)
        db_user = db.scalars(db_user).all()

        #if user does not exists in databse
        if db_user == []:
            db.close()
            return render_template("index.html", err_msg = f"{user_name} does not exist")
        
        #if user exist
        db_user = db_user[0]
        hashed_pass = db_user.Pass

        verify_pass = utils.verify_pass(password, hashed_pass)
        if verify_pass == False:
            db.close()
            return render_template("index.html", err_msg = "Wrong password! Try again")
        login_user(db_user)
        db.close()
        return redirect("/home/")
    except Exception as err:
        db.close()
        return {"details" : str(err)}

@app.route('/home/')
@login_required
def user_home():
    return render_template("home.html")


@app.route('/user/logout/')
@login_required
def user_logout():
    logout_user()
    return redirect('/')


@app.route('/user/signup/', methods=["POST"])
def user_signup(db = db.db_session()): #db is filename, db_session is defined funtion to start a session
    try:
        form_data = dict(request.form)

        db_user = select(models.Users).where(models.Users.Email == form_data["email"])
        db_user=db.scalars(db_user).all()
        if db_user != []:
            db.close()
            return render_template ("index.html", err_msg = f"User with {form_data['email']} already exists")

        new_user = models.Users()
        new_user.First_name = form_data["f_name"]
        new_user.Last_name = form_data["l_name"]
        new_user.Email = form_data["email"]
        new_user.Username = form_data["email"]
        new_user.Ph_no = form_data["contact"]
        new_user.Pass = utils.get_hashed_pass(form_data["password"])
        new_user.Created_at = datetime.now()
        new_user.Updated_at = datetime.now()
        db.add(new_user)
        db.commit()
        db.close()
        mail_body = f"""Welcome {form_data['f_name']},
Thanks for joining BlogU!, your hub for trending blogs across diverse categories. Discover, create, and connect with passionate bloggers worldwide.





Happy blogging ahead,
The BlogU Crew 
"""
        utils.send_mail(to = form_data["email"], subject=f"{form_data['f_name']},welcome to BlogU!", mail_body = mail_body)

        return redirect('/')
    
    except Exception as err:
        db.close()
        return {"details": str(err)}


@app.route('/user/update/', methods=["POST"])
@login_required
def user_update(db = db.db_session()): #db is filename, db_session is defined funtion to start a session
    try:
        form_data = dict(request.form)

        db_user = select(models.Users).where(models.Users.Email == form_data["email"])
        db_user=db.scalars(db_user).all()
        db_user=db_user[0]


        db_user.First_name = form_data["f_name"]
        db_user.Last_name = form_data["l_name"]
       
        # new_user.Username = form_data["email"]
        db_user.Ph_no = form_data["contact"]
        # new_user.Pass = utils.get_hashed_pass(form_data["password"])
        # new_user.Created_at = datetime.now()
        db_user.Updated_at = datetime.now()
        
        db.commit()
        db.close()

        return redirect('/home/')
    
    except Exception as err:
        db.close()
        return {"details": str(err)}

    
@app.route('/user/changepassword/', methods=["POST"])
@login_required
def user_change_password(db = db.db_session()):
    try:
        form_data = dict(request.form)
        old_pass = form_data["OldPassword"]
        new_pass = form_data["NewPassword"]

        user_id = current_user.id
        db_user = db.get(models.Users, user_id)
        if not utils.verify_pass(old_pass, db_user.Pass):
            db.close()
            return render_template("home.html", args = "Old password does't match")
        new_hashed_pass = utils.get_hashed_pass(new_pass)
        db_user.Pass = new_hashed_pass
        db.commit()
        db.close
        return render_template("home.html", successMsg = "Password sucessfully changed")



    except Exception as err:
        db.close()
        return {"details":str(err)}, 401



@app.route('/user/forgtopassword/')
def forgot_password(db = db.db_session()):
    try:
        email = request.args.get("email")

        db_user = select(models.Users).where(models.Users.Email == email)
        db_user = db.scalars(db_user).all()

        if db_user == []:
            db.close()
            return render_template("index.html", err_msg= f"user with {email} does not exist")
        db_user = db_user[0]
        hashed_pass = utils.reset_password(db_user.Email, db_user.First_name)
        db_user.Pass = hashed_pass
        db.commit()
        db.close()


        return render_template("index.html", succ_msg= f"Your new password has been sent. Please check your mail.")


    except Exception as err:
        db.close()
        return {"detail:": str(err)}



if __name__=="__main__":
    app.run(debug=True)