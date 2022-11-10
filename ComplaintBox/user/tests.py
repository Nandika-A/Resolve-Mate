from django.test import TestCase
from .models import CustomUser,Userdetails,WorkerDetails

class UserProfileTest(TestCase):

    def test_user_model_has_profile(self):
        user = CustomUser(
            email="user@gmail.com",
            username="89",
            password="123",
        )
        user.save()
        userd = Userdetails(
            user=user,
            phone_no="345",
            address="jio",

        )
        userd.save()
        userw = WorkerDetails(
            worker=userd,
            profession="345",
            biodata="jio",
            UPI="123"

        )
        userw.save()

        self.assertTrue(
            hasattr(user,'username')
        )