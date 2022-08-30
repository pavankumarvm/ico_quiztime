from rest_framework import serializers

from .models import Question, Quiz

class QuestionSerializer(serializers.ModelSerializer):
    """
        Serialize the data
    """
    class Meta:
        model = Question
        fields = ['question_id', 'question', 'option_A', 'option_B', 'option_C', 'option_D', 'answer', 'explanation', 'given_by']
        read_only_fields = ['given_by']
    
    def create(self, validated_data):
        return Question.objects.create(**validated_data)

class QuizSerializer(serializers.ModelSerializer):
    """
        Serialize the data
    """
    class Meta:
        model = Quiz
        fields = ['test_id', 'student_id', 'result', 'date_appeared']
        read_only_fields = ['test_id', 'student_id']

    def create(self, validated_data):
        return Quiz.objects.create(**validated_data)