from django.http import Http404

class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
