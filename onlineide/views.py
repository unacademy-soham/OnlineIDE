from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Submissions
from .serializers import SubmissionSerializer, UserSerializer
from .utils import create_code_file, execute_file
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
import multiprocessing as mp
from PIL import Image


def hello_world(request):
    return HttpResponse("Welcome to online ide")


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


@api_view(http_method_names=["POST"])
@permission_classes((permissions.AllowAny,))
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(UserSerializer(user).data, status=201)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data, status=200)


class SubmissionsViewSet(ModelViewSet):
    queryset = Submissions.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(user=request.user)
        return Response(self.get_serializer(queryset, many=True).data, status=200)

    def create(self, request, *args, **kwargs):
        request.data["status"] = "P"
        request.data["user"] = request.user.pk
        file_name = create_code_file(request.data.get("code"),
                                     request.data.get("language"))

        serializer = SubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()

        p = mp.Process(target=execute_file,
                    args=(file_name, request.data.get("language"), submission.pk))
        p.start()

        return Response({
            "message": "Submitted successfully"
        }, status=200)


@api_view(http_method_names=["POST"])
@permission_classes([permissions.AllowAny])
def create_thumbnail(request):
    file = request.FILES.get("file")
    print(file.content_type)
    image = Image.open(file)
    image = image.resize((30, 30))
    print(image)
    image.save('temp.jpg')
    return Response({
        "message": "Received"
    }, status=200)