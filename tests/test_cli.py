import pytest
from click.testing import CliRunner

from statuscheck import cli


def test_command_line_interface_no_args():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 2


@pytest.mark.skip
def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main, 'github')
    assert result.exit_code == 0
