from django.db import models

# Create your models here.
genres=[
    ('Action', 'Action'),
    ('Adventure', 'Adventure'), 
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Fantasy', 'Fantasy'),
    ('Horror', 'Horror'),
    ('Mystery', 'Mystery'),
    ('Romance', 'Romance'),
    ('Sci-Fi', 'Sci-Fi'),
    ('Thriller', 'Thriller'),
]
languages=[
    ('English', 'English'),
    ('Hindi', 'Hindi'),
    ('kannada', 'Kannada'),
    ('Telugu', 'Telugu'),
    ('Tamil', 'Tamil'),
    ('Malayalam', 'Malayalam'),
    ('Bengali', 'Bengali'),
    ('Punjabi', 'Punjabi'),
    ('Gujarati', 'Gujarati'),
    ('Marathi', 'Marathi'),
    ('Urdu', 'Urdu'),
    ('Odia', 'Odia'),
]

class Movie(models.Model):
    title= models.CharField(max_length=255)
    genre= models.CharField(max_length=255, choices=genres,null=True, blank=True)
    language= models.CharField(max_length=255, choices=languages,null=True, blank=True)
    synopsis= models.TextField(null=True, blank=True)
    duration_minutes= models.IntegerField(null=True, blank=True)
    release_date= models.DateField(null=True, blank=True)
    trailer_url= models.URLField(null=True, blank=True)
    status= models.CharField(max_length=255, choices=[('Upcoming', 'Upcoming'), ('Realeased', 'Realeased')], null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    movie_image= models.ImageField(upload_to='movies/', null=True, blank=True) 
    slug=models.CharField(max_length=2000,null=True,blank=True)


    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        self.slug='-'.join((self.title+' '+str(self.release_date)+' '+self.genre+' '+str(self.release_date)+' '+self.language).split())
        return super().save(*args,**kwargs)
    
class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='casts')
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255,null=True, blank=True)
    image=models.ImageField(upload_to='casts/', null=True, blank=True)  