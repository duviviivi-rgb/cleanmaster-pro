---
name: "react-best-practices"
description: "Provides React development best practices, code guidelines, and optimization strategies. Invoke when developing React components, optimizing React applications, or reviewing React code."
---

# React Best Practices Skill

## Overview

This skill provides comprehensive React development best practices, code guidelines, and optimization strategies. It helps ensure high-quality, maintainable, and performant React applications.

## Core Principles

### Component Design
- **Single Responsibility**: Each component should have a single, well-defined purpose
- **Reusability**: Design components to be reusable across the application
- **Composability**: Build complex components by composing simpler ones
- **Predictability**: Components should behave predictably based on their props

### State Management
- **Local State**: Use local state for component-specific data
- **Lifting State Up**: Lift state to the nearest common ancestor when multiple components need access
- **Context API**: Use Context API for global state that affects many components
- **State Libraries**: Consider state management libraries like Redux for complex applications

### Performance Optimization
- **Memoization**: Use `React.memo`, `useMemo`, and `useCallback` to avoid unnecessary re-renders
- **Virtualization**: Use virtualization for long lists
- **Code Splitting**: Split code into smaller chunks to reduce initial load time
- **Lazy Loading**: Lazy load components that are not immediately needed
- **Optimizing Rendering**: Avoid unnecessary re-renders by optimizing state updates

## Code Guidelines

### File Structure
- **Component Files**: Each component should have its own file
- **Organizing Components**: Group related components in directories
- **Naming Conventions**: Use PascalCase for component names, camelCase for variables and functions
- **Index Files**: Use index files to simplify imports

### Component Structure
- **Functional Components**: Use functional components with hooks
- **Props Typing**: Use TypeScript or PropTypes for prop validation
- **Component Organization**: Order component elements logically (imports, types, component, exports)
- **Commenting**: Add comments for complex logic or non-obvious code

### Hooks Usage
- **Hooks Order**: Call hooks in the same order every time
- **Hooks Rules**: Only call hooks at the top level, not inside loops, conditions, or nested functions
- **Custom Hooks**: Create custom hooks for reusable logic
- **Dependency Arrays**: Properly manage dependency arrays in `useEffect`, `useCallback`, and `useMemo`

### TypeScript Best Practices
- **Type Definitions**: Define clear and accurate types for props, state, and return values
- **Union Types**: Use union types for values that can have multiple types
- **Generics**: Use generics for reusable components and functions
- **Type Guards**: Use type guards to narrow types
- **Interface vs Type**: Use interfaces for object types, types for unions and intersections

## Common Patterns

### Container and Presentational Components
- **Container Components**: Manage state and logic
- **Presentational Components**: Focus on rendering UI

### Higher-Order Components (HOCs)
- **Purpose**: Reuse component logic
- **Naming**: Prefix HOCs with `with`
- **Props Passing**: Pass through unrelated props to the wrapped component

### Render Props
- **Purpose**: Share code between components using a prop whose value is a function
- **Flexibility**: Allows more flexible composition than HOCs

### Custom Hooks
- **Purpose**: Extract and reuse stateful logic
- **Naming**: Prefix custom hooks with `use`
- **Composition**: Combine multiple hooks to create more complex logic

## Optimization Techniques

### Performance Monitoring
- **React DevTools**: Use React DevTools to profile component performance
- **Chrome DevTools**: Use Chrome DevTools to analyze network requests and rendering performance
- **Lighthouse**: Use Lighthouse to audit performance, accessibility, and best practices

### Bundle Optimization
- **Tree Shaking**: Remove unused code
- **Minification**: Minify CSS and JavaScript
- **Compression**: Enable gzip or Brotli compression
- **CDN**: Use a CDN to serve static assets

### Render Optimization
- **Key Prop**: Always use a unique `key` prop for items in a list
- **Pure Components**: Use `React.memo` for components that render the same output with the same props
- **Avoid Inline Objects**: Avoid creating new objects or functions in the render method
- **Batch Updates**: React batches state updates automatically, but be mindful of when updates occur

## Testing

### Testing Strategies
- **Unit Testing**: Test individual components in isolation
- **Integration Testing**: Test how components work together
- **End-to-End Testing**: Test the entire application flow

### Testing Tools
- **Jest**: JavaScript testing framework
- **React Testing Library**: Test React components
- **Cypress**: End-to-end testing
- **Storybook**: Develop and test components in isolation

### Testing Best Practices
- **Test Behavior, Not Implementation**: Test what the component does, not how it does it
- **Mock Dependencies**: Mock external dependencies
- **Test Edge Cases**: Test edge cases and error scenarios
- **Maintainable Tests**: Write tests that are easy to understand and maintain

## Examples

### Component Structure

```tsx
// src/components/Button/Button.tsx
import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  className?: string;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  className = '',
}) => {
  const baseClasses = 'rounded-md font-medium transition-colors';
  
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700',
  }[variant];
  
  const sizeClasses = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg',
  }[size];
  
  const disabledClass = disabled ? 'opacity-50 cursor-not-allowed' : '';
  
  return (
    <button
      className={`${baseClasses} ${variantClasses} ${sizeClasses} ${disabledClass} ${className}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};

export default Button;
```

### Custom Hook

```tsx
// src/hooks/useLocalStorage.ts
import { useState, useEffect } from 'react';

function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((val: T) => T)) => void] {
  // Get from local storage then
  // parse stored json or return initialValue
  const readValue = (): T => {
    if (typeof window === 'undefined') {
      return initialValue;
    }

    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  };

  // State to store our value
  const [storedValue, setStoredValue] = useState<T>(readValue);

  // Return a wrapped version of useState's setter function that
  // persists the new value to localStorage
  const setValue = (value: T | ((val: T) => T)) => {
    try {
      // Allow value to be a function so we have the same API as useState
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;

      // Save state
      setStoredValue(valueToStore);

      // Save to local storage
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
      }
    } catch (error) {
      console.warn(`Error setting localStorage key "${key}":`, error);
    }
  };

  useEffect(() => {
    // Listen for changes to the key in other windows
    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === key && event.newValue) {
        setStoredValue(JSON.parse(event.newValue));
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [key]);

  return [storedValue, setValue];
}

export default useLocalStorage;
```

### Performance Optimization

```tsx
// src/components/ExpensiveComponent.tsx
import React, { useMemo } from 'react';

interface ExpensiveComponentProps {
  items: number[];
}

const ExpensiveComponent: React.FC<ExpensiveComponentProps> = ({ items }) => {
  // Memoize the result of the expensive calculation
  const expensiveResult = useMemo(() => {
    console.log('Performing expensive calculation...');
    return items.reduce((acc, item) => acc + item * item, 0);
  }, [items]); // Only recalculate when items changes

  return (
    <div>
      <h2>Expensive Component</h2>
      <p>Result: {expensiveResult}</p>
    </div>
  );
};

// Memoize the component itself to avoid unnecessary re-renders
export default React.memo(ExpensiveComponent);
```