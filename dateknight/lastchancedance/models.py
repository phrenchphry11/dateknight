from django.db import models

class Student(models.Model):
    email = models.CharField(max_lengt=200)
    first = models.CharField(max_length=200)
    last = models.CharField(max_length=200)
    year = models.IntField()

    @property
    def directory_url(self):
        return 'http://apps.carleton.edu/campus/directory/?email_address=' + self.carlnetid

    @property
    def photo(self):
        return 'http://apps.carleton.edu/stock/ldapimage.php?id=' + self.carlnetid

    @property
    def email(self):
        return self.carlnetid + '@carleton.edu'

    @property
    def crushed_on(self):
        return self.in_crushes.filter(deleted=False).exists()

    def __unicode__(self):
        return unicode(self.carlnetid)

class Crush(models.Model):
    egg = models.ForeignKey(Student, related_name = 'out_crushes')
    chicken = models.ForeignKey(Student, related_name = 'in_crushes')
    time = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.source) + ' => ' + unicode(self.target)

    class Meta:
        unique_together = ('source', 'target', 'time')

class Match(models.Model):
    egg = models.ForeignKey(Student, related_name = 'out_matches')
    chicken = models.ForeignKey(Student, related_name = 'in_matches')
    match_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.source) + ' <3 ' + unicode(self.target)

    class Meta:
        unique_together = (('egg', 'chicken'), ('chicken', 'egg'))
