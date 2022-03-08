/// <reference types="cypress" />

describe('UMF (questionaire) ui', () => {
  beforeEach(() => {
    const url = (() => {
      const stage = Cypress.env('STAGE')
      if (stage == "production")
        return "https://questionnaire.maap-project.org"
      else if (["main", "dit"].includes(stage) || stage.startsWith("refs"))
        return "https://questionnaire.dit.maap-project.org"
    })();

    cy.visit(url)
  })

  it('should have the correct title', () => {
    cy.title()
      .should('eq', 'MAAP User Shared Data Questionnaire')
  })

  it('should have a visible Start button', () => {
    cy.get('body > div > div > div > div > div.details_holder > div > div:nth-child(1) > button')
      .contains('Start New')
  })

  it('should have populated blurb', () => {
    cy.get('body > div > div > div > div > div.details_holder > p:nth-child(1)')
      .contains('Thank you for sharing your data with the MAAP community! As a reminder, data shared through this process should be provided by you. You are responsible for any content you upload to the MAAP and please do not post content that isn’t your own.')
  })

})
