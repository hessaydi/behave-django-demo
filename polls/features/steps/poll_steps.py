import datetime

from behave import given, then, when
from polls.models import Question
from django.urls import reverse
from django.utils import timezone
import requests

@given(u'A question {question_name} with text {question_text}')
def question_create(context, question_name, question_text):
    question = Question.objects.create(question_text=question_text,
                                       pub_date=timezone.now())
    context.questions[question_name] = question


@given(u'{question_name} has publish date set to {num_days} days {direction} today')
def step_impl(context, question_name, num_days, direction):
    question = context.questions[question_name]
    if direction.lower() == 'from':
        question.pub_date = timezone.now() + datetime.timedelta(days=int(num_days))
    elif direction.lower() == 'before':
        question.pub_date = timezone.now() - datetime.timedelta(days=int(num_days))
    else:
        raise NotImplementedError('Unknown direction ', direction)
    question.save()


@when(u'user visits the detail page for {question_name}')
def step_impl(context, question_name):
    question = context.questions[question_name]
    url = reverse('polls:detail', args=(question.id,))
    context.response = context.test.client.get(url)


@when(u'computer visits the detail page for {question_name}')
def step_impl(context, question_name):
    question = context.questions.get(question_name)
    url = reverse('polls:detail', args=(question.id,))
    context.response = context.test.client.get(url)


@then(u'user get a page not found error')
def step_impl(context):
    context.test.assertEqual(context.response.status_code, 404)


@then(u'user gets to see the details of {question_name}')
def step_impl(context, question_name):
    question = context.questions[question_name]
    context.test.assertContains(context.response, question.question_text)


@then(u'computer gets to see the details of {question_name} test')
def step_impl(context, question_name):
    question = context.questions.get(question_name)
    context.test.assertContains(context.response, question.question_text)


@given("I have the url of the application")
def step_impl(context):
    try:
        context.url = reverse('polls:it_test')
    except:
        raise NotImplementedError(u'STEP: Given I have the url of the application')


@when("I make an http post call")
def step_impl(context):
    context.response = context.test.client.get(context.url)

    # raise NotImplementedError(u'STEP: When I make an http post call')


@then("I must get a response with status code {status_code}")
def step_impl(context, status_code):
    print(context.response)
    assert str(context.response.status_code) == status_code
