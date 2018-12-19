from django.contrib import admin
from chat.models import Thread, ChatMessage


class ChatMessage(admin.TabularInline):
    model = ChatMessage


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]

    class Meta:
        model = Thread
