from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import UserSerializer

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            data = request.data
            name = data['name']
            email = data['email']
            email = email.lower()
            password = data['password']
            re_password = data['re_password']
            is_realtor = data['is_realtor']
            print(data)

            if is_realtor == 'True':
                is_realtor = True
            else:
                is_realtor = False


            if password == re_password:
                if len(password) >= 8:
                    print(User.objects.all())

                    if not User.objects.filter(email=email).exists():
                        if not is_realtor:
                            User.objects.create_user(name=name, email=email, password=password)
                            return Response({'success': 'User created successfully.'},
                                            status=status.HTTP_201_CREATED)
                        else:
                            User.objects.create_realtor(name=name, email=email, password=password)
                            return Response({'success': 'Realtor created successfully.'},
                                            status=status.HTTP_201_CREATED)

                    else:
                        return Response(
                            {'Error': 'This email already existed.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'Error': 'Password must have at least 8 characters.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'Error': 'Password does not match.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except:
            return Response(
                {'Error': 'Error in Registerview'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RetrieveUserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            print('request.user', user)
            user = UserSerializer(user)
            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                {'Error': 'Error in RetrieveUserView'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)