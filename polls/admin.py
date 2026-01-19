from django.contrib import admin
from django.db.models import Sum

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Inline admin for choices within question admin."""
    model = Choice
    extra = 3
    fields = ('choice_text', 'votes')
    readonly_fields = ('votes',) if not admin.site._registry else ()


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Question model."""
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {
            'fields': ['pub_date'], 
            'classes': ['collapse']
        }),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'total_votes')
    list_filter = ['pub_date', 'was_published_recently']
    search_fields = ['question_text']
    date_hierarchy = 'pub_date'
    ordering = ['-pub_date']
    
    def total_votes(self, obj):
        """Display total votes for this question."""
        total = obj.choices.aggregate(total=Sum('votes'))['total']
        return total or 0
    
    total_votes.short_description = 'Total Votes'
    total_votes.admin_order_field = 'choices__votes'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """Admin interface for Choice model."""
    list_display = ('choice_text', 'question', 'votes')
    list_filter = ['question', 'votes']
    search_fields = ['choice_text', 'question__question_text']
    ordering = ['-votes']
