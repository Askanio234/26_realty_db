from flask import Flask, render_template, request, redirect, url_for, session
from db_schema import db, Residences


app = Flask(__name__)

app.secret_key = "verysecretkeyexample"

PER_PAGE = 15


@app.route('/')
@app.route('/<int:page>')
def ads_list(page=1):
    query = Residences.query.filter(
                                Residences.is_active == True
                                ).paginate(page, PER_PAGE)
    return render_template('ads_list.html', ads=query)


@app.route('/search', methods=['POST'])
def search():
    session['region'] = request.form['oblast_district']
    session['min_price'] = request.form.get('min_price',
                                            None, type=int)
    session['max_price'] = request.form.get('max_price',
                                            None, type=int)
    session['is_new'] = request.form.get('new_building',
                                            False, type=bool)
    return redirect(url_for('filter_list'))


@app.route('/results/')
@app.route('/results/<int:page>')
def filter_list(page=1):
    queries = [Residences.settlement == session['region']]
    if session['min_price']:
        queries.append(Residences.price >= session['min_price'])
    if session['max_price']:
        queries.append(Residences.price <= session['max_price'])
    if session['is_new']:
        queries.append(Residences.is_new == True)
    filtered_list = Residences.query.filter(*queries).paginate(page,
                                                    PER_PAGE, False)

    return render_template('ads_list.html', ads=filtered_list)


if __name__ == "__main__":
    app.run()
