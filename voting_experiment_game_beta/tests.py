from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        plist = [1, 2, 3,]
        pvote = random.randint(0,1)
        pguess_avg = random.randint(0,100)/10
        decis = random.randint(0,1)
        if self.player.id_in_group in plist and self.subsession.round_number < 19:
            yield (views.Voting_stage3,{'vote':pvote})
            if self.subsession.round_number == 18:
                yield (views.Voting_stage3_2,{'belief_average':pguess_avg})
        elif self.subsession.round_number < 19:
            yield(views.Decision_stage1,{'final_decision':decis})
        if self.subsession.round_number == 19:
            yield (views.MyPage,{'age':24,'gender':'Male','field':'Economics'})
            yield (views.Results)
