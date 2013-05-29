from django.db import models

class Student(models.Model):
    carlnetid = models.CharField(max_length=30, unique=True)
    first = models.CharField(max_length=200)
    last = models.CharField(max_length=200)
    year = models.IntField()

    @property
    def directory_url(self):
        return 'http://apps.carleton.edu/campus/directory/?email_address=%s' % self.carlnetid

    @property
    def photo(self):
        return 'http://apps.carleton.edu/stock/ldapimage.php?id=%s' % self.carlnetid

    @property
    def email(self):
        return '%s@carleton.edu' % self.carlnetid

    @property
    def crushed_on(self):
        return self.in_crushes.filter(deleted=False).exists()

    def __unicode__(self):
        return unicode(self.carlnetid)

class Crush(models.Model):
    egg = models.ForeignKey(Student, related_name='out_crushes')
    chicken = models.ForeignKey(Student, related_name='in_crushes')
    time = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    def __unicode__(self):
        return '%s => %s' % (unicode(self.egg), unicode(self.chicken))

    class Meta:
        unique_together = ('egg', 'chicken', 'time')

class Match(models.Model):
    egg = models.ForeignKey(Student, related_name='out_matches')
    chicken = models.ForeignKey(Student, related_name='in_matches')
    match_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s <3 %s' % (unicode(self.egg), unicode(self.chicken))

    class Meta:
        unique_together = (('egg', 'chicken'), ('chicken', 'egg'))
