import os
from flask import Flask, request, render_template_string
app = Flask(__name__)

try:
    import africastalking
    username = os.environ.get("AT_USERNAME", "sandbox")
    api_key = os.environ.get("AT_API_KEY", "")
    if api_key:
        africastalking.initialize(username, api_key)
        sms = africastalking.SMS
    else:
        sms = None
except:
    sms = None

reports = []
sessions = {}

@app.route('/')
def home():
    return '<h2>Siri Sasa LIVE ✅</h2><a href="/report"><button style="padding:20px;background:green;color:white;font-size:20px">BONJEZA HAPA KURIPOTI</button></a><br><br><a href="/admin">Admin</a>'

@app.route('/ussd', methods=['POST'])
def ussd():
    text = request.values.get("text","")
    if text == "":
        return "CON Siri Sasa Muranga\n1. Ripoti Dhuluma\n2. Msaada wa haraka"
    if text == "1":
        return "CON Chagua aina:\n1. Nyumbani\n2. Ardhi\n3. Mifugo"
    if text.startswith("1*"):
        p=text.split("*")
        if len(p)==2:
            return "CON Eneo (Kijiji/Ward):"
        if len(p)==3:
            return "CON Eleza ufupi:"
        if len(p)==4:
            reports.append({"eneo":p[2],"maelezo":p[3]})
            return "END Asante! ID:1001\nImepokelewa."
    if text=="2":
        return "END DHARURA: 1195 GBV, 999 Polisi"
    return "END Asante"

@app.route('/report', methods=['GET','POST'])
def web_report():
    if request.method == 'POST':
        reports.append({"phone":request.form.get('phone'),"aina":request.form.get('aina'),"eneo":request.form.get('eneo'),"maelezo":request.form.get('maelezo')})
        return f"<h2>Asante! Imepokelewa ✅ ID:{len(reports)}</h2><a href='/report'>Ripoti nyingine</a> | <a href='/admin'>Admin</a>"
    return """
    <h2>Siri Sasa - Ripoti Bila Sandbox</h2>
    <form method='POST'>
    Namba ya Simu:<br><input name='phone' required><br><br>
    Aina:<br><select name='aina'><option>Wizi wa mifugo</option><option>Ardhi</option><option>Dhuluma</option></select><br><br>
    Eneo/Ward:<br><input name='eneo' required><br><br>
    Maelezo:<br><textarea name='maelezo' required></textarea><br><br>
    <button style='padding:15px;background:green;color:white'>TUMA RIPOTI</button>
    </form><br><a href='/admin'>Angalia Ripoti - Admin</a>
    """

@app.route('/admin')
def admin():
    html = "<h2>Ripoti Zote: {{reports|length}}</h2>{% for r in reports %}<p>{{r}}</p>{% endfor %}<br><a href='/'>Home</a> | <a href='/report'>Report</a>"
    return render_template_string(html, reports=reports)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
