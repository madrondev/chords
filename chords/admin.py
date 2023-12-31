from django.contrib import admin
from django.contrib import messages
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from . import forms
from . import models
from . import utils
from . import views


@admin.register(models.Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'pdf_chords_link', 'pdf_lyrics_link', 'key', 'time', 'tempo', 'year', 'source_link']
    list_filter = ['artist']
    search_fields = ['title', 'artist']
    fields = [
        ('title', 'artist'),
        ('key', 'time', 'tempo', 'year'),
        'chords',
    ]
    form = forms.SongForm

    class Media:
        css = dict(all=['fontawesomefree/css/all.min.css'])

    def get_url_name(self, name):
        info = dict(app_label=self.model._meta.app_label, model_name=self.model._meta.model_name, name=name)
        return '{app_label}_{model_name}_{name}'.format(**info)

    def save_model(self, request, obj, *args, **kwargs):
        result, _ = utils.get_chordpro_result(obj.get_data(), source_only=True)
        if result.returncode == 0:
            if result.stderr:
                msg = utils.format_html_from_bytes(result.stderr)
                messages.add_message(request, messages.WARNING, msg)
        else:
            msg = utils.format_html_from_bytes(result.stderr)
            messages.add_message(request, messages.ERROR, msg)
        super().save_model(request, obj, *args, **kwargs)

    def get_urls(self):
        urls = [
            path('<slug:pk>/pdf/chords/',
                self.admin_site.admin_view(views.SongPdfChordsView.as_view()),
                name=self.get_url_name('pdf_chords')
            ),
            path('<slug:pk>/pdf/lyrics/',
                self.admin_site.admin_view(views.SongPdfLyricsView.as_view()),
                name=self.get_url_name('pdf_lyrics')
            ),
            path('<slug:pk>/source/',
                self.admin_site.admin_view(views.SongSourceView.as_view()),
                name=self.get_url_name('source')
            ),
        ]
        return urls + super().get_urls()

    def pdf_chords_link(self, obj):
        name = 'admin:{}'.format(self.get_url_name('pdf_chords'))
        url = reverse(name, args=(obj.pk,))
        filename = utils.get_song_filename(obj.get_data(), 'pdf', suffix='chords')
        icon = '<i class="fa-regular fa-file-pdf fa-lg"></i>'
        return format_html('<a title="{}" href="{}">{}</a>', mark_safe(filename), url, mark_safe(icon))
    pdf_chords_link.short_description = _('chords')

    def pdf_lyrics_link(self, obj):
        name = 'admin:{}'.format(self.get_url_name('pdf_lyrics'))
        url = reverse(name, args=(obj.pk,))
        filename = utils.get_song_filename(obj.get_data(), 'pdf', suffix='lyrics')
        icon = '<i class="fa-regular fa-file-pdf fa-lg"></i>'
        return format_html('<a title="{}" href="{}">{}</a>', mark_safe(filename), url, mark_safe(icon))
    pdf_lyrics_link.short_description = _('lyrics')

    def source_link(self, obj):
        name = 'admin:{}'.format(self.get_url_name('source'))
        url = reverse(name, args=(obj.pk,))
        filename = utils.get_song_filename(obj.get_data(), 'cho')
        icon = '<i class="fa-regular fa-file-lines fa-lg"></i>'
        return format_html('<a title="{}" href="{}">{}</a>', mark_safe(filename), url, mark_safe(icon))
    source_link.short_description = _('source')
