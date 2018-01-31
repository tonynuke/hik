from django.contrib import admin
from django.utils.html import format_html

from .models import *
# Register your models here.

admin.site.register(Client)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    # display item image
    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.image.url))

    image_tag.short_description = 'Image'

    list_display = ('title', 'quantity', 'price', 'description', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name', )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'get_price', )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_owner', 'get_price', )


admin.site.register(Order)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('telephone', 'message', )