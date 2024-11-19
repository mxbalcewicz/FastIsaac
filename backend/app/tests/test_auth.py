from faker import Faker
from passlib.context import CryptContext

from app.models.user_models import User


class TestAuth:

    class Endpoints:
        login = "auth/login"
        register = "auth/register"
        refresh_token = "auth/refresh-token"

    def _get_unique_register_data(self, db_session) -> dict:
        faker = Faker()
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        while True:
            email = faker.email()
            username = faker.user_name()
            password = faker.password(length=12)
            hashed_password = pwd_context.hash(password)

            db_user = db_session.query(User).filter(User.email == email, User.username == username).first()

            if not db_user:
                return {
                    "email": email,
                    "username": username,
                    "password": hashed_password,
                    "password_confirm": hashed_password,
                }

    def _create_new_user(self, email: str, username: str, password: str, db_session):
        new_user = User(email=email, username=username, password=password)
        db_session.add(new_user)
        db_session.commit()
        return new_user

    def test_register(self, client, db_session):
        register_data = self._get_unique_register_data(db_session=db_session)
        response = client.post(self.Endpoints.register, json=register_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_register__user_email_already_registered(self, client, db_session):
        faker = Faker()
        username = faker.user_name()
        email = faker.email()
        password = faker.password()

        new_user = self._create_new_user(email=email, username=username, password=password, db_session=db_session)

        response = client.post(
            self.Endpoints.register,
            json={
                "email": new_user.email,
                "username": new_user.username,
                "password": password,
                "password_confirm": password,
            },
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Email is already registered"

    def test_register__user_passwords_do_not_match(self, client, db_session):
        email = "testemail@mail.com"
        username = "testusername"
        password = "testpass1234"

        response = client.post(
            self.Endpoints.register,
            json={"email": email, "username": username, "password": password, "password_confirm": password + "123"},
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Passwords do not match"

    def test_login_user_success(self, client, db_session):
        email = "testmail@mail.com"
        username = "test_user"
        password = "test_password"
        new_user = self._create_new_user(email=email, username=username, password=password, db_session=db_session)

        response = client.post(
            self.Endpoints.login,
            json={"email": new_user.email, "password": password},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_user_wrong_credentials(self, client, db_session):
        email = "testmail2@mail.com"
        username = "test_user2"
        password = "test_password"

        # TODO: Correct test db sessions crosscontamination
        user = self._create_new_user(email=email, username=username, password=password, db_session=db_session)

        response = client.post(
            self.Endpoints.login,
            json={"email": user.email, "password": "wrong_password"},
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Wrong credentials."
