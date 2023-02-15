import uuid
from django.utils import timezone
from django.db import models

# Create your models here.


class Author(models.Model):
    # Unique ID of the user
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    # Server host of the user
    host = models.URLField(max_length=200)

    # Max Length: 35 (First Name) + 35 (Last Name)
    displayName = models.CharField(max_length=70)

    github = models.URLField(max_length=200, unique=True)

    profileImage = models.URLField(max_length=200, unique=True, null=True)

    # Max Length: 64 (Username) + 255 (Domain)
    email = models.EmailField(max_length=320, unique=True)

    username = models.CharField(max_length=30, unique=True)
    
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    following = models.ManyToManyField(
        'self', related_name='followers', symmetrical=False, blank=True)
    
    sent_requests = models.ManyToManyField('self', related_name='follow_requests', symmetrical=False, blank=True)

    # Used for rapid lookup, will improve database performance
    class Meta:
        indexes = [
            models.Index(fields=['host'], name='host_idx'),
            models.Index(fields=['displayName'], name='displayName_idx'),
            models.Index(fields=['github'], name='github_idx'),
            models.Index(fields=['profileImage'], name='profileImage_idx'),
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['username'], name='username_idx')
        ]

    def __str__(self):
        return f"{self.displayName} ({self.id})"

class Post(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    made_by = models.ForeignKey(Author, related_name = "my_posts", on_delete=models.CASCADE)

    #if a private post was sent to a friend(only comes into play, when private, otherwise blank). Could it be sent to multiple people as private?
    receiver = models.ForeignKey(Author, blank = True, null = True, related_name = "private_posts", on_delete=models.CASCADE)

    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, unique=True)

    source = models.URLField(max_length=200, unique=True)
    origin = models.URLField(max_length=200, unique=True)

    date_published = models.DateTimeField(default=timezone.now)

    CONTENT_TYPE_CHOICES = [
        ("markdown", "text/markdown"),
        ("plain", "text/plain"),
        ("image-png", "image/png"),
        ("image-jpeg", "image/jpeg"),
    ]

    content_type = models.CharField(max_length=18, choices=CONTENT_TYPE_CHOICES)
    content = models.TextField()
    categories = models.TextField()
    comments_url = models.TextField()
    VISIBILITY_CHOICES = [
        ('PUBLIC', 'public'),
        ('PRIVATE', 'private'),
        ('FRIENDS', 'friends'),
    ]
    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES)
    unlisted = models.BooleanField(default=False)
    image = models.CharField(max_length=100,null=True, blank=True)


