from app_api.models import Category
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for category
    """
    class Meta:
        model = Category
        fields = ('id', 'label')
        

class CategoryView(ViewSet):
    """Rare category view
    """

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