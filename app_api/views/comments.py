from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Comment, Post, Author

class CommentView(ViewSet):

    def create(self, request):
            """Handle POST operations
            Returns
                Response -- JSON serialized event instance
            """
            post = Post.objects.get(pk=request.data["post"])
            author = Author.objects.get(user=request.auth.user)

            comment = Comment.objects.create(
                post=post,
                author=author,
                subject=request.data["subject"],
                content=request.data["content"],
                datetime=request.data["datetime"],
            )
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Comment
        fields = ('id', 'post_id', 'author_id', 'subject', 'content', 'datetime')
        depth = 1