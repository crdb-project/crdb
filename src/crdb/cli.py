import argparse
import crdb
from crdb._lib import _url, _server_request, query
import inspect
import re


def main(args=None):
    """
    Command line interface for CRDB.

    Returns unprocessed DB output to stdout.
    """
    parser = argparse.ArgumentParser(description=main.__doc__)

    descriptions = {
        k: re.sub(r"\s+", " ", v.strip())
        for (k, v) in re.findall(
            r"^ {4}([a-z_]+): *[a-z, ]+\n((?: {8}.+\n)+)", query.__doc__, re.MULTILINE
        )
    }

    for name, par in inspect.signature(_url).parameters.items():
        name2 = name.replace("_", "-")
        h = descriptions.get(name, "").replace("%", "%%")
        tp = par.annotation
        if isinstance(tp, str):
            tp = eval(tp)
        if par.default is inspect.Parameter.empty:
            parser.add_argument(name2, type=tp, help=h)
        else:
            parser.add_argument(f"--{name2}", type=tp, default=par.default, help=h)

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
    url = _url(**kwargs)
    data = _server_request(url, timeout=args.timeout)
    print("\n".join(data))
