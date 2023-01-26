from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class TitleInlineAdmin(admin.TabularInline):
    model = Title.genre.through
    min_num = 1
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ("name",)
    list_filter = ('category',)
    empty_value_display = '-пусто-'
    inlines = [TitleInlineAdmin]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('author', 'score', 'pub_date')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
