from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']


# https://otree.readthedocs.io/en/latest/mturk.html#session-config

mturk_hit_settings_compensation = {
    'keywords': [],
    'title': 'Compensation HIT',
    'description': '',
    'frame_height': 800,
    'minutes_allotted_per_assignment': 20,
    'expiration_hours': 168,
    'grant_qualification_id': '3OPOXV2R260YIB0WOK653HEZKCJI8A',
    'qualification_requirements': [
        {
            'QualificationTypeId': "3NCAQQYPG45BZJYRR28GQM0BV6CNNJ",
            'Comparator': "Exists",
        },
        {
            'QualificationTypeId': "3OPOXV2R260YIB0WOK653HEZKCJI8A",
            'Comparator': "DoesNotExist",
        },
    ]
}

mturk_hit_settings = {
    'keywords': ['bonus', 'short', 'academic'],
    'title': 'Task on Human Decision Making (with bonus)',
    'description': 'This HIT takes approximately 15 minutes to complete. Please accept this HIT only if you can commit to completing it right away and without interruption. You can earn a substantial bonus that exceeds the reward for this HIT.',
    'frame_height': 800,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 35,
    'expiration_hours': 168,
    'grant_qualification_id': '3TKFAEIWW949YA9UOC37ZR0HEHVBNF',
    'qualification_requirements': [
        {
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}],
        },
        {
            'QualificationTypeId': "000000000000000000L0",
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [90],
        },
        {
            'QualificationTypeId': "00000000000000000040",
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [100],
        },
        {
            'QualificationTypeId': "3TKFAEIWW949YA9UOC37ZR0HEHVBNF",
            'Comparator': "DoesNotExist",
        },
    ]
}

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.003,
    'participation_fee': 1.20,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
       'name': 'MAB Pilot Testing',
        'display_name': "MAB Pilot Testing",
        'num_demo_participants': 1
        'app_sequence': ['MAB'],
        'choice': False
    },

]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'Coins'
POINTS_DECIMAL_PLACES = 0

ROOMS = []

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')
ADMIN_USERNAME = 'karl'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# MTurk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})
OTREE_PRODUCTION = 1

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2@c$7&ita(ik@z(7h)%kr+w=u*f1r&q+7or%)&q&!%fb@9xjrc'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
# INSTALLED_APPS = ['otree']
INSTALLED_APPS = ['otree', 'otree_mturk_utils']
EXTENSION_APPS = ['otree_mturk_utils']
