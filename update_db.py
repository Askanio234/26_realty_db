import os
import argparse
import datetime
import json
from db_schema import Residences, db

YEARS_NEW = 2

TODAY = datetime.date.today().year


def load_file(filepath):
    if os.path.exists(filepath):
        return open(filepath, "r", encoding="utf-8")

    else:
        print("Некорректный путь до файла")


def load_data(json_file):
    return json.load(json_file)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Введите путь до файла")
    args = parser.parse_args()
    return args


def check_is_a_new_building(item):
    return item["under_construction"] or \
            (TODAY - (item["construction_year"] or 0) <= YEARS_NEW)


def get_inner_corp_id_list(json_data):
    return [item["id"] for item in json_data]


def update_residence_row(model, json_dict):
    for key, value in json_dict.items():
        if hasattr(model, key):
            if key != "id":
                setattr(model, key, value)
                setattr(model, 'active', True)
                model.is_new = check_is_a_new_building(json_dict)


def update_residences(json_data, inner_corp_ids):
    query = Residences.query.filter(
                            Residences.inner_corp_id.in_(inner_corp_ids))
    for residence in query:
        for item in json_data:
            if residence.inner_corp_id == item["id"]:
                update_residence_row(residence, item)
    db.session.commit()


def create_new_residences(json_data, inner_corp_ids):
    inner_corp_id_in_db = [item[0] for item in
                            db.session.query(Residences.inner_corp_id)]
    new_residences_corp_id = list(set(inner_corp_ids) -
                                    set(inner_corp_id_in_db))
    for item in json_data:
        for new_id in new_residences_corp_id:
            if item["id"] == new_id:
                residence_to_add = Residences(
                settlement=item["settlement"],
                is_under_construction=item["under_construction"],
                description=item["description"],
                price=item["price"],
                premise_area=item["premise_area"],
                address=item["address"],
                construction_year=item["construction_year"],
                rooms_number=item["rooms_number"],
                inner_corp_id=item["id"],
                is_new=check_is_a_new_building(item),
                is_active=True
                )
                db.session.add(residence_to_add)
    db.session.commit()


def disable_old_data(inner_corp_ids):
    query = Residences.query.filter(
                Residences.inner_corp_id.notin_(inner_corp_ids)).\
                update({"is_active": False}, synchronize_session=False)

    db.session.commit()


if __name__ == '__main__':
    args = get_args()
    json_file = load_file(args.input)
    json_data = load_data(json_file)
    list_of_inner_ids = get_inner_corp_id_list(json_data)
    update_residences(json_data, list_of_inner_ids)
    create_new_residences(json_data, list_of_inner_ids)
    disable_old_data(list_of_inner_ids)
    json_file.close()
