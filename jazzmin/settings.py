import copy
import logging
from typing import Dict

from django.conf import settings
from django.contrib.admin import AdminSite
from django.templatetags.static import static

from .utils import get_admin_url, get_model_meta

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {
    # title of the window
    "site_title": AdminSite.site_title,
    # Title on the brand, and the login screen (19 chars max)
    "site_header": AdminSite.site_header,
    # Relative path to logo for your site, used for favicon and brand on top left (must be present in static files)
    "site_logo": "vendor/adminlte/img/AdminLTELogo.png",
    # Welcome text on the login screen
    "welcome_sign": "Welcome",
    # Copyright on the footer
    "copyright": "",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": None,
    # Field name on user model that contains avatar image
    "user_avatar": "avatar",

    ############
    # Top Menu #
    ############
    # Links to put along the nav bar
    "topmenu_links": [],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ('app' url type is not allowed)
    "usermenu_links": [],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps to base side menu ordering off of
    "order_with_respect_to": [],
    # Custom links to append to side menu app groups, keyed on app name
    "custom_links": {},
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free
    # for a list of icon classes
    "icons": {"auth": "fas fa-users-cog", "auth.user": "fas fa-user", "auth.Group": "fas fa-users",},
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Activate Bootstrap modal
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
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
    "changeform_format_overrides": {},
    # Add a language dropdown into the admin
    "language_chooser": False,
    "facility_type":['Operational','Support','Base Utilities','Community'],
    "edit_field":['PAMU','Sub unit','Location',
                'Name of Facility','Facility Classification','Area/ lnM/ Width','Bldg/ Utility Code','Building Administrator','Mode of Acquisition','Year Acquired','Master Developmental Plan Alignment',
                'Building insurance Nr','Amount of insurance','Original Amount','Appraised Value','Date of Appraised Value',
                'Amount enhanced/ repair','Date/ Year of enhanced/repair','Fund','Date Requested','Date of Repair/ Enhancement','Amount of Repair/ Enhancement','Qualitative scale',
                'Camp Code','Name of Camp','Region','Total Area (Hectares)','Total Perimeter (Meter)','Topography',
                'Perimeter with Fence (Meter)','Type of Fence','Unit Code/ Administrator','Tenant Unit/ LGU/ CIV','Total Area Occupied/ Developed','Nr of facility established',
                'Type of Ownership','Authority of Ownership','Date Acquired','Date of renewal(if acquired through MOA, Reso, etc)',
                'Progress of titling','Date of Progress Titling','Unit in-charge of titling','Amount programmed for titling','Amount downloaded for titling',
                'Area of Idle land(Sq M/ Has)','Year Leased','Date of Expiration','Economic zone classification'],
    "Acquisition_Mode":['Donation','Modernization RA7897','Modernization RA10349','BCDA','Trust Reciept'],
    "pamus":['1ID','2ID','3ID','4ID','5ID','6ID','7ID','8ID','9ID','10ID','11ID','1BCT','51EBde','52EBde',
            '53EBde','54EBde','55EBde','AAR','AFPPS','AIR','APAO','APMC','ARESCOM','ARMOR','ASCOM','ASPA',
            'ASR','AVnR','CMOR','FCPA','FSRR','HHSG','IMCOM','LRR','SFR(A)','SOCOM','TRADOC'],
    "unit_list":["1002IBde","101Bde","102BDE","103 Brigade","107TH CO",
                "109th CO","10DTS","10FAU","10FPAO","10FSFO",
                "10FSSU","10IB","10IMB","10ISU","10RCDG",
                "1101BDE","111CO","112CO","11DTS","11FPAO",
                "11FSSU","11ISU","11RCDG","11SIGBN","11SSBn",
                "12FSFO","12FSSU","12ISU","1301DD","14AIB",
                "14FSFO","14RCDG","15AIB","15FPAO","15FSFO",
                "16FPAO","16ISU","17AIB","17FAU","17FPAO",
                "17FSFO","17IB","18IB","191MPBn","1ATG",
                "1Cav Co(S)","1CMOBn","1FSSU","1ID","1IMB",
                "1ISU","1LSG","1MBN","1MIB","1RCDG",
                "1SBn","1SRB","1SSBN","201BDE","202Bde",
                "202IBde","203BDE","20IB","21CAV COy","21SRC",
                "22CAV Coy","23CAV Coy","24ISU","2ASH","2CAV",
                "2CAVCoy","2DCAU","2DTS","2FSFO","2FSSU",
                "2IMB","2ISU","2LSG","2Mech Bde","2SFBN",
                "2SRB","2SRC","2SSBn","301BDE","302BDE",
                "303BDE","32IB","33IB","38IB","3cavcoy",
                "3FAB","3FSFO","3ISU","3Mech Bn","3RCDG",
                "3SigBn","3SRB","407CDC","40IB","41IB",
                "45IB","46IB","4CAVCoy","4DTS","4FAB",
                "4FPAO","4FSFO","4FSSU","4ISU","4RCDG",
                "4SRB","500ECB","501BDE","503BDE","512ECB",
                "513ECB","514ECB","51ESB","51ESC","522ECB",
                "524ECB","525ECB","534ECB","542ECB","543ECB",
                "544ECB","545ECB","546ECB","547ECB","548ECB",
                "549ECB","551ECB","552ECB","564ECB","565ECB",
                "5DCAU/ 77IB","5DTS","5FAB","5FSFO","5FSSU",
                "5IMB","5ISU","5RCDG","5SRB","601BDE",
                "602BDE","6CAV Coy","6DCAU","6FAB","6FAU",
                "6FMSC","6FSFO","6FSSU","6RCDG","6SBn",
                "701B","701BDE","702Bde","702CDC","703BDE",
                "703CDC","704CDC","72IB","77IB","78IB",
                "7DTS","7FSFO","7FSSU","7IMB","7RCDG",
                "801BDE","802BDE","802CDC","803BDE","806CDC",
                "84IB","86IB","88IB","8FSSU","8ISU",
                "8MIB","8RCDG","901st Bde","902BDE","903BDE",
                "91IB","95IB","98IB","9CMOBn","9DTS",
                "9FAB","9FSFO","9FSSU","9IMB","9ISU",
                "9PED","9RCDG","9SSBN","AABn","AFPCGSC",
                "AFPPS","AGH","AGSMO","AHO","AHRO",
                "AIR","AMC","APMC","AREC","ARO-M",
                "ASM","ATS","C2C","C2C (P)","CAC",
                "CB","CC (P)","CEASH","CLSH","CMOBN",
                "CMOR","CMOS","CSSH","DSM","EODBN",
                "ESBN","ESC","FBHFMC","FC","FCPA",
                "G3","G7","GSMO","H10ID","H11ID",
                "H1ID","H1SBN","H2ID","H3ID","H4ID",
                "H3ID","H4ID","H52E","H54E","H55E",
                "H5ID","H6ID","H7ID","H7RCDG","H8ID",
                "H9ID","HAAR","HASPA","HFSRR","HHSBn",
                "HHSG","HLRR","HQS","HSBn","HSFRA",
                "IMTC","K9BN","LETB","LRS","MATG",
                "LRS","MATG","MFO","MPBn","MTC (P)",
                "NCRRCDG","NETBn","OAA","OACE","OACESPA",
                "OACH","OACOCS","OACPA","OAGAD","OAIA",
                "OAJA","OAPM","OCDS","OCG","OG1",
                "OG10","OG3","OG5, PA","OG7","OG7/OG8",
                "OG7","OG7/OG8","OG9","OPCC","OVC",
                "PABAC","PAICoe","PAOLCI","PAPC","PED",
                "PED, HHSBn","PGAB","PMO","PSD","RAD",
                "RDC","REPEWC","SC (P)","SCS","SEBN",
                "SFS","SMAC","SOCOM","SRC","SRS",
                "SRC","SRS","SRTS","SSBN","SSC",
                "SSTS","SWMO","TAP","TF Gensan","TSS",
                "TSSC (P)","UPO","VATG"],
    "p_1ID":["101Bde","102BDE","103 Brigade","10IB","18IB","1CMOBn","1MIB","1SSBN","H1ID","HHSBn","SSBN"],
    "p_2ID":["201BDE", "202Bde", "202IBde", "203BDE", "2ASH", "2DCAU", "2DTS", "2SSBn", "H2ID"],
    "p_3ID":["301BDE", "302BDE", "303BDE", "H3ID"],
    "p_4ID":["10FAU", "4DTS", "4SRB", "88IB", "DSM", "H4ID", "SSBn"],
    "p_5ID":["17IB", "501BDE", "503BDE", "5DCAU/ 77IB", "5DTS", "77IB", "86IB", "95IB", "98IB", "CMOBN", "H5ID"],
    "p_6ID":["33IB", "38IB", "40IB", "601BDE", "602BDE", "6DCAU", "6FMSC", "CSSH", "H6ID", "HHSBN", "SSBN", "TF Gensan"],
    "p_7ID":["107TH CO", "701B", "701BDE", "702Bde", "703BDE", "7DTS", "84IB", "91IB", "G3", "H7ID", "HSBn", "REPEWC", "SSBn"],
    "p_8ID":["20IB", "46IB", "78IB", "801BDE", "802BDE", "803BDE", "8MIB", "CLSH", "H8ID"],
    "p_9ID":["9SSBN","109th CO", "901st Bde", "902BDE", "903BDE", "9CMOBn", "9DTS", "9IMB", "CEASH", "G7", "H9ID", "PED"], 
    "p_10ID":["1002IBde", "10DTS", "10IMB", "72IB", "H10ID"], 
    "p_11ID":["1101BDE", "11DTS", "11SSBn", "32IB", "3SRB", "41IB", "45IB", "H11ID"], 
    "p_FSRR":["1SRB", "21SRC", "2SRB", "2SRC", "4SRB", "5SRB", "HFSRR", "SRC", "SRS", "SRTS"],
    "p_SFR":["2SFBN", "6SBn", "HQS", "HSFRA", "SFS"], 
    "p_1BCT":["HQS"],
    "p_LRR":["HLRR", "LRS"], 
    "p_AVnR":["AMC", "HQS", "SMAC"], 
    "p_ARMOR":["1Cav Co(S)", "21CAV COy", "21CAV Coy","2CAV", "22CAV COy", "23CAV Coy", "2CAVCoy", "2Mech Bde", "3cavcoy", "3Mech Bn", "4CAVCoy", "6CAV Coy", "HHSBn", "HQS", "PED, HHSBn"],
    "p_51EBde":["513ECB", "514ECB", "51ESB", "51ESC", "522ECB", "525ECB", "548ECB", "564ECB", "565ECB", "HQS"], 
    "p_AFPPS":["112CO"], 
    "p_52EBde":["111CO","AFPPS", "512ECB", "524ECB", "534ECB", "544ECB", "ESBN", "ESC", "H52E"], 
    "p_53EBde":["542ECB", "543ECB", "546ECB", "552ECB", "ESC", "HQS"], 
    "p_54EBde":["1ID", "545ECB", "547ECB", "549ECB", "H54E"], 
    "p_55EBde":["H55E", "551ECB", "500ECB"], 
    "p_AAR":["3FAB", "4FAB", "5FAB", "6FAB", "9FAB", "ATS", "HAAR", "HQS"], 
    "p_AIR":["10ISU", "11ISU", "12ISU", "14AIB", "15AIB", "16ISU", "17AIB", "1ISU", "24ISU", "2ISU", "3ISU", "4ISU", "5ISU", "8ISU", "9ISU", "HQS", "K9BN", "PAICoe"], 
    "p_ASR":["11SIGBN", "3SigBn", "6SBn", "CB", "H1SBN", "HQS", "NETBn", "TSS"], 
    "p_IMCOM":["107th CO", "1301DD", "191MPBn", "1IMB", "2IMB", "5IMB", "7IMB", "9IMB", "9PED", "AFPCGSC", "AGSMO", "AHO", "AHRO", "AIR", "APMC", "AREC", "ASM", "FBHFMC", "HQS", "MPBn", "OAA", "OACE", "OACESPA", "OACH", "OACOCS", "OACPA", "OAGAD", "OAIA", "OAJA", "OAPM", "OCDS", "OCG", "OG1", "OG10", "OG3", "OG5, PA", "OG7", "OG7/OG8", "OG9", "OPCC", "OVC", "PABAC", "PAPC", "PGAB", "SEBN", "SSC", "SWMO", "UPO"], 
    "p_CMOR":["CMOR", "CMOS"], 
    "p_ASCOM":["10FSSU", "11FSSU", "12FSSU", "1FSSU", "1LSG", "1MBN", "1SBn", "2FSSU", "2LSG", "4FSSU", "5FSSU", "6FSSU", "7FSSU", "8FSSU", "9FSSU", "AABn", "EODBN", "HHSBn", "HQS", "PMO", "RDC", "SSTS"], 
    "p_TRADOC":["1ATG", "C2C", "C2C (P)", "CC (P)", "FC", "HQS", "IMTC", "MATG", "MTC (P)", "SC (P), CAC", "SCS", "TSSC (P)", "VATG"], 
    "p_ARESCOM":["10RCDG", "11RCDG", "14RCDG", "1RCDG", "3RCDG", "407CDC", "4RCDG","5RCDG", "6RCDG", "702CDC", "703CDC", "704CDC", "7RCDG", "802CDC","806CDC", "8RCDG", "9RCDG", "ATS", "H7RCDG", "HHSBn", "HQS", "NCRRCDG"], 
    "p_ASPA":["17FAU", "6FAU", "HASPA"], 
    "p_FCPA":["10FSFO", "12FSFO", "14FSFO", "15FSFO", "17FSFO", "2FSFO", "3FSFO", "4FSFO", "5FSFO","6FSFO", "7FSFO", "9FSFO", "FCPA", "HQS"], 
    "p_APAO":["10FPAO", "11FPAO", "15FPAO", "16FPAO", "17FPAO", "4FPAO", "HQS"], 
    "p_APMC":["APMC", "ARO-M", "GSMO", "LETB", "MFO", "PSD", "RAD", "TAP"],
    "p_HHSG":["1301DD", "AGH", "HHSG", "HQS", "HSBn", "OCG", "PAOLCI", "SEBN"], 
    "p_SOCOM":["SOCOM"],

}

