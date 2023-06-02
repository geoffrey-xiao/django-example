
from projects import models
from tests import BaseAPITest

from rest_framework import status


class TestProjectAPI(BaseAPITest):
    def test_project_filter(self):

        response = self.client.get('/api/project-list/?title=project1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data['results']), 1)

    def test_project_list(self):

        response = self.client.get('/api/project-list/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj = {
            "id": "58af6f37-8e15-48d9-9727-89ab8f1d7a7a",
            "owner": {
                "id": "b8ca071c-c694-4010-a85d-4aa89cfddf22",
                "name": "user1",
                "email": "user1@email.com",
                "username": "user1",
                "location": "beijing",
                "short_intro": "intro",
                "bio": "bio",
                # "profile_image": "http://127.0.0.1:8001/images/profiles/22437186.jpg",
                "social_github": 'social_github',
                "social_twitter": 'social_twitter',
                "social_linkedin": 'social_linkedin',
                "social_youtube": 'social_youtube',
                "social_website": 'social_website',
                # "created": "2021-06-17T14:54:05.016490Z",
                "user": 100002
            },
            "title": "project1",
            "description": "description",
            # "featured_image": "http://127.0.0.1:8001/images/codesniper.png",
            "demo_link": 'demo_link',
            "source_link": 'source_link',
            "vote_total": 0,
            "vote_ratio": 0,
            "tags": []
            # "created": "2021-06-16T17:14:49.166355Z"
        }

        rs = dict(response.data['results'][0])

        rs.pop('created')
        rs.pop('featured_image')

        rs.pop('owner')
        obj.pop('owner')

        # rs.owner.pop('profile_image')
        # rs.owner.pop('created')

        self.assertEqual(rs, obj)

    def test_project_detail(self):
        obj = {
            "id": "58af6f37-8e15-48d9-9727-89ab8f1d7a7a",
            "owner": {
                "id": "b8ca071c-c694-4010-a85d-4aa89cfddf22",
                "name": "user1",
                "email": "user1@email.com",
                "username": "user1",
                "location": "beijing",
                "short_intro": "intro",
                "bio": "bio",
                # "profile_image": "http://127.0.0.1:8001/images/profiles/22437186.jpg",
                "social_github": 'social_github',
                "social_twitter": 'social_twitter',
                "social_linkedin": 'social_linkedin',
                "social_youtube": 'social_youtube',
                "social_website": 'social_website',
                # "created": "2021-06-17T14:54:05.016490Z",
                "user": 100002
            },
            "title": "project1",
            "description": "description",
            # "featured_image": "http://127.0.0.1:8001/images/codesniper.png",
            "demo_link": 'demo_link',
            "source_link": 'source_link',
            "vote_total": 0,
            "vote_ratio": 0,
            "tags": []
            # "created": "2021-06-16T17:14:49.166355Z"
        }

        response = self.client.get(
            '/api/project-list/58af6f37-8e15-48d9-9727-89ab8f1d7a7a/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rs = dict(response.data)

        rs.pop('created')
        rs.pop('featured_image')

        rs.pop('owner')
        obj.pop('owner')
        self.assertEqual(rs, obj)

    def test_project_create(self):
        self.client.force_authenticate(user=self.user)
        obj = {
            "id": "58af6f37-8e15-48d9-9727-89ab8f1d7a6a",
            "owner": {
                "id": "b8ca071c-c694-4010-a85d-4aa89cfddf22",
                "name": "user1",
                "email": "user1@email.com",
                "username": "user1",
                "location": "beijing",
                "short_intro": "intro",
                "bio": "bio",
                # "profile_image": "http://127.0.0.1:8001/images/profiles/22437186.jpg",
                "social_github": 'social_github',
                "social_twitter": 'social_twitter',
                "social_linkedin": 'social_linkedin',
                "social_youtube": 'social_youtube',
                "social_website": 'social_website',
                # "created": "2021-06-17T14:54:05.016490Z",
                "user": self.user.id
            },
            "tags": [
                {
                    "id": "bf2a09d6-7b45-4727-aa97-531516ddaa21",
                    "name": "Django",
                    "created": "2021-06-15T15:40:43.128254Z"
                },
                {
                    "id": "e907a5fe-0dd0-4173-9c57-4125d4cada06",
                    "name": "JavaScript",
                    "created": "2021-06-15T15:40:51.963424Z"
                }
            ],
            "title": "project2",
            "description": "description",
            # "featured_image": "http://127.0.0.1:8001/images/codesniper.png",
            "demo_link": 'demo_link',
            "source_link": 'source_link',
            "vote_total": 0,
            "vote_ratio": 0,
            # "tags": []
            # "created": "2021-06-16T17:14:49.166355Z"
        }

        before_count = models.Project.objects.count()
        response = self.client.post('/api/project-list/', obj, format='json')

        after_count = models.Project.objects.count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(after_count-before_count, 1)

    def test_project_update(self):
        self.client.force_authenticate(user=self.user)
        obj = {
            "id": "58af6f37-8e15-48d9-9727-89ab8f1d7a6a",
            "owner": {
                "id": "b8ca071c-c694-4010-a85d-4aa89cfddf22",
                "name": "user1",
                "email": "user1@email.com",
                "username": "user1",
                "location": "beijing",
                "short_intro": "intro",
                "bio": "bio",
                # "profile_image": "http://127.0.0.1:8001/images/profiles/22437186.jpg",
                "social_github": 'social_github',
                "social_twitter": 'social_twitter',
                "social_linkedin": 'social_linkedin',
                "social_youtube": 'social_youtube',
                "social_website": 'social_website',
                # "created": "2021-06-17T14:54:05.016490Z",
                "user": self.user.id
            },
            "tags": [
                {
                    "id": "bf2a09d6-7b45-4727-aa97-531516ddaa21",
                    "name": "Django",
                    "created": "2021-06-15T15:40:43.128254Z"
                },
                {
                    "id": "e907a5fe-0dd0-4173-9c57-4125d4cada06",
                    "name": "JavaScript",
                    "created": "2021-06-15T15:40:51.963424Z"
                }
            ],
            "title": "project3",
            "description": "description",
            # "featured_image": "http://127.0.0.1:8001/images/codesniper.png",
            "demo_link": 'demo_link',
            "source_link": 'source_link',
            "vote_total": 0,
            "vote_ratio": 0,
            # "tags": []
            # "created": "2021-06-16T17:14:49.166355Z"
        }
        response = self.client.put(
            '/api/project-list/58af6f37-8e15-48d9-9727-89ab8f1d7a7a/', obj, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'project3')
