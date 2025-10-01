import { describe, it, expect, vi } from 'vitest'
import { render, screen, renderWithUser, waitFor } from '@/test/utils'
import { LoadingButton, ErrorState } from '@/components/ui'

// Example component for testing
const ExampleForm = ({ onSubmit }: { onSubmit: (data: any) => void }) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const formData = new FormData(e.target as HTMLFormElement)
    onSubmit({
      name: formData.get('name'),
      email: formData.get('email'),
    })
  }

  return (
    <form onSubmit={handleSubmit} aria-label="Contact form">
      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          name="name"
          type="text"
          required
          aria-describedby="name-help"
        />
        <div id="name-help">Enter your full name</div>
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          required
          aria-describedby="email-help"
        />
        <div id="email-help">Enter a valid email address</div>
      </div>

      <button type="submit">Submit Form</button>
    </form>
  )
}

describe('React Testing Library Configuration', () => {
  describe('Basic rendering', () => {
    it('renders components correctly', () => {
      render(<ExampleForm onSubmit={vi.fn()} />)

      // Test semantic queries
      expect(screen.getByRole('form', { name: /contact form/i })).toBeInTheDocument()
      expect(screen.getByRole('textbox', { name: /name/i })).toBeInTheDocument()
      expect(screen.getByRole('textbox', { name: /email/i })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /submit form/i })).toBeInTheDocument()
    })

    it('uses custom render with providers', () => {
      render(<ExampleForm onSubmit={vi.fn()} />, {
        providerProps: { theme: 'dark' }
      })

      expect(screen.getByRole('form')).toBeInTheDocument()
    })
  })

  describe('User interactions', () => {
    it('handles form submission with user events', async () => {
      const mockSubmit = vi.fn()
      const { user } = renderWithUser(<ExampleForm onSubmit={mockSubmit} />)

      // Fill out form
      await user.type(screen.getByLabelText(/name/i), 'John Doe')
      await user.type(screen.getByLabelText(/email/i), 'john@example.com')

      // Submit form
      await user.click(screen.getByRole('button', { name: /submit form/i }))

      // Verify submission
      expect(mockSubmit).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com',
      })
    })

    it('supports keyboard navigation', async () => {
      const { user } = renderWithUser(<ExampleForm onSubmit={vi.fn()} />)

      // Tab through form elements
      await user.tab()
      expect(screen.getByLabelText(/name/i)).toHaveFocus()

      await user.tab()
      expect(screen.getByLabelText(/email/i)).toHaveFocus()

      await user.tab()
      expect(screen.getByRole('button', { name: /submit form/i })).toHaveFocus()
    })
  })

  describe('Accessibility testing', () => {
    it('has proper ARIA attributes', () => {
      render(<ExampleForm onSubmit={vi.fn()} />)

      const nameInput = screen.getByLabelText(/name/i)
      const emailInput = screen.getByLabelText(/email/i)

      expect(nameInput).toHaveAttribute('aria-describedby', 'name-help')
      expect(emailInput).toHaveAttribute('aria-describedby', 'email-help')
      expect(nameInput).toBeRequired()
      expect(emailInput).toBeRequired()
    })

    it('provides helpful descriptions', () => {
      render(<ExampleForm onSubmit={vi.fn()} />)

      expect(screen.getByText('Enter your full name')).toBeInTheDocument()
      expect(screen.getByText('Enter a valid email address')).toBeInTheDocument()
    })
  })

  describe('Component testing with UI library', () => {
    it('tests LoadingButton states', async () => {
      const mockClick = vi.fn()
      const { user, rerender } = renderWithUser(
        <LoadingButton isLoading={false} onClick={mockClick}>
          Save Changes
        </LoadingButton>
      )

      const button = screen.getByRole('button', { name: /save changes/i })

      // Test enabled state
      expect(button).toBeEnabled()
      await user.click(button)
      expect(mockClick).toHaveBeenCalledOnce()

      // Test loading state
      rerender(
        <LoadingButton isLoading={true} onClick={mockClick}>
          Save Changes
        </LoadingButton>
      )

      expect(button).toBeDisabled()
      expect(screen.getByRole('status')).toBeInTheDocument() // Loading spinner
    })

    it('tests ErrorState component with retry', async () => {
      const mockRetry = vi.fn()
      const { user } = renderWithUser(
        <ErrorState
          title="Network Error"
          message="Failed to load data"
          onRetry={mockRetry}
        />
      )

      expect(screen.getByRole('alert')).toBeInTheDocument()
      expect(screen.getByText('Network Error')).toBeInTheDocument()
      expect(screen.getByText('Failed to load data')).toBeInTheDocument()

      const retryButton = screen.getByRole('button', { name: /try again/i })
      await user.click(retryButton)

      expect(mockRetry).toHaveBeenCalledOnce()
    })
  })

  describe('Async testing', () => {
    const AsyncComponent = () => {
      const [data, setData] = React.useState<string | null>(null)
      const [loading, setLoading] = React.useState(true)

      React.useEffect(() => {
        setTimeout(() => {
          setData('Loaded data')
          setLoading(false)
        }, 100)
      }, [])

      if (loading) {
        return <div role="status">Loading...</div>
      }

      return <div>{data}</div>
    }

    it('waits for async updates', async () => {
      render(<AsyncComponent />)

      expect(screen.getByRole('status')).toHaveTextContent('Loading...')

      await waitFor(() => {
        expect(screen.getByText('Loaded data')).toBeInTheDocument()
      })

      expect(screen.queryByRole('status')).not.toBeInTheDocument()
    })
  })

  describe('Error boundary testing', () => {
    const ThrowError = ({ shouldThrow }: { shouldThrow: boolean }) => {
      if (shouldThrow) {
        throw new Error('Test error')
      }
      return <div>No error</div>
    }

    it('catches component errors gracefully', () => {
      // Suppress console.error for this test
      const consoleError = vi.spyOn(console, 'error').mockImplementation(() => {})

      const { rerender } = render(
        <ErrorState>
          <ThrowError shouldThrow={false} />
        </ErrorState>
      )

      expect(screen.getByText('No error')).toBeInTheDocument()

      // Trigger error
      expect(() => {
        rerender(
          <ErrorState>
            <ThrowError shouldThrow={true} />
          </ErrorState>
        )
      }).toThrow()

      consoleError.mockRestore()
    })
  })
})

// Import React for JSX
import React from 'react'