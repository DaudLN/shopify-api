import pytest
from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework import status


@pytest.mark.django_db
class TestCreateCollection:
    # @pytest.mark.skip
    def test_if_user_is_anony_return_403(self):
        # Arrange, Act, Assert (AAA)

        # Act
        client = APIClient()
        response: Response = client.post("api/store/collections/", dict(title="a"))

        # Act
        assert response.status_code == status.HTTP_403_FORBIDDEN
