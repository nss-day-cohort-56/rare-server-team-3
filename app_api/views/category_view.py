from unicodedata import category
from app_api.models import Category
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for category
    """
    class Meta:
        model = Category
        fields = ('id', 'label')
        

class CategoryView(viewsets.ViewSet):
    """Rare category view
    """

    def list(self, request):
        """Handle GET requests to get all categories"""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """

        category = Category.objects.create(
            label=request.data["label"]
        )
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a category

        Returns:
        Response -- Empty body with 204 status code
        """

        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]

        category.organizer = category
        category.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)