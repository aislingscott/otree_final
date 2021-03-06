import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings
ROOM_DEFAULTS = {}
ROOMS = [
    {
        'name': 'xlab1',
        'display_name': 'xlab1',
        'participant_label_file': '_rooms/computers.txt',
    },
    {
        'name': 'xlab2',
        'display_name': 'xlab2',
        'participant_label_file': '_rooms/computers.txt',
    },
    {
        'name': 'xlab3',
        'display_name': 'xlab3',
        'participant_label_file': '_rooms/computers.txt',
    },
    {
        'name': 'xlab4',
        'display_name': 'xlab4',
        'participant_label_file': '_rooms/computers.txt',
    },
    {
        'name': 'xlab5',
        'display_name': 'xlab5',
    },
   ]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SENTRY_DSN = 'http://d0fe968b66cc427ca3ca75638abfdd53:cc0f55764d2643e4b95f6cd1f68d87a8@sentry.otree.org/115'
# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False

DEBUG = False


ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# don't share this with anybody.
SECRET_KEY = '{{ secret_key }}'

PAGE_FOOTER = ''

# To use a database other than sqlite,
# set the DATABASE_URL environment variable.
# Examples:
# postgres://USER:PASSWORD@HOST:PORT/NAME
# mysql://USER:PASSWORD@HOST:PORT/NAME

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')


# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ["django.contrib.humanize"]

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            Source code
        </a> for the below games.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Below are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish to create your own variations.
    Click one to learn more and play.
</p>
"""

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.,
    'participation_fee': 5.00,
    'num_bots': 6,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    #~ {
        #~ 'name': 'big_five',
        #~ 'display_name': "Big Five",
        #~ 'num_demo_participants': 1,
        #~ 'app_sequence': ['big_five'],
    #~ },
    #~ {
        #~ 'name': 'gssas_holtlaury',
        #~ 'display_name': "GSS Attitudinal Survey Questions & Holt/Laury Risk Preferences",
        #~ 'num_demo_participants': 1,
        #~ 'app_sequence': ['gssas_holtlaury'],
    #~ },
    #~ {
        #~ 'name': 'tt_checker',
        #~ 'display_name': "Trust Type Checker",
        #~ 'num_demo_participants': 2,
        #~ 'app_sequence': ['trust_type_check'],
    #~ },
    {
        'name': 'pre_survey',
        'display_name': "Pre Survey",
        'num_demo_participants': 2,
        'app_sequence': ['pre_survey'],
    },
    {
        'name': 'post_survey',
        'display_name': "Post Survey",
        'num_demo_participants': 1,
        'app_sequence': ['post_survey'],
    }
]

trusts = []
full = []

for reveal_variation  in ("reveal", "no-reveal"):
    for play_variation  in ("sequential_first"):
        for order_variation  in ("first_above", "first_below"):
            treatment_type = (reveal_variation,  play_variation, order_variation)
            trusts.append({
                "name": "trust_" + "_".join(treatment_type).replace("-", "_"),
                "display_name": "Trust ({})".format(", ".join(map(str.title, treatment_type))),
                "num_demo_participants": 2,
                'trust_score': "pss",
                "auto_trust_score": True,
                "treatment_type": treatment_type,
                'app_sequence': ["trust"]})
            full.append({
                "name": "full_" + "_".join(treatment_type).replace("-", "_"),
                "display_name": "Full Game ({})".format(", ".join(map(str.title, treatment_type))),
                "num_demo_participants": 4,
                'trust_score': "pss",
                "auto_trust_score": False,
                "treatment_type": treatment_type,
                'app_sequence': ["pre_survey", "trust", 'post_survey']})

SESSION_CONFIGS += trusts + full


# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