#######################################
# Currently available UI tweaks       #
# Use the UI builder to generate this #
#######################################
DEFAULT_UI_TWEAKS = {
    # Small text on the top navbar
    "navbar_small_text": False,
    # Small text on the footer
    "footer_small_text": False,
    # Small text everywhere
    "body_small_text": False,
    # Small text on the brand/logo
    "brand_small_text": False,
    # brand/logo background colour
    "brand_colour": False,
    # Link colour
    "accent": "accent-primary",
    # topmenu colour
    "navbar": "navbar-white navbar-light",
    # topmenu border
    "no_navbar_border": False,
    # Make the top navbar sticky, keeping it in view as you scroll
    "navbar_fixed": False,
    # Whether to constrain the page to a box (leaving big margins at the side)
    "layout_boxed": False,
    # Make the footer sticky, keeping it in view all the time
    "footer_fixed": False,
    # Make the sidebar sticky, keeping it in view as you scroll
    "sidebar_fixed": False,
    # sidemenu colour
    "sidebar": "sidebar-dark-primary",
    # sidemenu small text
    "sidebar_nav_small_text": False,
    # Disable expanding on hover of collapsed sidebar
    "sidebar_disable_expand": False,
    # Indent child menu items on sidebar
    "sidebar_nav_child_indent": False,
    # Use a compact sidebar
    "sidebar_nav_compact_style": False,
    # Use the AdminLTE2 style sidebar
    "sidebar_nav_legacy_style": False,
    # Use a flat style sidebar
    "sidebar_nav_flat_style": False,
    # Bootstrap theme to use (default, or from bootswatch, see THEMES below)
    "theme": "default",
    # Theme to use instead if the user has opted for dark mode (e.g darkly/cyborg/slate/solar/superhero)
    "dark_mode_theme": None,
}

