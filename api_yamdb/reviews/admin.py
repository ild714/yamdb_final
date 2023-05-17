from django.contrib import admin

from reviews.models import (
    YaMdbUser, Title, Genre, Category,
    GenreTitle, Review, Comment
)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    search_fields = ('username',)


admin.site.register(YaMdbUser, UserAdmin)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)
