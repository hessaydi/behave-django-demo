import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Model representing a poll question.
    
    Attributes:
        question_text (str): The text of the question.
        pub_date (datetime): The date and time when the question was published.
    """
    question_text = models.CharField(max_length=200, help_text="Enter the poll question")
    pub_date = models.DateTimeField('date published', help_text="Date and time of publication")

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self) -> str:
        """String representation of the Question."""
        return f"Question: {self.question_text}"

    def was_published_recently(self) -> bool:
        """
        Returns True if the question was published within the last 24 hours and not in the future.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """
    Model representing a choice for a poll question.
    
    Attributes:
        question (Question): The question this choice belongs to.
        choice_text (str): The text of the choice option.
        votes (int): The number of votes this choice has received.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200, help_text="Enter the choice option")
    votes = models.IntegerField(default=0, help_text="Number of votes received")

    class Meta:
        """
        Meta options for the model:
        - Orders instances by descending 'votes' and then by 'choice_text'.
        - Sets the singular verbose name to "Choice".
        - Sets the plural verbose name to "Choices".
        """
        ordering = ['-votes', 'choice_text']
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self) -> str:
        """String representation of the Choice."""
        return f"{self.choice_text} ({self.votes} votes)"

    def vote_percentage(self, total_votes: int | None = None) -> float:
        """
        Calculate the percentage of votes this choice received.

        Args:
            total_votes (int, optional): Total votes for the question. If None, calculated automatically.

        Returns:
            float: Percentage of votes (0-100).
        """
        if total_votes is None:
            total_votes = self.question.choices.aggregate(total=models.Sum('votes'))['total'] or 0
        if total_votes == 0:
            return 0.0
        return round((self.votes / total_votes) * 100, 2)
