from django.db import models
from ckeditor.fields import RichTextField

class HomePage(models.Model):
    title = models.CharField(max_length=200, default="Dr. Emmanuel N. Musa for Governor - Official Campaign Website of Gubernatorial Candidate Dr. Emmanuel N. Musa")
    logo = models.ImageField(upload_to='site_settings/', blank=True, null=True, help_text="Upload website logo")
    header_logo = models.ImageField(upload_to='site_settings/', blank=True, null=True, help_text="Upload header logo")
    footer_logo = models.ImageField(upload_to='site_settings/', blank=True, null=True, help_text="Upload footer logo")

    # Notification Bar
    notification_text = models.CharField(max_length=255, default="Join the team to elect Dr. Emmanuel N. Musa")
    notification_url = models.CharField(max_length=255, default="/signup/")

    # Hero Section
    hero_title = models.CharField(max_length=255, default="A Leader for Every Adamawaian")
    hero_eyebrow = models.CharField(max_length=255, default="Emnamu Foundation President Dr. Emmanuel N. Musa")
    hero_slogan = models.CharField(max_length=255, default="Keep Adamawa moving forward")
    hero_description = models.TextField(default="No matter where you live in Adamawa or what your background is, Emnamu Foundation President Dr. Emmanuel N. Musa has been hard at work to ensure that you, your family, and your community will thrive.")
    hero_button_text = models.CharField(max_length=100, default="Learn More About Dr. Emmanuel N. Musa")
    hero_button_url = models.URLField(default="https://jbpritzker.com/meet-jb-pritzker/")
    hero_image = models.ImageField(upload_to='home/hero/', blank=True, null=True, help_text="Main hero image at the top of the page")

    # Video Section
    video_thumbnail = models.ImageField(upload_to='home/video/', blank=True, null=True, help_text="Thumbnail for the launch video")
    video_url = models.URLField(default="https://www.youtube.com/watch?v=0HCOrIr7Umo", help_text="YouTube URL for the video")
    video_button_text = models.CharField(max_length=100, default="Play Launch Video")

    # Meet Candidate Section
    meet_candidate_image = models.ImageField(upload_to='home/candidate/', blank=True, null=True, help_text="Image for the 'Meet Dr. Musa' section")
    meet_candidate_image_2 = models.ImageField(upload_to='home/candidate/', blank=True, null=True)
    meet_candidate_image_3 = models.ImageField(upload_to='home/candidate/', blank=True, null=True)
    meet_candidate_eyebrow = models.CharField(max_length=255, default="Meet Dr. Emmanuel N. Musa")
    meet_candidate_title = models.CharField(max_length=255, default="A Leader for Every Adamawaian")
    meet_candidate_description = models.TextField(default="No matter where you live in Adamawa or what your background is, Dr. Emmanuel N. Musa has been hard at work to ensure that you, your family, and your community will thrive.")
    meet_candidate_button_text = models.CharField(max_length=100, default="Learn More About Dr. Emmanuel N. Musa")

    # Join Section
    join_title = models.CharField(max_length=255, default="Join #TeamDr.Emmanuel")
    join_disclaimer = models.TextField(default="By submitting your mobile phone number you are agreeing to receive periodic text messages from this organization. Message and data rates may apply. Text HELP for more information. Text STOP to stop receiving messages.")
    join_button_text = models.CharField(max_length=100, default="Sign Up")

    # Connect & Action Section
    connect_title = models.CharField(max_length=255, default="Get Connected")
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    threads_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)

    action_title = models.CharField(max_length=255, default="Take Action")
    action_button_text = models.CharField(max_length=100, default="Learn More")
    action_button_url = models.URLField(blank=True)

    # Meet Running Mate Section
    running_mate_title = models.CharField(max_length=255, default="Meet Christian")
    running_mate_description = models.TextField(default="From serving as a State Representative to Deputy Governor to the Adamawa Air National Guard, Christian Mitchell has dedicated himself to improving the lives and livelihoods of all Adamawaians. He is running for Lieutenant Governor to keep our state moving forward.")
    running_mate_button_text = models.CharField(max_length=100, default="Learn more about Christian")
    running_mate_image_1 = models.ImageField(upload_to='home/running_mate/', blank=True, null=True, help_text="First image for running mate section")
    running_mate_image_2 = models.ImageField(upload_to='home/running_mate/', blank=True, null=True, help_text="Second image for running mate section")

    # Vision/Accomplishments Section
    vision_title = models.CharField(max_length=255, default="Adamawa Is Heading In The Right Direction")
    vision_description = models.TextField(default="Through the Emnamu Foundation, Dr. Emmanuel N. Musa has demonstrated the leadership to make our state one of the best in the nation in education, youth mental health, workforce development, and fighting climate change. He will create jobs, balance our budget, and protect our freedoms. Discover how Dr. Emmanuel N. Musa will lead the way on issues you care about.")
    vision_button_text = models.CharField(max_length=100, default="Learn More About Dr. Musa's Vision")
    vision_image = models.ImageField(upload_to='home/vision/', blank=True, null=True, help_text="Image for the vision/accomplishments section")

    def __str__(self):
        return "Home Page Content"

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"

class MeetCandidatePage(models.Model):
    title = models.CharField(max_length=200, default="Meet Dr. Emmanuel N. Musa")
    content = RichTextField()
    image = models.ImageField(upload_to='candidate/', blank=True, null=True)

    class Meta:
        verbose_name = "Meet Dr. Musa Page"
        verbose_name_plural = "Meet Dr. Musa Page"

    def __str__(self):
        return self.title

class VolunteerPage(models.Model):
    title = models.CharField(max_length=200, default="Volunteer")
    content = models.TextField()
    image = models.ImageField(upload_to='volunteer/', blank=True, null=True)

    class Meta:
        verbose_name = "Volunteer Page"
        verbose_name_plural = "Volunteer Page"

    def __str__(self):
        return self.title

class Accomplishment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='accomplishments/', blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class MeetRunningMatePage(models.Model):
    title = models.CharField(max_length=200, default="Meet Christian")
    content = models.TextField()
    image = models.ImageField(upload_to='running_mate/', blank=True, null=True)

    class Meta:
        verbose_name = "Meet Running Mate Page"
        verbose_name_plural = "Meet Running Mate Page"

    def __str__(self):
        return self.title

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news/', blank=True, null=True)

    class Meta:
        verbose_name = "News & Update"
        verbose_name_plural = "News & Updates"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

class Signup(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=30, blank=True)
    consent_sms = models.BooleanField(default=True)
    source = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Signup"
        verbose_name_plural = "Signups"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

class EmailCampaign(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField(help_text="Email body content")
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Email Campaign"
        verbose_name_plural = "Email Campaigns"
        ordering = ['-created_at']

    def __str__(self):
        return self.subject
