from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Property
from .serializers import PropertiesSerializer


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    properties = Property.objects.all()
    serializers = PropertiesSerializer(properties, many=True)

    return JsonResponse({
        'success': serializers.data
    })