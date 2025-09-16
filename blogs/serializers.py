from rest_framework import serializers
from .models import Blog, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


# Nested Serializer: Die Comments sollen im Blog abgebildet werden
# Im Comment-Model steht: blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
class BlogSerializer(serializers.ModelSerializer):
    # Der Variablenname 'comments' muss gleich dem related_name Attribut von "blog" im Comment Model sein
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Blog
        fields = '__all__'