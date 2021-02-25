from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django import forms

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Pilot_Descr'
    num_rounds = 1
    players_per_group = None
    num_rounds_choice = 3
    num_rounds_points = 1
    num_priors = 100
    endowment_choice = 1
    endowment_points = 3
    safe_option = 6

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    choice = models.BooleanField()
    safe = models.BooleanField()
    feedback_3 = models.BooleanField()
    variance = models.BooleanField()
    endowment = models.IntegerField()
    sampling = models.BooleanField()
    end_button = models.BooleanField(initial=False, widget=widgets.RadioSelect, blank=True)

    instru_page = models.IntegerField(initial=1)
    controls = models.IntegerField(initial=0)
    comprehension_page = models.IntegerField(initial=1)
    completion_code = models.StringField()


    #################################
    # Comprehension Questions #######
    #################################

    cq_Pilot_1 = models.IntegerField(
        choices=[
            [9, 'I am not sure'],
            [1, 'Yes'],
            [99, 'No'],
            [999, 'Yes, but there is an additional option after 2 rounds'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='In this HIT you repeatedly choose between a number of options. Do you get the same set of options in all rounds of the HIT?',
        initial=0
    )

    cq_Pilot_2 = models.IntegerField(
        choices=[
            [1, 'each point invested, i.e. each draw, during the decision stage and possibly accruing sampling costs'],
            [9, 'coins drawn in the sampling stage'],
            [99, 'my performance in comparison to other workers'],
            [999, 'only my final decision'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='My total earnings depend on',
        initial=0
    )

    cq_Pilot_3 = models.IntegerField(
        choices=[
            [999, 'No, I have to choose blindly'],
            [9, 'Yes, I will see exactly how much each option is worth beforehand'],
            [99, 'Yes, I won\'t receive any prior statistics but will be able to sample through the options beforehand'],
            [1, 'Yes, I will see information from 100 prior draws for each option and can further sample through the options beforehand'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='In this HIT you repeatedly choose between a number of options. Will you have any prior information about the value of these options?',
        initial=0
    )

    cq_Pilot_3_simdesc = models.IntegerField(
        choices=[
            [999, 'No, I have to choose blindly'],
            [9, 'Yes, I will see exactly how much each option is worth beforehand'],
            [99, 'Yes, I won\'t receive any prior statistics but will be able to sample through the options beforehand'],
            [1, 'Yes, I will see information from 100 prior draws for each option and can further sample through the options beforehand'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='In this HIT you will decide how to allocate three points between three options. Will you have any prior information about the value of these options?',
        initial=0
    )
        
    cq_Pilot_4 = models.IntegerField(
        choices=[
            [999, 'need to invest all three points into one option'],
            [9, 'can not invest more than two points into one option'],
            [1, 'can choose to invest your three points however you want'],
            [99, 'can save points for later rounds'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='In each round, you',
        initial=0
    )

    cq_Pilot_5 = models.IntegerField(
        choices=[
            [999, 'contain the same coins'],
            [9, 'return a constant value'],
            [99, 'change over the course of the HIT'],
            [1, 'can differ in their composition of coins'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='All options',
        initial=0
    )

    cq_MS2_1 = models.IntegerField(
        choices=[
            [999, 'switch between stages whenever you want'],
            [1, 'sample all three options as long as you want'],
            [99, 'sample only for 15 rounds'],
            [9, 'cannot gather additional information about the options through your own experience'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='In this HIT, you can',
        initial=0
    )

    access_device = models.IntegerField(
        choices=[
            [0, 'Smartphone'],
            [1, 'Laptop'],
            [0, 'Tablet computer'],
            [1, 'Desktop PC'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label="",
    )

    attention_check_1 = models.IntegerField(
        choices=[
            [0, 'Never'],
            [0, 'Less than once a month'],
            [0, '1-3 times a month'],
            [0, 'Once a week'],
            [0, '2-3 times a week'],
            [0, '4-5 times a week'],
            [0, 'More than 5 times a week'],
            [1, 'Other'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label="",
    )

    attention_check_2 = models.StringField(blank=True)

