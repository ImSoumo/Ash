import glob
import importlib
from Lena import LOGGER
from os.path import basename, dirname, isfile

def __list_all_modules():
    "Generates List Of Lena Modules !"
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f)
           and f.endswith(".py")
           and not f.endswith("__init__.py")
           and not f.endswith("__main__.py")
    ]

    return all_modules

LOGGER.info("Loading Plugins !")
importlib.import_module("Lena.Modules.__main__")
ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
