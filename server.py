from flask import Flask, render_template, request
from db_schema import db, Residences


app = Flask(__name__)

PER_PAGE = 15

@app.route('/<int:page>')
@app.route('/')
def ads_list(page=1):
    query = Residences.query.filter(Residences.is_active == True).paginate(page, PER_PAGE)
    return render_template('ads_list.html', ads=query)


@app.route('/search/')
def filter_list():
    settlement = request.args.get('oblast_district')
    user_min_price = request.args.get('min_price')
    user_max_price = request.args.get('max_price')
    is_new_building = request.args.get('new_building', False)
    queries = [Residences.settlement == settlement]
    if user_min_price:
        queries.append(Residences.price >= int(user_min_price))
    if user_max_price:
        queries.append(Residences.price <= int(user_max_price))
    if is_new_building:
        queries.append(Residences.is_new == True)
    filtered_list = db.query(Residences).filter(*queries).all()

    return render_template('ads_list.html', ads=filtered_list)


if __name__ == "__main__":
    app.run()
