
from flask import Flask, request, session, redirect, url_for, flash
import random
from datetime import datetime, timedelta

# Flask-app instellen
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Simuleer een gebruikersdatabase
users = {
    "0612345678": {"email": "jaime@example.com", "otp": None, "otp_expires": None}
}

# HTML-template met Bootstrap
base_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">84Ideas</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="/about">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="/login">Login</a></li>
                    <li class="nav-item"><a class="nav-link" href="/contact">Contact</a></li>
                    {% if session.get('phone') %}
                    <li class="nav-item"><a class="nav-link" href="/logout">Logout</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        {content}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/')
def home():
    content = '''
    <h1 class="my-4">Homepagina</h1>
    <p>Welkom bij 84Ideas! Log in om verder te gaan.</p>
    '''
    return base_template.replace("{content}", content)

@app.route('/about')
def about():
    content = '''
    <h1 class="my-4">Aboutpagina</h1>
    <p>Dit is de about-pagina. Hier lees je meer over deze applicatie.</p>
    '''
    return base_template.replace("{content}", content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        if phone in users:
            # OTP genereren en opslaan
            otp = random.randint(100000, 999999)
            users[phone]['otp'] = otp
            users[phone]['otp_expires'] = datetime.now() + timedelta(minutes=5)
            print(f"Simulatie: Stuur OTP {otp} naar e-mail {users[phone]['email']}")
            flash("De OTP is verzonden naar je e-mail!", "info")
            return redirect(url_for('verify_otp', phone=phone))
        else:
            flash("Telefoonnummer niet gevonden!", "danger")
    content = '''
    <h1 class="my-4">Inloggen</h1>
    <form method="post" class="mb-4">
        <div class="mb-3">
            <label class="form-label">Telefoonnummer:</label>
            <input type="text" name="phone" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">Vraag OTP aan</button>
    </form>
    '''
    return base_template.replace("{content}", content)

@app.route('/verify-otp/<phone>', methods=['GET', 'POST'])
def verify_otp(phone):
    if request.method == 'POST':
        otp = request.form.get('otp')
        if phone in users:
            user = users[phone]
            if user['otp'] == int(otp) and datetime.now() < user['otp_expires']:
                session['phone'] = phone
                flash("Succesvol ingelogd!", "success")
                return redirect(url_for('home'))
            else:
                flash("Ongeldige of verlopen OTP!", "danger")
    content = f'''
    <h1 class="my-4">OTP Verificatie</h1>
    <p>Telefoonnummer: {phone}</p>
    <form method="post" class="mb-4">
        <div class="mb-3">
            <label class="form-label">OTP:</label>
            <input type="text" name="otp" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">Verifieer</button>
    </form>
    '''
    return base_template.replace("{content}", content)

@app.route('/logout')
def logout():
    session.pop('phone', None)
    flash("Je bent uitgelogd!", "info")
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    content = '''
    <h1 class="my-4">Contact</h1>
    <p>Neem contact op met <strong>84Ideas</strong>:</p>
    <ul>
        <li>Adres: Sarphatistraat 141C, 1018 GD Amsterdam</li>
        <li>E-mail: <a href="mailto:info@84ideas.com">info@84ideas.com</a></li>
        <li>Telefoon: +31 (0)20 123 4567</li>
    </ul>
    <form method="post" action="/submit-contact" class="mt-4">
        <div class="mb-3">
            <label class="form-label">Naam:</label>
            <input type="text" name="name" class="form-control" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Bericht:</label>
            <textarea name="message" class="form-control" rows="5" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Verstuur</button>
    </form>
    '''
    return base_template.replace("{content}", content)

if __name__ == "__main__":
    app.run(debug=True)

