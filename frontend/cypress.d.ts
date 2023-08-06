import { mount } from 'cypress/vue';

declare global {
  namespace Cypress {
    interface Chainable {
      mount: typeof mount;
      /**
       * Custom command to authenticate with Cognito credentials on the hosted UI.
       * @example cy.loginByCognito(Cypress.env('cognito_username'), Cypress.env('cognito_password'))
       */
      loginByCognito(username: string, password: string): Chainable<JQuery<HTMLElement>>
    }
  }
}