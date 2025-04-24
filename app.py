from flask import Flask, render_template, request, redirect
import requests
import re

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def obtener_seller_id(url_producto):
    try:
        response = requests.get(url_producto, headers=headers)
        seller_id_match = re.search(r'"seller_id":(\d+)', response.text)
        return seller_id_match.group(1) if seller_id_match else None
    except:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        seller_id = obtener_seller_id(url)
        if seller_id:
            return redirect(f'https://listado.mercadolibre.com.mx/_CustId_{seller_id}')
        else:
            return render_template('index.html', error='No se pudo obtener el vendedor.')
    return render_template('index.html')

# No se necesita app.run() para gunicorn
