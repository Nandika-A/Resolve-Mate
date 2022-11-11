import django_filters
from user.models import WorkerProfile

class UserProfileFilter(django_filters.FilterSet):
    class Meta:
        model = WorkerProfile
        fields = [
            'profession'
            ]
