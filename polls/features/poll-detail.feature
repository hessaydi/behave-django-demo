Feature: Get Settings for Polls Test
Implement different settings for polls - eg. published date

Background:

  Scenario: Questions published in future are not visible
    Given A question FutureQuestion with text Future Question
    And FutureQuestion has publish date set to 5 days from today
    When user visits the detail page for FutureQuestion
    Then user get a page not found error

  Scenario: Questions published in past are visible to the user
    Given A question PastQuestion with text Past Question
    And PastQuestion has publish date set to 5 days before today
    When user visits the detail page for PastQuestion
    Then user gets to see the details of PastQuestion

  Scenario: Question published in past are visible to the cumputer
    Given A question PastQuestion with text Past Question
    And PastQuestion has publish date set to 6 days before today
    When computer visits the detail page for PastQuestion
    Then computer gets to see the details of PastQuestion test

  Scenario: Calling the API pass with success
    Given I have the url of the application
    When I make an http post call
    Then I must get a response with status code 200

