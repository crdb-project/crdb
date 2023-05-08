"""Command line interface for CRDB."""
import argparse
import inspect
import re
import sys
import traceback

import crdb
from crdb.core import _server_request
from crdb.core import _url
from crdb.core import query
from typing import Optional, List


def main(args: Optional[List[str]] = None) -> None:
    """
    Command line interface for CRDB.

    Returns unprocessed DB output to stdout.
    """
    parser = argparse.ArgumentParser(description=main.__doc__)

    assert isinstance(query.__doc__, str)
    descriptions = {
        k: re.sub(r"\s+", " ", v.strip())
        for (k, v) in re.findall(
            r"^ {4}([a-z_]+): *[a-z, ]+\n((?: {8}.+\n)+)", query.__doc__, re.MULTILINE
        )
    }
    descriptions["format"] = (
        "Output format; one of 'usine', 'galprop', 'csv', 'csv-asimport'. "
        "Default is 'csv-asimport'."
    )

    for name, par in inspect.signature(_url).parameters.items():
        name2 = name.replace("_", "-")
        h = descriptions.get(name, "").replace("%", "%%")
        tp = par.annotation
        if isinstance(tp, str):
            tp = eval(tp)
        kwargs = {
            "type": tp,
            "help": h,
        }
        if par.default is not inspect.Parameter.empty:
            kwargs["default"] = par.default
        parser.add_argument(f"--{name2}" if "default" in kwargs else name2, **kwargs)

    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Timeout for server request in seconds. Default is 120.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"crdb-{crdb.__version__}",
        help="Print version of crdb Python library.",
    )

    args = parser.parse_args(args=args)
    kwargs = {k.replace("-", "_"): v for (k, v) in vars(args).items() if k != "timeout"}
    try:
        url = _url(**kwargs)
    except ValueError as e:
        sys.stderr.write("".join(traceback.format_exception_only(e)))  # type:ignore
        sys.exit(1)
    data = _server_request(url, timeout=args.timeout)
    print("\n".join(data))
