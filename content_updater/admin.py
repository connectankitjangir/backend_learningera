from django.contrib import admin
from .models import news_bar,our_videos,Feedback
# Register your models here.
class news_barAdmin(admin.ModelAdmin):
    list_display=('news_bar_video_link','news_bar_order')

admin.site.register(news_bar,news_barAdmin)

# class why_choose_usAdmin(admin.ModelAdmin):
#     list_display=('why_choose_us_description','why_choose_us_order')

# admin.site.register(why_choose_us,why_choose_usAdmin)

class our_videosAdmin(admin.ModelAdmin):
    list_display=('our_videos_video_link','our_videos_order')

admin.site.register(our_videos,our_videosAdmin)





# class about_usAdmin(admin.ModelAdmin):
#     list_display=('about_us_description','about_us_order')

# admin.site.register(about_us,about_usAdmin)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'email', 'comments')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

