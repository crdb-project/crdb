"""
Command line interface for CRDB.
"""
import argparse
from crdb._lib import _url, _server_request
import inspect

parser = argparse.ArgumentParser(description=__doc__)

for name, par in inspect.signature(_url).parameters.items():
    if par.default is inspect.Parameter.empty:
        parser.add_argument(name, type=par.annotation)
    else:
        parser.add_argument(f"--{name}", type=par.annotation, default=par.default)

parser.add_argument("--timeout", type=int, default=120)


def main(args=None):
    args = parser.parse_args(args=args)
    kwargs = vars(args)
    timeout = kwargs['timeout']
    del kwargs["timeout"]
    url = _url(**kwargs)
    data = _server_request(url, timeout=timeout)
    print("\n".join(data))
