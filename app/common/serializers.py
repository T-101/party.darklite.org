from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', [])
        exclude_fields = kwargs.pop('exclude_fields', [])
        super().__init__(*args, **kwargs)

        fields_keys = list(self.fields.keys())
        for item in fields_keys:
            if fields and item not in fields:
                self.fields.pop(item, None)
        for item in exclude_fields:
            self.fields.pop(item, None)
