/// <reference types="cypress" />
import FileUpload from './FileUpload.vue'

describe('<FileUpload />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-vue
    cy.mount(FileUpload)
  })
})