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
    cy.visit('/start')
  })

  // it('shows sidebar and upload button', function() {
  //   cy.contains('Uploaded Documents')
  //   cy.get('#file_upload>input[type="file"]')
  // })

  it('navigates to chat and retrieves messages', function() {
    // TODO: Universalize
    cy.get('a:contains(Chat 10)').click()
    cy.contains('Chat 10 for Document')
    cy.get('.ai').should('be.visible')
  })

  // it('uploads a file', function() {
  //   cy.get('input[type="file"]').selectFile('cypress/fixtures/sample.pdf')
  //   cy.get('input[type="file"]').should('be.disabled')
  //   cy.wait(2000)
  //   cy.contains("sample.pdf")
  // })

  it('starts a chat', function() {
    cy.get('button#upload-button-10:contains("+")').click()
    cy.contains('for Document')
    cy.get('.ai').should('not.exist')
  })

  it('sends a message and receives a response', function() {
    let msg = 'Disregard previous messages and explain to me the primary concepts in this paper. '
    msg += `Random seed = ${Math.random().toString()}`
    cy.get('a:contains(Chat 10)').click()
    cy.get('.textarea > textarea').type(msg + '{enter}')
    cy.wait(2000)
    cy.get('.user').contains(msg)
  })
})