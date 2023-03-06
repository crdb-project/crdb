from crdb.cli import main


def test_main():
    main(["B/C"])


def test_version(capsys):
    main(["-v"])
