from example.config import settings


class TestReadyController:

    def test_should_return_ok(self, app_runner):
        # given
        settings.USE_REDIS = False

        # when
        response = app_runner.get("/api/ready")

        # then
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_should_return_not_found_when_invalid_uri(self, app_runner):
        # given / when
        response = app_runner.get("/api/ready/123")

        # then
        assert response.status_code == 404

    def test_should_return_bad_gateway_when_redis_unavailable(self, app_runner):
        # given
        settings.USE_REDIS = True

        # when
        response = app_runner.get("/api/ready")

        # then
        assert response.status_code == 502
        assert response.json() == {
            "error": {
                "code": 502,
                "message": "Could not connect to Redis",
                "status": "BAD_GATEWAY",
            }
        }
