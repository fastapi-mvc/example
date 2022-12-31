import pytest
from example.cli import cli


class TestCliRoot:

    def test_should_exit_zero_when_invoked_empty(self, cli_runner):
        # given / when
        result = cli_runner.invoke(cli)

        # then
        assert result.exit_code == 0

    def test_should_exit_zero_when_invoked_with_help(self, cli_runner):
        # given / when
        result = cli_runner.invoke(cli, ["--help"])

        # then
        assert result.exit_code == 0

    def test_should_exit_error_when_invoked_with_invalid_option(self, cli_runner):
        # given / when
        result = cli_runner.invoke(cli, ["--not_exists"])

        # then
        assert result.exit_code == 2

    @pytest.mark.parametrize("args", [
        ["serve", "--help"],
        ["--verbose", "serve", "--help"]
    ])
    def test_should_exit_zero_when_invoked_with_options(self, cli_runner, args):
        # given / when
        result = cli_runner.invoke(cli, args)

        # then
        assert result.exit_code == 0
