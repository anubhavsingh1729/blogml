from django.apps import AppConfig
import nltk
nltk.download()

class DashboardConfig(AppConfig):
    name = 'dashboard'
