# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.food_finder import FoodFinder


class ActionShowFoods(Action):

    def name(self) -> Text:
        return "action_show_foods"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        _place = tracker.get_slot("place")
        if not _place:
            dispatcher.utter_message(text="Sorry I didn't get your place")
            return [SlotSet("place", None)]
        _found_place = FoodFinder.find_place_in_db(str(_place))
        if not _found_place:
            dispatcher.utter_message(text="Sorry, I have not idea about the place {}. You may try other places.")
            return [SlotSet("place", None)]
        _category = tracker.get_slot("food_category")
        if not _category:
            dispatcher.utter_message(text="Sorry I didn't get your food_category")
            return [SlotSet("food_category", None)]
        _found_category = FoodFinder.find_food_category_in_db(str(_category))
        if not _found_category:
            dispatcher.utter_message(text="Sorry, I have not idea about the food {}. You may try other foods.")
            return [SlotSet("food_category", None)]
        _rests = FoodFinder.find_restaurants(place=_found_place, food_category=_found_category)
        if not _rests:
            dispatcher.utter_message(text="Sorry, there is no {} food at {}".format(_category, _found_place))
            dispatcher.utter_message(text="You can try other foods or at other places")
            return [SlotSet("food_category", None), SlotSet("place", None)]
        _attachments = {
            "type": "template",
            "payload": {
                "template_type": "generic"
            }
        }
        _elements = [{"title": r["title"], "image_url": r["imageUrl"], "buttons":[]} for r in _rests]
        _attachments["payload"]["elements"] = _elements
        dispatcher.utter_message(text="Here are the foods found for you:")
        for _r in _rests:
            dispatcher.utter_message(text=_r["title"], image=_r["imageUrl"])
        return [SlotSet("food_category", None), SlotSet("place", None)]
