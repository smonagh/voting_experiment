from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import time
from ast import literal_eval


class Voting_stage1(Page):

    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list and self.subsession.round_number<19:

            return self.player

    def vars_for_template(self):
        return {'player_id': self.player.in_round(self.round_number).id_in_round,
                'vote_1': self.group.in_round(self.round_number).fill_table_1,
                'vote_2': self.group.in_round(self.round_number).fill_table_2,
                'vote_3': self.group.in_round(self.round_number).fill_table_3,
                'total_vote_display': self.group.total_vote_in_group,
                'votes_to_win': self.group.vote_to_win,
                'vote_weight': self.player.vote_weight,
                'x_payout': self.group.x_payout,
                'y_payout': self.group.y_payout}

class Voting_stage2(Voting_stage1):
    pass


class Voting_stage3(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list and self.subsession.round_number < 19:
            return self

    def vars_for_template(self):
        print('*************: ',self.group.equal_round)
        return {'player_id': self.player.in_round(self.round_number).id_in_round,
                'vote_1': self.group.in_round(self.round_number).fill_table_1,
                'vote_2': self.group.in_round(self.round_number).fill_table_2,
                'vote_3': self.group.in_round(self.round_number).fill_table_3,
                'total_vote_display': self.group.total_vote_in_group,
                'votes_to_win': self.group.vote_to_win,
                'vote_weight': self.player.vote_weight,
                'x_payout': self.group.x_payout,
                'y_payout': self.group.y_payout,
                'equal_round': self.group.equal_round}

    form_model = models.Player
    form_fields = ['vote']

class Voting_stage3_2(Page):

    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if (self.subsession.round_number == 18) and\
                self.player.id_in_group not in player_id_list and self.subsession.round_number<19:
            return self

    form_model = models.Player
    form_fields = ['belief_average']

    def vars_for_template(self):
        return {'player_id': self.player.in_round(self.round_number).id_in_round,
                'vote_1': self.group.in_round(self.round_number).fill_table_1,
                'vote_2': self.group.in_round(self.round_number).fill_table_2,
                'vote_3': self.group.in_round(self.round_number).fill_table_3,
                'total_vote_display': self.group.total_vote_in_group,
                'votes_to_win': self.group.vote_to_win,
                'vote_weight': self.player.vote_weight,
                'x_payout': self.group.x_payout,
                'y_payout': self.group.y_payout}


class Decision_stage1(Page):

    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group in player_id_list and self.subsession.round_number<19:
            return self.player

    def vars_for_template(self):
        return {'message_space': self.group.message_space, 'total_vote_x':self.group.total_vote_x,
                'total_vote_y':self.group.total_vote_y}

    form_model = models.Player
    form_fields = ['final_decision']


class Game_Wait_1(WaitPage):

    def after_all_players_arrive(self):
        self.group.total_vote_count(self.subsession.round_order)
        self.group.is_moral_cost()

class Game_Wait_2(WaitPage):

    def after_all_players_arrive(self):
        self.group.get_player_by_id(4).decision_for_group()
        self.group.set_payoffs()
        if self.round_number == 18:
            self.group.set_add_payoffs()



class Game_Wait_4(WaitPage):

        def is_displayed(self):
            if self.subsession.round_number == 18:
                return self

        def after_all_players_arrive(self):
            self.group.followed()


class MyPage(Page):
    def is_displayed(self):
        if self.subsession.round_number == 19:
            return self.player
    form_model = models.Player
    form_fields = ['age','field','gender']

class Game_Wait_3(WaitPage):
    def is_displayed(self):
        if self.subsession.round_number == 19:
            return self

    def after_all_players_arrive(self):
            self.group.final_payout_return()


class Results(Page):

    def is_displayed(self):
        if self.subsession.round_number == 19:
            return self.player

    def vars_for_template(self):
        rowlist = []
        player_payoffs =[]
        for i,j in enumerate(self.player.in_all_rounds()):
            if j.payoff_rounds == True:
                player_payoffs.append(i+1)

        for i in range (1,19):
            rowlist.append([i, self.player.in_round(i).vote ,self.group.in_round(i).group_suggestion,
                           self.group.in_round(i).g_final_decision,self.player.in_round(i).payout])
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
            x+=1
        return {'final_payout': self.player.final_payout,
                'us_conversion': self.player.final_us_payout,
                'belief_payout':self.player.in_round(18).belief_payout,
                'row_list': rowlist,
                'payoff_rounds':player_payoffs
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
