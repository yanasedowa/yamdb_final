from django.contrib import admin


from reviews.models import (
    Category, Comment, Review, Title)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'
    list_editable = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    seach_fields = ('name')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('author', 'pub_date')


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
