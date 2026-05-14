from flask import Flask, render_template, request
import requests as req

app = Flask(__name__, template_folder='templates', static_folder='frontend', static_url_path='')

CALLMEBOT_APIKEY = "VOTRE_APIKEY_ICI"
WHATSAPP_NUMBER  = "2250556600639"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    nom        = request.form.get('nom', '').strip()
    email      = request.form.get('email', '').strip()
    telephone  = request.form.get('telephone', '').strip()
    entreprise = request.form.get('entreprise', '').strip()
    service    = request.form.get('service', '').strip()
    budget     = request.form.get('budget', '').strip()
    message    = request.form.get('message', '').strip()

    # Validation de base
    if not nom or not email or not message:
        return render_template('index.html', message="Erreur : champs obligatoires manquants.")

    # Affichage dans le terminal
    print("=" * 40)
    print(f"  Nom        : {nom}")
    print(f"  Email      : {email}")
    print(f"  Telephone  : {telephone}")
    print(f"  Entreprise : {entreprise}")
    print(f"  Service    : {service}")
    print(f"  Budget     : {budget}")
    print(f"  Message    : {message}")
    print("=" * 40)

    # Envoi WhatsApp via CallMeBot
    texte = (
        f"🌟 NOUVELLE DEMANDE - BUZZ FLOW\n"
        f"👤 Nom : {nom}\n"
        f"📱 Telephone : {telephone}\n"
        f"📧 Email : {email}\n"
        f"🏢 Entreprise : {entreprise or 'Non renseignee'}\n"
        f"🎯 Service : {service}\n"
        f"💰 Budget : {budget}\n"
        f"📝 Projet : {message}"
    )
    try:
        url = (
            f"https://api.callmebot.com/whatsapp.php"
            f"?phone={WHATSAPP_NUMBER}"
            f"&text={req.utils.quote(texte)}"
            f"&apikey={CALLMEBOT_APIKEY}"
        )
        req.get(url, timeout=10)
    except Exception as e:
        print(f"Erreur envoi WhatsApp : {e}")

    # Affichage de la page merci
    return render_template('merci.html')

if __name__ == '__main__':
    app.run(debug=True)
