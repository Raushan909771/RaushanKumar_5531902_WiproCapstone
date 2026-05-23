Feature: Apollo shop by category

  Scenario Outline: Validate category visibility
    Given user opens Apollo application
    Then category "<category_name>" should be "<expected_result>"

    Examples:
      | category_name    | expected_result |
      | Health Monitors  | visible         |
      | Pain Relief      | visible         |
      | Baby Care        | visible         |
      | Fake Category    | not_visible     |
      | Invalid Product  | not_visible     |

  Scenario: Open Health Monitors category
    Given user opens Apollo application
    When user opens Health Monitors category
    Then Health Monitors page should be opened

  Scenario: Apply Doctor S Choice filter
    Given user opens Apollo application
    When user opens Health Monitors category
    Then Health Monitors page should be opened
    Then Brands filter should be visible
    When user applies Doctor S Choice filter
    Then Health Monitors page should be opened

  Scenario: Add Doctor S Choice product to cart
    Given user opens Apollo application
    When user adds Doctor S Choice product to cart
    Then cart page should be opened
    Then selected product should be present in cart

  Scenario: Proceed after adding product to cart
    Given user opens Apollo application
    When user adds Doctor S Choice product to cart
    Then cart page should be opened
    Then selected product should be present in cart
    When user clicks Proceed button
    Then next cart step should be opened