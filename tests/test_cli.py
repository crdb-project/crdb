from crdb.cli import main
import crdb


def test_main():
    main(["B/C"])


def test_version(capsys):
    try:
        main(["--version"])
    except SystemExit:
        pass
    c = capsys.readouterr()
    assert c.out == f"crdb-{crdb.__version__}\n"
