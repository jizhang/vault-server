from vault.services import user as user_svc


class TestUser:
    def test_get_password_digest(self):
        assert user_svc.get_password_digest('admin') == '132e92e991d94525638c1e5ffbf030eb'
