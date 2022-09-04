from django.contrib import admin

# Register your models here.
from main.models import AdvUser, Job, SubCategory, Category


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_date', 'expired_date', 'min_price')
    list_display_links = ('title',)
    search_fields = ('title', 'description',)


class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug_sub_cat': ('tittle_sub_cat',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug_cat': ('title_cat',)}


admin.site.register(AdvUser)
admin.site.register(Job, JobAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
