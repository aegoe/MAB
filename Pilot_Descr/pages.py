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
        if self.session.config['name'] == 'MAB_Testing':
            letters_and_digits = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(letters_and_digits) for i in range(7))) + str(random.randint(1, 8))
            self.player.completion_code = result_str
            self.participant.vars['completion_code'] = result_str
            self.player.variance = self.participant.vars['variance'] = self.session.config['variance']

            treatments = ['safe_choice', 'safe_no_choice', 'choice', 'no_choice']
            weights_2 = [0.5, 0.5, 0, 0]
            draw_2 = choice(treatments, 1, p=weights_2)
            self.participant.vars['draw_2'] = draw_2[0]
            if draw_2[0] == 'safe_choice':
                self.player.safe = self.participant.vars['safe'] = True
                self.player.choice = self.participant.vars['choice'] = True
            elif draw_2[0] == 'safe_no_choice':
                self.player.safe = self.participant.vars['safe'] = True
                self.player.choice = self.participant.vars['choice'] = False
            elif draw_2[0] == 'choice':
                self.player.safe = self.participant.vars['safe'] = False
                self.player.choice = self.participant.vars['choice'] = True
            else:
                self.player.safe = self.participant.vars['safe'] = False
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
                weights = [1, 0, 0, 0, 0, 0]
                draw = choice(order, 1, p=weights)
                self.participant.vars['draw'] = draw[0]

        elif self.session.config['name'] == 'MAB_MainStudy_Description':
            letters_and_digits = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(letters_and_digits) for i in range(7))) + str(random.randint(1, 8))
            self.player.completion_code = result_str
            self.participant.vars['completion_code'] = result_str
            self.player.variance = self.participant.vars['variance'] = self.session.config['variance']
            self.player.safe = self.participant.vars['safe'] = self.session.config['safe']
            self.player.sampling = self.participant.vars['sampling'] = self.session.config['sampling']

            treatments = ['choice', 'no_choice']
            weights_2 = [0.65, 0.35]
            draw_2 = choice(treatments, 1, p=weights_2)
            self.participant.vars['draw_2'] = draw_2[0]
            if draw_2[0] == 'choice':
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

        elif self.session.config['name'] == 'MAB_MainStudy_FreeSampling':
            letters_and_digits = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(letters_and_digits) for i in range(7))) + str(random.randint(1, 8))
            self.player.completion_code = result_str
            self.participant.vars['completion_code'] = result_str
            self.player.variance = self.participant.vars['variance'] = self.session.config['variance']
            self.player.safe = self.participant.vars['safe'] = self.session.config['safe']
            self.player.safe = self.participant.vars['sampling'] = self.session.config['sampling']
            self.player.sampling_round = self.participant.vars['sampling_round'] = 1
            self.player.points_sampling = self.participant.vars['points_sampling'] = 0
            self.player.end_button = self.participant.vars['end_button'] = False

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
        return {'participation_fee': self.session.config['participation_fee'],
                'conversion_factor': int(self.session.config['real_world_currency_per_point'] * 100),
                'choice': self.participant.vars['choice'],
                'safe': self.participant.vars['safe'],
                'endowment_choice': Constants.endowment_choice,
                'endowment_points': Constants.endowment_points,
                'draw': self.participant.vars['draw'],
                'variance': self.participant.vars['variance'],
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
                'variance': self.participant.vars['variance'],
                }

    def get_form_fields(self):
        if self.participant.vars['choice'] and not self.participant.vars['variance']:
            return ['cq_Pilot_1', 'cq_Pilot_2', 'cq_Pilot_3','cq_MS2_1']
        elif not self.participant.vars['choice'] and not self.participant.vars['variance']:
                return ['cq_Pilot_2', 'cq_Pilot_3_simdesc', 'cq_Pilot_4', 'cq_MS2_1']
        elif self.participant.vars['choice'] and  self.participant.vars['variance']:
            return ['cq_Pilot_1', 'cq_Pilot_2', 'cq_Pilot_5']
        elif not self.participant.vars['choice'] and self.participant.vars['variance']:
            return ['cq_Pilot_1', 'cq_Pilot_2', 'cq_Pilot_4', 'cq_Pilot_5']

    def before_next_page(self):
        if self.participant.vars['choice']:
            if sum([self.player.cq_Pilot_1, self.player.cq_Pilot_2, self.player.cq_Pilot_3, self.player.cq_MS2_1]) < 5:
                self.player.controls = 1
        else:
            if sum([self.player.cq_Pilot_2, self.player.cq_Pilot_3, self.player.cq_Pilot_4, self.player.cq_MS2_1]) < 5:
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


