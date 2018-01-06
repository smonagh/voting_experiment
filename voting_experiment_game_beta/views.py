from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import time



class Voting_stage1(Page):

    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list and self.subsession.round_number<7:
            self.player.start_time = time.clock()
            return self.player

    def before_next_page(self):
        self.player.elapsed_time = time.clock() - self.player.start_time

    def vars_for_template(self):
        return {'player_id': self.player.in_round(self.round_number).id_in_round,
                'vote_1': self.group.in_round(self.round_number).fill_table_1,
                'vote_2': self.group.in_round(self.round_number).fill_table_2,
                'vote_3': self.group.in_round(self.round_number).fill_table_3,
                'total_vote_display': self.group.total_vote_in_group, 'votes_to_win': self.group.vote_to_win,
                'vote_weight': self.player.vote_weight, 'treatment': self.participant.vars.get('treatment'),
                'x_payout': self.group.x_payout,
                'y_payout': self.group.y_payout}

class Voting_stage2(Voting_stage1):
    pass


class Voting_stage3(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list and self.subsession.round_number < 7:
            self.player.start_time = time.clock()
            return self

    def before_next_page(self):
        self.player.elapsed_time = time.clock() - self.player.start_time

    def vars_for_template(self):
        return {'player_id': self.player.in_round(self.round_number).id_in_round,
                'vote_1': self.group.in_round(self.round_number).fill_table_1,
                'vote_2': self.group.in_round(self.round_number).fill_table_2,
                'vote_3': self.group.in_round(self.round_number).fill_table_3,
                'total_vote_display': self.group.total_vote_in_group, 'votes_to_win': self.group.vote_to_win,
                'vote_weight': self.player.vote_weight, 'treatment': self.participant.vars.get('treatment'),
                'x_payout': self.group.x_payout,
                'y_payout': self.group.y_payout}

    form_model = models.Player
    form_fields = ['vote']

class Voting_stage3_2(Page):

    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if (self.subsession.round_number == 6) and\
                self.player.id_in_group not in player_id_list and self.subsession.round_number<7:
            return self

    form_model = models.Player
    form_fields = ['belief_average']

    def vars_for_template(self):
        return {'player_id': self.player.in_round(self.round_number).id_in_round,
                'vote_1': self.group.in_round(self.round_number).fill_table_1,
                'vote_2': self.group.in_round(self.round_number).fill_table_2,
                'vote_3': self.group.in_round(self.round_number).fill_table_3,
                'total_vote_display': self.group.total_vote_in_group, 'votes_to_win': self.group.vote_to_win,
                'vote_weight': self.player.vote_weight, 'treatment': self.participant.vars.get('treatment'),
                'x_payout': self.group.x_payout,
                'y_payout': self.group.y_payout}

class Voting_stage4(Page):
    def is_displayed(self):
        if self.subsession.round_number == 3:
            return self

class Decision_stage1(Page):

    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group in player_id_list and self.subsession.round_number<7:
            self.player.start_time = time.clock()
            return self.player

    def before_next_page(self):
        self.player.elapsed_time = time.clock() - self.player.start_time
    def vars_for_template(self):
        return {'message_space': self.group.message_space, 'total_vote_x':self.group.total_vote_x,
                'total_vote_y':self.group.total_vote_y}

    form_model = models.Player
    form_fields = ['final_decision']


class Game_Wait_1(WaitPage):
    def after_all_players_arrive(self):
        models.Group.total_vote_count(self.group)
        models.Group.make_suggestion(self.group)
        models.Group.is_moral_cost(self.group)
        models.Group.is_group_moral_cost(self.group)
        models.Group.get_treatment(self.group)

class Game_Wait_2(WaitPage):
    def after_all_players_arrive(self):
        models.Group.set_payoffs(self.group)
        models.Player.decision_for_group(self.group.get_player_by_id(4))


class Game_Wait_4(WaitPage):

        def is_displayed(self):
            if self.subsession.round_number == 6:
                return self

        def after_all_players_arrive(self):
            models.Player.followed(self.group)


class MyPage(Page):
    def is_displayed(self):
        if self.subsession.round_number == 7:
            return self.player
    form_model = models.Player
    form_fields = ['age','field','gender']

class Game_Wait_3(WaitPage):
    def is_displayed(self):
        if self.subsession.round_number == 7:
            return self

    def after_all_players_arrive(self):
            models.Group.final_payout_return(self.group)


class Results(Page):

    def is_displayed(self):
        if self.subsession.round_number == 7:
            return self.player

    def vars_for_template(self):
        rowlist = []

        for i in range (1,7):
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
        return {'final_payout': self.player.in_round(7).final_payout, 'us_conversion': self.player.final_us_payout,
                'belief_payout':self.player.in_round(7).belief_payout,
                'row11': rowlist[0][0], 'row12': rowlist[0][1], 'row13': rowlist[0][2], 'row14': rowlist[0][3],
                'row15': rowlist[0][4],
                'row21': rowlist[1][0], 'row22': rowlist[1][1], 'row23': rowlist[1][2], 'row24': rowlist[1][3],
                'row25': rowlist[1][4],
                'row31': rowlist[2][0], 'row32': rowlist[2][1], 'row33': rowlist[2][2], 'row34': rowlist[2][3],
                'row35': rowlist[2][4],
                'row41': rowlist[3][0], 'row42': rowlist[3][1], 'row43': rowlist[3][2], 'row44': rowlist[3][3],
                'row45': rowlist[3][4],
                'row51': rowlist[4][0], 'row52': rowlist[4][1], 'row53': rowlist[4][2], 'row54': rowlist[4][3],
                'row55': rowlist[4][4],
                'row61': rowlist[5][0], 'row62': rowlist[5][1], 'row63': rowlist[5][2], 'row64': rowlist[5][3],
                'row65': rowlist[5][4]}



page_sequence = [
    Voting_stage3,
    Game_Wait_1,
    Decision_stage1,
    Game_Wait_4,
    Voting_stage3_2,
    Voting_stage4,
    Game_Wait_2,
    MyPage,
    Game_Wait_3,
    Results
]
