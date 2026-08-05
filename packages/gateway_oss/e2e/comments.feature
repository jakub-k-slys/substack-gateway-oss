Feature: Post comment endpoints

  Scenario: Lifecycle — create, reply, list, react, delete
    Given valid credentials
    And a test post ID
    # 1) create a top-level comment under the post
    When I create a post comment with body "e2e top-level — safe to delete"
    Then the response status is 201
    And the response has field "id"
    Given the created post comment ID is saved as the top
    # 2) reply to it
    When I reply to the top post comment with body "e2e reply — safe to delete"
    Then the response status is 201
    And the response has field "id"
    Given the created post comment ID is saved as the reply
    # 3) list replies of the top — must contain our reply
    When I list replies of the top post comment
    Then the response status is 200
    And the response field "items" is a list
    And the items contain the reply post comment
    # 4) fetch the top comment
    When I fetch the top post comment
    Then the response status is 200
    And the response has field "id"
    # 5) react and un-react
    When I like the top post comment
    Then the response status is 204
    When I unlike the top post comment
    Then the response status is 204
    # 6) cleanup — delete reply, then top
    When I delete the reply post comment
    Then the response status is 204
    When I delete the top post comment
    Then the response status is 204

  Scenario: Reply to a non-existent comment returns 404
    Given valid credentials
    When I reply to post comment "1" with body "should fail"
    Then the response status is 404