class Priors(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],

               }
    #def before_next_page(self):
     #   self.participant.payoff = 40



########################################################################################################################
# DECISION ## ##########################################################################################################
########################################################################################################################

class SamplingTransition(Page):
    form_model = 'player'
    form_fields = ['end_button',]

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'choice': self.participant.vars['choice'],
                }



class Decision_Sampling(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.player.end_button != True and self.player.round_number <= self.participant.vars['sampling_round']
        elif not self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.player.end_button != True and self.player.round_number <= self.participant.vars['sampling_round']
        else:
            pass

    def get_form_fields(self):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1_samp', 'option_2_samp', 'option_3_samp', 'end_button']

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1_samp', 'option_2_samp', 'option_3_samp', 'option_safe', 'end_button']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1_samp', 'option_2_samp', 'option_3_samp', 'end_button']

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1_samp', 'option_2_samp', 'option_3_samp', 'option_safe', 'end_button']

    def error_message(self, values):
        if self.participant.vars['choice'] and not self.participant.vars['safe'] and self.player.end_button != True:
            if values['option_1_samp'] + values['option_2_samp'] + values['option_3_samp'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1_samp'] + values['option_2_samp'] + values['option_3_samp'] > 1:
                return 'You can only choose one option per round.'

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1_samp'] + values['option_2_samp'] + values['option_3_samp'] + values['option_safe'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1_samp'] + values['option_2_samp'] + values['option_3_samp'] + values['option_safe'] > 1:
                return 'You can only choose one option per round.'

        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] and self.player.end_button != True:
            if values['option_1_samp'] + values['option_2_samp'] + values['option_3_samp'] < 3:
                return 'You have to use all three points'
            elif values['option_1_samp'] + values['option_2_samp'] + values['option_3_samp'] > 3:
                return 'You can only use three points per round'

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1_samp'] + values['option_2_samp'] + values['option_3_samp'] + values['option_safe'] < 3:
                return 'You have to use all three points'
            elif values['option_1_samp'] + values['option_2_samp'] + values['option_3_samp'] + values['option_safe'] > 3:
                return 'You can only use three points per round'

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               'safe': self.participant.vars['safe'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],
               'end_button': self.player.end_button,
               'sampling_round': self.participant.vars['sampling_round'],
               'sampling_rnd_2': self.player.sampling_rnd_2,

               }

    def before_next_page(self):

        self.participant.vars['sampling_round']+=1
        self.participant.vars['points_sampling']+=1

        if self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['3', '4', '5', '6', '7', '8', '9', '10']
            Urn_2 = ['0', '1', '2', '3', '20', '25', '35', '40']
            Urn_3 = ['6']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.25, 0.25, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [1]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1_samp)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2_samp)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3_samp)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str


            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            payoffs = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    payoffs += values

            self.player.payoff = payoffs

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            payoffs_1 = 0
            payoffs_2 = 0
            payoffs_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        payoffs_1 += v
                    if i == 'count_2':
                        payoffs_2 += v
                    if i == 'count_3':
                        payoffs_3 += v

            if self.player.end_button == True:
                self.player.option_3_samp = 1

        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['3', '4', '5', '6', '7', '8', '9', '10']
            Urn_2 = ['0', '1', '2', '3', '20', '25', '35', '40']
            Urn_3 = ['6']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.25, 0.25, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [1]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1_samp)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2_samp)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3_samp)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str

            print(self.player.urn_draws_1)
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
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

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

            if self.player.end_button == True:
                self.player.option_3_samp = 3



