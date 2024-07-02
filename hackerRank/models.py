from django.db import models
import uuid
# Create your models here.
class Submissions(models.Model):
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  problemName = models.CharField(max_length=255,null=False,blank=False)
  username = models.CharField(max_length=150,null=False,blank=False)
  submissionId = models.IntegerField(unique=True)
  lang = models.CharField(max_length=100,null=False,blank=False)
  # duringContest = models.CharField(max_length=3,null=False,blank=False)
  srcLink = models.URLField(max_length=2000)
