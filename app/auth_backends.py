from app.models import CustomUser
import hashlib


class CustomUserModelBackend:

    def hash(self, token):
        m=hashlib.sha1()
        m.update(token)
        r = m.hexdigest()
        return r[:30]

    def authenticate(self, token=None):
        try:
            user = CustomUser.objects.get(username=self.hash(token))
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(username=self.hash(token))
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
