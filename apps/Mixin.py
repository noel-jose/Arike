from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class UserPermissionMixin(PermissionRequiredMixin):
    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms = self.get_permission_required()
        if self.request.user.role in perms:
            return True
        else:
            return False
