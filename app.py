from flask import Flask, render_template, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'users'
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)

# WTForms for Registration and Login
class CustomerForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    pincode = StringField("Pincode", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route('/', methods=['GET', 'POST'])
def register():
    form = CustomerForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data
        address = form.address.data
        city = form.city.data
        pincode = form.pincode.data

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store data into database
        cursor = mysql.connection.cursor()

        # Check if the email already exists
        cursor.execute('SELECT email FROM user_table WHERE email = %s', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('This email is already registered. Please use a different email or log in.', 'danger')
            cursor.close()
            return redirect(url_for('register'))

        cursor.execute(
            'INSERT INTO user_table (email, password, name, address, city, pincode) VALUES (%s, %s, %s, %s, %s, %s)',
            (email, hashed_password, name, address, city, pincode))
        mysql.connection.commit()
        cursor.close()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user_table WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            session['user'] = user[0]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        email = session['user']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user_table WHERE email = %s', (email,))
        user_info = cursor.fetchone()
        cursor.close()
        return render_template('dashboard.html', user=user_info)
    else:
        flash('You need to log in first!', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=7000)
