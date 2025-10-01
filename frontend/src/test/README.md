# React Testing Library Best Practices

This guide covers best practices for testing React components using React Testing Library with Vitest.

## Testing Philosophy

React Testing Library follows the principle: **"The more your tests resemble the way your software is used, the more confidence they can give you."**

### Core Principles

1. **Test behavior, not implementation**
2. **Query by accessibility attributes when possible**
3. **Focus on user interactions**
4. **Avoid testing internal state or props directly**

## Query Priority

Use queries in this order of preference:

### 1. Accessible to Everyone
```tsx
// ✅ Best - accessible to everyone
screen.getByRole('button', { name: /submit/i })
screen.getByLabelText(/username/i)
screen.getByDisplayValue(/john/i)
```

### 2. Semantic Queries
```tsx
// ✅ Good - semantic HTML
screen.getByAltText(/profile picture/i)
screen.getByTitle(/close/i)
```

### 3. Test IDs (Last Resort)
```tsx
// ⚠️ Only if other queries don't work
screen.getByTestId('complex-component')
```

## Common Testing Patterns

### Basic Component Test
```tsx
import { render, screen } from '@/test/utils'
import { Button } from './Button'

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument()
  })
})
```

### Testing User Interactions
```tsx
import { renderWithUser } from '@/test/utils'
import { Counter } from './Counter'

describe('Counter', () => {
  it('increments when button is clicked', async () => {
    const { user } = renderWithUser(<Counter />)

    const button = screen.getByRole('button', { name: /increment/i })
    const count = screen.getByText('0')

    await user.click(button)

    expect(screen.getByText('1')).toBeInTheDocument()
  })
})
```

### Testing Forms
```tsx
import { renderWithUser } from '@/test/utils'
import { ContactForm } from './ContactForm'

describe('ContactForm', () => {
  it('submits form with correct data', async () => {
    const mockSubmit = vi.fn()
    const { user } = renderWithUser(<ContactForm onSubmit={mockSubmit} />)

    await user.type(screen.getByLabelText(/name/i), 'John Doe')
    await user.type(screen.getByLabelText(/email/i), 'john@example.com')
    await user.click(screen.getByRole('button', { name: /submit/i }))

    expect(mockSubmit).toHaveBeenCalledWith({
      name: 'John Doe',
      email: 'john@example.com'
    })
  })
})
```

### Testing Async Components
```tsx
import { render, screen, waitFor } from '@/test/utils'
import { UserProfile } from './UserProfile'

describe('UserProfile', () => {
  it('displays user data after loading', async () => {
    render(<UserProfile userId="123" />)

    expect(screen.getByText(/loading/i)).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.getByText(/john doe/i)).toBeInTheDocument()
    })

    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
  })
})
```

### Testing Error States
```tsx
import { render, screen } from '@/test/utils'
import { ErrorBoundary } from './ErrorBoundary'

const ThrowError = () => {
  throw new Error('Test error')
}

describe('ErrorBoundary', () => {
  it('displays error message when child component throws', () => {
    render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    )

    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument()
  })
})
```

### Testing with Providers
```tsx
import { render, screen } from '@/test/utils'
import { ThemeButton } from './ThemeButton'

describe('ThemeButton', () => {
  it('renders with dark theme', () => {
    render(<ThemeButton />, {
      providerProps: { theme: 'dark' }
    })

    expect(screen.getByRole('button')).toHaveClass('dark-theme')
  })
})
```

## Custom Matchers

### Common Jest-DOM Matchers
```tsx
// Visibility
expect(element).toBeVisible()
expect(element).toBeInTheDocument()

// Content
expect(element).toHaveTextContent('Hello')
expect(element).toContainHTML('<span>Hello</span>')

// Attributes
expect(element).toHaveAttribute('disabled')
expect(element).toHaveClass('active')
expect(element).toHaveStyle('color: red')

// Form elements
expect(input).toHaveValue('test')
expect(input).toBeChecked()
expect(input).toBeInvalid()
```

