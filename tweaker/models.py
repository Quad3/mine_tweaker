from django.db import models
from datetime import datetime

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
        ordering = ['created_at']


class Comment(RecordMixin):
    likes = models.ManyToManyField('accounts.CustomUser', through=CommentLike)
