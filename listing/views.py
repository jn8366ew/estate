from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import ListingSerializer
from django.contrib.postgres.search import SearchVector, SearchQuery

from .models import Listing


# only for realtor users
class ManageListingView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'error': 'This user has no permission to get data.'},
                                status=status.HTTP_403_FORBIDDEN)

            slug = request.query_params.get('slug')

            if not slug:
                listing = Listing.objects.order_by('-date_created').filter(
                    realtor=user.email
                )
                listing = ListingSerializer(listing, many=True)


                return Response(
                    {'listings': listing.data},
                    status=status.HTTP_200_OK
                )

            if not Listing.objects.order_by('-date_created').filter(
                realtor=user.email,
                slug=slug
            ).exists():
                return Response(
                    {'alert': 'Listing not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            listing = Listing.objects.get(realtor=user.email, slug=slug)
            listing = ListingSerializer(listing)

            print(listing)
            print(listing.data)

            return Response(
                {'listing': listing.data},
                status=status.HTTP_200_OK
            )

        except:
            return Response({'Error': 'Error at Get in ManageListingView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve_values(self, data):
        title = data['title']
        slug = data['slug']
        address = data['address']
        city = data['city']
        state = data['state']
        zipcode = data['zipcode']
        description = data['description']
        price = data['price']

        try:
            price = int(price)

        except:
            return Response({'error': 'Price must be an integer'},
                            status=status.HTTP_400_BAD_REQUEST)

        bedrooms = data['bedrooms']
        try:
            bedrooms = int(bedrooms)

        except:
            return Response({'error': 'Bedrooms must be an integer'},
                            status=status.HTTP_400_BAD_REQUEST)

        bathrooms = data['bathrooms']
        try:
            bathrooms = float(bathrooms)

        except:
            return Response({'error': 'Bathrooms must be an float'},
                            status=status.HTTP_400_BAD_REQUEST)

        if bathrooms <= 0 or bathrooms >= 10:
            bathrooms = 1.0

        bathrooms = round(bathrooms, 1)

        sale_type = data['sale_type']
        if sale_type == 'FOR_SALE':
            sale_type = 'For Rent'
        else:
            sale_type = 'For Sale'

        home_type = data['home_type']
        if home_type == 'CONDO':
            home_type = 'Condo'
        elif home_type == 'APARTMENT':
            home_type = 'Apartment'
        else:
            home_type = 'House'

        main_photo = data['main_photo']
        photo_1 = data['photo_1']
        photo_2 = data['photo_2']
        photo_3 = data['photo_3']
        is_published = data['is_published']

        if is_published == True:
            is_published = True
        else:
            is_published = False

        data = {
            'title': title,
            'slug': slug,
            'address': address,
            'city': city,
            'state': state,
            'zipcode': zipcode,
            'description': description,
            'price': price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'sale_type': sale_type,
            'home_type': home_type,
            'main_photo': main_photo,
            'photo_1': photo_1,
            'photo_2': photo_2,
            'photo_3': photo_3,
            'is_published': is_published
        }

        return data

    def post(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'error': 'This user has no permission to request.'},
                                status=status.HTTP_403_FORBIDDEN)
            data = request.data

            self.retrieve_values(data)

            title = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published = data['is_published']

            # Check whether slug is unique or not
            if Listing.objects.filter(slug=slug).exists():
                return Response({'error': 'Listing with this slug already existed.'},
                                status=status.HTTP_400_BAD_REQUEST)

            Listing.objects.create(
                realtor = user.email,
                title = title,
                slug = slug,
                address = address,
                city = city,
                state = state,
                zipcode= zipcode,
                description = description,
                price = price,
                bedrooms = bedrooms,
                bathrooms = bathrooms,
                sale_type = sale_type,
                home_type = home_type,
                main_photo = main_photo,
                photo_1 = photo_1,
                photo_2 = photo_2,
                photo_3 = photo_3,
                is_published = is_published,
            )

            return Response(
                {'success': 'Listing created successfully.'},
                status=status.HTTP_201_CREATED
            )

        except:
            return Response({'error':'Error at Post in ManageListingView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'This user has no permission to update data.'},
                    status=status.HTTP_403_FORBIDDEN)

            data = request.data

            self.retrieve_values(data)

            title = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published = data['is_published']

            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({'error': 'Data of this relator with a slug does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

            Listing.objects.filter(realtor=user.email, slug=slug).update(
                realtor=user.email,
                title=title,
                slug=slug,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                description=description,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                sale_type=sale_type,
                home_type=home_type,
                main_photo=main_photo,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                is_published=is_published,
            )
            return Response({'success': 'Listing updated successfully'},
                            status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Error at put in ManageListingView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response(
                    {'error': 'This user has no permission to patch data.'},
                    status=status.HTTP_403_FORBIDDEN)

            data = request.data

            slug = data['slug']
            is_published = data['is_published']

            if is_published == 'True':
                is_published = True
            else:
                is_published = False

            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({"Data of this relator with a slug does not exist."},
                                status=status.HTTP_404_NOT_FOUND)

            Listing.objects.filter(realtor=user.email, slug=slug).update(
                is_published = is_published
            )
            return Response({'success': 'Updated listing publish status successfully'},
                            status=status.HTTP_200_OK)

        except:
            return Response({'error': 'Error at patch in ManageListingView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'This user has no permission to delete data.'},
                    status=status.HTTP_403_FORBIDDEN)

            data = request.data
            try:
                slug = data['slug']
            except:
                return Response(
                    {'error': 'Slug must be provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({'error': 'Data of this relator with a slug does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

            Listing.objects.filter(realtor=user.email, slug=slug).delete()

            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({'success': 'Deleted data successfully.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed deleting data.'},
                                status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error': 'Error during deleting data in ManageListingView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# for all users
class ListingDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = request.query_params.get('slug')

            if not slug:
                return Response({'error':'Must provide slug'},
                                status=status.HTTP_400_BAD_REQUEST)

            if not Listing.objects.filter(slug=slug, is_published=True).exists():
                return Response({'alert':'Could not find any published data with a slug'},
                                status=status.HTTP_404_NOT_FOUND)

            listing = Listing.objects.get(slug=slug, is_published=True)
            listing = ListingSerializer(listing)

            print(type(listing))
            print(type(listing.data))

            return Response({'listing': listing.data},
                            status=status.HTTP_200_OK)



        except:
            return Response({'error':'Error in ListingDetailView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListingView(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            if not Listing.objects.filter(is_published=True).exists():
                return Response({'alert':'Could not find any published data'},
                                status=status.HTTP_404_NOT_FOUND)

            listings = Listing.objects.order_by('-date_created').filter(is_published=True)
            listings = ListingSerializer(listings, many=True)
            return Response({'listings': listings.data},
                            status=status.HTTP_200_OK)


        except:
            return Response({'error': 'Error in ListingView'},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Only search data that is_published is true.
class SearchListingView(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        try:
            city = request.query_params.get('city')
            state = request.query_params.get('state')
            max_price = request.query_params.get('max_price')
            try:
                max_price = int(max_price)
            except:
                return Response(
                    {'error': 'Max price must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            bedrooms = request.query_params.get('bedrooms')
            try:
                bedrooms = int(bedrooms)
            except:
                return Response(
                    {'error': 'Bedrooms must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            bathrooms = request.query_params.get('bathrooms')
            try:
                bathrooms = float(bathrooms)
            except:
                return Response(
                    {'error': 'Bathrooms must be float'},
                    status=status.HTTP_400_BAD_REQUEST)

            if bathrooms < 0 or bathrooms >= 10:
                bathrooms = 1.0
            bathrooms = round(bathrooms, 1)

            sale_type = request.query_params.get('sale_type')
            if sale_type == 'FOR_SALE':
                sale_type = 'For Sale'
            else:
                sale_type = 'For Rent'

            home_type = request.query_params.get('home_type')
            if home_type == 'HOUSE':
                home_type = 'House'
            elif home_type == 'CONDO':
                home_type = 'Condo'
            else:
                home_type = 'Apartment'

            search = request.query_params.get('search')
            if not search:
                return Response({'error': 'Search criteria is required'})
            vector = SearchVector('title', 'description')
            query = SearchQuery(search)

            if not Listing.objects.annotate(search=vector).filter(
                search=query,
                city=city,
                state=state,
                price__lte=max_price,
                bedrooms__gte=bedrooms,
                bathrooms__gte=bathrooms,
                sale_type=sale_type,
                home_type=home_type,
                is_published=True).exists():
                return Response({'error': 'No data with criteria'},
                                status=status.HTTP_404_NOT_FOUND)

            listings = Listing.objects.annotate(search=vector).filter(
                        search=query,
                        city=city,
                        state=state,
                        price__lte=max_price,
                        bedrooms__gte=bedrooms,
                        bathrooms__gte=bathrooms,
                        sale_type=sale_type,
                        home_type=home_type,
                        is_published=True)

            listings = ListingSerializer(listings, many=True)

            return Response({'listings': listings.data},
                            status=status.HTTP_200_OK)

            """
            listings = Listing.objects.filter(
                    title__search=search,
                    description__search=search,
                    is_published=True
                )
            이 코드로는 쿼리셋이 반환이 안된다. 

            """




        except:
            return Response({'error': 'Error in SearchListingView'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

