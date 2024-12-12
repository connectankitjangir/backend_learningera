from django.contrib import admin
from .models import TypingPassage

class TypingPassageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'passage_text')

admin.site.register(TypingPassage, TypingPassageAdmin)
