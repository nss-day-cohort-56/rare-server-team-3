"""View module for handling requests about tags"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Tag


class TagView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_type = Tag.objects.get(pk=pk)
            serializer = TagSerializer(game_type)
            return Response(serializer.data)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        tag = Tag.objects.create(
            label=request.data["label"]
        )
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """

        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]
        
        tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
# Adding for list delete Tag PR! Will delete after. Please check on client to see that tags are deletable!

    def destroy(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Tag
        fields = ('id', 'label')

