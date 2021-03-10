from otree.api import (
    Currency as c, currency_range, BasePlayer
)

from _builtin import Page, WaitPage
from .models import Constants
import random
from numpy.random import choice
import numpy
import time
#from numpy import random
#from otree_mturk_utils.views import Page, CustomMturkWaitPage
from functools import reduce
from collections import Counter
import string


########################################################################################################################
# Device ###############################################################################################################
########################################################################################################################

class Device(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['access_device']

    def before_next_page(self):

        if self.session.config['name'] == 'PS1':
            letters_and_digits = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(letters_and_digits) for i in range(7))) + str(random.randint(1, 8))
            self.player.completion_code = result_str
            self.participant.vars['completion_code'] = result_str
            self.player.safe = self.participant.vars['safe'] = self.session.config['safe']
            self.player.sampling = self.participant.vars['sampling'] = self.session.config['sampling']

            treatments = ['choice', 'no_choice']
            weights_3 = [0.5, 0.5]
            draw_3 = choice(treatments, 1, p=weights_3)
            self.participant.vars['draw_2'] = draw_3[0]
            if draw_3[0] == 'choice':
                self.player.feedback_3 = self.participant.vars['feedback_3'] = True
                self.player.choice = self.participant.vars['choice'] = True
            else:
                self.player.feedback_3 = self.participant.vars['feedback_3'] = False
                self.player.choice = self.participant.vars['choice'] = False

            if self.participant.vars['safe']:
                order =['TSRH', 'STRH', 'RTSH', 'TRSH', 'SRTH', 'RSTH', 'HSTR', 'SHTR', 'THSR', 'HTSR', 'STHR', 'TSHR', 'TRHS',
                    'RTHS', 'HTRS', 'THRS', 'RHTS', 'HRTS', 'HRST', 'RHST', 'SHRT', 'HSRT', 'RSHT', 'SRHT']
                weights = [1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24,
                    1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24]
                draw = choice(order, 1, p=weights)
                self.participant.vars['draw'] = draw[0]

            else:
                order = ['TSR', 'STR', 'RTS', 'TRS', 'SRT', 'RST']
                weights = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]
                draw = choice(order, 1, p=weights)
                self.participant.vars['draw'] = draw[0]






########################################################################################################################
# AttentionCheck #######################################################################################################
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
        return {'participation_fee': self.session.config['participation_fee'],
                'conversion_factor': int(self.session.config['real_world_currency_per_point'] * 100),
                'choice': self.participant.vars['choice'],
                'safe': self.participant.vars['safe'],
                'endowment_choice': Constants.endowment_choice,
                'endowment_points': Constants.endowment_points,
                'draw': self.participant.vars['draw'],
                'feedback_3': self.participant.vars['feedback_3'],

                }

    def before_next_page(self):
        self.player.instru_page += 1


########################################################################################################################
# ComprehensionQuestions ###############################################################################################
########################################################################################################################

class ComprehensionQuestions(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1 and self.player.controls != 1

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee'],
                'conversion_factor': int(self.session.config['real_world_currency_per_point'] * 1000),
                'choice': self.participant.vars['choice'],
                'safe': self.participant.vars['safe'],
                'endowment_choice': Constants.endowment_choice,
                'endowment_points': Constants.endowment_points,
                }

    def get_form_fields(self):
        if self.participant.vars['choice'] :
            return ['cq_PS1', 'cq_PS2', 'cq_PS3','cq_PS5']
        elif not self.participant.vars['choice'] :
                return ['cq_PS1', 'cq_PS2', 'cq_PS3','cq_PS5']

    def before_next_page(self):
        if self.participant.vars['choice']:
            if sum([self.player.cq_PS1, self.player.cq_PS2, self.player.cq_PS3, self.player.cq_PS5]) < 5:
                self.player.controls = 1
        else:
            if sum([self.player.cq_PS1, self.player.cq_PS2, self.player.cq_PS3, self.player.cq_PS5]) < 5:
                self.player.controls = 1

        self.player.comprehension_page += 1


class DeadEnd2(Page):
    def is_displayed(self) -> bool:
        return self.player.in_round(1).controls !=1 and self.round_number == 1



########################################################################################################################
# PRIORS ###############################################################################################################
########################################################################################################################
class PriorsTransition(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               }


# class Priors(Page):
#     form_model = 'player'
#
#     def is_displayed(self):
#         return self.round_number == 1
#
#     def vars_for_template(self):
#         return{'choice': self.participant.vars['choice'],
#                'draw': self.participant.vars['draw'],
#                'sampling': self.participant.vars['sampling'],
#
#                }
    #def before_next_page(self):
     #   self.participant.payoff = 40


page_sequence = [
    Device,
    AttentionCheck,
    DeadEnd,
    InstruStart,
    InstruStart,
    InstruStart,
    InstruStart,
    InstruStart,
    ComprehensionQuestions,
    ComprehensionQuestions,
    DeadEnd2,
    PriorsTransition,
    #Priors,
]
