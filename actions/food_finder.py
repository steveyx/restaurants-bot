import pandas as pd
import json


def load_json(filename="restaurant_data/unreal_restaurants.json"):
    with open(filename) as data_file:
        data = json.load(data_file)
    return data


class FoodFinder:
    df_places = pd.read_csv("restaurant_data/places.csv")
    places_dict = df_places.set_index('name').to_dict(orient="index")
    restaurants = load_json()
    food_categories = list(set([c.strip().title() for r in restaurants for c in r["category"]]))

    @classmethod
    def find_restaurants(cls, place=None, food_category=None, max_results=10):
        _rests = [r for r in cls.restaurants if " ".join(r["category"]).find(food_category.title()) > -1]
        _rests = [r for r in _rests if place in [p['name'].title() for p in r["places"]]]
        if len(_rests) > max_results:
            return _rests[:max_results]
        return _rests

    @classmethod
    def find_place_in_db(cls, place_text):
        _txt = place_text.strip().title()
        if _txt in cls.places_dict:
            return _txt
        return None

    @classmethod
    def find_food_category_in_db(cls, category_text):
        _txt = category_text.strip().title()
        if _txt in cls.food_categories:
            return _txt
        return None
