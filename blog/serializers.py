from rest_framework import serializers

from blog.models import Post, Comment, Reply


class ReplySerializer(serializers.Serializer):
    content = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField(read_only=True)
    replycomment = ReplySerializer(many=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def get_reply(self, obj):
        reply = Reply.objects.filter(comment=obj.id)
        return ReplySerializer(reply, obj.id).data


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, max_length=100)
    content = serializers.CharField(required=True, max_length=1000)
    image = serializers.FileField(required=True, allow_empty_file=False)
    commentpost = CommentSerializer(many=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('code', instance.code)
        instance.image = validated_data.get('linenos', instance.linenos)
        instance.save()
        return instance

    def get_post(self, instance):
        return Post.objects.all().order_by("-created_at")

    def get_commentpost(self, obj):
        comments = Comment.objects.filter(post_id=obj.id)
        return CommentSerializer(comments, many=True).data
