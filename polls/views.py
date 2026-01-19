from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import Choice, Question
from .utils import get_published_questions_queryset, format_poll_results


def health_check(request):  # noqa: ARG001
    """
    Health check endpoint for monitoring the application status.
    
    Returns:
        JsonResponse: A JSON response indicating the service is healthy.
    """
    response = {"status": "healthy", "message": "Service is running successfully"}
    return JsonResponse(response)

class IndexView(generic.ListView):
    """
    View to display the list of latest published questions.
    
    Shows the 5 most recent questions that have been published
    (excluding future-dated questions).
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        
        Returns:
            QuerySet: Up to 5 most recent published questions.
        """
        return get_published_questions_queryset(Question).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    View to display the details of a specific question with voting options.
    
    Only shows questions that have been published (not future-dated).
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        
        Returns:
            QuerySet: Published questions only.
        """
        return get_published_questions_queryset(Question)


class ResultsView(generic.DetailView):
    """
    View to display the voting results for a specific question.
    """
    model = Question
    template_name = 'polls/results.html'
    
    def get_context_data(self, **kwargs):
        """
        Add formatted poll results to the context.
        
        Returns:
            dict: Context data including formatted poll results.
        """
        context = super().get_context_data(**kwargs)
        context.update(format_poll_results(self.object))
        return context


@require_http_methods(["POST"])
def vote(request, question_id):
    """
    Handle voting for a specific question.
    
    Args:
        request: The HTTP request object.
        question_id (int): The ID of the question being voted on.
        
    Returns:
        HttpResponseRedirect: Redirect to results page on success.
        HttpResponse: Re-render detail page with error on failure.
    """
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except KeyError:
        # No choice was selected
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    except question.choice_set.model.DoesNotExist:
        # Invalid choice ID
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Selected choice does not exist.",
        })
    except ValueError:
        # Invalid choice ID format
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Invalid choice selection.",
        })
    else:
        # Successful vote
        selected_choice.votes += 1
        selected_choice.save()
        
        # Add success message
        messages.success(request, f'Your vote for "{selected_choice.choice_text}" has been recorded!')
        
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
