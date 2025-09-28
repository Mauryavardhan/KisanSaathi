# Contributing to Kisan Saathi

Thank you for your interest in contributing to Kisan Saathi! We welcome contributions from the community to help improve this AI-powered agricultural advisory platform.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information** including:
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Screenshots or error messages
   - Environment details (OS, browser, Node.js version)

### Suggesting Features

1. **Check the roadmap** to see if the feature is already planned
2. **Open a feature request** with detailed description
3. **Explain the use case** and why it would benefit farmers
4. **Consider implementation complexity** and provide suggestions

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch** from `main`
3. **Make your changes** following our coding standards
4. **Write tests** for new functionality
5. **Update documentation** if needed
6. **Submit a pull request**

## 🚀 Development Setup

### Prerequisites

- Node.js 18.0.0 or higher
- PostgreSQL 14.0 or higher
- Git

### Quick Start

```bash
# Clone your fork
git clone https://github.com/yourusername/kisan-saathi-frontend.git
cd kisan-saathi-frontend

# Run setup script
./scripts/dev-setup.sh

# Start development server
npm run dev
```

### Development Workflow

1. **Sync with upstream**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes and commit**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Coding Standards

### TypeScript

- Use TypeScript for all new code
- Define proper interfaces and types
- Avoid `any` type unless absolutely necessary
- Use strict mode settings

### React Components

```typescript
// ✅ Good
interface ButtonProps {
  variant?: 'primary' | 'secondary'
  children: React.ReactNode
  onClick?: () => void
}

export function Button({ variant = 'primary', children, onClick }: ButtonProps) {
  return (
    <button 
      className={cn('btn', variant === 'primary' && 'btn-primary')}
      onClick={onClick}
    >
      {children}
    </button>
  )
}

// ❌ Avoid
export function Button(props: any) {
  return <button {...props} />
}
```

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

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add crop recommendation feature
fix: resolve authentication issue
docs: update API documentation
style: improve dashboard layout
refactor: optimize database queries
test: add unit tests for auth service
```

### CSS/Styling

- Use TailwindCSS utility classes
- Create component variants with `cva`
- Follow mobile-first responsive design
- Use CSS custom properties for theming

```typescript
// ✅ Good
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        secondary: "bg-secondary text-secondary-foreground",
      },
      size: {
        default: "h-10 px-4",
        sm: "h-9 px-3",
      },
    },
  }
)
```

## 🧪 Testing

### Unit Tests

```typescript
import { render, screen } from '@testing-library/react'
import { Button } from '../button'

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button')).toHaveTextContent('Click me')
  })

  it('handles click events', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    screen.getByRole('button').click()
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

### Integration Tests

```typescript
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { CropRecommendation } from '../crop-recommendation'

describe('CropRecommendation', () => {
  it('submits form and displays results', async () => {
    render(<CropRecommendation />)
    
    await userEvent.type(screen.getByLabelText(/location/i), 'Delhi')
    await userEvent.selectOptions(screen.getByLabelText(/soil type/i), 'loamy')
    await userEvent.click(screen.getByRole('button', { name: /get recommendations/i }))
    
    await waitFor(() => {
      expect(screen.getByText(/recommended crops/i)).toBeInTheDocument()
    })
  })
})
```

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run specific test file
npm test button.test.tsx

# Generate coverage report
npm run test:coverage
```

## 🌍 Internationalization

### Adding New Languages

1. **Create language file**
   ```typescript
   // locales/hi.json
   {
     "common": {
       "loading": "लोड हो रहा है...",
       "error": "त्रुटि",
       "success": "सफलता"
     },
     "dashboard": {
       "welcome": "स्वागत है",
       "askQuestion": "प्रश्न पूछें"
     }
   }
   ```

2. **Update language configuration**
   ```typescript
   // lib/i18n.ts
   export const supportedLanguages = [
     { code: 'en', name: 'English' },
     { code: 'hi', name: 'हिंदी' },
     // Add new language here
   ]
   ```

### Using Translations

```typescript
import { useTranslation } from 'next-i18next'

export function Dashboard() {
  const { t } = useTranslation('dashboard')
  
  return (
    <div>
      <h1>{t('welcome')}</h1>
      <button>{t('askQuestion')}</button>
    </div>
  )
}
```

## 🔒 Security Guidelines

### API Security

- Validate all inputs on both client and server
- Use parameterized queries to prevent SQL injection
- Implement rate limiting for API endpoints
- Never expose sensitive data in client-side code

### Authentication

- Use secure session management
- Implement proper CSRF protection
- Validate user permissions for all actions
- Use HTTPS in production

### Data Privacy

- Follow GDPR and local privacy regulations
- Minimize data collection to what's necessary
- Implement proper data encryption
- Provide clear privacy policies

## 📚 Documentation

### Code Documentation

```typescript
/**
 * Processes crop recommendation request
 * @param request - The crop recommendation parameters
 * @param userContext - User's farming context
 * @returns Promise<CropRecommendation[]> Array of recommended crops
 * @throws {ValidationError} When required parameters are missing
 * @example
 * ```typescript
 * const recommendations = await getCropRecommendations({
 *   soilType: 'loamy',
 *   location: 'Punjab'
 * })
 * ```
 */
export async function getCropRecommendations(
  request: CropRecommendationRequest,
  userContext?: UserContext
): Promise<CropRecommendation[]> {
  // Implementation
}
```

### API Documentation

- Document all endpoints with OpenAPI/Swagger
- Provide request/response examples
- Include error codes and messages
- Keep documentation updated with code changes

## 🚀 Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality 
- **PATCH** version for bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version number bumped
- [ ] Database migrations tested
- [ ] Performance benchmarks meet standards
- [ ] Security review completed

## 📞 Getting Help

### Community Support

- **Discord**: [Join our community](https://discord.gg/kisansaathi)
- **GitHub Discussions**: [Ask questions](https://github.com/yourusername/kisan-saathi-frontend/discussions)
- **Email**: dev@kisansaathi.com

### Mentorship

New contributors can request mentorship for:
- First-time contributions
- Complex feature development
- Code review and best practices
- Career guidance in agricultural technology

## 📜 Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

### Our Standards

- **Be respectful** to all community members
- **Be inclusive** and welcoming to newcomers
- **Be constructive** in feedback and discussions
- **Be patient** with questions and learning processes
- **Be collaborative** in problem-solving

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Annual contributor spotlight
- Conference speaking opportunities

## 📊 Metrics and Goals

We track these metrics to measure our impact:
- **Code Quality**: Test coverage, linting scores
- **Performance**: Page load times, API response times
- **Accessibility**: WCAG compliance scores
- **User Experience**: Task completion rates, user satisfaction
- **Agricultural Impact**: Number of farmers helped, success stories

Thank you for contributing to Kisan Saathi and helping farmers across India! 🌾
