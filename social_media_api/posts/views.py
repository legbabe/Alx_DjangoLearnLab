from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType



@api_view(['GET', 'POST'])  # Example, adjust to your method type
@permission_classes([IsAuthenticated])
def some_view(request, pk):
    post = get_object_or_404(Post, pk=pk)  
    return Response(PostSerializer(post).data)


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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response({"error": "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a notification
    Notification.objects.create(
        recipient=post.author,
        actor=request.user,
        verb="liked your post",
        target=post,
        target_content_type=ContentType.objects.get_for_model(Post),
        target_object_id=post.id
    )

    return Response({"message": "Post liked"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post,  pk=pk)
    like = Like.objects.filter(user=request.user, post=post).first()

    if not like:
        return Response({"error": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)

    like.delete()
    return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)