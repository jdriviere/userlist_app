from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo

from forms import UserForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/new_users'

mongo = PyMongo(app)


@app.route('/')
def home():
    users = mongo.db.new_users.find({})

    return render_template('index.html', users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()

    if form.validate_on_submit():
        new_user = mongo.db.new_users
        new_user.insert({
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'username': form.username.data,
            'password': form.password.data,
        })

        flash('User registered successfully!', 'success')

        return redirect('register')

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
