from djongo import models
from django.contrib.auth.models import AbstractUser
from django                     import forms


class User(AbstractUser):
	_id         = models.ObjectIdField()
	code        = models.CharField('code', max_length=6, null=True)
	email       = models.EmailField('email', unique=True)
	downloads   = models.IntegerField('downloads', default=0)
	totalemails = models.IntegerField('totalemails', default=0)

	class Meta:
		db_table = "user"


class Label(models.Model):
	value      = models.TextField()
	confidence = models.FloatField() 

	class Meta:
		abstract = True

	def __str__(self):
		return self.value


class EmailSender(models.Model):
	name    = models.TextField()
	emailAddress = models.EmailField()

	class Meta:
		abstract = True

	def __str__(self):
		return self.name


class Entity(models.Model):
	text      = models.TextField()
	start_pos = models.IntegerField()
	end_pos   = models.IntegerField()
	labels    = models.EmbeddedField(model_container=Label)
					
	class Meta:
		abstract = True

	def __str__(self):
		return self.text


class EntityForm(forms.ModelForm):
	class Meta:
		model  = Entity 
		fields = "__all__"


class Relation(models.Model):
	entity_A  = models.EmbeddedField(model_container=Entity)
	entity_B  = models.EmbeddedField(model_container=Entity)
	relations = models.ArrayField(model_container=Entity, model_form_class=EntityForm)

	class Meta:
		abstract = True

	def __str__(self):
		return self.entity_a


class RelationForm(forms.ModelForm):
	class Meta:
		model  = Relation 
		fields = "__all__"


class Emails(models.Model):
	from_user     = models.EmbeddedField(model_container=EmailSender)
	subject   = models.TextField()
	body      = models.TextField()
	entities  = models.ArrayField(model_container=Entity, model_form_class=EntityForm)					
	relations = models.ArrayField(model_container=Relation, model_form_class=RelationForm)
	
	class Meta:
		db_table = "emails"

	def __str__(self):
		return self.subject
		
