import json

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from library_api.serializers import ClientSerializer
from library_api.tests.factories.client import ClientFactory


class TestClient(TestCase):

    def setUp(self) -> None:
        self.length = 70
        self.clients = ClientFactory.create_batch(self.length)
        self.url_list = reverse('client-list')
        self.url_detail = 'client-detail'

    def test_integrity_url(self):
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_size(self):
        size = 10
        response = self.client.get(self.url_list, {'size': size})

        results = response.data.get('results', 0)

        self.assertEqual(len(results), size)

    def test_offset_10(self):
        offset = 10
        size = 10
        response = self.client.get(self.url_list, {'offset': offset, 'size': size, 'ordering': 'id'})

        data = response.data
        results = data.get('results', 0)

        self.assertEqual(len(results), 10)
        self.assertEqual(data.get('next').get('offset'), offset + size)
        self.assertEqual(data.get('previous').get('offset'), offset - size)

    def test_offset_20(self):
        offset = 20
        size = 10
        response = self.client.get(self.url_list, {'offset': offset, 'size': size, 'ordering': 'id'})

        data = response.data
        results = data.get('results', 0)

        self.assertEqual(len(results), 10)
        self.assertEqual(data.get('next').get('offset'), offset + size)
        self.assertEqual(data.get('previous').get('offset'), offset - size)

    def test_offset_last(self):
        size = 10
        offset = (len(self.clients) // size) * size
        response = self.client.get(self.url_list, {'offset': offset, 'size': size, 'ordering': 'id'})

        data = response.data

        self.assertEqual(data.get('next'), None)
        self.assertEqual(data.get('previous').get('offset'), offset - size)

    def test_get_all(self):
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(json.loads(response.content)["count"]), self.length)

    def test_get_only(self):
        client = self.clients[-1]
        url = reverse(self.url_detail, kwargs={'pk': client.pk})
        expected = ClientSerializer(client)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected.data)

    def test_get_only_not_found(self):
        url = reverse(self.url_detail, kwargs={'pk': self.length * 10})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_valid(self):
        client = ClientFactory.simple_generate(create=False)
        client.id = len(self.clients) + 1
        data = ClientSerializer(client).data
        response = self.client.post(self.url_list, data, format='json')
        response_verification = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(json.loads(response_verification.content)["count"]), self.length + 1)

    def test_post_invalid(self):
        invalid_data = {}
        response = self.client.post(self.url_list, invalid_data, format='json')
        response_verification = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(int(json.loads(response_verification.content)["count"]), self.length)

    def test_post_invalid_already_exists(self):
        client = self.clients[-1]
        data = ClientSerializer(client).data
        response = self.client.post(self.url_list, data, format='json')
        response_verification = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(int(json.loads(response_verification.content)["count"]), self.length)

    def test_update(self):
        client_setup = self.clients[-1]
        url = reverse(self.url_detail, kwargs={'pk': client_setup.pk})
        client = ClientFactory.simple_generate(create=False)
        client.id = client_setup.pk
        data = ClientSerializer(client).data

        response = self.client.patch(url, data, format='json', content_type='application/json')
        response_verify = self.client.get(url)
        instance_expected = response_verify.data.serializer.instance

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(instance_expected, client)

    def test_delete(self):
        client_setup = self.clients[-1]
        url = reverse(self.url_detail, kwargs={'pk': client_setup.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