## Mocking Strategies

### Mock API Calls
```tsx
import { vi } from 'vitest'

// Mock module
vi.mock('@/lib/api', () => ({
  fetchUser: vi.fn(() => Promise.resolve({ name: 'John Doe' }))
}))
```

### Mock React Hooks
```tsx
import { vi } from 'vitest'
import * as useBreakpoint from '@/hooks/useBreakpoint'

// Mock hook return value
vi.spyOn(useBreakpoint, 'useBreakpoint').mockReturnValue('lg')
```

### Mock Next.js Router
```tsx
// Already configured in setup.ts
// Use in tests:
const mockPush = vi.fn()
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush })
}))
```

## Accessibility Testing

### Test ARIA Attributes
```tsx
it('has proper accessibility attributes', () => {
  render(<Modal title="Settings" />)

  expect(screen.getByRole('dialog')).toHaveAttribute('aria-labelledby')
  expect(screen.getByRole('dialog')).toHaveAttribute('aria-modal', 'true')
})
```

### Test Keyboard Navigation
```tsx
it('supports keyboard navigation', async () => {
  const { user } = renderWithUser(<Menu />)

  await user.tab()
  expect(screen.getByRole('menuitem')).toHaveFocus()

  await user.keyboard('{ArrowDown}')
  expect(screen.getByRole('menuitem', { name: /second item/i })).toHaveFocus()
})
```

## Performance Testing

### Test Loading States
```tsx
it('shows loading spinner while fetching data', () => {
  render(<DataList />)
  expect(screen.getByRole('status', { name: /loading/i })).toBeInTheDocument()
})
```

### Test Error Boundaries
```tsx
it('catches and displays errors gracefully', () => {
  const consoleError = vi.spyOn(console, 'error').mockImplementation(() => {})

  render(
    <ErrorBoundary>
      <ComponentThatThrows />
    </ErrorBoundary>
  )

  expect(screen.getByText(/error occurred/i)).toBeInTheDocument()
  consoleError.mockRestore()
})
```

## Common Anti-Patterns

### ❌ Don't Test Implementation Details
```tsx
// Bad - testing internal state
expect(component.state.isOpen).toBe(true)

// Good - testing behavior
expect(screen.getByText(/modal content/i)).toBeVisible()
```

### ❌ Don't Use Container Queries
```tsx
// Bad - using container
const { container } = render(<Button />)
expect(container.firstChild).toHaveClass('btn')

// Good - using screen
expect(screen.getByRole('button')).toHaveClass('btn')
```

### ❌ Don't Query by Class Names
```tsx
// Bad - implementation detail
screen.getByClassName('submit-button')

// Good - semantic meaning
screen.getByRole('button', { name: /submit/i })
```

## Debugging Tests

### Use screen.debug()
```tsx
it('debugs the rendered DOM', () => {
  render(<Component />)
  screen.debug() // Prints the DOM to console
})
```

### Use screen.logTestingPlaygroundURL()
```tsx
it('provides testing playground URL', () => {
  render(<Component />)
  screen.logTestingPlaygroundURL() // Provides URL to testing playground
})
```

### Use Custom Debug Function
```tsx
import { logRoles } from '@testing-library/react'

it('shows available roles', () => {
  const { container } = render(<Component />)
  logRoles(container) // Shows all available roles
})
```

## File Organization

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── index.ts
│   └── Modal/
│       ├── Modal.tsx
│       ├── Modal.test.tsx
│       └── index.ts
├── test/
│   ├── setup.ts
│   ├── utils.tsx
│   ├── mocks/
│   │   ├── api.ts
│   │   └── router.ts
│   └── fixtures/
│       └── users.ts
```

## Naming Conventions

- Test files: `Component.test.tsx`
- Test suites: `describe('ComponentName', () => {})`
- Test cases: `it('should do something when condition', () => {})`
- Mock functions: `mockFunctionName`
- Test IDs: `data-testid="component-name"`

This guide ensures your tests are maintainable, reliable, and follow React Testing Library best practices.