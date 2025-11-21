from rest_framework.views import APIView
from .renderers import UserRenderer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import (userRegistrationSerializer, userLoginSerializer, UserProfileSerializer,
                          changeUserPasswordSerializer, userPasswordResetEmailSerializer,
                        UserPasswordResetSerializer, StudentRegistrationSerializer)
# Create your views here.

#! Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class userRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = userRegistrationSerializer(data=request.data)

        if serializer.is_valid():
           user = serializer.save()
           token = get_tokens_for_user(user)
           return Response({'Msg':'The User Registration is Successfull', 'token':token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class  StudentRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    # def get(self, request):
    #     return Response({"message": "Send a POST request to register a student"})



    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)

        if serializer.is_valid():
           student = serializer.save()
           token = get_tokens_for_user(student.User)
           return Response({'Msg':'The Student Registration is Successfull', 'token':token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class userLoginView(APIView):
   renderer_classes = [UserRenderer]

   def post(self, request):
        serializer = userLoginSerializer(data=request.data)
      
        if serializer.is_valid():
            #? Using Validated_data for getting clean fields
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        # Runs when serializer.is_valid() is false
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
   
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class changeUserPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = changeUserPasswordSerializer(data=request.data, context={'user':request.user})

        if serializer.is_valid():
            serializer.save()
            return Response({'Msg': 'Password Changed Successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class userPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = userPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'Email': 'Password Reset Email Sent successfully!, Please Check your email.'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class userPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'Email': 'Password reset Successfull.'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)