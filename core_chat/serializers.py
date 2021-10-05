import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from core_chat.models import MessageModel
from rest_framework.serializers import ModelSerializer, CharField




class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user)
        msg.save()
        return msg
    
    def update(self, instance, validated_data):
        
        instance.seen_timestamp = datetime.datetime.now()
        instance.save()
        instance.notify_ws_clients_seen()
        return instance

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body', 'seen_timestamp')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username','get_full_name')
