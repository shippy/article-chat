// https://docs.cypress.io/guides/end-to-end-testing/amazon-cognito-authentication
const loginToCognito = (username: string, password: string) => {
  Cypress.log({
    displayName: 'COGNITO LOGIN',
    message: [`🔐 Authenticating | ${username}`],
    autoEnd: false
  })

  cy.visit('/')
  cy.contains('Log in', {
    includeShadowDom: true
  }).click()

  cy.origin(
    Cypress.env('cognito_domain'),
    {
      args: {
        username,
        password
      }
    },
    ({ username, password }) => {
      // Cognito log in page has some elements of the same id but are off screen.
      // We only want the visible elements to log in
      cy.get('input[name="username"]:visible').type(username)
      cy.get('input[name="password"]:visible').type(password, {
        // use log: false to prevent your password from showing in the Command Log
        log: false
      })
      cy.get('input[name="signInSubmitButton"]:visible').click()
    }
  )

  // give a few seconds for redirect to settle
  cy.wait(2000)

  // verify we have made it passed the login screen
  cy.contains('Uploaded Documents').should('be.visible')
}

// right now our custom command is light. More on this later!
Cypress.Commands.add('loginByCognito', (username: string, password: string) => {
  cy.session(
    `cognito-${username}`,
    () => {
      return loginToCognito(username, password)
    },
    {
      validate() {
        cy.visit('/start')
        // revalidate our session to make sure we are logged in
        cy.contains('Uploaded Documents').should('be.visible')
      }
    }
  )
})
