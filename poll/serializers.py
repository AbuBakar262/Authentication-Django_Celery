from rest_framework import serializers

from poll.models import Poll


class PollSerializer(serializers.ModelSerializer):
    question = serializers.CharField(required=True)

    class Meta:
        model = Poll
        fields = '__all__'

    def validate(self, attrs):
        if Poll.objects.filter(question=attrs.get('question')).exists():
            message = 'Poll already created!'
            raise serializers.ValidationError(message)
        return attrs
