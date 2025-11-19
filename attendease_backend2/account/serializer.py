from rest_framework import serializers
from .models import User

#! Below we are Importing for sending Password reset email
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs={
            'password':{'write_only':True}
        }

    #? Validating password and password2 while registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does not match')
        return attrs
    
    #! You have to write this if you have created your own custom-User Model
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        # user = self.context.get('user')

        if password!=password2:
            raise serializers.ValidationError('Password and Confirm Password does not match')
        return attrs
    
    def save(self, **kwargs):
        user = self.context.get('user')
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print(token)
            link = 'https://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link '+link)

            # TODO: The Email Sending is Pending........
            # Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            # Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are Not a Registered User')
        
class UserPasswordResetSerialier(serializers.Serializer):

    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password!=password2:
                raise serializers.ValidationError('Password and Confirm Password does not match')
            
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)

            token_gen = PasswordResetTokenGenerator()
            if not token_gen.check_token(user, token):
                raise serializers.ValidationError('Token Not Valid or expired')

            user.set_password(password)
            user.save()
            return attrs
        
        except DjangoUnicodeDecodeError:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token Not Valid or expired')


    
    
    