import datetime
import requests
from db_schema import Residences, db_session
from sqlalchemy import exc

source_url = "https://devman.org/assets/ads.json"

def convert_to_datetime(year):
    if year:
        return datetime.datetime.strptime(str(year), "%Y")


def update_or_create_residences(json_data):
    for item in json_data:
        work_id = item["id"]
        residence = db_session.query(Residences).filter(
                                    Residences.work_id == work_id
                                                        ).first()
        if residence is not None:
            residence.is_active = True
        else:
            residence_to_add = Residences(
                settlement = item["settlement"],
                is_under_construction = item["under_construction"],
                description = item["description"],
                price = item["price"],
                living_area = item["living_area"],
                premise_area = item["premise_area"],
                has_balcony = item["has_balcony"],
                address = item["address"],
                construction_year = convert_to_datetime(
                                        item["construction_year"]),
                rooms_number = item["rooms_number"],
                work_id = item["id"],
                is_active = True
                )
            db_session.add(residence_to_add)
    db_session.commit()


def disable_old_data():
    all_residences = db_session.query(Residences).all()
    if all_residences is not None:
        for residence in all_residences:
            residence.is_active = False
        db_session.commit()


if __name__ == '__main__':
    disable_old_data()
    json_data = requests.get(source_url).json()
    update_or_create_residences(json_data)