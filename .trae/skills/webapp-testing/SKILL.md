---
name: "webapp-testing"
description: "Provides web application testing strategies, best practices, and tools. Invoke when testing web applications, creating test plans, or optimizing test coverage."
---

# Web App Testing Skill

## Overview

This skill provides comprehensive web application testing strategies, best practices, and tools. It helps ensure high-quality, reliable, and performant web applications through effective testing methodologies.

## Testing Types

### Unit Testing
- **Purpose**: Test individual components or functions in isolation
- **Tools**: Jest, Mocha, Jasmine, Vitest
- **Scope**: Testing specific functionality without dependencies
- **Benefits**: Fast execution, easy debugging, early issue detection

### Integration Testing
- **Purpose**: Test how components or services work together
- **Tools**: React Testing Library, Enzyme, Cypress
- **Scope**: Testing interactions between multiple components or services
- **Benefits**: Catch integration issues, verify component interactions

### End-to-End (E2E) Testing
- **Purpose**: Test the entire application flow from user perspective
- **Tools**: Cypress, Selenium, Playwright, Puppeteer
- **Scope**: Testing complete user journeys
- **Benefits**: Verify real-world user scenarios, catch end-to-end issues

### Performance Testing
- **Purpose**: Test application performance under various conditions
- **Tools**: Lighthouse, WebPageTest, JMeter, LoadRunner
- **Scope**: Testing load time, responsiveness, resource usage
- **Benefits**: Identify performance bottlenecks, ensure optimal user experience

### Accessibility Testing
- **Purpose**: Test application accessibility for users with disabilities
- **Tools**: axe-core, Lighthouse, WAVE
- **Scope**: Testing compliance with WCAG guidelines
- **Benefits**: Ensure inclusivity, avoid legal issues

### Security Testing
- **Purpose**: Test application security vulnerabilities
- **Tools**: OWASP ZAP, Burp Suite, SonarQube
- **Scope**: Testing for security flaws, vulnerabilities
- **Benefits**: Protect user data, prevent security breaches

## Testing Strategies

### Test-Driven Development (TDD)
- **Approach**: Write tests before writing code
- **Cycle**: Red (fail), Green (pass), Refactor
- **Benefits**: Better code design, higher test coverage, fewer bugs

### Behavior-Driven Development (BDD)
- **Approach**: Write tests in natural language to describe behavior
- **Tools**: Cucumber, Jest with BDD syntax
- **Benefits**: Better communication between stakeholders, clearer test intent

### Continuous Integration (CI) Testing
- **Approach**: Run tests automatically on code changes
- **Tools**: Jenkins, GitHub Actions, CircleCI, Travis CI
- **Benefits**: Early issue detection, faster feedback, consistent testing

### Smoke Testing
- **Approach**: Run basic tests to verify critical functionality
- **Scope**: Testing core features after changes
- **Benefits**: Quick validation, prevent broken builds

### Regression Testing
- **Approach**: Run existing tests to ensure changes don't break existing functionality
- **Scope**: Testing previously working features
- **Benefits**: Catch regressions early, maintain software quality

## Testing Tools

### Frontend Testing Tools
- **Jest**: JavaScript testing framework with built-in mocking
- **React Testing Library**: Testing library for React components
- **Cypress**: End-to-end testing framework
- **Playwright**: Cross-browser testing framework
- **Enzyme**: Testing utility for React

### Performance Testing Tools
- **Lighthouse**: Open-source tool for performance, accessibility, and best practices
- **WebPageTest**: Detailed performance analysis
- **JMeter**: Load testing tool
- **LoadRunner**: Enterprise load testing tool

### Accessibility Testing Tools
- **axe-core**: Accessibility testing engine
- **Lighthouse**: Includes accessibility audits
- **WAVE**: Web Accessibility Evaluation Tool
- **A11y**: Accessibility testing tools

### Security Testing Tools
- **OWASP ZAP**: Open-source security testing tool
- **Burp Suite**: Web vulnerability scanner
- **SonarQube**: Code quality and security scanner
- **Snyk**: Dependency vulnerability scanner

## Test Writing Best Practices

### Test Structure
- **Arrange-Act-Assert**: Set up test conditions, perform action, verify results
- **Clear Naming**: Use descriptive test names that explain what they're testing
- **Isolation**: Tests should be independent and not rely on each other
- **Coverage**: Test critical paths, edge cases, and error scenarios

### Test Maintenance
- **DRY Principle**: Don't repeat yourself in tests
- **Mocking**: Mock external dependencies to isolate tests
- **Fixtures**: Use test fixtures for consistent test data
- **Documentation**: Document test cases and their purpose

### Test Performance
- **Parallel Testing**: Run tests in parallel to speed up execution
- **Selective Testing**: Run only relevant tests for changes
- **Test Optimization**: Optimize slow tests
- **CI Integration**: Integrate tests into CI pipeline

## Testing Workflow

### Test Planning
1. **Identify Test Scenarios**: Define what to test based on requirements
2. **Prioritize Tests**: Focus on critical functionality first
3. **Create Test Cases**: Write detailed test cases
4. **Set Up Test Environment**: Configure test environment

### Test Execution
1. **Run Tests**: Execute tests according to plan
2. **Monitor Results**: Track test results and failures
3. **Debug Issues**: Investigate and fix test failures
4. **Update Tests**: Update tests as requirements change

### Test Reporting
1. **Generate Reports**: Create test reports with results
2. **Analyze Results**: Identify patterns in test failures
3. **Communicate Findings**: Share results with stakeholders
4. **Continuous Improvement**: Use insights to improve testing process

## Examples

### Unit Test Example (Jest)

```javascript
// src/components/Button.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button Component', () => {
  test('renders button with text', () => {
    render(<Button>Click Me</Button>);
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  test('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);
    fireEvent.click(screen.getByText('Click Me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('renders disabled button', () => {
    render(<Button disabled>Click Me</Button>);
    expect(screen.getByText('Click Me')).toBeDisabled();
  });

  test('renders button with different variants', () => {
    render(<Button variant="primary">Primary</Button>);
    render(<Button variant="secondary">Secondary</Button>);
    render(<Button variant="danger">Danger</Button>);
    
    expect(screen.getAllByRole('button')).toHaveLength(3);
  });
});
```

### End-to-End Test Example (Cypress)

```javascript
// cypress/e2e/homepage.cy.js
describe('Homepage', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('displays disk overview', () => {
    cy.get('.disk-overview').should('be.visible');
    cy.get('.disk-card').should('have.length.at.least', 1);
  });

  it('allows quick scan', () => {
    cy.get('button').contains('快速扫描').click();
    cy.get('.scan-progress').should('be.visible');
    cy.get('.scan-result').should('be.visible');
  });

  it('navigates to scan page', () => {
    cy.get('a').contains('扫描').click();
    cy.url().should('include', '/scan');
    cy.get('h1').contains('扫描');
  });

  it('navigates to clean page', () => {
    cy.get('a').contains('清理').click();
    cy.url().should('include', '/clean');
    cy.get('h1').contains('清理');
  });
});
```

### Performance Test Example (Lighthouse)

```javascript
// lighthouse.config.js
const { runLighthouse } = require('lighthouse');

async function runPerformanceTest() {
  const results = await runLighthouse({
    url: 'http://localhost:3000',
    options: {
      onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
    },
  });

  console.log('Performance score:', results.categories.performance.score * 100);
  console.log('Accessibility score:', results.categories.accessibility.score * 100);
  console.log('Best practices score:', results.categories['best-practices'].score * 100);
  console.log('SEO score:', results.categories.seo.score * 100);
}

runPerformanceTest();
```