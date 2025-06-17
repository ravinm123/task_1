from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.core.cache import cache
from .models import UserActivityLog
from .serializers import UserActivityLogSerializer,RegisterSerializer,LoginSerializer
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import make_aware
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
CACHE_TTL = 60 * 5


class RegisterAPIView(APIView):
    # permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Generate tokens manually:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserActivityLogListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cache_key = f"user_activity_{user.id}_{request.get_full_path()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        queryset = UserActivityLog.objects.filter(user=user)

        # Optional filters
        action = request.query_params.get('action')
        start = request.query_params.get('start')
        end = request.query_params.get('end')

        if action:
            queryset = queryset.filter(action=action)
        if start and end:
            try:
                start_date = make_aware(datetime.fromisoformat(start))
                end_date = make_aware(datetime.fromisoformat(end))
                queryset = queryset.filter(timestamp__range=(start_date, end_date))
            except ValueError:
                return Response({"error": "Invalid date format. Use ISO format."}, status=400)

        serializer = UserActivityLogSerializer(queryset, many=True)
        cache.set(cache_key, serializer.data, CACHE_TTL)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserActivityLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            cache.delete_pattern(f"user_activity_{request.user.id}_*")
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



class UserActivityLogTransitionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            log = UserActivityLog.objects.get(pk=pk, user=request.user)
        except UserActivityLog.DoesNotExist:
            return Response({"error": "Not found."}, status=404)

        status_value = request.data.get("status")
        if status_value not in dict(UserActivityLog.STATUS_CHOICES):
            return Response({"error": "Invalid status."}, status=400)

        log.status = status_value
        log.save()
        cache.delete_pattern(f"user_activity_{request.user.id}_*")
        return Response({"status": "updated"}, status=200)