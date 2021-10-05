from rest_framework import serializers

from executive import models


class InstructionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstructionResponseType
        fields = ('id', 'code', 'name')


class InstructionRecipientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstructionRecipient
        fields = ('id', 'instruction', 'branch')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        del ret['instruction']
        ret['branch'] = {
            'id': instance.branch_id,
            'name': instance.branch.name
        }
        return ret


class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileAttachment
        fields = ('id', 'content_type', 'object_id', 'content_object', 'title', 'file')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        del ret['content_type'], ret['object_id']
        return ret


class InstructionRecordSerializer(serializers.ModelSerializer):
    recipients = InstructionRecipientsSerializer(many=True)

    class Meta:
        model = models.InstructionRecord
        fields = ('id', 'subject', 'description', 'due_date', 'created_by', 'recipients', 'attachments')

    def create(self, validated_data):
        recipients = validated_data.pop('recipients', None) or []
        instance = super().create(validated_data)

        for recipient in recipients:
            serialized_obj = InstructionRecipientsSerializer(
                data={**recipient, 'branch': recipient['branch'].id, 'instruction': instance.id}
            )
            serialized_obj.is_valid(raise_exception=True)
            _ = serialized_obj.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret['attachments'] = []

        for attachment in instance.attachments.all():
            ret['attachments'].append({
                'id': attachment.id,
                'title': attachment.title,
                'url': attachment.file.url
            })

        return ret
