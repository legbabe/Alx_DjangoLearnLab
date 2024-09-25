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

@api_view(['POST'])
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if not post:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if created:
        # Create a notification for the post author
        Notification.objects.create(
            recipient=post.author,  # Notify the post author
            actor=request.user,  # The user who liked the post
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.id
        )
        return Response({"message": "Post liked"}, status=status.HTTP_200_OK)
    
    return Response({"error": "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def unlike_post(request, post_id):
    try:
        like = Like.objects.get(post_id=post_id, user=request.user)
        like.delete()
        return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({"error": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_notifications(request):
    notifications = request.user.notifications.filter(unread=True).order_by('-timestamp')
    notifications_data = [
        {
            "actor": notification.actor.username,
            "verb": notification.verb,
            "timestamp": notification.timestamp,
            "target": str(notification.target),
            "unread": notification.unread,
        }
        for notification in notifications
    ]
    return Response({"notifications": notifications_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.mark_as_read()
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)    
