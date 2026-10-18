Feature: MCP draft tools
  As a Claude AI assistant
  I want to use MCP tools to manage Substack post drafts
  So that I can read, create, and delete drafts programmatically

  Scenario: list_drafts returns draft list
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack list-drafts endpoint returns the sample response
    When I call the MCP tool list_drafts
    Then the MCP result field "items" is not null

  Scenario: get_draft returns draft data
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack get-draft endpoint returns the sample response for draft 189535264
    When I call the MCP tool get_draft with draft_id 189535264
    Then the MCP result field "title" is not null

  Scenario: create_draft returns created draft data
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack create-draft endpoint returns the sample response
    When I call the MCP tool create_draft with title "Test Draft"
    Then the MCP result field "id" is not null
    And the MCP result field "uuid" is not null

  Scenario: delete_draft returns confirmation message
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack delete-draft endpoint returns status 204 for draft 189535264
    When I call the MCP tool delete_draft with draft_id 189535264
    Then the MCP result is "Draft 189535264 deleted successfully."

  Scenario: update_draft rejects a stale expected_updated_at with a tool error
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack get-draft endpoint returns the sample response for draft 189535264
    When I call the MCP tool update_draft with draft_id 189535264, title "late edit" and expected_updated_at "2026-01-01T00:00:00.000Z"
    Then the MCP call fails with a tool error containing "changed since it was read"
    And no Substack PUT request was sent

  Scenario: update_draft with a matching expected_updated_at succeeds
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack get-draft endpoint returns the sample response for draft 189535264
    And the Substack update-draft endpoint returns the sample response for draft 189535264
    When I call the MCP tool update_draft with draft_id 189535264, title "test1" and expected_updated_at "2026-03-01T09:53:35.569Z"
    Then the MCP result field "title" is "test1"
    And the MCP result field "updated_at" is "2026-03-01T09:53:35.569Z"

  Scenario: create_draft with a broken substack-node fence is a tool error naming the line
    Given a valid MCP token and publication URL "https://example.substack.com"
    And the Substack user-settings endpoint returns the sample response
    When I call the MCP tool create_draft with a broken substack-node fence body
    Then the MCP call fails with a tool error containing "line 1"
