from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.tea import Tea
from flask_app.models.user import User


@app.route('/new/tea')
def new_tea():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_tea.html',user=User.get_by_id(data))


@app.route('/create/tea',methods=['POST'])
def create_tea():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tea.validate_tea(request.form):
        return redirect('/new/tea')
    data = {
        "name": request.form["name"],
        "location": request.form["location"],
        "tea_color": request.form["tea_color"],
        "date_made": request.form["date_made"],
        "user_id": session["user_id"]
    }
    Tea.save(data)
    return redirect('/dashboard')

@app.route('/edit/tea/<int:id>')
def edit_tea(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_tea.html",edit=Tea.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/tea',methods=['POST'])
def update_tea():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tea.validate_tea(request.form):
        return redirect('/new/tea')
    data = {
        "name": request.form["name"],
        "location": request.form["location"],
        "tea_color": request.form["tea_color"],
        "date_made": request.form["date_made"],
        "id": request.form['id']
    }
    Tea.update(data)
    return redirect('/dashboard')

@app.route('/tea/<int:id>')
def show_tea(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    print(Tea.get_one(data))

    return render_template("show_tea.html",tea=Tea.get_one(data),user=User.get_by_id(user_data))

@app.route('/my_teas/<int:id>')
def my_teas(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": id
    }
    return render_template("my_tea.html",user=User.get_my_tea(user_data))

@app.route('/destroy/tea/<int:id>')
def destroy_tea(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Tea.destroy(data)
    return redirect('/dashboard')