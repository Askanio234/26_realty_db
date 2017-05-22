import os
import argparse
import datetime
import json
from db_schema import Residences, db

YEARS_NEW = 2

TODAY = datetime.date.today().year


def load_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    else:
        print("Некорректный путь до файла")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Введите путь до файла")
    args = parser.parse_args()
    return args


def check_is_a_new(item):
    return item["under_construction"] or \
            (TODAY - (item["construction_year"] or 0) <= YEARS_NEW)


def update_or_create_residences(json_data):
    for item in json_data:
        work_id = item["id"]
        residence = Residences.query.filter(
                                    Residences.work_id == work_id
                                                        ).first()
        if residence is not None:
            residence.is_active = True
        else:
            residence_to_add = Residences(
                settlement=item["settlement"],
                is_under_construction=item["under_construction"],
                description=item["description"],
                price=item["price"],
                living_area=item["living_area"],
                premise_area=item["premise_area"],
                has_balcony=item["has_balcony"],
                address=item["address"],
                construction_year=item["construction_year"],
                rooms_number=item["rooms_number"],
                work_id=item["id"],
                is_new=check_is_a_new(item),
                is_active=True
                )
            db.session.add(residence_to_add)
    db.session.commit()


def disable_old_data():
    all_residences = Residences.query.all()
    if all_residences is not None:
        for residence in all_residences:
            residence.is_active = False
        db.session.commit()


if __name__ == '__main__':
    args = get_args()
    json_file = load_data(args.input)
    update_or_create_residences(json_file)