class Feedback_Sampling(Page):
    form_model = 'player'
    form_fields = ['end_button',]

    def is_displayed(self):
        if self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.player.end_button != True and self.player.round_number <= self.participant.vars['sampling_round']
        elif not self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.player.end_button != True and self.player.round_number <= self.participant.vars['sampling_round']
        else:
            pass

    def vars_for_template(self):
        return {'payoff': self.player.payoff,
                'payoff_1': self.player.payoff_1,
                'payoff_2': self.player.payoff_2,
                'payoff_3': self.player.payoff_3,
                'choice': self.participant.vars['choice'],
                'urn_draws_1': self.player.urn_draws_1,
                'urn_draws_2': self.player.urn_draws_2,
                'urn_draws_3': self.player.urn_draws_3,
                'urn_draws_4': self.player.urn_draws_4,
                'payoff_4': self.player.payoff_4,
                'safe': self.participant.vars['safe'],
                'draw': self.participant.vars['draw'],
                'feedback_3': self.participant.vars['feedback_3'],
                'sampling': self.participant.vars['sampling'],
                'end_button': self.player.end_button,
                'sampling_round': self.participant.vars['sampling_round'],
                'points_sampling': self.participant.vars['points_sampling'],
                }

    def before_next_page(self):
        self.player.payoff = 0

# class HelpPage(Page):
#     form_model = 'player'
#
#     def is_displayed(self):
#         if self.participant.vars['choice'] and self.participant.vars['sampling']:
#             return self.player.round_number <= self.participant.vars['sampling_round']
#         elif not self.participant.vars['choice'] and self.participant.vars['sampling']:
#             return self.player.round_number <= self.participant.vars['sampling_round']
#         else:
#             pass
#
#     def vars_for_template(self):
#         return{'end_button': self.player.end_button,
#
#         }


class DecisionTransition(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.player.end_button == True and self.player.round_number <= self.participant.vars['sampling_round']
        elif not self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.player.end_button == True and self.player.round_number <= self.participant.vars['sampling_round']
        else:
            pass

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'end_button': self.player.end_button,
               'payoff': self.participant.payoff,
               'sampling_round': self.participant.vars['sampling_round'],
               'points_sampling': self.participant.vars['points_sampling'],
               'round_number': self.player.round_number,
               }

    def before_next_page(self):
        # self.participant.payoff = self.participant.payoff - self.participant.payoff
        self.player.end_button = self.participant.vars['end_button'] = True
        if self.participant.vars['sampling_round'] > 1:
            self.participant.vars['sampling_round'] = self.participant.vars['sampling_round'] - 1
        else:
            pass


