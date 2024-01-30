from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from model import db, User, Book, Section, Borrowing, Issued  # Database Information and importing Here

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Laibrary_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

with app.app_context():
    db.init_app(app)
    db.create_all()
'''======================================== This is a Index Route ================================================================'''
@app.route('/')
def index():
    return render_template('index.html')

'''======================================== This is a User Login  Route ================================================================'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('User does not exist')
            return redirect(url_for('login'))

        if not user.check_password(password):
            flash('Incorrect Password')
            return redirect(url_for('login'))

        # Login successful, redirect to the user page
        return redirect(url_for('user_dashboard'))
        # return "Hello world"

    # If the request method is GET, render the login template
    return render_template('login.html')

'''======================================== This is a Admin Login Route ================================================================'''
@app.route('/admin_login', methods=['Get','Post'])
def admin_login():
    username = None
    password = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'admin':
            return redirect(url_for('admin'))

    return render_template('admin_login.html')

'''======================================== This is a New User Register Route ================================================================'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        occupation = request.form.get('occupation')
        # Validate form data
        if not all((username, password, name,occupation)):
            flash('Invalid form data. Please fill in all fields.')
            return redirect(url_for('register'))

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different username.')
            return redirect(url_for('register'))

        # Create a new user and add to the database
        user = User(username=username, password=password, name=name,occupation=occupation)
        db.session.add(user)
        db.session.commit()

        flash('User successfully registered. You can now log in.')
        return redirect(url_for('login'))

    # If the request method is GET, render the registration template
    return render_template('register.html')

'''======================================== This is a User Dashboard Route ================================================================'''
@app.route('/user')
def user_dashboard():
    return render_template('user_main.html')

'''======================================== This is a Admin Dashboard Route ================================================================'''
#============================== This is a Admin Dashboard Routes ================>
@app.route('/admin')
def admin():
    return render_template('/admin/admin_main.html')
#============================== This is a Admin-Section Routes ===================>
@app.route('/admin/section')
def section():
    sections = Section.query.all()
    return render_template('/admin/admin_section.html', Sections=sections)
#======================== Add Section Routes ================>
@app.route('/section/add_section', methods=['GET', 'POST'])
def add_section():
    if request.method == 'POST':
        sect_name = request.form.get('section_name')
        sect_desc = request.form.get('section_desc')

        if sect_name=='' or sect_desc=='':
            flash('Section does not exist.', 'error')
        elif Section.query.filter_by(name=sect_name).first():
            flash('Section name already exists. Please choose a different name.')
        else:
            # Create a new section with the current date and time
            section = Section(name=sect_name, description=sect_desc, date_created=datetime.now())
            db.session.add(section)
            db.session.commit()
            flash('Section added successfully.', 'success')
            return redirect(url_for('section'))

    return render_template('/admin/add_section.html')


#======================== Edit Section Routes ================>
@app.route('/section/<int:id>/edit_section',methods=['GET','POST'])
def edit_section(id):
    section = Section.query.get(id)

    if request.method == 'POST':
        new_name = request.form.get('section_name')
        new_description = request.form.get('section_desc')

        section.name = new_name
        section.description = new_description

        db.session.commit()

        flash('Section updated successfully.')

        return redirect(url_for('section'))

    return render_template('/admin/edit_section.html')
#======================== Delete Section Routes ================>
@app.route('/section/<int:id>/delete_section')
def delete_section(id):
    section = Section.query.get(id)
    if not section:
        flash('Section does not exist.')
        return redirect(url_for('section'))
    db.session.delete(section)
    db.session.commit()
    flash('Section deleted successfully.')
    return redirect(url_for('section'))
#=========================== This is a Admin-Section Books Routes ================>
@app.route('/section/<int:id>/books')
def books(id):
    section = Section.query.get(id)
    books = Book.query.filter_by(section_id=id).all()
    return render_template('/admin/admin_books.html', section=section, books=books)

#=========================== This is a Admin-Reader Routes =======================>
@app.route('/admin/reader')
def reader():
    return render_template('/admin/admin_Reader.html')


'''======================================== This is a Debug statement ================================================================'''

if __name__ == '__main__':
    app.run(debug=True)
