from flask import Flask, render_template, request
from db_schema import db_session, Residences

app = Flask(__name__)


@app.route('/')
def ads_list():
    return render_template('ads_list.html', ads=db_session.query(Residences).filter(Residences.is_active == True).all()
    )


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
    filtered_list = db_session.query(Residences).filter(*queries).all()

    return render_template('ads_list.html', ads=filtered_list)


if __name__ == "__main__":
    app.run()
