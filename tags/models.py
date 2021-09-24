from django.db import models


class TagCategory(models.Model):
    class Meta:
        verbose_name = 'Tag Category'
        verbose_name_plural = 'Tag Categories'

    name = models.CharField('Category name', max_length=50, unique=True, null=False)
    description = models.TextField('Description', null=True, blank=True)

    def __str__(self):
        return self.name


class TagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('category')


class Tag(models.Model):
    name = models.CharField('Name', max_length=100, null=False)
    category = models.ForeignKey('tags.TagCategory', related_name='tags', on_delete=models.CASCADE)

    objects = TagManager()

    class Meta:
        unique_together = [('name', 'category')]

    def __str__(self):
        return '[%s] %s' % (self.category, self.name)


class DataLocationTagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('tag')


class DataLocationTag(models.Model):
    data_location = models.ForeignKey('dataset.DataLocation', related_name='tags', on_delete=models.CASCADE)
    tag = models.ForeignKey('tags.Tag', on_delete=models.CASCADE)

    objects = DataLocationTagManager()

    class Meta:
        unique_together = [('data_location', 'tag')]

    def __str__(self):
        return '%s - %s' % (self.tag.category, self.tag.name)


