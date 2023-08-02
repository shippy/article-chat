describe('Logged-out Homepage spec', () => {
  it('loads with blurb', () => {
    cy.visit('http://localhost:5173')
    cy.get('img')
  }),
  it('has clickable login link', () => {
    cy.visit('http://localhost:5173')
    cy.contains('Log in').click()
  })
})

describe('Logged-in Homepage spec', () => {
  beforeEach(function() {
    cy.loginByCognito(Cypress.env('cognito_username'), Cypress.env('cognito_password'))
  })

  // it('shows sidebar and upload button', function() {
  //   cy.contains('Uploaded Documents')
  //   cy.get('#file_upload>input[type="file"]')
  // })

  it('navigates to chat and retrieves messages', function() {
    cy.visit('/start')
    // TODO: Universalize
    cy.get('a:contains(Chat 10)').click()
    cy.contains('Chat 10 for Document')
    cy.get('.ai').should('be.visible')
  })

  // it('uploads a file', function() {})

  // it('starts a chat', function() {})

  // it('sends a message and receives a response', function() {})
})