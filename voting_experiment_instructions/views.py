from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions_A(Page):

    def is_displayed(self):
        if self.player.id_in_group != Constants.players_per_group:
            return self.player

class Instructions_B(Page):

    def is_displayed(self):
        if self.player.id_in_group == Constants.players_per_group:
            return self.player

    form_model = models.Player
    form_fields = ['decision_field']


class Comprehension_1(Page):
    def is_displayed(self):
        if self.player.id_in_group != Constants.players_per_group:
            return self.player

    form_model = models.Player
    form_fields = ['q_1', 'q_2', 'q_3']

    def error_message(self, values):
        wrong = False
        if values['q_1'] != "Project Y":
            self.player.num_wrong += 1
            wrong = True
        if values['q_2'] != 'E$12':
            self.player.num_wrong += 1
            wrong = True
        if values['q_3'] != "Project X":
            self.player.num_wrong += 1
            wrong = True

        if wrong:
            return 'You have chosen one or more wrong answers. Please read the question again and try to answer once more'


class Comprehension_2(Page):
    def is_displayed(self):
        if self.player.id_in_group != Constants.players_per_group:
            return self.player

    form_model = models.Player
    form_fields = ['q_4', "q_5"]

    def error_message(self, values):
        wrong = False
        if values['q_4'] != 'Message X: "Project X will earn you more money than Project Y"':
            self.player.num_wrong += 1
            wrong = True
        if values['q_5'] != 'Message X: "Project X will earn you more money than Project Y"':
            self.player.num_wrong += 1
            wrong = True

        if wrong :
            return 'You have chosen one or more wrong answers. Please read the question again and try to answer once more'


class Comprehension_3(Page):
    def is_displayed(self):
        if self.player.id_in_group != Constants.players_per_group:
            return self.player

    form_model = models.Player
    form_fields = ['q_6', "q_7"]

    def error_message(self, values):
        wrong = False

        if values['q_6'] != 'Message X: “Project X will earn you more money than Project Y"':
            self.player.num_wrong += 1
            wrong = True

        if values['q_7'] != 'Message Y: “Project Y will earn you more money than Project X"':
            self.player.num_wrong += 1
            wrong = True

        if wrong:
            return """You have chosen one or more wrong answers.
            Please read the question again and try to answer once more"""

class Comprehension_5(Page):

    form_model = models.Player
    form_fields = ['q_9']

    def is_displayed(self):
        if self.player.id_in_group != Constants.players_per_group:
            return self.player

    def error_message(self, values):
        wrong = False

        if values['q_9'] != 'True':
            self.player.num_wrong += 1
            wrong = True

        if wrong:
            return ' You have chosen one or more wrong answers. Please read the question again and try to answer once more.'

class Comprehension_6(Page):

    form_model = models.Player
    form_fields = ['q_8']

    def is_displayed(self):
        if self.player.id_in_group != Constants.players_per_group:
            return self.player

    def error_message(self, values):
        wrong = False

        if values['q_8'] != '''The decision that you make, the decisions that other participants make, and who among the three Type A participants in a given round is randomly selected to earn the money that is associated with the project that the Type B participant chose to implement''':
            self.player.num_wrong += 1
            wrong = True

        if wrong:
            return ' You have chosen one or more wrong answers. Please read the question again and try to answer once more.'

class Post_Instruction_Page(WaitPage):
    def after_all_players_arrive(self):
        pass


page_sequence = [
    Instructions_A,
    Instructions_B,
    Comprehension_1,
    Comprehension_2,
    Comprehension_3,
    Comprehension_5,
    Comprehension_6
    ]

'''
Instructions_A,
    Instructions_B,
    Comprehension_1,
    Comprehension_2,
    Comprehension_3,
    Comprehension_5,
    Comprehension_6
'''
