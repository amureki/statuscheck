from click.testing import CliRunner

from statuscheck import cli


def test_cli_no_args():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 2


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.main, "github")
    assert result.exit_code == 0


def test_cli_all():
    runner = CliRunner()
    result = runner.invoke(cli.main, "all")
    assert result.exit_code == 0
