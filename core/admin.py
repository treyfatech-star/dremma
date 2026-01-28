from django.contrib import admin
from django.http import HttpResponse
from django.core.mail import send_mass_mail
from django.utils import timezone
from django.contrib import messages
import csv
from .models import HomePage, MeetCandidatePage, Accomplishment, NewsArticle, VolunteerPage, Signup, EmailCampaign

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_text')
    fieldsets = (
        ('General Settings', {
            'fields': ('title', 'logo', 'header_logo', 'footer_logo', 'notification_text', 'notification_url')
        }),
        ('Hero Section', {
            'fields': ('hero_eyebrow', 'hero_slogan', 'hero_title', 'hero_description', 'hero_button_text', 'hero_button_url', 'hero_image')
        }),
        ('Video Section', {
            'fields': ('video_thumbnail', 'video_url', 'video_button_text')
        }),
        ('Meet Candidate Section', {
            'fields': ('meet_candidate_image', 'meet_candidate_image_2', 'meet_candidate_image_3', 'meet_candidate_eyebrow', 'meet_candidate_title', 'meet_candidate_description', 'meet_candidate_button_text')
        }),
        ('Meet Running Mate Section', {
            'fields': ('running_mate_title', 'running_mate_description', 'running_mate_button_text', 'running_mate_image_1', 'running_mate_image_2')
        }),
        ('Vision/Accomplishments Section', {
            'fields': ('vision_title', 'vision_description', 'vision_button_text', 'vision_image')
        }),
        ('Join Section', {
            'fields': ('join_title', 'join_disclaimer', 'join_button_text')
        }),
        ('Connect & Action Section', {
            'fields': ('connect_title', 'facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'threads_url', 'tiktok_url', 'action_title', 'action_button_text', 'action_button_url')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(MeetCandidatePage)
class MeetCandidatePageAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def has_add_permission(self, request):
        # Only allow one instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Accomplishment)
class AccomplishmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)



@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(VolunteerPage)
class VolunteerPageAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def has_add_permission(self, request):
        # Only allow one instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile_phone', 'postal_code', 'consent_sms', 'created_at', 'source')
    search_fields = ('first_name', 'last_name', 'email', 'mobile_phone', 'postal_code', 'source')
    list_filter = ('created_at', 'source', 'consent_sms')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    list_per_page = 50
    empty_value_display = '-'
    fieldsets = (
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'mobile_phone')
        }),
        ('Location', {
            'fields': ('postal_code',)
        }),
        ('Consent', {
            'fields': ('consent_sms',)
        }),
        ('Meta', {
            'fields': ('source', 'created_at')
        }),
    )
    actions = ['export_selected_signups', 'export_emails_txt', 'export_phones_txt', 'export_contacts_csv']

    def has_add_permission(self, request):
        return False

    def export_selected_signups(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="signups.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Mobile Phone', 'Postal Code', 'Consent SMS', 'Source', 'Created At'])
        for s in queryset:
            writer.writerow([s.first_name, s.last_name, s.email, s.mobile_phone, s.postal_code, 'Yes' if s.consent_sms else 'No', s.source, s.created_at.isoformat()])
        return response
    export_selected_signups.short_description = 'Export selected signups to CSV'

    def export_emails_txt(self, request, queryset):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="emails.txt"'
        emails = queryset.exclude(email='').values_list('email', flat=True)
        for email in emails:
            response.write(f"{email}\n")
        return response
    export_emails_txt.short_description = 'Export emails to TXT'

    def export_phones_txt(self, request, queryset):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="phones.txt"'
        phones = queryset.exclude(mobile_phone='').values_list('mobile_phone', flat=True)
        for phone in phones:
            response.write(f"{phone}\n")
        return response
    export_phones_txt.short_description = 'Export mobile phones to TXT'

@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'sent_at')
    readonly_fields = ('sent_at',)
    actions = ['send_campaign']

    def send_campaign(self, request, queryset):
        for campaign in queryset:
            if campaign.sent_at:
                self.message_user(request, f"Campaign '{campaign.subject}' already sent at {campaign.sent_at}", level=messages.WARNING)
                continue

            # Get all signups with email
            signups = Signup.objects.exclude(email='').values_list('email', flat=True)
            if not signups:
                self.message_user(request, "No recipients found.", level=messages.WARNING)
                continue

            # Prepare messages
            messages_to_send = []
            for email in signups:
                messages_to_send.append((campaign.subject, campaign.message, None, [email]))

            try:
                send_mass_mail(tuple(messages_to_send), fail_silently=False)
                campaign.sent_at = timezone.now()
                campaign.save()
                self.message_user(request, f"Campaign '{campaign.subject}' sent to {len(messages_to_send)} recipients.", level=messages.SUCCESS)
            except Exception as e:
                self.message_user(request, f"Error sending campaign '{campaign.subject}': {str(e)}", level=messages.ERROR)

    send_campaign.short_description = "Send selected campaigns to all signups"

admin.site.site_header = "Admin"
admin.site.site_title = "Admin"
admin.site.index_title = "Admin"
