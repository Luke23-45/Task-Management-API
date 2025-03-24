from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.filters import OrderingFilter
from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer
from .permissions import IsOwner
from rest_framework import throttling 
import logging
from rest_framework.response import Response


logger = logging.getLogger(__name__) 

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['title', 'status', 'created_at', 'updated_at'] # Fields to allow ordering by
    ordering = ['-created_at'] 
    throttle_classes = [throttling.UserRateThrottle]
    throttle_scope = 'user' 

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)
        logger.info(f"User {self.request.user.id} created a new task: {serializer.instance.title}")
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        status = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        if status:
            queryset = queryset.filter(status=status)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset.order_by(*self.ordering) 