import os
import copy
from unittest import mock

import pytest
from example import ApplicationLoader
from example.cli.serve import serve

fake_pid_file = os.path.join(
    os.path.dirname(__file__), "test.pid",
)


class TestCliServeCommand:

    @pytest.fixture
    def patched_serve(self, asgi_app):
        cmd = copy.deepcopy(serve)
        wsgi_patch = mock.patch(
            "example.cli.serve.ApplicationLoader", spec=ApplicationLoader,
        )
        get_app_patch = mock.patch(
            "example.cli.serve.get_application", return_value=asgi_app,
        )
        cmd.wsgi_mock = wsgi_patch.start()
        cmd.get_app_mock = get_app_patch.start()
        yield cmd
        wsgi_patch.stop()
        get_app_patch.stop()
        del cmd

    def test_should_exit_zero_when_invoked_with_help(self, cli_runner):
        # given / when
        result = cli_runner.invoke(serve, ["--help"])

        # then
        assert result.exit_code == 0

    def test_should_exit_error_when_invoked_with_invalid_option(self, cli_runner):
        # given / when
        result = cli_runner.invoke(serve, ["--not_exists"])

        # then
        assert result.exit_code == 2

    @pytest.mark.parametrize(
        "args, expected",
        [
            (
                [],
                {},
            ),
            (
                ["--bind", "localhost:5000", "-w", 2],
                {
                    "bind": "localhost:5000",
                    "workers": 2,
                },
            ),
            (
                [
                    "--bind",
                    "localhost:5000",
                    "-w",
                    2,
                    "--daemon",
                    "--env",
                    "FOO=BAR",
                    "--env",
                    "USE_FORCE=True",
                    "--pid",
                    fake_pid_file,
                ],
                {
                    "bind": "localhost:5000",
                    "workers": 2,
                    "daemon": True,
                    "raw_env": ("FOO=BAR", "USE_FORCE=True"),
                    "pidfile": fake_pid_file,
                },
            ),
            (
                [
                    "--bind",
                    "localhost:5000",
                    "-w",
                    2,
                    "-D",
                    "-e",
                    "FOO=BAR",
                    "-e",
                    "USE_FORCE=True",
                    "--pid",
                    fake_pid_file,
                ],
                {
                    "bind": "localhost:5000",
                    "workers": 2,
                    "daemon": True,
                    "raw_env": ("FOO=BAR", "USE_FORCE=True"),
                    "pidfile": fake_pid_file,
                },
            ),
        ],
    )
    def test_should_create_wsgi_app_with_parsed_arguments(self, cli_runner, patched_serve, args, expected):
        # given / when
        result = cli_runner.invoke(patched_serve, args)

        # then
        assert result.exit_code == 0
        patched_serve.wsgi_mock.assert_called_once_with(
            application=patched_serve.get_app_mock.return_value,
            overrides=expected,
        )
        patched_serve.wsgi_mock.return_value.run.assert_called_once()

    def test_should_exit_error_when_invalid_pid_file_given(self, cli_runner):
        # given / when
        result = cli_runner.invoke(serve, ["--pid", "/path/does/not/exist"])

        # then
        assert result.exit_code == 2
