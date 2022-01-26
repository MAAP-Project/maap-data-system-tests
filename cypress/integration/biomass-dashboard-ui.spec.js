/// <reference types="cypress" />

describe('biomass dashboard ui', () => {
  beforeEach(() => {
    // if stage == "production":
    //   return "https://earthdata.nasa.gov/maap-biomass"
    // elif stage == "staging":
    // return "https://uat.earthdata.nasa.gov/maap-biomass"
    // elif stage in ["main", "dit"]:
    // return "https://biomass.dit.maap-project.org"

    // Cypress starts out with a blank slate for each test
    // so we must tell it to visit our website with the `cy.visit()` command.
    // Since we want to visit the same URL at the start of all our tests,
    // we include it in our beforeEach function so that it runs before each test
    cy.visit('https://biomass.dit.maap-project.org')
  })


  it('should have the correct title', () => {
    cy.title().should('eq', 'Biomass Earthdata Dashboard')
  })

  it('should have populated the Products and Country Pilots menus', () => {
    cy.get(
      'header > div > nav > div > div > ul > li > section > ul > li > a[href="/products/global"] > span '
    ).should('have.text', 'All (Global)')

    cy.get(
      'header > div > nav > div > div > ul > li > section > ul > li > a[href="/products/cci_biomass"] > span '
    ).should('have.text', 'CCI Biomass 2020')

    cy.get(
      'header > div > nav > div > div > ul > li > section > ul > li > a[href="/country_pilots/japan"] > span '
    ).should('have.text', 'Japan')
  })

})
