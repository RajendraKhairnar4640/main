
from django.shortcuts import render,HttpResponseRedirect
from myapp.models import Like, Post,Comments
from .serializers import LikeSerializer, PostSerializer,RegisterSerializer,CommentsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


class PostAPI(APIView):
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,]
    def get(self,request,pk=None,format=None):
        id=pk
        if id is not None:
            post = Post.objects.get(id=id)
            serializer = PostSerializer(post)
            return Response(serializer.data,status=status.HTTP_200_OK)
            

        post = Post.objects.all()
        serializer = PostSerializer(post,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,format=None):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created..!'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk,format=None):
        id = pk
        post = Post.objects.get(id=id)
        serializer = PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'complete data updated'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk,format=None):
        id=pk
        item = Post.objects.get(id=id)
        serializer = PostSerializer(item,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data updated.!'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,post_id,format=None):
        id=post_id
        item = Post.objects.get(id=id)
        item.delete()
        return Response({'msg':'Data Deleted.!'})

class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    
    def post(self,request,format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(response_data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CommentAPI(APIView): 
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,]   
    def get(self,request):
        try:
            com = Comments.objects.all()
            serializers = CommentsSerializer(com,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except com.DoesNotExist:
            return Response({
                "message": "comments doesnt exist"
            },status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request,format=None):
        try:
            serializer = CommentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Comment Created.!'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e,{'errors':serializer.errors,'msg':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,pk,format=None):
        try:
            id=pk
            comments = Comments.objects.get(id=id)
            serializer = CommentsSerializer(comments,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,pk,format=None):
        comments = Comments.objects.get(pk=pk)
        comments.delete()
        return Response({'msg':'Comment Deleted.!'},status=status.HTTP_200_OK)

class LikeAPI(APIView):
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,] 
    def get(self,request):
        print(request.user)
        try:
            com = Like.objects.all()
            serializers = LikeSerializer(com,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except com.DoesNotExist:
            return Response({
                "message": "Like doesnt exist"
            },status=status.HTTP_400_BAD_REQUEST)

    def post(self,request,format=None):
        try:
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'msg':'Like Created.!'},status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e,{'errors':serializer.errors,'msg':'something went wrong'})

