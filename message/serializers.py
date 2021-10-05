from rest_framework import serializers

from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.account.name')

    class Meta:
        model = Message
        fields = ('id', 'remarks', 'created_at', 'created_by')


class MessageCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'remarks', 'content_type', 'object_id')

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret['created_at'] = instance.created_at
        ret['created_by'] = instance.created_by.account.name

        return ret
