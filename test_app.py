from flask import Flask, render_template, request, redirect, session
import csv, random, os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Define the path to the CSV file
CSV_FILE = 'College_Students.csv'

# Check if the CSV file exists, if not, create it with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Stu_ID', 'Stu_FullName', 'Age', 'Stu_ContactNo', 'Stu_Email', 'Address', 'Department', 'Specialization', 'School', 'Program_Year', 'Father_Name', 'Mother_Name', 'P_ContactNo', 'P_Email'])
        writer.writeheader()


# Function to read data from the CSV file
def read_csv():
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)


# Function to write data to the CSV file
def write_csv(students):
    with open(CSV_FILE, 'w', newline='') as file:
        fieldnames = ['Stu_ID', 'Stu_FullName', 'Age', 'Stu_ContactNo', 'Stu_Email', 'Address', 'Department',
                      'Specialization', 'School', 'Program_Year', 'Father_Name', 'Mother_Name', 'P_ContactNo', 'P_Email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)


# Function to generate a random unique student ID
def generate_unique_id():
    while True:
        student_id = random.randint(1000, 9999)
        students = read_csv()
        if not any(student['Stu_ID'] == str(student_id) for student in students):
            return str(student_id)


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == '123' and password == '123':
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', message='Invalid credentials. Please try again.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        # Generate a random unique student ID
        Stu_Id = generate_unique_id()
        return render_template('add_student.html', Stu_Id=Stu_Id)
    
    elif request.method == 'POST':
        # Generate a random unique student ID
        Stu_Id = generate_unique_id()
        
        # Get the student details from the form
        Stu_Id = request.form['Stu_ID']
        Stu_FullName = request.form['Stu_FullName']
        Age = request.form['Age']
        Stu_ContactNo = request.form['Stu_ContactNo']
        Stu_Email = request.form['Stu_Email']
        Address = request.form['Address']
        Department = request.form['Department']
        Specialization = request.form['Specialization']
        School = request.form['School']
        Program_Year = request.form['Program_Year']
        Father_Name = request.form['Father_Name']
        Mother_Name = request.form['Mother_Name']
        P_ContactNo = request.form['P_ContactNo']
        P_Email = request.form['P_Email']
        
        # Add student to the CSV file
        students = read_csv()
        
        students.append({'Stu_ID': Stu_Id, 'Stu_FullName': Stu_FullName, 'Age': Age, 'Stu_ContactNo': Stu_ContactNo, 'Stu_Email': Stu_Email, 'Address': Address, 'Department': Department, 'Specialization': Specialization, 'School': School, 'Program_Year': Program_Year, 'Father_Name': Father_Name, 'Mother_Name': Mother_Name, 'P_ContactNo': P_ContactNo, 'P_Email': P_Email})
        
        write_csv(students)
        return redirect('/')


@app.route('/search_student', methods=['POST'])
def search_student():
    Stu_Id = request.form['Stu_ID']
    students = read_csv()
    for student in students:
        if student['Stu_ID'] == Stu_Id:
            return render_template('student.html', student=student)
    return 'Student not found!'


@app.route('/update_student', methods=['GET', 'POST'])
def update_student():
    if request.method == 'GET':
        return render_template('update_student.html')
    
    elif request.method == 'POST':
        Stu_Id = request.form['Stu_ID']
        Stu_FullName = request.form['Stu_FullName']
        Age = request.form['Age']
        Stu_ContactNo = request.form['Stu_ContactNo']
        Stu_Email = request.form['Stu_Email']
        Address = request.form['Address']
        Department = request.form['Department']
        Specialization = request.form['Specialization']
        School = request.form['School']
        Program_Year = request.form['Program_Year']
        Father_Name = request.form['Father_Name']
        Mother_Name = request.form['Mother_Name']
        P_ContactNo = request.form['P_ContactNo']
        P_Email = request.form['P_Email']
            
        students = read_csv()
        for student in students:
            if student['Stu_ID'] == Stu_Id:
                student['Stu_FullName'] = Stu_FullName
                student['Age'] = Age
                student['Stu_ContactNo'] = Stu_ContactNo
                student['Stu_Email'] = Stu_Email
                student['Address'] = Address
                student['Department'] = Department
                student['Specialization'] = Specialization
                student['School'] = School
                student['Program_Year'] = Program_Year
                student['Father_Name'] = Father_Name
                student['Mother_Name'] = Mother_Name
                student['P_ContactNo'] = P_ContactNo
                student['P_Email'] = P_Email
                
                write_csv(students)
                return 'Student record updated successfully !!'
    return 'Student record not found !!'


@app.route('/delete_student', methods=['POST'])
def delete_student():
    Stu_Id = request.form['Stu_ID']
    students = read_csv()
    for student in students:
        if student['Stu_ID'] == Stu_Id:
            students.remove(student)
            write_csv(students)
            return 'Student record deleted successfully !!'
    return 'Student record not found !!'


@app.route('/display_students')
def display_students():
    students = read_csv()
    return render_template('students.html', students=students)


if __name__ == '__main__':
    app.run(debug=True)
