from .models import Drink, db


class DrinkAccess:
    @classmethod
    def get_all_drinks(cls):
        drinks = Drink.query.order_by(Drink.id).all()
        return drinks
