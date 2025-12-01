from rest_framework import serializers
from account.models import User
# from core.models import Student, Course, Semester
from core.models import Student, Course, Teacher
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from account.utils import Util
import os


class userRegistrationSerializer(serializers.ModelSerializer):
    password2= serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']

        if attrs['role']=='Admin' or attrs['role']=='admin':
            raise serializers.ValidationError('Role: The Role You entered is Invalid')

        if password!=password2:
            raise serializers.ValidationError('Password: The Password does not Match')
        
        return attrs
    
    #! You have to write this if you have created your own custom-User Model
    def create(self, validated_data):
       validated_data.pop('password2')
       return User.objects.create_user(**validated_data)


class StudentRegistrationSerializer(serializers.Serializer):
    # User fields
    email = serializers.EmailField()
    name = serializers.CharField()
    gender = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    role = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    # Student fields
    roll_number = serializers.CharField()
    phone_number = serializers.CharField(required=False)
    course_id = serializers.IntegerField()
    current_semester = serializers.IntegerField(required=False, allow_null=True)
    year_of_study = serializers.IntegerField(required=False)

    # ---------------------------
    # FIELD-LEVEL VALIDATIONS
    # ---------------------------

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_roll_number(self, value):
        if Student.objects.filter(roll_number=value).exists():
            raise serializers.ValidationError("This roll number is already taken.")
        return value

    # ---------------------------
    # GLOBAL VALIDATION (your logic added here)
    # ---------------------------
    def validate(self, attrs):

        password = attrs.get('password')
        password2 = attrs.get('password2')

        # Check Role
        if attrs.get('role').lower() == 'admin':
            raise serializers.ValidationError(
                {"role": "The role you entered is invalid for student registration."}
            )

        if attrs.get('role').lower() != 'student':
            raise serializers.ValidationError(
                {"role": "The role you entered is invalid for student registration."}
            )


        # Passwords must match
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        # Check if course exists
        if not Course.objects.filter(id=attrs['course_id']).exists():
            raise serializers.ValidationError({"course_id": "Invalid course id."})

        # Check if semester exists (if provided)
        # sem_id = attrs.get('current_semester_id')
        # if sem_id is not None and not Semester.objects.filter(id=sem_id).exists():
        #     raise serializers.ValidationError({"current_semester_id": "Invalid semester id."})

        return attrs

    # ---------------------------
    # CREATE METHOD
    # ---------------------------
    def create(self, validated_data):
        # Remove password2 before saving
        validated_data.pop('password2')

        # Extract student fields
        roll_number = validated_data.pop('roll_number')
        phone_number = validated_data.pop('phone_number', None)
        course_id = validated_data.pop('course_id')
        current_semester = validated_data.pop('current_semester', None)
        year_of_study = validated_data.pop('year_of_study', None)

        try:
            with transaction.atomic():

                # Create User
                user = User.objects.create_user(
                    email=validated_data['email'],
                    name=validated_data['name'],
                    gender=validated_data.get('gender'),
                    role=validated_data['role'],
                    password=validated_data['password']
                )

                # Create Student
                student = Student.objects.create(
                    user=user,
                    roll_number=roll_number,
                    phone_number=phone_number,
                    course_id=course_id,
                    current_semester=current_semester,
                    year_of_study=year_of_study
                )

                return student

        except Exception as e:
            # Optional: Raise a custom error
            raise serializers.ValidationError({"error": str(e)})


