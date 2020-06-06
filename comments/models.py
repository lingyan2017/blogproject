from django.db import models


# Create your models here.
class Comment(models.Model):
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = models.TextField('内容')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    post = models.ForeignKey('blog.Post', verbose_name='文章', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])
