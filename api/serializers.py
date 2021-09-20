from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',)
    score = serializers.IntegerField()

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        author = self.context['request'].user
        method = self.context.get('request').method
        if (Review.objects.filter(author=author, title_id=title_id).exists()
                and method == 'POST'):
            raise serializers.ValidationError('Вы уже оставляли отзыв')
        return data

    class Meta:
        fields = '__all__'
        read_only_fields = ('title',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = '__all__'
        read_only_fields = ('review',)
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializerGet(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerPost(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    year = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = '__all__'