THEMES = {
    # light themes
    "default": "vendor/bootswatch/default/bootstrap.min.css",
    "cerulean": "vendor/bootswatch/cerulean/bootstrap.min.css",
    "cosmo": "vendor/bootswatch/cosmo/bootstrap.min.css",
    "flatly": "vendor/bootswatch/flatly/bootstrap.min.css",
    "journal": "vendor/bootswatch/journal/bootstrap.min.css",
    "litera": "vendor/bootswatch/litera/bootstrap.min.css",
    "lumen": "vendor/bootswatch/lumen/bootstrap.min.css",
    "lux": "vendor/bootswatch/lux/bootstrap.min.css",
    "materia": "vendor/bootswatch/materia/bootstrap.min.css",
    "minty": "vendor/bootswatch/minty/bootstrap.min.css",
    "pulse": "vendor/bootswatch/pulse/bootstrap.min.css",
    "sandstone": "vendor/bootswatch/sandstone/bootstrap.min.css",
    "simplex": "vendor/bootswatch/simplex/bootstrap.min.css",
    "sketchy": "vendor/bootswatch/sketchy/bootstrap.min.css",
    "spacelab": "vendor/bootswatch/spacelab/bootstrap.min.css",
    "united": "vendor/bootswatch/united/bootstrap.min.css",
    "yeti": "vendor/bootswatch/yeti/bootstrap.min.css",
    # dark themes
    "darkly": "vendor/bootswatch/darkly/bootstrap.min.css",
    "cyborg": "vendor/bootswatch/cyborg/bootstrap.min.css",
    "slate": "vendor/bootswatch/slate/bootstrap.min.css",
    "solar": "vendor/bootswatch/solar/bootstrap.min.css",
    "superhero": "vendor/bootswatch/superhero/bootstrap.min.css",
}

