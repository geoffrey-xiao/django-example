from projects.models import Project, Tag
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from users.models import Profile


class BaseAPITest(APITestCase):
    user: User = None
    user2: User = None

    tag: Tag = None
    tag2: Tag = None

    owner: Profile = None
    owner2: Profile = None

    project: Project = None
    project2: Project = None

    def setUp(self):
        self.user, created = User.objects.get_or_create(
            id=10001,
            username='user1',
            email='user1@email.com'
        )

        self.tag = Tag.objects.create(
            id="a8082f41-7ced-4745-bdb7-22a788b8f71f",
            name='tag'
        )

        self.owner = Profile.objects.create(
            id="b8ca071c-c694-4010-a85d-4aa89cfddf22",
            name='user1',
            email='user1@email.com',
            username='user1',
            location='beijing',
            short_intro='intro',
            bio='bio',
            profile_image='profile_image',
            social_github='social_github',
            social_twitter='social_twitter',
            social_linkedin='social_linkedin',
            social_youtube='social_youtube',
            social_website='social_website',
            user=self.user)

        self.project = Project.objects.create(
            id='58af6f37-8e15-48d9-9727-89ab8f1d7a7a',
            title='project1',
            description='description',
            featured_image='featured_image',
            demo_link='demo_link',
            source_link='source_link',
            vote_total=0,
            vote_ratio=0,
            owner=self.owner
        )
