from vault.services import UserService


class TestUser:
    def test_get_password_digest(self):
        assert UserService.get_password_digest('admin') == '132e92e991d94525638c1e5ffbf030eb'
