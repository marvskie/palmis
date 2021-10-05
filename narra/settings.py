import os
from os.path import join

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", "test")

DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(" ")
APPEND_SLASH = True


APPS = [
    'commons.apps.CommonsConfig',
    'login.apps.LoginConfig',
    'inventory.apps.InventoryConfig',
    'message.apps.MessageConfig',
    'preferences.apps.PreferencesConfig',
    'executive.apps.ExecutiveConfig',

    #This line is for adding Application
    'mobility.apps.MobilityConfig',
    'engineering.apps.EngineeringConfig',
    'firepower.apps.FirepowerConfig',
    'tosb.apps.TosbConfig',
    'exec.apps.ExecConfig',
    'adminbranch.apps.AdminBranchConfig',
    'samb.apps.SAMBConfig',
    'camb.apps.CAMBConfig',
    'lob.apps.LobConfig',
    'ppb.apps.PpbConfig',
    'lsdb.apps.LsdbConfig',
    'famis.apps.FamisConfig',
]

INSTALLED_APPS = [
    'jazzmin',
    'rest_framework',
    'oauth2_provider',
    'corsheaders',
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'admin_reorder',
    'import_export',
    'admin_totals', 
    'core_chat',
    'channels'
] + APPS

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
)

AUTHENTICATION_BACKEND = (
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'commons.permissions.BaseAuthenticatedPermission',
    # ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 25,
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend', ),
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '3/second',
    #     'user': '15/second'
    # }

    # chat rest framework
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'},
    'ACCESS_TOKEN_EXPIRE_SECONDS': 1800,  # 30 min
    'REFRESH_TOKEN_EXPIRE_SECONDS': 1800,  # 30 min
    'OAUTH_DELETE_EXPIRED': True,
}

ROOT_URLCONF = 'narra.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'narra.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_L10N = True
USE_TZ = False
    

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '', 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

X_FRAME_OPTIONS = 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

# ============ chat settings

