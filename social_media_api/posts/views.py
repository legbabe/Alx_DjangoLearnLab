from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Notification
from .models import Post, Like
from django.contrib.contenttypes.models import ContentType


def user_feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You can only edit your own posts.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You can only edit your own comments.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete()

