from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Comment, Post, Author

class CommentView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single comment
        Returns:
            Response -- JSON serialized comment
        """
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'NO COMMENT FOR YOU': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all posts
        Returns:
            Response -- JSON serialized list of posts
        """
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


    def create(self, request):
            """Handle POST operations
            Returns
                Response -- JSON serialized event instance
            """
            post = Post.objects.get(pk=request.data["post_id"])
            author = Author.objects.get(author=request.auth.user)

            comment = Comment.objects.create(
                post=post,
                author=author,
                subject=request.data["subject"],
                content=request.data["content"],
            )
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a category

        Returns:
        Response -- Empty body with 204 status code
        """

        comment = Comment.objects.get(pk=pk)
        comment.subject = request.data["subject"]
        comment.content = request.data["content"]

        comment.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'subject', 'content', 'datetime')
        depth = 2