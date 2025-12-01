from rest_framework.views import APIView
from .renderers import UserRenderer
from rest_framework.response import Response
from rest_framework import status
from core.models import Teacher, Student
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from .serializers import (userRegistrationSerializer, userLoginSerializer, UserProfileSerializer,
                            changeUserPasswordSerializer, userPasswordResetEmailSerializer,
                            UserPasswordResetSerializer, StudentRegistrationSerializer,
                            teacherRegistrationSerializer, TeacherProfileSerializer,
                            StudentProfileSerializer)
from account.permissions import IsTeacher, IsStudent, IsAdmin

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

    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)

        if serializer.is_valid():
           student = serializer.save()
           token = get_tokens_for_user(student.user)
           return Response({
            'Msg': 'The Student Registration is Successful',
            'student_id': student.id,         # FIXED
            'user_id': student.user.id,
            'token': token
          }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class teacherRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = teacherRegistrationSerializer(data=request.data)

        if serializer.is_valid():
           teacher = serializer.save()
           token = get_tokens_for_user(teacher.user)
           return Response({
                'Msg': 'The Teacher Registration is Successful',
                'teacher_id': teacher.id,       # FIXED
                'user_id': teacher.user.id,
                'token': token
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#! User Login View
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
                role = user.role
                student_or_teacher_id = None
                context = {}
                if role == 'teacher':
                    try:
                        teacher = Teacher.objects.get(user=user)
                        student_or_teacher_id = teacher.id
                        empCode_RollNo = teacher.employee_code
                        context = {'role': 'teacher',
                                    'id': student_or_teacher_id, 
                                    'empCode_RollNo':empCode_RollNo
                                    }
                    except Teacher.DoesNotExist:
                        return Response({'errors':{'non_field_errors':['Teacher profile not found']}}, status=status.HTTP_404_NOT_FOUND)
                elif role == 'student':
                    try:
                        student = Student.objects.get(user=user)
                        student_or_teacher_id = student.id
                        empCode_RollNo = student.roll_number
                        context = {'role': 'student', 
                                   'id': student_or_teacher_id, 
                                   'empCode_RollNo':empCode_RollNo
                                    }
                    except Student.DoesNotExist:
                        return Response({'errors':{'non_field_errors':['Student profile not found']}}, status=status.HTTP_404_NOT_FOUND)
                token = get_tokens_for_user(user)
                
                return Response({'user_id': user.id,'user_name': user.name,'context': context ,'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        # Runs when serializer.is_valid() is false
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
   
# ! User Logout View
class userLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'msg':'User Logged out Successfully', 'logout':True}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'errors':{'non_field_errors':['Invalid refresh token']}}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TeacherProfileView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    renderer_classes = [UserRenderer]

    def get(self, request):
        try:
            teacher = Teacher.objects.select_related("user", "department").get(user=request.user)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherProfileSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    renderer_classes = [UserRenderer]

    def get(self, request):
        try:
            student = Student.objects.select_related("user").get(user=request.user)
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentProfileSerializer(student)
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
    
class send_attendance_emailView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    renderer_classes = [UserRenderer]

    def post(self, request):
        # Logic to send attendance email
        # This is a placeholder for the actual implementation
        return Response({'Msg': 'Attendance email sent successfully.'}, status=status.HTTP_200_OK)