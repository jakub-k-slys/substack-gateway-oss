Feature: MCP note engagement tools
  As an AI assistant
  I want to like, unlike, and reply to Substack notes through MCP
  So that I can manage note engagement programmatically

  Scenario: like_note returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack like-note endpoint returns status 200 for note 234058408
    When I call the MCP tool like_note with note_id 234058408
    Then the MCP result is "Note 234058408 liked successfully."

  Scenario: unlike_note returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack unlike-note endpoint returns status 204 for note 238483442
    When I call the MCP tool unlike_note with note_id 238483442
    Then the MCP result is "Note 238483442 unliked successfully."

  Scenario: reply_to_note returns the created reply id
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack note-reply endpoint returns id 555
    When I call the MCP tool reply_to_note with note_id 234058408 and body "nice"
    Then the MCP result field "id" is "555"

  Scenario: list_note_replies returns the replies
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack note-replies endpoint returns two replies for note 234058408
    When I call the MCP tool list_note_replies with note_id 234058408
    Then the MCP result list "items" has 2 items
