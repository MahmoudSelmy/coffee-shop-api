from .models import Drink
import json

class DrinkAccess:
    @classmethod
    def get_all_drinks(cls):
        drinks = Drink.query.order_by(Drink.id).all()
        return drinks

    @classmethod
    def get_all_drinks_short(cls):
        drinks = cls.get_all_drinks()
        drinks = [drink.short() for drink in drinks]
        return drinks

    @classmethod
    def get_all_drinks_long(cls):
        drinks = cls.get_all_drinks()
        drinks = [drink.long() for drink in drinks]
        return drinks

    @classmethod
    def create_new_drink(cls, data):
        title = data.get('title', None)
        recipe = data.get('recipe', None)
        if title is None or recipe is None:
            raise ValueError(' Invalid data')
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        return drink

    @classmethod
    def get_drink_by_id(cls, drink_id):
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            ValueError('Invalid drink_id')
        return drink

    @classmethod
    def update_drink(cls, drink_id, data):
        drink = cls.get_drink_by_id(drink_id)
        title = data.get('title', None)
        recipe = data.get('recipe', None)
        if title is not None:
            drink.title = title
        if recipe is not None:
            drink.recipe = """{}""".format(recipe)
        drink.update()
        return drink

    @classmethod
    def delete_drink(cls, drink_id):
        drink = cls.get_drink_by_id(drink_id)
        drink.delete()
