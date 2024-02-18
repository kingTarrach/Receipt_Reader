from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask.sessions import SecureCookieSessionInterface
from PIL import Image, ImageEnhance
from io import BytesIO
import pytesseract
import re
import os


app = Flask(__name__)
app.secret_key = 'secret_key' #os.urandom(24)  # CHANGE TO os.urandom once done testing



@app.route('/')
def index():
    return render_template('uploadImage.html')

@app.route('/uploadImage.html')
def upload_image():
    return render_template('uploadImage.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        image = Image.open(BytesIO(file.read()))
        enhancer1 = ImageEnhance.Sharpness(image)
        enhancer2 = ImageEnhance.Contrast(image)
        image_edit = enhancer1.enhance(20.0)
        image_edit = enhancer2.enhance(1.5)

        result = pytesseract.image_to_string(image_edit)
        items, subtotal = parse_receipt(result)

        session['items'] = items
        session['subtotal'] = subtotal

        return jsonify({'success': True})  # Indicate success to the frontend
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    

def parse_receipt(text):
    items = []
    subtotal = 0.0
    item_regex = re.compile(r"(.+?)\s+(\(\d+\)\s+)?(\d+\.\d+)\s*(?:x\s*(\d+))?")

    for line in text.split('\n'):
        if "SUBTOTAL" in line:
            subtotal_match = re.search(r"\d+(?:[.,]\d+)?", line)
            if subtotal_match:
                subtotal_str = subtotal_match.group(0).replace(',', '.')
                subtotal = float(subtotal_str)
            break

        match = item_regex.search(line)
        if match:
            item_name = match.group(1)
            item_price = float(match.group(3))
            
            items.append({'itemName': item_name, 'price': item_price})

    return items, subtotal

@app.route('/items')
def show_items():
    items = session.get('items', [])
    subtotal = session.get('subtotal', 0)
    return render_template('itemList.html', items=items, subtotal=subtotal)


if __name__ == '__main__':
    app.run(debug=True)
