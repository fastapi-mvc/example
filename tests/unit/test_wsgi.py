import sys
import os

import mock
from fastapi_mvc_example.wsgi import run_wsgi


@mock.patch("fastapi_mvc_example.wsgi.ApplicationLoader")
def test_run_wsgi(loader_mock):
    run_wsgi("localhost", "5555", "2")
    loader_mock.assert_called_once()
    assert sys.argv == [
        "--gunicorn",
        "-c",
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../../fastapi_mvc_example/config/gunicorn.conf.py"
            )
        ),
        "-w",
        "2",
        "-b localhost:5555",
        "fastapi_mvc_example.app.asgi:application"
    ]
