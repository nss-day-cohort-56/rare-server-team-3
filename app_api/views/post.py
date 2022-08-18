"""View module for handling requests about games"""
from unicodedata import category
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Post, Author, Category

class PostView(ViewSet):
    """Group project post view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single post
        Returns:
            Response -- JSON serialized post
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, satus=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all posts
        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Post.objects.all()
        category = request.query_params.get('category', None)
        if category is not None:
            posts = posts.filter(category_id=category)
        author = request.query_params.get('author', None)
        if author is not None:
            posts = posts.filter(author_id=author)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized post instance
        """
        author = Author.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])
        post = Post.objects.create(
            title=request.data["title"],
            publication_date=request.data["publication_date"],
            category=category,
            content=request.data["content"],
            author=author,
            image_url=request.data["image_url"]
            
        )
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a post
        Returns:
            Response -- Empty body with 204 status code
        """
        author = Author.objects.get(author=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])
        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.content = request.data["content"]
        post.image_url = request.data["image_url"]
        category = category
        author = author
        post.save()
        post.post_tags.set(request.data["tags"])
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ('id','title', 'publication_date',
                'category', 'author', 'content', 'image_url','post_tags')
        depth = 2
