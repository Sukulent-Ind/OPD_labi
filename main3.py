from flask import Flask, render_template, request
import math as mt

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("a.html")

@app.route('/', methods=['post', 'get'])
def form():
    if request.method == 'POST':
        sin_, cos_, tg_, ctg_ = 0, 0, "Не вычисляется", "Не вычисляется"
        val, pers = float(request.form.get('val')), int(request.form.get('pers'))

        if request.form['units'] == "degree":
            val = val * mt.pi / 180

        sin_ = round(mt.sin(val), pers)
        cos_ = round(mt.cos(val), pers)

        if cos_:
            tg_ = round(sin_ / cos_, pers)

        if sin_:
            ctg_ = round(cos_ / sin_, pers)

        return render_template('a.html', ans_sin=sin_, ans_cos=cos_, ans_tg=tg_, ans_ctg=ctg_)

    return render_template('a.html')


if __name__ == '__main__':
    app.run()