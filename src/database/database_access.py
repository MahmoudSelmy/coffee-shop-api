from .models import Drink, db


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
        try:
            title = data['title']
            recipe = """{}""".format(data['recipe'])
        except KeyError:
            raise ValueError(' Invalid data')
        drink = Drink(title=title, recipe=recipe)
        drink.insert()
        return drink
