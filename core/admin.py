from django.contrib import admin
from .models import Author, Work, Category, CorpusEntry
from .models import Author, Work, Category, CorpusEntry, GameImage

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender')
    search_fields = ('full_name',)

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_year')
    list_filter = ('author', 'genre')
    search_fields = ('title',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(GameImage)
class GameImageAdmin(admin.ModelAdmin):
    list_display = ('correct_answer', 'image')

@admin.register(CorpusEntry)
class CorpusEntryAdmin(admin.ModelAdmin):
    list_display = ('entry_title', 'category', 'work', 'short_meaning')
    search_fields = ('entry_title', 'meaning', 'example_text')
    list_filter = ('category', 'work__author', 'work')

    def short_meaning(self, obj):
        return obj.meaning[:50] + "..." if obj.meaning else ""
    short_meaning.short_description = "Мағынасы"
