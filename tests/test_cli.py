from crdb.cli import main
import crdb
import re


def test_main():
    main(["B/C"])


def test_version(capsys):
    try:
        main(["--version"])
    except SystemExit:
        pass
    c = capsys.readouterr()
    m = re.match(r"crdb-([0-9]+\.[0-9]+\.[0-9]+)", c.out)
    assert m
    assert m.group(1) == crdb.__version__
