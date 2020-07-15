from otree.api import (
    Currency as c, currency_range, BasePlayer
)

from ._builtin import Page, WaitPage
from .models import Constants
import random
from numpy.random import choice
import numpy
import time
# from numpy import random
#from otree_mturk_utils.views import Page, CustomMturkWaitPage
from otree.models_concrete import PageCompletion
from functools import reduce
from collections import Counter


########################################################################################################################
# Device ###############################################################################################################
########################################################################################################################

class Device(Page):
    form_model = 'player'
    form_fields = ['access_device']


########################################################################################################################
# AttentionCheck ##########################################################################################################
########################################################################################################################


class AttentionCheck(Page):
    def is_displayed(self):
        return self.player.access_device != 0

    form_model = 'player'
    form_fields = ['attention_check_1', 'attention_check_2']




########################################################################################################################
# DeadEnd ##############################################################################################################
########################################################################################################################

class DeadEnd(Page):

    # this page is only displayed to people with mobile devices
    # which we do not want to partake and that are "trapped" on this page due to the missing {% next_button %}
    def is_displayed(self):
        return self.player.access_device == 0 or self.player.attention_check_1 == 0 or self.player.attention_check_2 != "chair"


########################################################################################################################
# InstruStart ##########################################################################################################
########################################################################################################################


class InstruStart(Page):

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee']}


class Decision(Page):
    form_model = 'player'
    form_fields = ['option_1', 'option_2', 'option_3']

    def error_message(self, values):
            if self.participant.vars['choice']:
                self.player.options_overall = self.player.in_round(self.round_number).option_1 + self.player.in_round(self.round_number).option_2 + self.player.in_round(self.round_number).option_3
                if self.player.options_overall > Constants.endowment_choice:
                    return 'You can only choose one option one time per round.'
            else:
                self.player.options_overall = self.player.in_round(self.round_number).option_1 + self.player.in_round(self.round_number).option_2 + self.player.in_round(self.round_number).option_3
                if self.player.options_overall > Constants.endowment_points:
                    return 'You can only use ' + Constants.endowment_points + 'points per round.'




    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'option_1': self.participant.vars['option_1'],
               'option_2': self.participant.vars['option_2'],
               'option_3': self.participant.vars['option_3'],
               'endowment': self.participant.vars['endowment'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               'Urn_1': Constants.Urn_1,
               'Urn_2': Constants.Urn_2,
               'Urn_3': Constants.Urn_3,

               }

    def before_next_page(self):
        if self.participant.vars['choice']:
            pass
        else:
            self.player.draws_1 = random.choices(Constants.Urn_1, k = self.player.option_1)
            self.player.draws_2 = random.choices(Constants.Urn_2, k = self.player.option_2)
            self.player.draws_3 = random.choices(Constants.Urn_3, k = self.player.option_3)

            self.player.count_1 = Counter(self.player.draws_1)
            self.player.count_2 = Counter(self.player.draws_2)
            self.player.count_3 = Counter(self.player.draws_3)

            data_counts = {}
            data_counts['count_1'] = self.player.count_1
            data_counts['count_2'] = self.player.count_2
            data_counts['count_3'] = self.player.count_3

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == 'Black':
                        data_counts[i][k] = v * Constants.black
                    elif k == 'Yellow':
                        data_counts[i][k] = v * Constants.yellow
                    elif k == 'Blue':
                        data_counts[i][k] = v * Constants.blue
                    elif k == 'Green':
                        data_counts[i][k] = v * Constants.green
                    elif k == 'White':
                        data_counts[i][k] = v * Constants.white

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v




#class ResultsWaitPage(WaitPage):


#   def after_all_players_arrive(self):
#      pass


class Results(Page):
    pass


page_sequence = [
    Device,
    AttentionCheck,
    DeadEnd,
    InstruStart,
    Decision,
    Results
]
