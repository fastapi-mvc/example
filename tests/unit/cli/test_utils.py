import os
from unittest import mock

import pytest
from click import BadParameter
from example.cli.utils import validate_directory


class TestValidateDirectory:

    def test_should_return_original_value(self):
        # given / when
        path = os.path.dirname(__file__)
        result = validate_directory(
            mock.Mock(),
            mock.Mock(),
            path,
        )

        # then
        assert result == path

    def test_should_raise_when_path_not_exists(self):
        # given
        path = "/path/does/not/exist"

        # when / then
        with pytest.raises(BadParameter):
            validate_directory(
                mock.Mock(),
                mock.Mock(),
                path,
            )

    def test_should_raise_when_path_not_writable(self):
        # given
        path = "/etc"

        # when / then
        with pytest.raises(BadParameter):
            validate_directory(
                mock.Mock(),
                mock.Mock(),
                path,
            )