DARK_THEMES = ("darkly", "cyborg", "slate", "solar", "superhero")

CHANGEFORM_TEMPLATES = {
    "single": "jazzmin/includes/single.html",
    "carousel": "jazzmin/includes/carousel.html",
    "collapsible": "jazzmin/includes/collapsible.html",
    "horizontal_tabs": "jazzmin/includes/horizontal_tabs.html",
    "vertical_tabs": "jazzmin/includes/vertical_tabs.html",
}


def get_search_model_string(jazzmin_settings: Dict) -> str:
    """
    Get a search model string for reversing an admin url.

    Ensure the model name is lower cased but remain the app name untouched.
    """

    app, model_name = jazzmin_settings["search_model"].split(".")
    return "{app}.{model_name}".format(app=app, model_name=model_name.lower())


def get_settings() -> Dict:
    jazzmin_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = {x: y for x, y in getattr(settings, "JAZZMIN_SETTINGS", {}).items() if y is not None}
    jazzmin_settings.update(user_settings)

    # Extract search url from search model
    if jazzmin_settings["search_model"]:
        jazzmin_settings["search_url"] = get_admin_url(get_search_model_string(jazzmin_settings))
        model_meta = get_model_meta(jazzmin_settings["search_model"])
        if model_meta:
            jazzmin_settings["search_name"] = model_meta.verbose_name_plural.title()
        else:
            jazzmin_settings["search_name"] = jazzmin_settings["search_model"].split(".")[-1] + "s"

    # Deal with single strings in hide_apps/hide_models and make sure we lower case 'em
    if type(jazzmin_settings["hide_apps"]) == str:
        jazzmin_settings["hide_apps"] = [jazzmin_settings["hide_apps"]]
    jazzmin_settings["hide_apps"] = [x.lower() for x in jazzmin_settings["hide_apps"]]

    if type(jazzmin_settings["hide_models"]) == str:
        jazzmin_settings["hide_models"] = [jazzmin_settings["hide_models"]]
    jazzmin_settings["hide_models"] = [x.lower() for x in jazzmin_settings["hide_models"]]

    # Ensure icon model names and classes are lower case
    jazzmin_settings["icons"] = {x.lower(): y.lower() for x, y in jazzmin_settings.get("icons", {}).items()}

    # ensure all model names are lower cased
    jazzmin_settings["changeform_format_overrides"] = {
        x.lower(): y.lower() for x, y in jazzmin_settings.get("changeform_format_overrides", {}).items()
    }

    return jazzmin_settings


