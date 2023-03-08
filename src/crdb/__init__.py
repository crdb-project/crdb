from importlib.metadata import version

__version__ = version("crdb")

from ._lib import (
    query,
    clear_cache,
    experiment_masks,
    VALID_NAMES,
    reference_urls,
    bibliography,
    all,
)


__all__ = [
    "__version__",
    "VALID_NAMES",
    "query",
    "clear_cache",
    "experiment_masks",
    "reference_urls",
    "bibliography",
    "all",
]
