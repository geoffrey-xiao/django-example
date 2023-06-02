from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    # reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    # def get_reviews(self, obj):
    #     reviews = obj.review_set.all()
    #     serializer = ReviewSerializer(reviews, many=True)
    #     return serializer.data


class MessageSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    message = serializers.CharField()

    def validate(self, attrs):
        if attrs['code'] != 0:
            raise serializers.ValidationError('A non field error')

        return attrs
