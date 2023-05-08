"""CRDB Python frontend."""

from importlib.metadata import version

from crdb.core import COMBINE
from crdb.core import ELEMENTS
from crdb.core import VALID_NAMES
from crdb.core import all
from crdb.core import bibliography
from crdb.core import clear_cache
from crdb.core import experiment_masks
from crdb.core import query
from crdb.core import reference_urls
from crdb.core import solar_system_composition

__all__ = (
    "__version__",
    "VALID_NAMES",
    "COMBINE",
    "ELEMENTS",
    "all",
    "bibliography",
    "clear_cache",
    "experiment_masks",
    "query",
    "reference_urls",
    "solar_system_composition",
)

__version__ = version("crdb")
