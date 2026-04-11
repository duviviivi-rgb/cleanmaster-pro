---
name: "vercel-deploy"
description: "Provides Vercel deployment strategies, best practices, and configuration guidelines. Invoke when deploying web applications to Vercel, optimizing deployment settings, or troubleshooting deployment issues."
---

# Vercel Deploy Skill

## Overview

This skill provides comprehensive Vercel deployment strategies, best practices, and configuration guidelines. It helps ensure smooth and optimized deployment of web applications to the Vercel platform.

## Vercel Basics

### What is Vercel?
- **Definition**: Vercel is a cloud platform for static sites and serverless functions
- **Key Features**: Automatic deployments, serverless functions, edge network, global CDN
- **Supported Frameworks**: Next.js, React, Vue, Angular, Svelte, and more
- **Pricing**: Free tier available, with paid plans for additional features

### Vercel Workflow
1. **Connect Repository**: Connect your GitHub, GitLab, or Bitbucket repository
2. **Configure Project**: Set up project settings and environment variables
3. **Deploy**: Vercel automatically deploys your application on every commit
4. **Preview**: Test changes with preview deployments
5. **Production**: Deploy to production with a custom domain

## Deployment Configuration

### Project Settings
- **Framework Preset**: Select the appropriate framework (Next.js, React, etc.)
- **Root Directory**: Specify the root directory of your project
- **Build Command**: Custom build command if needed
- **Output Directory**: Specify the build output directory
- **Environment Variables**: Configure environment variables for different environments

### Environment Variables
- **Development**: Variables for local development
- **Preview**: Variables for preview deployments
- **Production**: Variables for production deployments
- **Secret Management**: Use Vercel's secret management for sensitive information

### Build Configuration
- **Build Command**: Default build command based on framework
- **Install Command**: Custom install command if needed
- **Output Directory**: Default output directory based on framework
- **Node Version**: Specify Node.js version

## Deployment Strategies

### Continuous Deployment
- **Automatic Deployments**: Deploy on every commit to specified branches
- **Preview Deployments**: Create preview deployments for pull requests
- **Production Deployments**: Deploy to production from specific branches

### Branch Deployments
- **Main Branch**: Deploy to production
- **Feature Branches**: Create preview deployments
- **Staging Branch**: Deploy to staging environment

### Environment Management
- **Development**: Local development environment
- **Preview**: Staging environment for testing
- **Production**: Live production environment

## Optimization Techniques

### Performance Optimization
- **Static Generation**: Use static generation for faster page loads
- **Incremental Static Regeneration**: Update static pages without full rebuild
- **Edge Functions**: Run code at the edge for lower latency
- **Image Optimization**: Use Vercel's image optimization for faster loading

### Build Optimization
- **Caching**: Cache dependencies and build outputs
- **Parallel Builds**: Run builds in parallel for faster deployment
- **Optimized Dependencies**: Remove unused dependencies
- **Tree Shaking**: Remove unused code

### Security Best Practices
- **HTTPS**: Enable HTTPS for all deployments
- **CORS**: Configure CORS settings
- **Content Security Policy**: Set up content security policy
- **Environment Variables**: Use environment variables for sensitive information

## Common Issues and Solutions

### Deployment Failures
- **Build Errors**: Check build logs for error messages
- **Dependency Issues**: Ensure dependencies are properly installed
- **Environment Variables**: Verify environment variables are set correctly
- **Build Timeouts**: Optimize build process to avoid timeouts

### Performance Issues
- **Slow Load Times**: Optimize images, code, and assets
- **High TTFB**: Use static generation or edge functions
- **Large Bundle Size**: Implement code splitting and tree shaking
- **Serverless Function Cold Starts**: Optimize function code

### Configuration Issues
- **Routing Issues**: Configure Vercel rewrites and redirects
- **API Routes**: Set up API routes correctly
- **Custom Domains**: Configure DNS settings properly
- **SSL Certificates**: Ensure SSL certificates are valid

## Vercel CLI

### Installation
```bash
npm i -g vercel
```

### Common Commands
- **Login**: `vercel login`
- **Deploy**: `vercel`
- **Deploy to Production**: `vercel --prod`
- **Configure Project**: `vercel config`
- **View Deployments**: `vercel ls`
- **Remove Deployment**: `vercel remove`

### CLI Configuration
- **vercel.json**: Project configuration file
- **.vercelignore**: Files to ignore during deployment
- **Environment Variables**: Set via CLI or dashboard

## Examples

### vercel.json Configuration

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "NODE_ENV": "production"
  },
  "cleanUrls": true,
  "trailingSlash": false
}
```

### Next.js Deployment

```json
{
  "version": 2,
  "builds": [
    {
      "src": "next.config.js",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    }
  ]
}
```

### React Vite Deployment

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### Serverless Function Example

```javascript
// api/hello.js
module.exports = (req, res) => {
  const name = req.query.name || 'World';
  res.status(200).json({ message: `Hello, ${name}!` });
};
```

### Environment Variables Example

```bash
# Set environment variable via CLI
vercel env add API_KEY production

# Set multiple environment variables
vercel env add --git API_KEY

# List environment variables
vercel env ls
```