Feature: Apollo login

  Scenario: Login with valid mobile number and OTP
    Given user opens Apollo application
    When user enters valid mobile number
    Then OTP screen should be visible
    When user enters OTP manually
    Then login should be submitted successfully