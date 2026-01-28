from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import HomePage, MeetCandidatePage, Accomplishment, NewsArticle, VolunteerPage, Signup
from .forms import SignupForm
from urllib.parse import urlparse, parse_qs

def index(request):
    # Get the homepage content, or create default if it doesn't exist
    home_page, created = HomePage.objects.get_or_create(
        defaults={
            "title": "Dr. Emmanuel N. Musa for Governor - Official Campaign Website of Gubernatorial Candidate Dr. Emmanuel N. Musa",
            "notification_text": "Join the team to elect Dr. Emmanuel N. Musa",
            "notification_url": "https://action.jbpritzker.com/a/teamjb",
            "hero_title": "A Leader for Every Adamawaian",
            "hero_description": "No matter where you live in Adamawa or what your background is, Dr. Emmanuel N. Musa has been hard at work to ensure that you, your family, and your community will thrive.",
            "hero_button_text": "Learn More About Dr. Emmanuel N. Musa",
            "hero_button_url": "https://jbpritzker.com/meet-jb-pritzker/"
        }
    )

    # Build embed-friendly video URL
    def to_embed_url(url: str) -> str:
        if not url:
            return url
        u = urlparse(url)
        host = u.netloc.lower()
        if 'youtube.com' in host:
            qs = parse_qs(u.query)
            vid = qs.get('v', [None])[0]
            if vid:
                return f"https://www.youtube.com/embed/{vid}"
            return url
        if 'youtu.be' in host:
            vid = u.path.strip('/')
            if vid:
                return f"https://www.youtube.com/embed/{vid}"
            return url
        if 'vimeo.com' in host:
            # vimeo.com/123456789 -> player.vimeo.com/video/123456789
            vid = u.path.strip('/').split('/')[0]
            if vid and vid.isdigit():
                return f"https://player.vimeo.com/video/{vid}"
            return url
        return url

    def to_thumb_url(url: str, uploaded_thumb):
        if uploaded_thumb:
            return uploaded_thumb.url
        if not url:
            return None
        u = urlparse(url)
        host = u.netloc.lower()
        if 'youtube.com' in host:
            qs = parse_qs(u.query)
            vid = qs.get('v', [None])[0]
            if vid:
                return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
            return None
        if 'youtu.be' in host:
            vid = u.path.strip('/')
            if vid:
                return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
            return None
        return None

    context = {
        'home_page': home_page,
        'video_embed_url': to_embed_url(home_page.video_url),
        'video_thumb_url': to_thumb_url(home_page.video_url, home_page.video_thumbnail),
    }
    return render(request, 'core/index.html', context)

def meet_candidate(request):
    page, created = MeetCandidatePage.objects.get_or_create(defaults={'title': 'Meet Dr. Emmanuel N. Musa', 'content': 'Content goes here...'})
    return render(request, 'core/meet_candidate.html', {'page': page})



def accomplishments(request):
    items = Accomplishment.objects.all()
    return render(request, 'core/accomplishments.html', {'items': items})

def news_list(request):
    articles = NewsArticle.objects.all()
    return render(request, 'core/news_list.html', {'articles': articles})

def news_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug)
    return render(request, 'core/news_detail.html', {'article': article})

def volunteer(request):
    page, created = VolunteerPage.objects.get_or_create(defaults={'title': 'Volunteer', 'content': 'Join our team...'})
    return render(request, 'core/volunteer.html', {'page': page})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for signing up!')
            return redirect('index')
        messages.error(request, 'Please correct the errors and try again.')
        return render(request, 'core/signup.html', {'form': form})

    # Handle GET request - Render signup page
    form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})