MESSAGES_TO_LOAD = 15
CHANNEL_LAYERS = {
    "default": {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
# Could be changed to the config below to scale:
# "BACKEND": "asgi_redis.RedisChannelLayer",
# "CONFIG": {
#     "hosts": [("localhost", 6379)],
# },
ASGI_APPLICATION = 'narra.routing.application'

# ============ end chat settings

# JAZZMIN APP Settings 
#  theme candidate = lux, minty
JAZZMIN_SETTINGS= {
    # "navbar_small_text": False,
    # "footer_small_text": False,
    # "body_small_text": False,
    # "brand_small_text": False,
    # "brand_colour": False,
    # "accent": "accent-primary",
    # "navbar": "navbar-white navbar-light",
    # "no_navbar_border": False,
    # "navbar_fixed": False,
    # "layout_boxed": False,
    # "footer_fixed": False,
    # "sidebar_fixed": False,
    # "sidebar": "sidebar-dark-primary",
    # "sidebar_nav_small_text": False,
    # "sidebar_disable_expand": False,
    # "sidebar_nav_child_indent": False,
    # "sidebar_nav_compact_style": False,
    # "sidebar_nav_legacy_style": False,
    # "sidebar_nav_flat_style": False,
    "theme": "minty",
    # "dark_mode_theme": None
    # title of the window
    "site_title": "PA Logistics Management Information System",

    # Title on the brand, and the login screen (19 chars max)
    "site_header": "PALMIS",

    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    "site_logo": "logo.png",

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Philippine Army Logistics Management Information System",

    # Copyright on the footer
    "copyright": "PALMIS - OG4, PA",

    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "exec.FileAttachment",

    # Field name on user model that contains avatar image
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        # {"name": "Accounts", "url": "/commons/account", "new_window": False},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Executive", "url": "/exec", "new_window": False},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Chat", "url": "/chat", "new_window": False},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Calendar", "url": "/custom/calendar", "new_window": False},

        # model admin to link to (Permissions checked against model)
        # {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        # {"app": "books"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        # {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ['auth', 'commons','inventory', 'message', 'oauth2_provider', 'django_otp', 'otp_totp','preferences','core_chat'],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [
        "ppb.Status",
        "ppb.ObjectCode",
        "ppb.MajorPap",
        "ppb.SubPap",
        "ppb.SuggestedPap",
        "ppb.MissionArea",
        "ppb.ExpenseClass",
        "ppb.Kma",
        "ppb.Dpg",
        "ppb.StrategicObjective",
        "ppb.StrategicProgram",
        "ppb.PawafItemView",
        "ppb.KeyProgram",
        "ppb.PawafItemEndUser", 
        "ppb.FundReleaseItem", 
        "ppb.FundReleaseAsaItem",
        "ppb.PbdgObjective",
        "ppb.ProgramObjective"
    ],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
                              "admin",
                              "exec", "exec.FileAttachment", "exec.Task", "exec.Categories",
                              "adminbranch.RosterOfTroops","adminbranch.AdminMooe", "adminbranch.AdminEquipment", "adminbranch.IncomingCommunication", "adminbranch.OutgoingCommunication",
                              "mobility.VehicleRecord", "mobility.RepairRecord", "mobility.RegistrationStatus", "mobility.InsuranceSchedule", "mobility.DisposalRecord",
                              "camb.DASProjects","camb.DASProjectStatus","camb.FMSProjects","camb.SRDPProjects","camb.InternationalLogisticsActivities","camb.ReferencesHelpfulLinks","camb.ReferencesDefenseExhibits","camb.ReferencesPolicies","camb.ReferencesBrochures","camb.DraftDocuments","camb.IncomingCommunication","camb.OutgoingCommunication",
                              "lob.LogisticsSupportPlan","lob.PCHT","lob.AccomplishmentReport","lob.CommandDirectedActivities","lob.IssuesAndConcerns","lob.IncomingCommunication","lob.OutgoingCommunication",
                              "lsdb.InternationalMilitaryAffairsActivity","lsdb.LogisticsOfficersForumActivity","lsdb.LogisticsStaffVisit","lsdb.ATRStrategicPrograms","lsdb.LogisticsSchooling","lsdb.ApprovedResolutionsCourse","lsdb.CourseApplicationProcedure","lsdb.ExecomPropertyAccountabilityPersonnel","lsdb.SurveyBoard","lsdb.LogisticsReference","lsdb.CoaFindingsAOM","lsdb.CoaFindingsCAAR","lsdb.IncomingCommunication","lsdb.OutgoingCommunication",
                              "engineering.BuildingRecord","engineering.HeavyEquipment","engineering.LightRecord","engineering.WaterRecord","engineering.InsuranceOfBuilding","engineering.SurveyTitlingFencing","engineering.LotRental","engineering.DetailedArchitecturalAndEngineeringDesign","engineering.ComprehensiveMasterDevelopmentPlan","engineering.CapitalOutlay","engineering.InteragencyTransferFund","engineering.BasesConversionAndDevelopmentAuthority","engineering.IncomingCommunication","engineering.OutgoingCommunication",
                              "ppb.Pawaf","ppb.PawafItem","ppb.FundRelease","ppb.FundReleaseAsa",
                              "samb.PAProject","samb.PITCProject","samb.BACRecord","samb.TWGRecord","samb.IncomingCommunication","samb.OutgoingCommunication",  
                              "tosb.ICIERecord","tosb.RMCRecord","tosb.OERecap","tosb.OEMasterList","tosb.OEProgramming","tosb.OEStockStatus","tosb.TOSPolicies","tosb.IncomingCommunication","tosb.OutgoingCommunication",
                              "firepower.Firearm","firepower.Ammunition","firepower.Accessories","firepower.SpareParts","firepower.StatusOfFillUp","firepower.TOEPaWide","firepower.TOEMotherUnit","firepower.ProgramsRepairAndMaintenance","firepower.ProgramsProcurement","firepower.ProgramsDisposal","firepower.ProgramsDemilitarization","firepower.ExpenditureAmmunition","firepower.IncomingCommunication","firepower.OutgoingCommunication",
                              ],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages", 
            "url": "make_messages", 
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free
    # for a list of icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "army.css",
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "horizontal_tabs", "auth.group": "horizontal_tabs",},
    # Add a language dropdown into the admin
    "language_chooser": True,
   
}

# ADMIN reorder settings 
ADMIN_REORDER = (
    # Keep original label and models
    'sites',

    # # Rename app
    # {'app': 'engineering', 'label': 'Engineering Branch'},

    # # # Reorder app models
    # {'app': 'adminbranch', 'models': ('adminbranch.RosterOfTroops','adminbranch.AdminMooe', 'adminbranch.AdminEquipment')},
    {'app': 'exec', 'models': ('exec.FileAttachment','exec.Task')},

    # # # Exclude models
    # # {'app': 'auth', 'models': ('auth.User', )},

    # # # Cross-linked models
    # # {'app': 'auth', 'models': ('auth.User', 'sites.Site')},

    # # models with custom name
    # {'app': 'engineering', 'models': (
    #     {'model': 'engineering.HeavyEquipment', 'label': 'Heavy'},
    # )},
)

try:
    from narra.settings_dev import *
except Exception as e:
    print(e)
    print('No localsettings found.')
