from rest_framework import serializers
from myapp.models import Like, Post,Comments
from django.contrib.auth.models import User

from django.contrib.auth.password_validation import validate_password


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields=['id','description','pic','date_posted','user_name','tags']


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password','password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        password2 = validated_data.get('password2')

        if password == password2:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({
                'error': 'Both Password Do Not Match'
            })


class CommentsSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(),many=False)
    username = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=False)
    class Meta:
        model = Comments
        fields = ['id','post','username','comment']

    def to_representation(self, instance):
        self.fields['post'] =  PostSerializer(read_only=True)
        self.fields['username'] = UserSerializer(read_only=True)
        return super(CommentsSerializer, self).to_representation(instance)

class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(),many=False)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=False)
    class Meta:
        model = Like
        fields = ['id','post','user']

    # def to_representation(self, instance):
    #     self.fields['post'] =  PostSerializer(read_only=True)
    #     self.fields['user'] = UserSerializer(read_only=True)
    #     return super(LikeSerializer, self).to_representation(instance)



