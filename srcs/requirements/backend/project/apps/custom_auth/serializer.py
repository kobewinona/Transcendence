# from rest_framework import serializers
# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }


# from rest_framework import serializers
# from django.contrib.auth.hashers import make_password
# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password', 'email')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data['password'])
#         return super().create(validated_data)

from django import forms
from django.contrib.auth.models import User

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
