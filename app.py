from flask import Flask, request, session, redirect, url_for, flash, render_template
import random
from datetime import datetime, timedelta

# Flask-app instellen
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Simuleer een gebruikersdatabase
users = {
    "0612345678": {"email": "jaime@example.com", "otp": None, "otp_expires": None}
}

# Home verwijst naar KPI's
@app.route('/')
def home_redirect():
    return redirect(url_for('kpis'))

@app.route('/dashboard')
def dashboard():
    """Dashboard pagina."""
    return render_template('dashboard.html', title="Dashboard")

@app.route('/kpis')
def kpis():
    """KPI's pagina."""
    return render_template('kpis.html', title="KPI's")

@app.route('/videocall')
def videocall():
    """VideoCall pagina."""
    return render_template('videocall.html', title="VideoCall")

@app.route('/service-user')
def service_user():
    """Service User pagina."""
    return render_template('service_user.html', title="Service User")

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
    return render_template('login.html', title="Login")

@app.route('/verify-otp/<phone>', methods=['GET', 'POST'])
def verify_otp(phone):
    if request.method == 'POST':
        otp = request.form.get('otp')
        if phone in users:
            user = users[phone]
            if user['otp'] == int(otp) and datetime.now() < user['otp_expires']:
                session['phone'] = phone
                flash("Succesvol ingelogd!", "success")
                return redirect(url_for('kpis'))  # Verwijzing naar de KPI-pagina
            else:
                flash("Ongeldige of verlopen OTP!", "danger")
    return render_template('verify_otp.html', title="Verifieer OTP", phone=phone)

@app.route('/logout')
def logout():
    session.pop('phone', None)
    flash("Je bent uitgelogd!", "info")
    return redirect(url_for('login'))  # Verwijzing naar de login-pagina

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact")

if __name__ == "__main__":
    app.run(debug=True)
