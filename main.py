from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def home():
    return 'Siri Sasa LIVE'

@app.route('/ussd', methods=['POST'])
def ussd():
    text = request.values.get("text","")
    if text == "":
        return "CON Siri Sasa Muranga\n1. Ripoti Dhuluma\n2. Dharura\n3. Fuata Ripoti\n4. Msaada\n"
    if text == "1":
        return "CON Chagua aina:\n1. Nyumbani\n2. Mtoto\n3. Kazini\n4. Kijinsia\n5. Nyingine"
    if text.startswith("1*"):
        p=text.split("*")
        if len(p)==2:
            return "CON Eneo (Kijiji/Ward):"
        if len(p)==3:
            return "CON Eleza ufupi:"
        if len(p)==4:
            return "END Asante! ID:1001\nImepokelewa. Piga 1195 dharura."
    if text=="2":
        return "END DHARURA: 1195 GBV, 999 Polisi"
    if text=="3":
        return "END Ripoti IN REVIEW"
    if text=="4":
        return "END MSAADA: 1195, 116, 999"
    return "END Asante"
