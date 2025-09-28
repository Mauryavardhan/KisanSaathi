# Contributing to Kisan Saathi

Thank you for your interest in contributing to Kisan Saathi! This project was developed as an academic exercise to create a comprehensive agricultural advisory platform.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Create detailed issue reports** including:
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, Node.js version)

### Suggesting Features

1. **Open a feature request** with detailed description
2. **Explain the agricultural use case** and benefits for farmers
3. **Consider implementation feasibility** and provide suggestions

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch** from `main`
3. **Make your changes** following our coding standards
4. **Test your changes** thoroughly
5. **Submit a pull request** with clear description

## 🚀 Development Setup

### Prerequisites

- Node.js 18.0.0 or higher
- Git for version control

### Quick Start

```bash
# Clone your fork
git clone https://github.com/yourusername/KisanSaathi.git
cd KisanSaathi

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
npx prisma migrate dev --name init
npx prisma db seed

# Start development server
npm run dev
```

## 📝 Coding Standards

### File Organization

```
components/
├── ui/           # Reusable UI components
├── features/     # Feature-specific components  
├── layout/       # Layout components
└── forms/        # Form-related components

app/
├── dashboard/    # Dashboard pages
├── api/          # API routes
└── globals.css   # Global styles
```

### Naming Conventions

- **Files**: `kebab-case.tsx`
- **Components**: `PascalCase`
- **Functions**: `camelCase`
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Types/Interfaces**: `PascalCase`

### Git Commit Messages

Use clear, descriptive commit messages:

```
feat: add crop recommendation feature
fix: resolve authentication issue
docs: update setup instructions
style: improve dashboard layout
refactor: optimize database queries
test: add component tests
```

### CSS/Styling

- Use TailwindCSS utility classes
- Follow mobile-first responsive design
- Maintain consistent spacing and colors
- Use semantic HTML elements

## 🧪 Testing

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Check TypeScript
npm run type-check

# Run linting
npm run lint
```

### Writing Tests

- Write unit tests for utility functions
- Test React components with user interactions
- Ensure proper error handling
- Test responsive design on different screen sizes

## 📚 Documentation

### Code Documentation

- Use JSDoc comments for complex functions
- Document component props and interfaces
- Explain agricultural domain logic
- Keep README updated with new features

### Commit Guidelines

- Keep commits focused on single changes
- Write clear commit messages
- Reference issue numbers when applicable
- Update documentation for user-facing changes

## 🌱 Agricultural Domain

When working on agricultural features:

- Research proper farming terminology
- Understand seasonal crop cycles
- Consider regional farming practices
- Validate agricultural data accuracy

## 📞 Getting Help

### Community Support

- **GitHub Issues**: [Report bugs or ask questions](https://github.com/Mauryavardhan/KisanSaathi/issues)
- **Discussions**: [General discussions and ideas](https://github.com/Mauryavardhan/KisanSaathi/discussions)

### Development Help

For questions about:
- Setting up the development environment
- Understanding the codebase structure
- Implementing new features
- Testing and debugging

Create an issue with the "help wanted" label.

## 📜 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors:

- **Be respectful** to all community members
- **Be constructive** in feedback and discussions
- **Be patient** with questions and learning processes
- **Be collaborative** in problem-solving

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation updates

Thank you for contributing to Kisan Saathi and helping create better tools for farmers! 🌾