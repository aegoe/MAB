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
    form_fields = []

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'option_1': self.participant.vars['option_1'],
               'option_2': self.participant.vars['option_2'],
               'option_3': self.participant.vars['option_3'],
               'endowment': self.participant.vars['endowment'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,



               }

    def before_next_page(self):
        if self.participant.vars['choice']:
            xyz
        else:
            adsd




class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    Device,
    AttentionCheck,
    DeadEnd,
    InstruStart,
    MyPage,
    ResultsWaitPage,
    Results
]
