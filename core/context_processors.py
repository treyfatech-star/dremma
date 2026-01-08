from .models import HomePage

def global_settings(request):
    home_page = HomePage.objects.first()
    return {
        'home_page': home_page
    }
