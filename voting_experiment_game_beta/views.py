from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
from ast import literal_eval


class Voting_stage1(Page):

    def is_displayed(self):
        player_id_list = [x * Constants.players_per_group for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list and self.subsession.round_number < Constants.num_rounds:

            return self.player

    def vars_for_template(self):
        treatment = literal_eval(self.subsession.round_order)[self.round_number]
        treatment_dict = literal_eval(self.subsession.treatment_dict)
        if treatment == 1:
            if self.player.id_in_group:
                vote_display = random.randint(1, 2)
            else:
                vote_display = random.randint(3, 5)
        elif treatment == 2:
            if self.player.id_in_group:
                vote_display = 3
            else:
                vote_display = 1
        else:
            vote_display = random.randint(1, 5)
        return {'player_id': self.player.in_round(self.round_number).id_in_round,
                'votes': treatment_dict['treatment_{}'.format(treatment)]['votes'],
                'vote_display': vote_display,
                'total_vote_display': self.group.total_vote_in_group,
                'votes_to_win': self.group.vote_to_win,
                'vote_weight': self.player.vote_weight,
                'x_payout': self.group.x_payout,
                'y_payout': self.group.y_payout}

class Voting_stage3(Page):
    def is_displayed(self):
        player_id_list = [x * Constants.players_per_group for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list and self.subsession.round_number < Constants.num_rounds:
            return self

    def vars_for_template(self):
        treatment = literal_eval(self.subsession.round_order)[self.round_number - 1]
        treatment_dict = literal_eval(self.subsession.treatment_dict)
        if treatment == 1:
            if self.player.id_in_group:
                vote_display = random.randint(1,2)
            else:
                vote_display = random.randint(3,5)
        elif treatment == 2:
            if self.player.id_in_group:
                vote_display = 3
            else:
                vote_display = 1
        else:
            vote_display = random.randint(1, 5)
        return {'player_id': self.player.in_round(self.round_number).id_in_round,
                'votes': treatment_dict['treatment_{}'.format(treatment)]['votes'],
                'vote_display': vote_display,
                'total_vote_display': self.group.total_vote_in_group,
                'votes_to_win': self.group.vote_to_win,
                'vote_weight': self.player.vote_weight,
                'x_payout': self.group.x_payout,
                'y_payout': self.group.y_payout,
                'conflict_round': self.group.conflict_round}

    form_model = models.Player
    form_fields = ['vote']

class Voting_stage3_2(Page):

    def is_displayed(self):
        if (self.subsession.round_number == 30) and\
                self.player.id_in_group != Constants.players_per_group and self.subsession.round_number < Constants.num_rounds:
            return self

    form_model = models.Player
    form_fields = ['belief_average']
    def vars_for_template(self):
        treatment = literal_eval(self.subsession.round_order)[self.round_number - 1]
        treatment_dict = literal_eval(self.subsession.treatment_dict)
        if treatment == 1:
            if self.player.id_in_group:
                vote_display = random.randint(1, 2)
            else:
                vote_display = random.randint(3, 5)
        elif treatment == 2:

            if self.player.id_in_group:
                vote_display = 3
            else:
                vote_display = 1
        else:
            vote_display = random.randint(1, 5)
        return {'player_id': self.player.in_round(self.round_number).id_in_round,
                'votes': treatment_dict['treatment_{}'.format(treatment)]['votes'],
                'vote_display': vote_display,
                'total_vote_display': self.group.total_vote_in_group,
                'votes_to_win': self.group.vote_to_win,
                'vote_weight': self.player.vote_weight,
                'x_payout': self.group.x_payout,
                'y_payout': self.group.y_payout}


class Decision_stage1(Page):

    def is_displayed(self):
        player_id_list = [x * Constants.players_per_group for x in range(0, 12)]
        if self.player.id_in_group in player_id_list and self.subsession.round_number< Constants.num_rounds:
            return self.player

    def vars_for_template(self):
        return {'message_space': self.group.message_space, 'total_vote_x':self.group.total_vote_x,
                'total_vote_y':self.group.total_vote_y}

    form_model = models.Player
    form_fields = ['final_decision']


class Game_Wait_1(WaitPage):

    def after_all_players_arrive(self):
        if self.subsession.round_number < Constants.num_rounds:
            self.group.total_vote_count()
            self.group.assign_moral_cost()

class Game_Wait_2(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_final_decision()
        self.group.determine_followed()
        self.group.set_payoffs()
        if self.round_number == Constants.num_rounds - 1:
            average = self.subsession.set_followed_average()
            for player in self.group.get_players():
                if player.id_in_group < Constants.players_per_group:
                    self.group.set_add_payoffs(average)


class Game_Wait_4(WaitPage):

        def is_displayed(self):
            if self.subsession.round_number == Constants.num_rounds - 1:
                return self

        def after_all_players_arrive(self):
            pass

class MyPage(Page):
    def is_displayed(self):
        if self.subsession.round_number == Constants.num_rounds:
            return self.player
    form_model = models.Player
    form_fields = ['age', 'field', 'gender']

class Game_Wait_3(WaitPage):
    def is_displayed(self):
        if self.subsession.round_number == Constants.num_rounds:
            return self

    def after_all_players_arrive(self):
            self.subsession.final_payoff_return()
            for player in self.subsession.get_players():
                print(player.final_payout, player.id_in_group, player.in_rounds(30, 30)[0].belief_payout, self.subsession.in_round(30).followed_average)


class Results(Page):

    def is_displayed(self):
        if self.subsession.round_number == Constants.num_rounds:
            return self.player

    def vars_for_template(self):
        rowlist = []
        player_payoffs =[]
        for i, j in enumerate(self.player.in_all_rounds()):
            if j.payoff_rounds:
                player_payoffs.append(i+1)

        for i in range(1, Constants.num_rounds):
            rowlist.append([i, self.player.in_round(i).vote, self.group.in_round(i).group_suggestion,
                           self.group.in_round(i).g_final_decision, self.player.in_round(i).payout])
        x = 0
        y = 0
        for i in rowlist:
            for j in i:
                if type(j) == bool:
                    if not j:
                        rowlist[x][y] = 'Project X'
                    elif j:
                        rowlist[x][y] = 'Project Y'
                y += 1
            y = 0
            x += 1

        return {'final_payout': self.player.final_payout,
                'us_conversion': self.player.final_us_payout,
                'belief_payout': self.player.in_round(Constants.num_rounds - 1).belief_payout,
                'row_list': rowlist,
                'payoff_rounds': player_payoffs
                }


page_sequence = [
    Voting_stage3,
    Game_Wait_1,
    Decision_stage1,
    Game_Wait_4,
    Voting_stage3_2,
    Game_Wait_2,
    MyPage,
    Game_Wait_3,
    Results
]
