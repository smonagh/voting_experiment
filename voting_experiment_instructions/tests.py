from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):

    def play_round(self):
        #Define Bot play
        plist = [1,2,3]

        if self.player.id_in_group in plist:
            yield(views.Screen_2_A)
            yield (views.Screen_3_A)
            yield (views.Screen_4_A)
            yield (views.Screen_5_A)
            yield (views.Section_6_A)
            yield (views.Comprehenstion_1, {'q_1': 'Project Y', 'q_2': 'E$12', 'q_3': 'Project X'} )
            yield (views.Comprehension_2, {'q_4': 'in one round'})
            yield (views.Comprehension_3, {'q_5': 'Message X: “Project X will earn you more money than Project Y"',
                                           'q_6': 'Message X: “Project X will earn you more money than Project Y"'})
            yield (views.Comprehension_4, {'q_7': 'Message X: “Project X will earn you more money than Project Y"',
                                           'q_8': 'Message Y: “Project Y will earn you more money than Project X”'})
        else:
            yield(views.Screen_2_B)
            yield(views.Screen_3_B)
