"""
Utility functions for the polls application.
"""
from django.utils import timezone
from django.db.models import Sum


def get_published_questions_queryset(model_class):
    """
    Get a queryset of published questions (not future-dated).
    
    Args:
        model_class: The Question model class.
        
    Returns:
        QuerySet: Questions that have been published.
    """
    return model_class.objects.filter(pub_date__lte=timezone.now())


def calculate_vote_statistics(question):
    """
    Calculate voting statistics for a question.
    
    Args:
        question: Question instance.
        
    Returns:
        dict: Dictionary containing vote statistics.
    """
    choices = question.choices.all()
    total_votes = choices.aggregate(total=Sum('votes'))['total'] or 0
    
    statistics = {
        'total_votes': total_votes,
        'choices_count': choices.count(),
        'choices_with_votes': choices.filter(votes__gt=0).count(),
        'choice_stats': []
    }
    
    for choice in choices:
        choice_stat = {
            'choice': choice,
            'votes': choice.votes,
            'percentage': choice.vote_percentage(total_votes) if hasattr(choice, 'vote_percentage') else 0
        }
        statistics['choice_stats'].append(choice_stat)
    
    # Sort by votes descending
    statistics['choice_stats'].sort(key=lambda x: x['votes'], reverse=True)
    
    return statistics


def format_poll_results(question):
    """
    Format poll results for display.
    
    Args:
        question: Question instance.
        
    Returns:
        dict: Formatted results ready for template rendering.
    """
    stats = calculate_vote_statistics(question)
    
    return {
        'question': question,
        'total_votes': stats['total_votes'],
        'choices_count': stats['choices_count'],
        'has_votes': stats['total_votes'] > 0,
        'choice_results': stats['choice_stats']
    }