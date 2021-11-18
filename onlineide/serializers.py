from rest_framework import serializers
from .models import User, Submissions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissions
        fields = "__all__"
