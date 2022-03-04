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

  it('should have populated the about box', () => {

    // these use the ends with operator "$=" because in DIT, the URLs are off of the root (/),
    // whereas in Earthdata deployments for staging and prod they're off of /maap-biomass    
    cy.get(
      '#main-content > main > div > div > section:nth-child(1) > h2'
    ).should('have.text', 'About the Metadata Management Tool')
  })

})
