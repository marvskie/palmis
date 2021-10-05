from rest_framework import serializers

from exec.models import FileComment, Task

class FileCommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField()
    class Meta:
        model = FileComment
        fields = ['id', 'created_by', 'created_at', 'text', 'commented_by']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'custom_id','created_by', 'created_at', 'start_time', 'end_time', 'location', 'description']
