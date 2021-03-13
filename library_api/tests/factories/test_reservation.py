import json

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from library_api.tests.factories.book import BookFactory
from library_api.tests.factories.client import ClientFactory


class TestClient(TestCase):

    def setUp(self) -> None:
        self.length = 10
        self.clients = ClientFactory.create_batch(self.length)
        self.books = BookFactory.create_batch(self.length * 3)

        self.url_book_list = reverse('book-list')
        self.url_book_detail = 'book-detail'
        self.url_book_reserve = 'book-reserve'
        self.url_client_list = reverse('client-list')
        self.url_client_detail = 'client-detail'
        self.url_client_books = 'client-books'
        self.url_reservation_list = reverse('reservation-list')
        self.url_reservation_detail = 'reservation-detail'

    def test_integrity_urls(self):
        response_book = self.client.get(self.url_book_list)
        response_client = self.client.get(self.url_client_list)
        response_reservation = self.client.get(self.url_reservation_list)

        self.assertEqual(response_book.status_code, status.HTTP_200_OK)
        self.assertEqual(response_client.status_code, status.HTTP_200_OK)
        self.assertEqual(response_reservation.status_code, status.HTTP_200_OK)

    def test_size(self):
        self.reserve_factory()
        size = 2
        response = self.client.get(self.url_reservation_list, {'size': size})

        results = response.data.get('results', 0)

        self.assertEqual(len(results), size)

    def reserve_factory(self):
        books = BookFactory.create_batch(10)
        client = ClientFactory.create_batch(10)
        for pk, c in ((b.pk, c.pk) for c, b in zip(client, books)):
            url = reverse(self.url_book_reserve, kwargs={'pk': pk})
            data = {'client': c}
            response = self.client.post(path=url, data=data, format='json', content_type='application/json')
            assert response.status_code == status.HTTP_201_CREATED

    def test_offset_2(self):
        self.reserve_factory()
        offset = 2
        size = 2
        response = self.client.get(self.url_reservation_list, {'offset': offset, 'size': size, 'ordering': 'id'})

        data = response.data
        results = data.get('results', 0)

        self.assertEqual(len(results), size)
        self.assertEqual(data.get('next').get('offset'), offset + size)
        self.assertEqual(data.get('previous').get('offset'), offset - size)

    def test_offset_4(self):
        self.reserve_factory()
        offset = 4
        size = 2
        response = self.client.get(self.url_reservation_list, {'offset': offset, 'size': size, 'ordering': 'id'})

        data = response.data
        results = data.get('results', 0)

        self.assertEqual(len(results), size)
        self.assertEqual(data.get('next').get('offset'), offset + size)
        self.assertEqual(data.get('previous').get('offset'), offset - size)

    def test_offset_last(self):
        self.reserve_factory()
        size = 2
        offset = (len(self.clients) // size) * size
        response = self.client.get(self.url_reservation_list, {'offset': offset, 'size': size, 'ordering': 'id'})

        data = response.data

        self.assertEqual(data.get('next'), None)
        self.assertEqual(data.get('previous').get('offset'), offset - size)

    def test_get_all(self):
        self.reserve_factory()
        response = self.client.get(self.url_reservation_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(json.loads(response.content)["count"]), 10)

    # def test_get_only(self):
    #     client = self.clients[-1]
    #     url = reverse(self.url_detail, kwargs={'pk': client.pk})
    #     expected = ClientSerializer(client)
    #     response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, expected.data)
    #
    # def test_get_only_not_found(self):
    #     url = reverse(self.url_detail, kwargs={'pk': self.length * 10})
    #     response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #
    # def test_post_valid(self):
    #     client = ClientFactory.simple_generate(create=False)
    #     client.id = len(self.clients) + 1
    #     data = ClientSerializer(client).data
    #     response = self.client.post(self.url_list, data, format='json')
    #     response_verification = self.client.get(self.url_list)
    #
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(int(json.loads(response_verification.content)["count"]), self.length + 1)
    #
    # def test_post_invalid(self):
    #     invalid_data = {}
    #     response = self.client.post(self.url_list, invalid_data, format='json')
    #     response_verification = self.client.get(self.url_list)
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(int(json.loads(response_verification.content)["count"]), self.length)
    #
    # def test_post_invalid_already_exists(self):
    #     client = self.clients[-1]
    #     data = ClientSerializer(client).data
    #     response = self.client.post(self.url_list, data, format='json')
    #     response_verification = self.client.get(self.url_list)
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(int(json.loads(response_verification.content)["count"]), self.length)
    #
    # def test_update(self):
    #     client_setup = self.clients[-1]
    #     url = reverse(self.url_detail, kwargs={'pk': client_setup.pk})
    #     client = ClientFactory.simple_generate(create=False)
    #     client.id = client_setup.pk
    #     data = ClientSerializer(client).data
    #
    #     response = self.client.patch(url, data, format='json', content_type='application/json')
    #     response_verify = self.client.get(url)
    #     instance_expected = response_verify.data.serializer.instance
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(instance_expected, client)
    #
    # def test_delete(self):
    #     client_setup = self.clients[-1]
    #     url = reverse(self.url_detail, kwargs={'pk': client_setup.pk})
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