def get_ui_tweaks() -> Dict:
    raw_tweaks = copy.deepcopy(DEFAULT_UI_TWEAKS)
    raw_tweaks.update(getattr(settings, "JAZZMIN_UI_TWEAKS", {}))
    tweaks = {x: y for x, y in raw_tweaks.items() if y not in (None, "", False)}

    # These options dont work well together
    if tweaks.get("layout_boxed"):
        if "navbar_fixed" in tweaks:
            del tweaks["navbar_fixed"]
        if "footer_fixed" in tweaks:
            del tweaks["footer_fixed"]

    bool_map = {
        "navbar_small_text": "text-sm",
        "footer_small_text": "text-sm",
        "body_small_text": "text-sm",
        "brand_small_text": "text-sm",
        "sidebar_nav_small_text": "text-sm",
        "no_navbar_border": "border-bottom-0",
        "sidebar_disable_expand": "sidebar-no-expand",
        "sidebar_nav_child_indent": "nav-child-indent",
        "sidebar_nav_compact_style": "nav-compact",
        "sidebar_nav_legacy_style": "nav-legacy",
        "sidebar_nav_flat_style": "nav-flat",
        "layout_boxed": "layout-boxed",
        "sidebar_fixed": "layout-fixed",
        "navbar_fixed": "layout-navbar-fixed",
        "footer_fixed": "layout-footer-fixed",
        "actions_sticky_top": "sticky-top",
    }

    for key, value in bool_map.items():
        if key in tweaks:
            tweaks[key] = value

    def classes(*args: str) -> str:
        return " ".join([tweaks.get(arg, "") for arg in args if arg]).strip()

    theme = tweaks["theme"]
    if theme not in THEMES:
        logger.warning("{} not found in {}, using default".format(theme, THEMES.keys()))
        theme = "default"

    dark_mode_theme = tweaks.get("dark_mode_theme", None)
    if dark_mode_theme and dark_mode_theme not in DARK_THEMES:
        logger.warning("{} is not a dark theme, using darkly".format(dark_mode_theme))
        dark_mode_theme = "darkly"

    return {
        "raw": raw_tweaks,
        "theme": {"name": theme, "src": static(THEMES[theme])},
        "dark_mode_theme": {"name": dark_mode_theme, "src": static(THEMES[theme])},
        "sidebar_classes": classes("sidebar", "sidebar_disable_expand"),
        "navbar_classes": classes("navbar", "no_navbar_border", "navbar_small_text"),
        "body_classes": classes(
            "accent", "body_small_text", "navbar_fixed", "footer_fixed", "sidebar_fixed", "layout_boxed",
        )
        + " theme-{}".format(theme),
        "actions_classes": classes("actions_sticky_top"),
        "sidebar_list_classes": classes(
            "sidebar_nav_small_text",
            "sidebar_nav_flat_style",
            "sidebar_nav_legacy_style",
            "sidebar_nav_child_indent",
            "sidebar_nav_compact_style",
        ),
        "brand_classes": classes("brand_small_text", "brand_colour"),
        "footer_classes": classes("footer_small_text"),
    }
