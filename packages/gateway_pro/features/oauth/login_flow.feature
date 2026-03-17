Feature: OAuth login flow
  As a gateway user
  I want to authenticate through the three-phase login flow
  So that I can connect my Substack account via OAuth

  Background:
    Given a registered gateway user "user@example.com" with password "secret123"
    And a valid OAuth auth request "test-req-id" for client "test-client"

  # ------------------------------------------------------------------
  # Phase 1 — email + password login
  # ------------------------------------------------------------------

  Scenario: Valid credentials redirect to token form
    When I submit the login form with email "user@example.com" and password "secret123" for request "test-req-id"
    Then the response status code is 302
    And the redirect location contains "/login/token?session_id="

  Scenario: Wrong password shows error
    When I submit the login form with email "user@example.com" and password "wrong" for request "test-req-id"
    Then the response status code is 200
    And the response body contains "Invalid email or password"

  Scenario: Unknown email shows error
    When I submit the login form with email "nobody@example.com" and password "secret123" for request "test-req-id"
    Then the response status code is 200
    And the response body contains "Invalid email or password"

  Scenario: Expired auth request shows error
    Given the auth request "test-req-id" has expired
    When I submit the login form with email "user@example.com" and password "secret123" for request "test-req-id"
    Then the response status code is 200
    And the response body contains "Session expired"

  Scenario: Empty fields show error
    When I submit the login form with empty email and password for request "test-req-id"
    Then the response status code is 200
    And the response body contains "All fields are required"

  # ------------------------------------------------------------------
  # Phase 2 — Substack token submission
  # ------------------------------------------------------------------

  Scenario: Valid token submission shows success page
    Given I have completed phase 1 login with "user@example.com" and "secret123"
    When I submit the token form with a valid Substack token and publication URL "https://test.substack.com"
    Then the response status code is 200
    And the response body contains "Step 3 of 3"
    And the response body contains "All done!"

  Scenario: Invalid Substack token shows error
    Given I have completed phase 1 login with "user@example.com" and "secret123"
    When I submit the token form with token "not-valid-base64!!!" and publication URL "https://test.substack.com"
    Then the response status code is 200
    And the response body contains "Step 2 of 3"

  Scenario: Expired login session shows error
    Given I have completed phase 1 login with "user@example.com" and "secret123"
    And the login session has expired
    When I submit the token form with a valid Substack token and publication URL "https://test.substack.com"
    Then the response status code is 200
    And the response body contains "Session expired"

  # ------------------------------------------------------------------
  # Phase 3 — success page
  # ------------------------------------------------------------------

  Scenario: Success page has a button instead of JavaScript redirect
    Given I have completed phase 1 login with "user@example.com" and "secret123"
    When I submit the token form with a valid Substack token and publication URL "https://test.substack.com"
    Then the response body contains "Complete setup"
    And the success page has a styled button link
    And the response body does not contain "<script>"
    And the response body does not contain "window.location"

  Scenario: Success page includes auth code and state in redirect link
    Given I have completed phase 1 login with "user@example.com" and "secret123"
    When I submit the token form with a valid Substack token and publication URL "https://test.substack.com"
    Then the response body contains "code="
    And the response body contains "state=some-state"

  # ------------------------------------------------------------------
  # Doctype rendering
  # ------------------------------------------------------------------

  Scenario: Login page doctype is not HTML-escaped
    When I visit the login page with request_id "test-req-id"
    Then the response status code is 200
    And the response body starts with "<!doctype html>"
    And the response body does not contain "&lt;!doctype html&gt;"

  Scenario: Token form doctype is not HTML-escaped
    When I visit the token form with session_id "any-sid"
    Then the response status code is 200
    And the response body starts with "<!doctype html>"
    And the response body does not contain "&lt;!doctype html&gt;"

  Scenario: Success page doctype is not HTML-escaped
    Given I have completed phase 1 login with "user@example.com" and "secret123"
    When I submit the token form with a valid Substack token and publication URL "https://test.substack.com"
    Then the response body starts with "<!doctype html>"
    And the response body does not contain "&lt;!doctype html&gt;"

  # ------------------------------------------------------------------
  # Data integrity
  # ------------------------------------------------------------------

  Scenario: Credentials are stored after token submission
    Given I have completed phase 1 login with "user@example.com" and "secret123"
    When I submit the token form with a valid Substack token and publication URL "https://test.substack.com"
    Then the user credentials are stored with publication URL "https://test.substack.com"

  Scenario: Auth code is created after token submission
    Given I have completed phase 1 login with "user@example.com" and "secret123"
    When I submit the token form with a valid Substack token and publication URL "https://test.substack.com"
    Then an auth code is created for client "test-client"

  Scenario: Login session and auth request are cleaned up
    Given I have completed phase 1 login with "user@example.com" and "secret123"
    When I submit the token form with a valid Substack token and publication URL "https://test.substack.com"
    Then the login session is deleted
    And the auth request is deleted
