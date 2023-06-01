# Third Party Stuff
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from apps.base.response import Ok


class MultipleSerializerMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultipleSerializerMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @list_route
            def my_action:
                ...

        If there's no serializer available for that action than
        the default serializer class will be returned as fallback.
        """
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class CustomModelViewSet(ModelViewSet):
    filter_backends = [OrderingFilter]
    ordering_fields = "__all__"

    @action(detail=False, methods=["get"], url_path="all", url_name="all")
    def get_all(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer_class()
        serializer = serializer(queryset, many=True)
        return Ok(serializer.data)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
