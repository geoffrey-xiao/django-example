from pstats import Stats
from rest_framework import status
from rest_framework.test import APITestCase
from projects import models
from tests.factories import TagFactory


class TestTagAPI(APITestCase):
    def test_tag_filter(self):
        tag = models.Tag.objects.create(name='tag1')

        response = self.client.get('/api/tags/?name=tag1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_tag_list(self):
        tag = models.Tag.objects.create(
            name='tag2', id='1d02fe79-cda4-486d-ac3b-15feb4e08d99')

        obj = {
            'id': '1d02fe79-cda4-486d-ac3b-15feb4e08d99',
            'name': 'tag2'
        }

        response = self.client.get('/api/tags/')

        rs = dict(response.data['results'][0])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(rs.pop('created'))
        self.assertDictEqual(obj, rs)

    def test_tag_detail(self):
        tag = models.Tag.objects.create(
            name='tag3', id='1d02fe79-cda4-486d-ac3b-15feb4e08d66')

        obj = {
            'id': '1d02fe79-cda4-486d-ac3b-15feb4e08d66',
            'name': 'tag3'
        }

        response = self.client.get(
            '/api/tags/1d02fe79-cda4-486d-ac3b-15feb4e08d66/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.pop('created'))
        self.assertDictEqual(dict(response.data), obj)

    def test_tag_create(self):
        # tag = models.Tag.objects.create(
        #     name='tag3', id='1d02fe79-cda4-486d-ac3b-15feb4e08d55')

        obj = {
            'id': '1d02fe79-cda4-486d-ac3b-15feb4e08d55',
            'name': 'tag4'
        }

        before_count = models.Tag.objects.count()

        response = self.client.post('/api/tags/', obj, format='json')

        after_count = models.Tag.objects.count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(after_count-before_count, 1)

    def test_tag_update(self):
        obj = {
            # 'id': '1d02fe79-cda4-486d-ac3b-15feb4e08d15',
            'name': 'tag5'
        }

        response = self.client.post('/api/tags/', obj, format='json')

        rs = dict(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(rs.pop('created'))
        # self.assertTrue(rs.pop('id'))
        self.assertEqual(rs['name'], obj['name'])

        rs['name'] = 'tag6'
        url = f'/api/tags/{rs["id"]}/'
        response = self.client.put(url, rs, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'tag6')

    def test_tag_factory(self):
        tag = TagFactory.create(name='test_factory')
        response = self.client.get('/api/tags/?tag_name=test_factory')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
