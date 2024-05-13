from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)

        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Se requiere un email')

        if not password:
            raise ValueError('Se requiere una contraseña')

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user

    def base_query(self):
        queryset = self.get_queryset()
        return queryset.select_related('residence_city', 'type').only(
            'id_user',
            'email',
            'identity_document',
            'phone_number',
            'first_name',
            'last_name',
            'date_of_birth',
            'residence_city',
            'type',
            'is_active',
        )

    def get_user_profile(self, id_user):
        return self.base_query().get(id_user=id_user)
