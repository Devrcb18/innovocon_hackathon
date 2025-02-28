import webview
from flask import Flask, render_template, request, redirect, url_for, jsonify
import smtplib
from email.message import EmailMessage
import threading

app = Flask(__name__)
app.secret_key = "stud"

questions = [
    {
        "question": "1. What is the SI unit of electric current?",
        "options": ["Ohm", "Volt", "Ampere", "Watt"],
        "answer": "Ampere"
    },
    {
        "question": "2. Which device is used to measure electric current?",
        "options": ["Voltmeter", "Ammeter", "Ohmmeter", "Galvanometer"],
        "answer": "Ammeter"
    },
    {
        "question": "3. Ohm's law is represented by which equation?",
        "options": ["V = IR", "P = IV", "F = ma", "E = mc²"],
        "answer": "V = IR"
    },
    {
        "question": "4. Which material is commonly used as an electrical insulator?",
        "options": ["Copper", "Iron", "Rubber", "Aluminum"],
        "answer": "Rubber"
    },
    {
        "question": "5. What is the function of a diode in an electrical circuit?",
        "options": ["To increase resistance", "To store energy", "To allow current to flow in one direction", "To amplify signals"],
        "answer": "To allow current to flow in one direction"
    },
    {
        "question": "6. What is the SI unit of electrical resistance?",
        "options": ["Ohm", "Volt", "Ampere", "Watt"],
        "answer": "Ohm"
    },
    {
        "question": "7. Which law states that the current through a conductor is directly proportional to the voltage across it?",
        "options": ["Faraday's Law", "Ohm's Law", "Kirchhoff's Law", "Coulomb's Law"],
        "answer": "Ohm's Law"
    },
    {
        "question": "8. What is the SI unit of electric charge?",
        "options": ["Joule", "Coulomb", "Volt", "Ampere"],
        "answer": "Coulomb"
    },
    {
        "question": "9. Which component is used to store electrical energy in a circuit?",
        "options": ["Resistor", "Capacitor", "Inductor", "Diode"],
        "answer": "Capacitor"
    },
    {
        "question": "10. What is the primary function of a transformer?",
        "options": ["To convert AC to DC", "To step up or step down voltage", "To store electrical energy", "To measure current"],
        "answer": "To step up or step down voltage"
    }
]


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'devrcb1845@gmail.com'
EMAIL_PASSWORD = 'eexq ckjq nhah eznn' 
# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/creators.html')
def creator():
    return render_template("creators.html")

@app.route('/mcq.html', methods=['GET', 'POST'])
def mcq():
    if request.method == 'POST':
        user_answers = request.form
        score = 0

        for i, question in enumerate(questions):
            if user_answers.get(str(i)) == question["answer"]:
                score += 1

        return redirect(url_for('result', score=score))

    return render_template("mcq.html", questions=questions)

@app.route('/results.html')
def result():
    score = request.args.get('score', type=int)
    return render_template('results.html', score=score, total=len(questions))

@app.route('/circuit.html')
def circuit():
    return render_template('circuit.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    user_email = request.json.get('email')
    user_score = request.json.get('score')

    subject = "Your MCQ Test Score"
    body = f"""
    Hello,

    Congratulations on completing the MCQ Test!
    Your Score: {user_score}

    Keep learning and growing!

    Best regards,
    Team Web_Weavers
    """

    try:
        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.set_content(body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({'message': 'Email sent successfully!'})
    except Exception as e:
        print(f"Error: {e}") 
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(port=5000)).start()
    webview.create_window('Student Portal', 'http://localhost:5000')
    webview.start()