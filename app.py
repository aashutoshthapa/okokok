from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, random secret key

# Sample data (replace with database connection and queries if using a database)
classes = {}  # Key: class name, Value: list of student dictionaries (name, attendance)
classes['12C'] = [
    {'name': 'Alice', 'attendance': ['1', '0', '1']},  # June 1, 2, 3
    {'name': 'Bob', 'attendance': ['0', '1', '0']},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/zatil', methods=['GET', 'POST'])
def zatil():
    if request.method == 'GET':
        return render_template('zatil_login.html')
    else:  # POST (login attempt)
        key = request.form['key']
        if key == 'zatilsirhandsome':
            session['zatil_logged_in'] = True
            return render_template('zatil_dashboard.html', classes=classes)
        else:
            return render_template('zatil_login.html', error='Incorrect key')

@app.route('/zatil/create_class', methods=['POST'])
def create_class():
    if 'zatil_logged_in' not in session:
        return 'Unauthorized', 401
    class_name = request.form['class_name']
    if class_name not in classes:
        classes[class_name] = []
        return render_template('zatil_dashboard.html', classes=classes, success='Class created')
    else:
        return render_template('zatil_dashboard.html', classes=classes, error='Class already exists')

@app.route('/zatil/edit_attendance/<class_name>', methods=['GET', 'POST'])
def edit_attendance(class_name):
    if 'zatil_logged_in' not in session:
        return 'Unauthorized', 401
    if class_name not in classes:
        return 'Class not found', 404
    if request.method == 'GET':
        return render_template('zatil_attendance.html', class_name=class_name, students=classes[class_name])
    else:  # POST (attendance update)
        for student in classes[class_name]:
            attendance_data = request.form.get(student['name'])
            if attendance_data:
                student['attendance'] = list(attendance_data)
                calculate_attendance_percentage(student)  # Update percentage
        return render_template('zatil_attendance.html', class_name=class_name, students=classes[class_name], success='Attendance updated')

@app.route('/students')
def students():
    return render_template('students_select.html', classes=list(classes.keys()))

@app.route('/students/view_attendance/<class_name>', methods=['GET'])
def view_attendance(class_name):
    if class_name not in classes:
        return 'Class not found', 404
    return render_template('students_attendance.html', class_name=class_name, students=classes[class_name])

def calculate_attendance_percentage(student):
    present
