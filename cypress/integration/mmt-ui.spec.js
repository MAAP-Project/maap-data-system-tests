/// <reference types="cypress" />

describe('mmt ui', () => {
  beforeEach(() => {
    const url = (() => {
      const stage = Cypress.env('STAGE')
      if (stage == "production")
        return "https://mmt.maap-project.org"
      else if (["main", "dit"].includes(stage) || stage.startsWith("refs"))
        return "https://mmt.dit.maap-project.org"
    })();

    cy.visit(url)
  })

  it('should have the correct title', () => {
    cy.title().should('eq', 'Metadata Management Tool')
  })

  it('should have populated the about MMT box', () => {
    cy.get('#main-content > main > div > div > section:nth-child(1) > h2')
      .should('have.text', 'About the Metadata Management Tool')
  })

  it('should have populated the about CMR box', () => {
    cy.get('#main-content > main > div > div > section:nth-child(2) > h2')
      .should('have.text', 'About the CMR')
  })

})
