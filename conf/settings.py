from os.path import join
from stars_processing.filters_tools.base_filter import BaseFilter
from db_tier.base_query import LightCurvesDb

#TODO: Upgrade this module and make script for constructing these folders structure


#Level of verbosity (higher number means more info)
VERBOSITY = 0

OBJECT_SUFFIX = "pickle"
CONF_FILE_SEPARATOR = "="

#TODO: Add absolute path!
BASE_DIR = ".."

FILTERS_IMPL_PATH = join( BASE_DIR, "stars_processing", "filters_impl" )
DB_CONNECTORS = join( BASE_DIR, "db_tier", "connectors" )

TO_THE_DATA_FOLDER = join( BASE_DIR, "../data" )               #Path to the data folder
LC_FOLDER = join( TO_THE_DATA_FOLDER, "light_curves" )                                    #Name of folder of light curves

FILTERS_PATH = join( TO_THE_DATA_FOLDER, "star_filters" )       #Path to the folder of prepared filters

#
IMPLEMENTED_CLASSES = { "filters" : ( FILTERS_IMPL_PATH, BaseFilter ),
                        "connectors" : ( DB_CONNECTORS, LightCurvesDb ) }

STARS_PATH = {"stars" : join( LC_FOLDER, "some_stars" ),
              "quasars" : join( LC_FOLDER, "quasars" ),
              "eyer_quasars" : join( LC_FOLDER, "qso_eyer" ),
              "mqs_quasars" : join( LC_FOLDER, "mqs_quasars" ),
              "be_eyer" : join( LC_FOLDER, "be_eyer" ),
              "dpv" : join( LC_FOLDER, "dpv" ),
              "lpv" : join( LC_FOLDER, "lpv" ),
              "rr_lyr" : join( LC_FOLDER, "rr_lyr" ),
              "cepheids" : join( LC_FOLDER, "cepheids" ),
              }