class Decision(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars['choice'] and not self.participant.vars['sampling']:
            return self.round_number <= Constants.num_rounds_choice
        elif not self.participant.vars['choice'] and not self.participant.vars['sampling']:
            return self.round_number <= Constants.num_rounds_points
        elif self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.round_number >= self.participant.vars['sampling_round'] and self.round_number <= (self.participant.vars['sampling_round'] + Constants.num_rounds_choice -1)
        elif not self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.round_number >=  self.participant.vars['sampling_round']  and self.round_number <= (self.participant.vars['sampling_round'] + Constants.num_rounds_points -1)

    def get_form_fields(self):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

    def error_message(self, values):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 1:
                return 'You can only choose one option per round.'

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 1:
                return 'You can only choose one option per round.'

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 3:
                return 'You can only use three points per round'

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 3:
                return 'You can only use three points per round'

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               'safe': self.participant.vars['safe'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],
               'payoff': self.participant.payoff,
               'points_sampling': self.participant.vars['points_sampling'],
               'sampling_round': self.participant.vars['sampling_round'],

               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['3', '4', '5', '6', '7', '8', '9', '10']
            Urn_2 = ['0', '1', '2', '3', '20', '25', '35', '40']
            Urn_3 = ['6']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.25, 0.25, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [1]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str


            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            payoffs = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    payoffs += values

            self.player.payoff = payoffs

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            payoffs_1 = 0
            payoffs_2 = 0
            payoffs_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        payoffs_1 += v
                    if i == 'count_2':
                        payoffs_2 += v
                    if i == 'count_3':
                        payoffs_3 += v

            self.player.payoff_1 = payoffs_1
            self.player.payoff_2 = payoffs_2
            self.player.payoff_3 = payoffs_3

            if (self.round_number - self.participant.vars['sampling_round']) % 2 == 0 and self.round_number >2:
                self.player.payoff_1_m2 = self.player.in_round(self.round_number - 2).payoff_1
                self.player.payoff_2_m2 = self.player.in_round(self.round_number - 2).payoff_2
                self.player.payoff_3_m2 = self.player.in_round(self.round_number - 2).payoff_3

                self.player.payoff_1_m1 = self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_m1 = self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_m1 = self.player.in_round(self.round_number - 1).payoff_3

                self.player.payoff_all3 = self.player.payoff + self.player.in_round(self.round_number - 2).payoff + self.player.in_round(self.round_number - 1).payoff

                self.player.payoff_1_all3 = self.player.payoff_1 + self.player.in_round(self.round_number - 2).payoff_1 + self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_all3 = self.player.payoff_2 + self.player.in_round(self.round_number - 2).payoff_2 + self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_all3 = self.player.payoff_3 + self.player.in_round(self.round_number - 2).payoff_3 + self.player.in_round(self.round_number - 1).payoff_3

                self.player.urn_draws_1_m2 = self.player.in_round(self.round_number - 2).urn_draws_1
                self.player.urn_draws_2_m2 = self.player.in_round(self.round_number - 2).urn_draws_2
                self.player.urn_draws_3_m2 = self.player.in_round(self.round_number - 2).urn_draws_3

                self.player.urn_draws_1_m1 = self.player.in_round(self.round_number - 1).urn_draws_1
                self.player.urn_draws_2_m1 = self.player.in_round(self.round_number - 1).urn_draws_2
                self.player.urn_draws_3_m1 = self.player.in_round(self.round_number - 1).urn_draws_3

                self.player.option_1_all3 = self.player.option_1 + self.player.in_round(self.round_number - 2).option_1 + self.player.in_round(self.round_number - 1).option_1
                self.player.option_2_all3 = self.player.option_2 + self.player.in_round(self.round_number - 2).option_2 + self.player.in_round(self.round_number - 1).option_2
                self.player.option_3_all3 = self.player.option_3 + self.player.in_round(self.round_number - 2).option_3 + self.player.in_round(self.round_number - 1).option_3

            else:
                pass

        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['3', '4', '5', '6', '7', '8', '9', '10']
            Urn_2 = ['0', '1', '2', '3', '20', '25', '35', '40']
            Urn_3 = ['6']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.25, 0.25, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [1]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str

            print(self.player.urn_draws_1)
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
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

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



class Feedback(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars['choice'] and not self.participant.vars['sampling']:
            return self.round_number <= Constants.num_rounds_choice
        elif not self.participant.vars['choice'] and not self.participant.vars['sampling']:
            return self.round_number <= Constants.num_rounds_points
        elif self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.round_number >= self.participant.vars['sampling_round'] and self.round_number <= (self.participant.vars['sampling_round'] + Constants.num_rounds_choice -1) and ((self.round_number - self.participant.vars['sampling_round']) % 2 == 0) and ((self.round_number - self.participant.vars['sampling_round']) != 0)
        elif not self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.round_number >=  self.participant.vars['sampling_round']  and self.round_number <= (self.participant.vars['sampling_round'] + Constants.num_rounds_points -1)


    def vars_for_template(self):
        return {'payoff': self.player.payoff,
                'payoff_1': self.player.payoff_1,
                'payoff_2': self.player.payoff_2,
                'payoff_3': self.player.payoff_3,
                'choice': self.participant.vars['choice'],
                'urn_draws_1': self.player.urn_draws_1,
                'urn_draws_2': self.player.urn_draws_2,
                'urn_draws_3': self.player.urn_draws_3,
                'urn_draws_4': self.player.urn_draws_4,
                'payoff_4': self.player.payoff_4,
                'safe': self.participant.vars['safe'],
                'draw': self.participant.vars['draw'],
                'feedback_3': self.participant.vars['feedback_3'],
                }





########################################################################################################################
# Questionnaire and Final Page #########################################################################################
########################################################################################################################


class Questionnaire(Page):
    form_model ='player'

    def get_form_fields(self):
        if self.player.questionnaire_page == 1:
            return []
        elif self.player.questionnaire_page == 2:
            return ['q_risk']
        elif self.player.questionnaire_page == 3:
            return ['q_exploration_strategy']
        elif self.player.questionnaire_page == 4 and self.participant.vars['choice']:
            return ['q_mean_sequential', 'q_sd_sequential', 'q_ld_sequential', 'q_hd_sequential', 'q_descr_exp']
        elif self.player.questionnaire_page == 4 and not self.participant.vars['choice']:
            return ['q_mean_simultan', 'q_sd_simultan', 'q_ld_simultan', 'q_hd_simultan', 'q_descr_exp']
        elif self.player.questionnaire_page == 5:
            epo = [f'q_epo_{i}' for i in range(1, 14)]
            return epo
        elif self.player.questionnaire_page == 6:
            return ['q_year', 'q_sex', 'q_employment', 'q_education',
                    'q_ethnicity']


    def is_displayed(self):
        if self.participant.vars['choice']:
            return self.round_number == (self.participant.vars['sampling_round'] + Constants.num_rounds_choice -1)
        else:
            return self.round_number == (self.participant.vars['sampling_round'])

    def vars_for_template(self):
        return{'questionnaire_page': self.player.questionnaire_page,
               'choice':self.participant.vars['choice'],
               'safe': self.participant.vars['safe'],
               'variance': self.participant.vars['variance'],
               'round': self.player.round_number,

               }

    def before_next_page(self):
        self.player.questionnaire_page += 1

        if self.player.questionnaire_page == 6:
            self.player.smplrnd = self.participant.vars['sampling_round']
            if self.participant.vars['choice']:
                if self.participant.vars['points_sampling'] == 0:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session)
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee()

                elif self.participant.vars['points_sampling'] > 0 and self.participant.vars['points_sampling'] <= 15:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.02
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.02

                elif self.participant.vars['points_sampling'] > 15 and self.participant.vars['points_sampling'] <= 30:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.04
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.04

                elif self.participant.vars['points_sampling'] > 30 and self.participant.vars['points_sampling'] <= 45:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.06
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.06

                elif self.participant.vars['points_sampling'] > 45 and self.participant.vars['points_sampling'] <= 60:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.06
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.06

                elif self.participant.vars['points_sampling'] > 60 and self.participant.vars['points_sampling'] <= 75:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.08
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.08

                elif self.participant.vars['points_sampling'] > 75 and self.participant.vars['points_sampling'] <= 90:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.1
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.1

                elif self.participant.vars['points_sampling'] > 90 and self.participant.vars['points_sampling'] <= 105:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.12
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.12

                elif self.participant.vars['points_sampling'] > 105:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.14
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.14

            elif not self.participant.vars['choice']:
                if self.participant.vars['points_sampling'] == 0:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session)
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee()

                elif self.participant.vars['points_sampling'] > 0 and self.participant.vars['points_sampling'] <= 5:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.02
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.02

                elif self.participant.vars['points_sampling'] > 5 and self.participant.vars['points_sampling'] <= 10:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.04
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.04

                elif self.participant.vars['points_sampling'] > 10 and self.participant.vars['points_sampling'] <= 15:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.06
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.06

                elif self.participant.vars['points_sampling'] > 15 and self.participant.vars['points_sampling'] <= 20:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.06
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.06

                elif self.participant.vars['points_sampling'] > 20 and self.participant.vars['points_sampling'] <= 25:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.08
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.08

                elif self.participant.vars['points_sampling'] > 25 and self.participant.vars['points_sampling'] <= 30:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.1
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.1

                elif self.participant.vars['points_sampling'] > 30 and self.participant.vars['points_sampling'] <= 35:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.12
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.12

                elif self.participant.vars['points_sampling'] > 35:
                    self.participant.vars['bonus'] = self.participant.payoff.to_real_world_currency(self.session) - 0.14
                    self.participant.vars['total_payoff'] = self.participant.payoff_plus_participation_fee() - 0.14



class FinalInfo(Page):
    def is_displayed(self):
        if self.participant.vars['choice']:
            return self.round_number == (self.participant.vars['sampling_round'] + Constants.num_rounds_choice - 1)
        else:
            return self.round_number == (self.participant.vars['sampling_round'])

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee'],
                'total_payoff': self.participant.vars['total_payoff'],
                'bonus': self.participant.vars['bonus'],
                'completion_code': self.participant.vars['completion_code'],
                }



page_sequence = [
    Device,
    AttentionCheck,
    DeadEnd,
    InstruStart,
    InstruStart,
    InstruStart,
    InstruStart,
    InstruStart,
    InstruStart,
    InstruStart,
    ComprehensionQuestions,
    ComprehensionQuestions,
    DeadEnd2,
    PriorsTransition,
    Priors,
    SamplingTransition,
    Decision_Sampling,
    Feedback_Sampling,
    #HelpPage,
    DecisionTransition,
    Decision,
    Feedback,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    FinalInfo,
]
