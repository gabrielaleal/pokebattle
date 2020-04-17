from django.shortcuts import get_object_or_404


class UrlFieldDefault:
    def set_context(self, serializer_field):
        field_id = serializer_field.context["view"].kwargs.get(self.url_id_name)
        self.field_default = get_object_or_404(self.model, id=field_id)

    def __call__(self):
        return self.field_default

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)
