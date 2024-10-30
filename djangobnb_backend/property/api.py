from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import PropertyForm
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

@api_view(['POST', 'FILES'])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)

    if form.is_valid():
        property = form.save(commit=False)
        property.land_lord = request.user
        property.save()

        return JsonResponse({'success': True})
    else:
        print(form.errors, form.non_field_errors())

        return JsonResponse({'errors': form.errors.as_json()}, status= 400)