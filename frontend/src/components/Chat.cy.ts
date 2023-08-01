import Chat from './Chat.vue'

describe('<Chat />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-vue
    cy.mount(Chat)
  })
})