from .serializers import UserDetailSerializer
from .models import User
from django.http import JsonResponse
from property.serializers import ReservationListSerializer

from rest_framework.decorators import api_view, authentication_classes, permission_classes


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_landlord(request, pk):
    user = User.objects.get(id = pk)
    if user or user is not None:
        serializers = UserDetailSerializer(user, many=False)

        return JsonResponse({'success' : serializers.data}, safe= False)
    else:
        return JsonResponse({'errors' : "User not found"}, safe= False)

@api_view(['GET'])
def reservation_list(request):
    reservations = request.user.reservations.all()

    if reservations is not None:
        serializers = ReservationListSerializer(reservations, many=True)
        return JsonResponse({'success': serializers.data}, safe= False)
    else:
        return JsonResponse({'errors': "No Reservations found"}, safe= False)