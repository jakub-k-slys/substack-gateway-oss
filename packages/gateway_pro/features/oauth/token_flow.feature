Feature: OAuth token flow
  As a gateway operator
  I want the provider to issue and refresh tokens correctly
  So that agents can call tools beyond the initial access-token lifetime

  Background:
    Given the OAuth provider is configured with jwt secret "test-secret"
    And a registered OAuth client "client-1"
    And a valid auth code "code-abc" for client "client-1" belonging to user 42

  # ------------------------------------------------------------------
  # exchange_authorization_code
  # ------------------------------------------------------------------

  Scenario: Authorization code exchange returns access and refresh tokens
    When I exchange auth code "code-abc" for client "client-1"
    Then the token response contains an access token
    And the token response contains a refresh token
    And the access token expires in 3600 seconds
    And the access token contains user_id 42

  Scenario: Authorization code cannot be used twice
    When I exchange auth code "code-abc" for client "client-1"
    And I exchange auth code "code-abc" for client "client-1" again
    Then the second exchange raises an invalid_grant error

  # ------------------------------------------------------------------
  # load_refresh_token
  # ------------------------------------------------------------------

  Scenario: Valid refresh token is loaded with user_id
    When I exchange auth code "code-abc" for client "client-1"
    And I load the refresh token for client "client-1"
    Then the loaded refresh token has user_id 42

  Scenario: Revoked refresh token cannot be loaded
    When I exchange auth code "code-abc" for client "client-1"
    And the refresh token is revoked
    And I load the refresh token for client "client-1"
    Then the loaded refresh token is None

  # ------------------------------------------------------------------
  # exchange_refresh_token — the bug this PR fixes
  # ------------------------------------------------------------------

  Scenario: Refreshed access token preserves user_id
    When I exchange auth code "code-abc" for client "client-1"
    And I exchange the refresh token for client "client-1"
    Then the new access token contains user_id 42
    And the new refresh token is different from the original

  Scenario: Original refresh token is revoked after exchange
    When I exchange auth code "code-abc" for client "client-1"
    And I exchange the refresh token for client "client-1"
    And I load the original refresh token for client "client-1"
    Then the loaded refresh token is None

  Scenario: Refresh token can be used only once (rotation)
    When I exchange auth code "code-abc" for client "client-1"
    And I exchange the refresh token for client "client-1"
    And I exchange the original refresh token for client "client-1" again
    Then the second refresh raises an invalid_grant error
