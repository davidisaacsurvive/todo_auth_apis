from django.shortcuts import render
from base.serializers import UserSerializer, TodoSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from base.models import Todo
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class UserRegistrationView(APIView):
    serializer_class = UserSerializer

    @extend_schema(
            request=UserSerializer
    )

    def post(self, request):
        user = request.user
        print("WHO IS REGISTERING",user)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoListCreateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoSerializer

    @extend_schema(
        request=TodoSerializer,)
    def get(self, request):
        todo = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        user = request.user
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request, pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
        except Todo.DoesNotExist:
            return Response(data={"detail": "Todo not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TodoSerializer(todo)
        return Response(serializer.data)


    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
        except Todo.DoesNotExist:
            return Response(data={"detail": "Todo not found."}, status=status.HTTP_404_NOT_FOUND)
        
        todo.delete()
        return Response(data={"detail": "Todo record deleted."}, status=status.HTTP_204_NO_CONTENT)
    

class TodoPaginatedView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.AllowAny,)


    def list(self,request):
        queryset = self.get_queryset()
        serializer = TodoSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListAllTodos(APIView):
    serializer_class = TodoSerializer
    pagination_class = PageNumberPagination

    def get(self, request):
        q = self.request.query_params.get('q', None)

        print("QUERY PARAMS", q)
        

        if q is not None:
            todos = Todo.objects.filter(title__startswith=q)
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(todos, request)
            serializer = TodoSerializer(page, many=True)
        else:
            todos = Todo.objects.all()
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(todos, request)
            serializer = TodoSerializer(page, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)