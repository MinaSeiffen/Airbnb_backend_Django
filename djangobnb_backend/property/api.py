from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import PropertyForm
from .models import Property, Reservation
from .serializers import PropertiesSerializer, PropertiesDetailSerializer, ReservationListSerializer
from useraccount.models import User
from rest_framework_simplejwt.tokens import AccessToken

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    # Auth
    try:
        token = request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
        token = AccessToken(token)
        user_id = token.payload['user_id']
        user = User.objects.get(id = user_id)
    except Exception as e:
        user = None

    favourites = []
    properties = Property.objects.all()

    # filtering properties by landlord if exists
    land_lord_id = request.GET.get('land_lord_id', '')
    is_favourite = request.GET.get('is_favourite', '')

    if land_lord_id:
        properties = properties.filter(land_lord_id = land_lord_id)

    if is_favourite and user:
        properties = properties.filter(favourited__in= [user])

    # Favourite
    if user:
        for property in properties:
            if user in property.favourited.all():
                favourites.append(property.id)


    serializers = PropertiesSerializer(properties, many=True)

    return JsonResponse({
        'success': {
            'all_properties': serializers.data,
            'favourites': favourites
        }
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

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_detail(request, pk):
    property = Property.objects.get(id=pk)

    serializers = PropertiesDetailSerializer(property, many=False)

    return JsonResponse({
        'success': serializers.data
    })


@api_view(['POST'])
def book_property(request, pk):
    try:
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        number_of_nights = request.POST.get('number_of_nights', '')
        total_price = request.POST.get('total_price', '')
        guests = request.POST.get('guests', '')

        property = Property.objects.get(id = pk)

        Reservation.objects.create(
            property = property,
            start_date = start_date,
            end_date = end_date,
            number_of_nights = number_of_nights,
            total_price = total_price,
            guests = guests,
            created_by = request.user
        )

        return JsonResponse({'success': True})

    except Exception as e:
        print("Error", e)

        return JsonResponse({'errors': True})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
    property = Property.objects.get(id=pk)
    reservations = property.reservations.all()

    serializers = ReservationListSerializer(reservations, many=True)

    return JsonResponse({'success' : serializers.data}, safe= False)


@api_view(['POST'])
def toggle_favourite (request, pk):
    property = Property.objects.get(id= pk)

    # Checking if user is authenticated
    if request.user is None:
        return JsonResponse({'error': 'Please, Login First'})

    if request.user in property.favourited.all():
        property.favourited.remove(request.user)
        return JsonResponse({'success': {'is_favourite': False}})
    else:
        property.favourited.add(request.user)
        return JsonResponse({'success': {'is_favourite': True}})