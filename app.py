from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # ⬅️ TO gre tukaj

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
