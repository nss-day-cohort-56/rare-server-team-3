from app_api.models import Author
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class AuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for category
    """
    class Meta:
        model = Author
        fields = ('author', 'bio', 'profile_image_url')
        depth = 1
        

class AuthorView(viewsets.ViewSet):
    """Rare category view
    """
    def retrieve(self, request, pk):
        """Handle GET requests for single author
        Returns:
            Response -- JSON serialized author
        """
        try:
            author = Author.objects.get(pk=pk)
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        except Author.DoesNotExist as ex:
            return Response({'NO COMMENT FOR YOU': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all author"""
        author = Author.objects.order_by('author__first_name')
        serializer = AuthorSerializer(author, many=True)
        return Response(serializer.data)


    # def update(self, request, pk):
    #     """Handle PUT requests for a category

    #     Returns:
    #     Response -- Empty body with 204 status code
    #     """

    #     category = Author.objects.get(pk=pk)
    #     category.label = request.data["label"]

    #     category.organizer = category
    #     category.save()

        # return Response(None, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk):
    #     """Handle DELETE requests for a category

    #     Returns:
    #     Response -- Empty body with 204 status code
    #     """
    #     category = Author.objects.get(pk=pk)
    #     category.delete()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)