from app.models import CustomUser

class CustomUserModelBackend:

    def authenticate(self, token=None):
        try:
            user = CustomUser.objects.get(username=token)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(username=token)
            user.is_active = True
            user.is_staff = True
            user.is_superuser = False
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
