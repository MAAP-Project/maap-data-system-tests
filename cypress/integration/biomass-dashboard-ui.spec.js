/// <reference types="cypress" />

describe('biomass dashboard ui', () => {
  beforeEach(() => {

    const url = (() => {
      const stage = Cypress.env('STAGE')
      if (stage == "production")
        return "https://earthdata.nasa.gov/maap-biomass"
      else if (stage == "staging")
        return "https://uat.earthdata.nasa.gov/maap-biomass"
      else if (["main", "dit"].includes(stage) || stage.startsWith("refs"))
        return "https://biomass.dit.maap-project.org"
    })();

    cy.visit(url)
  })


  it('should have the correct title', () => {
    cy.title()
      .should('eq', 'Biomass Earthdata Dashboard')
  })

  it('should have populated the Products and Country Pilots menus', () => {

    // these use the ends with operator "$=" because in DIT, the URLs are off of the root (/),
    // whereas in Earthdata deployments for staging and prod they're off of /maap-biomass    
    cy.get('header > div > nav > div > div > ul > li > section > ul > li > a[href$="/products/global"] > span ')
      .should('have.text', 'All (Global)')

    cy.get('header > div > nav > div > div > ul > li > section > ul > li > a[href$="/products/cci_biomass"] > span ')
      .should('have.text', 'CCI Biomass 2020')

    cy.get('header > div > nav > div > div > ul > li > section > ul > li > a[href$="/country_pilots/japan"] > span ')
      .should('have.text', 'Japan')
  })

})