class teacherRegistrationSerializer(serializers.Serializer):
   # User fields
    email = serializers.EmailField()
    name = serializers.CharField()
    gender = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    role = serializers.CharField(default='teacher')
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    # Student fields
    employee_code = serializers.CharField()
    phone_number = serializers.IntegerField(required=False)
    department = serializers.IntegerField()
    designation = serializers.CharField(required=False, allow_null=True)
    joining_date = serializers.DateField(required=False)

    # ---------------------------
    # FIELD-LEVEL VALIDATIONS
    # ---------------------------

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_employee_code(self, value):
        if Teacher.objects.filter(employee_code=value).exists():
            raise serializers.ValidationError("This Employee Code is already taken.")
        return value

    # ---------------------------
    # GLOBAL VALIDATION (your logic added here)
    # ---------------------------
    def validate(self, attrs):

        password = attrs.get('password')
        password2 = attrs.get('password2')

        # Check Role
        if attrs.get('role').lower() == 'admin':
            raise serializers.ValidationError(
                {"role": "The role you entered is invalid for teacher registration."}
            )

        if attrs.get('role').lower() != 'teacher':
            raise serializers.ValidationError(
                {"role": "The role you entered is invalid for teacher registration."}
            )


        # Passwords must match
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        return attrs

    # ---------------------------
    # CREATE METHOD
    # ---------------------------
    def create(self, validated_data):

        # Remove password2 before saving
        validated_data.pop('password2')

        # Extract Teacher fields

        employee_code = validated_data.pop('employee_code')
        phone_number = validated_data.pop('phone_number', None)
        department_id = validated_data.pop('department')
        designation = validated_data.pop('designation', None)
        joining_date = validated_data.pop('joining_date', None)

        try:
            with transaction.atomic():

                # Create User
                user = User.objects.create_user(
                    email=validated_data['email'],
                    name=validated_data['name'],
                    gender=validated_data.get('gender'),
                    role=validated_data['role'],
                    password=validated_data['password']
                )

                # Create Student
                teacher = Teacher.objects.create(
                    user=user,
                    employee_code=employee_code,
                    phone_number=phone_number,
                    department_id=department_id,
                    designation=designation,
                    joining_date=joining_date
                )

                return teacher

        except Exception as e:
            # Optional: Raise a custom error
            raise serializers.ValidationError({"error": str(e)})


class userLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,style={'input_type': 'password'},required=True)


    # class Meta:
    #     # model = User
    #     fields= ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'name', 'gender','role']

#?: feaching all the details of the logged-in Teacher
class TeacherProfileSerializer(serializers.ModelSerializer):

    user = UserProfileSerializer(read_only=True)
    dept_name = serializers.SerializerMethodField()
    class Meta:
        model = Teacher
        fields = ['user', 'employee_code', 'phone_number', 'dept_name', 'designation', 'joining_date']

    def get_dept_name(self, obj):
        return obj.department.dept_name

# ?: feaching all the details of the logged-in Student 
class StudentProfileSerializer(serializers.ModelSerializer):

    user = UserProfileSerializer(read_only=True)
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['user', 'roll_number', 'phone_number', 'course_name', 'current_semester', 'year_of_study']

    def get_course_name(self, obj):
        return obj.course.course_name


class changeUserPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(write_only=True,style={'input_type': 'password'},required=True)
    password2 = serializers.CharField(write_only=True,style={'input_type': 'password'},required=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']

        if password!=password2:
            raise serializers.ValidationError('Password: The Password does not Match')
        
        return attrs

    #! we have to manually save when we are using the serialzers.serializer
    def save(self, **kwargs):
        user = self.context.get('user')
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class userPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
            email = attrs['email']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email = email)
                uid = urlsafe_base64_encode(force_bytes(user.id))
                print('Encoded UID', uid)
                token = PasswordResetTokenGenerator().make_token(user)
                print('Password Reset Token', token)
                frontend_domain = os.environ.get('FRONTEND_URL')
                link = f'{frontend_domain}/reset/'+uid+'/'+token
                print('Password Reset Link', link)

                #?: This Feature is in Working Mode
                # Send EMail
                body = 'Click Following Link to Reset Your Password '+link
                data = {
                    'subject':'Reset Your Password',
                    'body':body,
                    'to_email':user.email
                }
                Util.send_email(data)

                return attrs
            else:
                raise serializers.ValidationError('You are Not a Registered User') 

class UserPasswordResetSerializer(serializers.Serializer):
    
        password = serializers.CharField(style={'input_type': 'password'},required=True, write_only=True)
        password2 = serializers.CharField(style={'input_type': 'password'},required=True, write_only=True)

        class Meta:
            fields = ['password', 'password2']

        def validate(self, attrs):
            try:
                password = attrs['password']
                password2 = attrs['password2']
                uid = self.context.get('uid')
                token = self.context.get('token')

                if password!=password2:
                    raise serializers.ValidationError('Password: The Password does not Match')
                
                id = smart_str(urlsafe_base64_decode(uid))
                user = User.objects.get(id=id)

                token_gen = PasswordResetTokenGenerator()
                if not token_gen.check_token(user, token):
                    raise serializers.ValidationError('Token is not Valid or Expired')
                
                user.set_password(password)
                user.save()
                return attrs
            
            except DjangoUnicodeDecodeError:
                    PasswordResetTokenGenerator().check_token(user, token)
                    raise serializers.ValidationError('Token Not Valid or expired')

