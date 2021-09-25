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
    name_in_url = 'MS_3'
    num_rounds = 100
    num_rounds_choice = 3
    num_rounds_points = 1
    #num_rounds_choice_sampling = 6
    #num_rounds_points_sampling = 2
    players_per_group = None
    endowment_choice = 1
    endowment_points = 3
    num_priors = 20
    choice_image = {'Option Resch' : 'https://i.imgur.com/kr0xYz1.png', 'Option Schin' : 'https://i.imgur.com/6kqKG77.png', 'Option Taw': 'https://i.imgur.com/1BZVMwB.png'}
    choice_image_str = {'Option Schin' : 'https://i.imgur.com/6kqKG77.png', 'Option Resch' : 'https://i.imgur.com/kr0xYz1.png', 'Option Taw': 'https://i.imgur.com/1BZVMwB.png'}
    choice_image_rts = {'Option Taw': 'https://i.imgur.com/1BZVMwB.png', 'Option Resch' : 'https://i.imgur.com/kr0xYz1.png', 'Option Schin' : 'https://i.imgur.com/6kqKG77.png'}
    choice_image_trs = {'Option Resch' : 'https://i.imgur.com/kr0xYz1.png', 'Option Taw': 'https://i.imgur.com/1BZVMwB.png', 'Option Schin' : 'https://i.imgur.com/6kqKG77.png'}
    choice_image_srt = {'Option Schin' : 'https://i.imgur.com/6kqKG77.png', 'Option Taw': 'https://i.imgur.com/1BZVMwB.png', 'Option Resch' : 'https://i.imgur.com/kr0xYz1.png'}
    choice_image_rst = {'Option Taw': 'https://i.imgur.com/1BZVMwB.png', 'Option Schin' : 'https://i.imgur.com/6kqKG77.png', 'Option Resch' : 'https://i.imgur.com/kr0xYz1.png'}


    #choices = ['Option Resch', 'Option Schin', 'Option Taw']
    #choices2 = ['Option Resch', 'Option Schin', 'Option Taw']
    #choices3 = ['Option Resch', 'Option Schin', 'Option Taw']
    #choices4 = ['Option Resch', 'Option Schin', 'Option Taw']

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
    incentive = models.BooleanField()
    sampling = models.BooleanField()
    option_1_samp = models.IntegerField(initial=0, label="Option Resch", blank=True)
    option_2_samp = models.IntegerField(initial=0, label="Option Schin", blank=True)
    option_3_samp = models.IntegerField(initial=0, label="Option Taw", blank=True)

    payoff_1_samp = models.IntegerField()
    payoff_2_samp = models.IntegerField()
    payoff_3_samp = models.IntegerField()
    urn_draws_1_samp = models.StringField()
    urn_draws_2_samp = models.StringField()
    urn_draws_3_samp = models.StringField()

    option_1 = models.IntegerField(initial=0, label="Option Resch")
    option_2 = models.IntegerField(initial=0, label="Option Schin")
    option_3 = models.IntegerField(initial=0, label="Option Taw")
    option_safe = models.IntegerField(initial=0, label = "Hexagon")

    urn_draws_1 = models.StringField()
    urn_draws_2 = models.StringField()
    urn_draws_3 = models.StringField()
    urn_draws_4 = models.StringField()
    payoff_1 = models.IntegerField()
    payoff_2 = models.IntegerField()
    payoff_3 = models.IntegerField()
    payoff_4 = models.IntegerField()

    endowment_after_sampling = models.IntegerField()

    instru_page = models.IntegerField(initial=1)
    belief_page = models.IntegerField(initial=1)
    questionnaire_page = models.IntegerField(initial=1)
    controls = models.IntegerField(initial=0)
    comprehension_page = models.IntegerField(initial=1)
    completion_code = models.StringField()
    sampling_round = models.IntegerField(initial=1)
    points_sampling = models.IntegerField(initial=0)
    decision_1_page = models.IntegerField(initial=1)
    decision_2_page = models.IntegerField(initial=1)

    ranking = models.StringField(blank=True)
    rankingsd = models.StringField(blank=True)
    rankingld = models.StringField(blank=True)
    rankinghd = models.StringField(blank=True)

    payoff_a = models.CurrencyField()
    payoff_b = models.CurrencyField()
    urn_draws_1_a = models.StringField()
    urn_draws_2_a = models.StringField()
    urn_draws_3_a = models.StringField()
    urn_draws_1_b = models.StringField()
    urn_draws_2_b = models.StringField()
    urn_draws_3_b = models.StringField()
    option_1_a = models.IntegerField()
    option_2_a = models.IntegerField()
    option_3_a = models.IntegerField()
    option_1_b = models.IntegerField()
    option_2_b = models.IntegerField()
    option_3_b = models.IntegerField()
    payoff_1_a = models.IntegerField()
    payoff_2_a = models.IntegerField()
    payoff_3_a = models.IntegerField()
    payoff_1_b = models.IntegerField()
    payoff_2_b = models.IntegerField()
    payoff_3_b = models.IntegerField()

    payoffbelief_1 = models.CurrencyField()
    payoffbelief_2 = models.CurrencyField()

    mean_1 = models.FloatField(
        min=0, max=40, label="Mean: Option 1", blank=False
    )

    mean_2 = models.FloatField(
        min=0, max=40, label="Mean: Option 2", blank=False
    )

    mean_3 = models.FloatField(
        min=0, max=40, label="Mean: Option 3", blank=False
    )

    #################################
    # Comprehension Questions #######
    #################################

    cq1_MS3 = models.IntegerField(
        choices=[
            [9, 'No, options change between stages'],
            [1, 'Yes'],
            [99, 'No, options change for the sampling phase'],
            [999, 'Yes, but there is an additional option in the last investment decision'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='In this HIT you repeatedly choose between a number of options. Do you get the same set of options in all rounds of the HIT?',
        initial=0
    )

    cq2_MS3 = models.IntegerField(
        choices=[
            [999, 'each point invested, i.e. each draw, during the sampling stage and the main investment decision'],
            [9, 'each point invested during the sampling stage'],
            [99, 'my performance in comparison to other workers'],
            [1, 'each point invested in the main investment decision'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='My total earnings depend on',
        initial=0
    )

    cq3_MS3 = models.IntegerField(
        choices=[
            [999, 'No, I have to choose blindly'],
            [9, 'Yes, I will see exactly how much each option is worth beforehand'],
            [1, 'Yes, I will be able to sample through the options beforehand'],
            [99, 'Yes, I will see descriptive information based on 150 draws for each option'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='In this HIT you repeatedly choose between a number of options. In the main investment decision, will you have any prior information about the value of these options?',
        initial=0
    )

    cq4_MS3 = models.IntegerField(
        choices=[
            [999, 'No, I have to choose blindly'],
            [9, 'Yes, for my second investment decision, I will see exactly how much each option is worth beforehand'],
            [1, 'Yes, I will have information from 20 prior draws and the information gathered during the sampling phase'],
            [99, 'Yes, for my second investment decision, I will have the same information as I did for the first investment decision'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='In this HIT you repeatedly choose between a number of options. In the second investment decision, will you have any prior information about the value of these options?',
        initial=0
    )

    cq5_MS3 = models.IntegerField(
        choices=[
            [1, 'can differ in their composition of coins'],
            [999, 'contain the same coins'],
            [9, 'return a constant value'],
            [99, 'change over the course of the HIT'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label='Options',
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

    q_sampling_strategy =models.LongStringField(blank=False, label="")

    q_firm =models.LongStringField(blank=False, label="")

    q_fadein =models.LongStringField(blank=False, label="")

    q_fadeout =models.LongStringField(blank=False, label="")

    q_saving =models.LongStringField(blank=False, label="")

    q_wealth =models.LongStringField(blank=False, label="")

    q_function = models.IntegerField(
        choices=[
            [1, 'Yes'],
            [2, 'No'],
        ],
        widget=widgets.RadioSelect,
        label="",
        blank=False
    )

    q_function_yes = models.LongStringField(blank=False, label="")

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

    q_maxoption_3 = models.IntegerField(
        choices = [
            [1, 'Triangle'],
            [2, 'Circle'],
            [3, 'Rectangle'],
            [4, 'Hexagon'],
            [5, 'In the long run, they would all return the same value'],
        ],
        widget=widgets.RadioSelect,
        label="",
        blank=False
    )

    q_decisive_information = models.IntegerField(
        choices = [
            [1, 'Mean'],
            [2, 'Standard Deviation'],
            [3, 'Lowest Draw'],
            [4, 'Highest Draw'],

            ],
        widget=widgets.RadioSelect,
        label="",
        blank=False
    )

    q_descr_exp = models.IntegerField(
        choices = [
            [1, 'The provided summary information'],
            [2, 'Your own sampling experience'],

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



    def sixitems(label):
        return models.IntegerField(
            choices=[
                [1, '1'],
                [2, '2'],
                [3, '3'],
                [4, '4'],
                [5, '5'],
                [6, '6'],
            ],
            widget=widgets.RadioSelectHorizontal,
            blank=False,
            label=label
        )

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

    def thirteenitems(label):
        return models.IntegerField(
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
                [10, '10'],
                [11, '11'],
                [12, '12'],
                [13, '13'],
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

    q_epo_1 = sevenitems('Before I act I consider what I will gain or lose in the future as a result of my actions.')
    q_epo_2 = sevenitems('I try to anticipate as many consequences of my actions as I can.')
    q_epo_3 = sevenitems('Before I make a decision I consider all possible outcomes.')
    q_epo_4 = sevenitems('I always try to assess how important the potential consequences of my decisions might be.')
    q_epo_5 = sevenitems('I try hard to predict how likely different consequences are.')
    q_epo_6 = sevenitems('Usually I carefully estimate the risk of various outcomes occurring.')
    q_epo_7 = sevenitems('I keep a positive attitude that things always turn out all right.')
    q_epo_8 = sevenitems('I prefer to think about the good things that can happen rather than the bad.')
    q_epo_9 = sevenitems('When thinking over my decisions I focus more on their positive end results.')
    q_epo_10 = sevenitems('I tend to think a lot about the negative outcomes that might occur as a result of my actions.')
    q_epo_11 = sevenitems('I am often afraid that things might turn out badly.')
    q_epo_12 = sevenitems('When thinking over my decisions I focus more on their negative end results.')
    q_epo_13 = sevenitems('I often worry about what could go wrong as a result of my decisions.')

    q_max_scale_1 = sevenitems('No matter how satisfied I am with my job, it’s only right for me to be on the lookout for better opportunities.')
    q_max_scale_2 = sevenitems('When I am in the car listening to the radio, I often check other stations to see if something better is playing, even if I am relatively satisfied with what I’m listening to.')
    q_max_scale_3 = sevenitems('I often find it difficult to shop for a gift for a friend')
    q_max_scale_4 = sevenitems('Choosing a tv show or a movie to watch is really difficult. I’m always struggling to pick the best one.')
    q_max_scale_5 = sevenitems('I never settle for second best.')
    q_max_scale_6 = sevenitems('No matter what I do, I have the highest standards for myself.')


    q_mean_sequential = sevenitems('The summary information about each option\'s mean informed my main decision')
    q_sd_sequential = sevenitems('The summary information about each option\'s standard deviation informed my main decision')
    q_ld_sequential = sevenitems('The summary information about each option\'s lowest draw informed my main decision')
    q_hd_sequential = sevenitems('The summary information about each option\'s highest draw informed my main decision')


    q_mean_simultan = sevenitems('The summary information about each option\'s mean informed my main decision')
    q_sd_simultan = sevenitems('The summary information about each option\'s standard deviation informed my main decision')
    q_ld_simultan = sevenitems('The summary information about each option\'s lowest draw informed my main decision')
    q_hd_simultan = sevenitems('The summary information about each option\'s highest draw informed my main decision')