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
    name_in_url = 'Pilot_BRET'
    num_rounds = 5
    num_rounds_choice = 5
    num_rounds_points = 5
    players_per_group = None
    endowment_choice = 1
    endowment_points = 3

    a = -7
    b = -6
    c = -4
    d = -3
    e = 1
    f = 4
    g = 9
    h = 11
    i = 12

    # yellow = 0
    # blue = 1
    # green = 2
    # white = -2
    # Urn_1 = [('Black', 1), ('Yellow', 5), ('Blue', 3), ('Green', 1)]
    # Urn_2 = [('Black', 1), ('Yellow', 3), ('Blue', 5), ('Green', 1)]
    # Urn_3 = [('White', 1), ('Yellow', 5), ('Black', 3), ('Green', 1)]
    safe_option = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    choice = models.BooleanField()
    safe = models.BooleanField()
    test_urns = models.BooleanField()
    variance = models.BooleanField()
    endowment = models.IntegerField()
    option_1 = models.IntegerField(initial=0, label="Triangle")
    option_2 = models.IntegerField(initial=0, label="Circle")
    option_3 = models.IntegerField(initial=0, label="Rectangle")
    option_safe = models.IntegerField(initial=0, label = "Hexagon")
    #draws_1 = models.IntegerField()
    #draws_2 = models.IntegerField()
    #draws_3 = models.IntegerField()
    #count_1 = {}
    #count_2 = {}
    #count_3 = {}
    #data_counts = {}
    urn_draws_1 = models.StringField()
    urn_draws_2 = models.StringField()
    urn_draws_3 = models.StringField()
    urn_draws_4 = models.StringField()
    #payoff = models.CurrencyField(initial=None)
    payoff_1 = models.CurrencyField()
    payoff_2 = models.CurrencyField()
    payoff_3 = models.CurrencyField()
    payoff_4 = models.CurrencyField()
    instru_page = models.IntegerField(initial=1)
    questionnaire_page = models.IntegerField(initial=1)
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
            [999, 'Yes, but there is an additional option after 40 rounds'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='In this HIT you repeatedly choose between a number of options. Do you get the same set of options in all rounds of the HIT?',
        initial=0
    )

    cq_Pilot_2 = models.IntegerField(
        choices=[
            [1, 'each point invested, i.e. each draw '],
            [9, 'one randomly chosen round'],
            [99, 'my performance in comparison to other workers'],
            [999, 'the last 20 rounds'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='My total earnings depend on',
        initial=0
    )

    cq_Pilot_3 = models.IntegerField(
        choices=[
            [999, 'have the same average value'],
            [9, 'return a constant value'],
            [99, 'change over the course of the HIT'],
            [1, 'can differ in their average value'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='All options',
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

    #################################
    # Questions #####################
    #################################


    q_risk = models.IntegerField(
        choices=[
            [1, '1'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6'],
            [7, '7'],
            [8, '8'],
            [9, '9'],
            [10, '10']
        ],
        widget=widgets.RadioSelect,
        label="How do you see yourself: are you generally a person who is fully prepared to take risks or do you try to avoid taking risks?",
        blank=False
    )

    q_exploration_strategy =models.LongStringField(blank=False, label="")

    q_firm =models.LongStringField(blank=False, label="")

    q_fadein =models.LongStringField(blank=False, label="")

    q_fadeout =models.LongStringField(blank=False, label="")

    q_saving =models.LongStringField(blank=False, label="")

    q_wealth =models.LongStringField(blank=False, label="")

    q_maxoption = models.IntegerField(
        choices = [
            [1, 'Triangle'],
            [2, 'Circle'],
            [3, 'Rectangle'],
            [4, 'Hexagon'],
        ],
        widget=widgets.RadioSelect,
        label="",
        blank=False
    )

    q_maxoption_2 = models.IntegerField(
        choices = [
            [1, 'Triangle'],
            [2, 'Circle'],
            [3, 'Rectangle'],
        ],
        widget=widgets.RadioSelect,
        label="",
        blank=False
    )


    q_year = models.IntegerField(label="", blank=False, min=1900, max=2019)

    q_sex = models.IntegerField(
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Prefer not to answer'],
        ],
        widget=widgets.RadioSelect,
        label="",
        blank=False
    )

    q_employment = models.IntegerField(
        choices=[
            [1, 'Working (paid employee)'],
            [2, 'Working (self-employed)'],
            [3, 'Not working (temporary layoff from a job)'],
            [4, 'Not working (looking for work)'],
            [5, 'Not working (retired)'],
            [6, 'Not working (disabled)'],
            [7, 'Not working (other)'],
            [8, 'Prefer not to answer']
        ],
        widget=widgets.RadioSelect,
        label="",
        blank=False
    )

    q_education = models.IntegerField(
        choices=[
            [1, 'Less than high school degree'],
            [2, 'High school graduate (high school diploma or equivalent including GED)'],
            [3, 'Some college but no degree'],
            [4, 'Associate degree in college (2-year)'],
            [5, 'Bachelor’s degree in college(4 - year)'],
            [6, 'Master’s degree'],
            [7, 'Doctoral degree'],
            [8, 'Professional degree (JD, MD)'],
        ],
        widget=widgets.RadioSelect,
        label="",
        blank=False
    )

    OPTIONS = (
        ('AA', 'African American'),
        ('AI', 'American Indian'),
        ('AS', 'Asian'),
        ('H', 'Hispanic/Latino'),
        ('W', 'White/Caucasian'),
        ('O', 'Other'),
    )

    q_ethnicity = models.StringField(widget=forms.CheckboxSelectMultiple(choices=OPTIONS), label='', blank=False)


    def option_1_max(self):
        if self.session.config['choice']:
            return Constants.endowment_choice
        else:
            return Constants.endowment_points

    def option_2_max(self):
        if self.session.config['choice']:
            return Constants.endowment_choice
        else:
            return Constants.endowment_points

    def option_3_max(self):
        if self.session.config['choice']:
            return Constants.endowment_choice
        else:
            return Constants.endowment_points

    def option_safe_max(self):
        if self.session.config['choice']:
            return Constants.endowment_choice
        else:
            return Constants.endowment_points



    def sevenitems(label):
        return models.IntegerField(
            choices=[
                [1, '1'],
                [2, '2'],
                [3, '3'],
                [4, '4'],
                [5, '5'],
                [6, '6'],
                [7, '7'],
            ],
            widget=widgets.RadioSelectHorizontal,
            blank=False,
            label=label
        )


    q_imi_1 = sevenitems('I enjoyed doing this task very much.')
    q_imi_2 = sevenitems('This task was fun to do.')
    q_imi_3 = sevenitems('I thought this was a boring task.')
    q_imi_4 = sevenitems('This task did not hold my attention at all.')
    q_imi_5 = sevenitems('I would describe this task as very interesting.')
    q_imi_6 = sevenitems('I thought this task was quite enjoyable.')
    q_imi_7 = sevenitems('While I was doing this task, I was thinking about how much I enjoyed it.')
