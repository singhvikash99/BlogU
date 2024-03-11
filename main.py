from flask import Flask, render_template, request, redirect
import models, db, utils
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from sqlalchemy import select
from datetime import datetime
from sqlalchemy.orm import joinedload

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
def user_home(db = db.db_session()):
    db_category = select(models.Category)
    db_category = db.scalars(db_category).all()

    db_blogs = select(models.Blogs).where(models.Blogs.is_deleted == 0).options(joinedload(models.Blogs.blogs_user).load_only(
        models.Users.First_name
        )).options(
            joinedload(models.Blogs.blogs_category).load_only(
                models.Category.category
                )).options(
            joinedload(models.Blogs.blogs_responses).load_only(
                models.Response.response_type, models.Response.user_id
                ))

    db_blogs = db_blogs.order_by(models.Blogs.updated_at.desc())
    
    db_blogs = db.scalars(db_blogs).unique().all()
    db.close()
     
    return render_template("home.html", categories = db_category, blog_data = db_blogs)


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

@app.route('/blogs/create/', methods = ["POST"])
@login_required
def create_blog(db = db.db_session()):
    try:
        form_data = dict(request.form)
        new_blog = models.Blogs()
        new_blog.user_id = current_user.id
        new_blog.title = form_data["blog_title"]
        new_blog.content = form_data["blog_content"]
        new_blog.category_id = form_data["category"]
        new_blog.created_at = datetime.now()
        new_blog.updated_at = datetime.now()
        new_blog.is_deleted = 0
        db.add(new_blog)
        db.commit()

        db.close()

        return redirect('/home/')


    except Exception as err:
        db.close()
        return {"details" : str(err)}, 403

@app.route('/home/myblogs/')
@login_required
def my_blogs( db = db.db_session()):
    try:
        db_category = select(models.Category)
        db_category = db.scalars(db_category).all()

        db_blogs = select(models.Blogs).where((models.Blogs.user_id == current_user.id), (models.Blogs.is_deleted == 0)).options(joinedload(models.Blogs.blogs_user).load_only(
            models.Users.First_name
            )).options(
                joinedload(models.Blogs.blogs_category).load_only(
                    models.Category.category
                    )).options(
                joinedload(models.Blogs.blogs_responses).load_only(
                    models.Response.response_type, models.Response.user_id
                    ))

        db_blogs = db_blogs.order_by(models.Blogs.updated_at.desc())
        
        db_blogs = db.scalars(db_blogs).unique().all()
        db.close()
        
        return render_template("blogs.html", categories = db_category, blog_data = db_blogs)
        
    except Exception as err:
        db.close()
        return {"details" : str(err)}


@app.route('/blogs/update/', methods = ["POST"])
@login_required
def update_post(db = db.db_session()):
    try:
        form_data = dict(request.form)
        blog_id = int(request.args.get("blog_id"))

        db_blog = db.get(models.Blogs,blog_id)
        db_title = form_data['blog_title']
        db_blog.content = form_data['blog_content']
        db_blog.category_id = form_data[category]
        db_blog.updated_at = datetime.now()

        db.commit()
        db.close()

        return redirect ('/home/myblogs/')




    except Exception as err:
        db.close()
        return {"details" : str(err)}

@app.route('/blogs/delete/')
@login_required
def delete_post(db = db.db_session()):
    try:
        blog_id = int(request.args.get("blog_id"))

        db_blog = db.get(models.Blogs, blog_id)

        db_blog.is_deleted = 1

        db.commit()
        db.close

        return redirect('/home/myblogs/')

    except Exception as err:
        db.close()
        return {"details" : str(err)}

@app.route('/blogs/like/')
def like_blog(db = db.db_session()):
    try:
        blog_id = request.args.get("blog_id")
        
        db_blog = select(models.Blogs).where((models.Blogs.id == blog_id), (models.Blogs.is_deleted == 0))
        db_blog = db.scalars(db_blog).all()

        if not db_blog:
            db.close()
            return {"details" : str(err)}
        
        db_response = select(models.Response).where((models.Response.blog_id == blog_id), (models.Response.response_type == 1), (models.Response.user_id))
        db_response = db.scalars(db_response).first()
        if db_response:
            db.delete(db_response)
            db.commit()
            db.close()
            return redirect('/home/')

        new_resp = models.Response()
        new_resp.blog_id = blog_id
        new_resp.user_id = current_user.id 
        new_resp.response_type = 1
        db.add(new_resp)
        db.commit()
        db.close()

        return redirect ('/home/')

    except Exception as err:
        db.close()
        return {"details" : str(err)}, 403


if __name__=="__main__":
    app.run(debug=True)