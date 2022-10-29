import django_filters
from user.models import UserProfile

class UserProfileFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = [
            'profession'
            ]
