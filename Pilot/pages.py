from otree.api import (
    Currency as c, currency_range, BasePlayer
)

from _builtin import Page, WaitPage
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
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['access_device']


########################################################################################################################
# AttentionCheck ##########################################################################################################
########################################################################################################################


class AttentionCheck(Page):
    def is_displayed(self):
        return self.player.access_device != 0 and self.round_number == 1

    form_model = 'player'
    form_fields = ['attention_check_1', 'attention_check_2']




########################################################################################################################
# DeadEnd ##############################################################################################################
########################################################################################################################

class DeadEnd(Page):

    # this page is only displayed to people with mobile devices
    # which we do not want to partake and that are "trapped" on this page due to the missing {% next_button %}
    def is_displayed(self):
        return self.player.access_device == 0 or self.player.attention_check_1 == 0 or self.player.attention_check_2 != "chair" and self.round_number == 1


########################################################################################################################
# InstruStart ##########################################################################################################
########################################################################################################################


class InstruStart(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee']}

    def before_next_page(self):
        self.player.choice = self.participant.vars['choice'] = self.session.config['choice']


class Decision(Page):
    form_model = 'player'
    form_fields = ['option_1', 'option_2', 'option_3']

    def error_message(self, values):
        if self.participant.vars['choice']:
            pass
        else:
            if values['option_1'] + values['option_2'] + values['option_3'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 3:
                return 'You can only use three points per round'

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               #'option_1': self.participant.vars['option_1'],
               #'option_2': self.participant.vars['option_2'],
               #'option_3': self.participant.vars['option_3'],
               #'endowment': self.participant.vars['endowment'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               # 'Urn_1': Constants.Urn_1,
               # 'Urn_2': Constants.Urn_2,
               # 'Urn_3': Constants.Urn_3,

               }

    def before_next_page(self):
        if self.participant.vars['choice']:
            pass
        else:

            Urn_1 = ['Black', 'Yellow', 'Blue', 'Green']
            Urn_2 = ['Black', 'Yellow', 'Blue', 'Green']
            Urn_3 = ['White', 'Yellow', 'Black', 'Green']

            weights_1 = [1, 5, 3, 1]
            weights_2 = [1, 3, 5, 1]
            weights_3 = [1, 5, 3, 1]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3

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

        print('Your total payoff for this round is: ', self.player.payoff)
        print('Your payoff from Option 1 using', self.player.option_1, 'draws is: ', self.player.payoff_1)
        print('Your payoff from Option 2 using', self.player.option_2, 'draws is: ', self.player.payoff_2)
        print('Your payoff from Option 3 using', self.player.option_3, 'draws is: ', self.player.payoff_3)



class Feedback(Page):
    form_model = 'player'
    #form_fields = ['option_1', 'option_2', 'option_3']

    def vars_for_template(self):
        return {'payoff': self.player.payoff,
                'payoff_1': self.player.payoff_1,
                'payoff_2': self.player.payoff_2,
                'payoff_3': self.player.payoff_3,

                }



class Results(Page):
    def is_displayed(self):
        if self.session.config['choice']:
            return self.round_number == Constants.num_rounds_choice
        else:
            return self.round_number == Constants.num_rounds_points



page_sequence = [
    Device,
    AttentionCheck,
    DeadEnd,
    InstruStart,
    Decision,
    Feedback,
    Results
]
