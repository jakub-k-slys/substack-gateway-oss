Feature: MCP comment engagement tools
  As an AI assistant
  I want to create, reply to, fetch, delete, like, unlike, and list replies to
  Substack post comments through MCP
  So that I can participate in post discussions programmatically

  Scenario: create_post_comment returns the created comment
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack post comment endpoint for post 55 returns id 900
    When I call the MCP tool create_post_comment with post_id 55 and body "hello"
    Then the MCP result field "id" is "900"

  Scenario: reply_to_post_comment returns the created reply
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack reader comment endpoint for id 42 resolves to post 77
    And the Substack comment reply endpoint for post 77 returns id 901
    When I call the MCP tool reply_to_post_comment with comment_id 42 and body "re"
    Then the MCP result field "id" is "901"

  Scenario: get_post_comment returns the comment
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack reader comment endpoint for id 42 resolves to post 77
    When I call the MCP tool get_post_comment with comment_id 42
    Then the MCP result field "id" is "42"

  Scenario: delete_post_comment returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack delete comment endpoint for id 42 returns status 204
    When I call the MCP tool delete_post_comment with comment_id 42
    Then the MCP result is "Comment 42 deleted successfully."

  Scenario: list_post_comment_replies returns the replies
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack comment replies endpoint for id 42 returns two replies
    When I call the MCP tool list_post_comment_replies with comment_id 42
    Then the MCP result list "items" has 2 items

  Scenario: like_post_comment returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack comment reaction endpoint for id 42 accepts a like
    When I call the MCP tool like_post_comment with comment_id 42
    Then the MCP result is "Comment 42 liked successfully."

  Scenario: unlike_post_comment returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack comment reaction endpoint for id 42 accepts an unlike
    When I call the MCP tool unlike_post_comment with comment_id 42
    Then the MCP result is "Comment 42 unliked successfully."
