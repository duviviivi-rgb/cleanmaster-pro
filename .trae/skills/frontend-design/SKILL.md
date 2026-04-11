---
name: "frontend-design"
description: "Provides frontend design guidelines, best practices, and Figma implementation strategies. Invoke when designing UI components, creating design systems, or implementing Figma designs."
---

# Frontend Design Skill

## Overview

This skill provides comprehensive frontend design guidelines, best practices, and strategies for implementing Figma designs into React applications. It helps ensure consistent design across the application and provides practical implementation advice.

## Design Principles

### Core Design Principles
- **Consistency**: Maintain consistent design patterns, colors, typography, and spacing throughout the application
- **Clarity**: Ensure UI elements are clear and easy to understand
- **Accessibility**: Design for all users, including those with disabilities
- **Responsiveness**: Design for different screen sizes and devices
- **Performance**: Optimize design elements for performance

### Color System

#### Primary Colors
- **Primary**: #1E88E5 (Blue)
- **Secondary**: #4CAF50 (Green)
- **Accent**: #FF9800 (Orange)
- **Error**: #F44336 (Red)

#### Neutral Colors
- **White**: #FFFFFF
- **Light Gray**: #F5F5F5
- **Medium Gray**: #E0E0E0
- **Dark Gray**: #9E9E9E
- **Black**: #333333

### Typography

#### Font Hierarchy
- **Headings**: 16-24px, bold
- **Subheadings**: 14-16px, semibold
- **Body Text**: 14px, regular
- **Small Text**: 12px, regular

#### Font Family
- **Primary**: System default font (Segoe UI on Windows, San Francisco on macOS)
- **Fallback**: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif

### Spacing System

#### Base Spacing Unit
- **Base**: 4px

#### Spacing Scale
- **XS**: 8px
- **S**: 16px
- **M**: 24px
- **L**: 32px
- **XL**: 48px

### Component Design

#### Buttons
- **Primary**: Blue background, white text, rounded corners (4px)
- **Secondary**: White background, blue border, rounded corners (4px)
- **Disabled**: Gray background, light gray text

#### Cards
- **Shadow**: 0 2px 4px rgba(0, 0, 0, 0.1)
- **Border Radius**: 8px
- **Padding**: 16px

#### Forms
- **Input Fields**: Light gray border, blue border on focus
- **Labels**: 14px, semibold
- **Error Messages**: Red text, 12px

## Figma Implementation

### Design to Code Workflow
1. **Design Review**: Review Figma designs for consistency and feasibility
2. **Component Identification**: Identify reusable components
3. **Style Extraction**: Extract colors, typography, and spacing from Figma
4. **Component Implementation**: Implement components in React
5. **Validation**: Validate implementation against Figma designs

### Figma Best Practices
- **Use Components**: Create reusable components in Figma
- **Use Styles**: Define color, typography, and spacing styles in Figma
- **Use Auto Layout**: Use Figma's Auto Layout for responsive designs
- **Use Variants**: Create component variants for different states
- **Document Design System**: Document the design system in Figma

### Converting Figma to React
- **Measurements**: Use Figma's measurement tools to get exact dimensions
- **Export Assets**: Export images and icons from Figma
- **Copy Text**: Copy text content from Figma
- **Inspect Styles**: Use Figma's Inspect panel to get CSS values
- **Component Structure**: Map Figma components to React components

## Web Design Guidelines

### Layout
- **Grid System**: Use a 12-column grid system
- **Breakpoints**: Define responsive breakpoints (mobile, tablet, desktop)
- **Alignment**: Align elements to the grid for consistency

### Responsive Design
- **Mobile First**: Design for mobile first, then expand to larger screens
- **Flexbox**: Use flexbox for flexible layouts
- **Grid**: Use CSS Grid for complex layouts
- **Media Queries**: Use media queries for responsive adjustments

### Performance Optimization
- **Image Optimization**: Optimize images for web
- **Font Loading**: Optimize font loading
- **CSS Optimization**: Minify and bundle CSS
- **Component Lazy Loading**: Lazy load components when possible

## Examples

### Button Component

```jsx
// Primary Button
const PrimaryButton = ({ children, onClick, disabled }) => (
  <button
    className={`px-6 py-2 rounded-lg font-medium transition-colors ${
      disabled
        ? 'bg-gray-400 text-white cursor-not-allowed'
        : 'bg-blue-600 text-white hover:bg-blue-700'
    }`}
    onClick={onClick}
    disabled={disabled}
  >
    {children}
  </button>
);

// Secondary Button
const SecondaryButton = ({ children, onClick, disabled }) => (
  <button
    className={`px-6 py-2 rounded-lg font-medium transition-colors ${
      disabled
        ? 'border border-gray-300 text-gray-400 cursor-not-allowed'
        : 'border border-blue-600 text-blue-600 hover:bg-blue-50'
    }`}
    onClick={onClick}
    disabled={disabled}
  >
    {children}
  </button>
);
```

### Card Component

```jsx
const Card = ({ title, children, className = '' }) => (
  <div className={`bg-white rounded-lg shadow p-6 ${className}`}>
    {title && <h2 className="text-lg font-semibold mb-4">{title}</h2>}
    {children}
  </div>
);
```

### Form Input Component

```jsx
const FormInput = ({ label, name, value, onChange, error, required = false }) => (
  <div className="mb-4">
    <label
      htmlFor={name}
      className="block text-sm font-medium text-gray-700 mb-2"
    >
      {label} {required && <span className="text-red-500">*</span>}
    </label>
    <input
      id={name}
      name={name}
      value={value}
      onChange={onChange}
      className={`w-full px-3 py-2 border rounded-md ${error ? 'border-red-500' : 'border-gray-300'}`}
    />
    {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
  </div>
);
```