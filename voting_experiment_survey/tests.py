from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (views.MyPage, {'age': 18, 'gender': 'Male', 'field': 'Economics'})
        yield (views.Results)
