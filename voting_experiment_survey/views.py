from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    form_model = models.Player
    form_fields = ['age','field','gender']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    def vars_for_template(self):
        return {'final_payoff': self.player.participant.vars.get('final_payoff')}


page_sequence = [
    MyPage,
    Results
]
