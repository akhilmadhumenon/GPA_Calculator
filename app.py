
from flask import Flask, render_template, request

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

def calculate_gpa(grades, credits):
    total_credits = sum(credits)
    weighted_sum = sum(grade_dict[grade] * credit for grade, credit in zip(grades, credits))
    gpa = weighted_sum / total_credits
    return gpa

grade_dict = {'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6, 'E': 5, 'F': 0}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_subjects = int(request.form['num_subjects'])
        return render_template('calculator.html', num_subjects=num_subjects)
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    num_subjects = int(request.form['num_subjects'])
    grades = [request.form[f'grade_{i}'].upper() for i in range(1, num_subjects + 1)]
    credits = [float(request.form[f'credit_{i}']) for i in range(1, num_subjects + 1)]

    # Check if the entered grade is valid
    for grade in grades:
        if grade not in grade_dict:
            return render_template('calculator.html', num_subjects=num_subjects, error_message=f"Invalid grade '{grade}'. Please enter a valid grade.")

    gpa = calculate_gpa(grades, credits)
    return render_template('result.html', gpa_result=f"{gpa:.2f}")

if __name__ == '__main__':
    app.run(debug=True)
