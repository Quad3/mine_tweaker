from django.db import models

from .model_mixins import RecordMixin, LikeIntermediaryMixin


class PostLike(LikeIntermediaryMixin):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class CommentLike(LikeIntermediaryMixin):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)

    class Meta:
        ordering = ['likes']


class Post(RecordMixin):
    likes = models.ManyToManyField('accounts.CustomUser', through=PostLike)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return str(self.id)

    def get_absolute_url(self) -> str:
        return f'post/{self.id}'


class Comment(RecordMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField('accounts.CustomUser', through=CommentLike)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return str(self.id)
