from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,request,redirect,session,flash
from flask_app.models import user,post
bcrypt = Bcrypt(app)


@app.route('/post/create', methods=["POST"])
def create_post():
    if 'user_id' not in session:
        return redirect('/')
    if not post.Post.validate_post(request.form):
        return redirect('/dashboard')
    data = {
        "sender_id": request.form['sender_id'],
        "receiver_id": request.form['receiver_id'],
        "message" : request.form['message']
    }
    print(request.form)
    post.Post.create_post(data)
    session['counter'] +=1
    return redirect ('/dashboard')


@app.route('/post/delete/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/danger')
    data = {
        'id': id
    }
    post.Post.delete_post(data)
    return redirect('/dashboard')

@app.route('/danger')
def danger():
    return render_template("danger.html")