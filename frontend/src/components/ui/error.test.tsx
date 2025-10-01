import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@/test/utils'
import {
  ErrorMessage,
  ErrorState,
  ErrorCard,
  FormError,
  ErrorAlert,
  NetworkError,
  NotFoundError,
} from './error'

describe('ErrorMessage', () => {
  it('renders with default destructive variant', () => {
    render(<ErrorMessage>Something went wrong</ErrorMessage>)
    const message = screen.getByRole('alert')
    expect(message).toBeInTheDocument()
    expect(message).toHaveTextContent('Something went wrong')
    expect(message).toHaveClass('text-destructive')
  })

  it('applies warning variant styles', () => {
    render(<ErrorMessage variant="warning">Warning message</ErrorMessage>)
    const message = screen.getByRole('alert')
    expect(message).toHaveClass('text-yellow-600')
  })

  it('applies info variant styles', () => {
    render(<ErrorMessage variant="info">Info message</ErrorMessage>)
    const message = screen.getByRole('alert')
    expect(message).toHaveClass('text-blue-600')
  })
})

describe('ErrorState', () => {
  it('renders with default error variant', () => {
    render(<ErrorState />)
    expect(screen.getByRole('alert')).toBeInTheDocument()
    expect(screen.getByText('Something went wrong')).toBeInTheDocument()
    expect(screen.getByText('An unexpected error occurred. Please try again.')).toBeInTheDocument()
  })

  it('renders custom title and message', () => {
    render(
      <ErrorState
        title="Custom Error"
        message="Custom error message"
      />
    )
    expect(screen.getByText('Custom Error')).toBeInTheDocument()
    expect(screen.getByText('Custom error message')).toBeInTheDocument()
  })

  it('shows retry button when onRetry is provided', () => {
    const handleRetry = vi.fn()
    render(<ErrorState onRetry={handleRetry} />)

    const retryButton = screen.getByRole('button', { name: /try again/i })
    expect(retryButton).toBeInTheDocument()

    retryButton.click()
    expect(handleRetry).toHaveBeenCalledOnce()
  })

  it('hides retry button when showRetry is false', () => {
    const handleRetry = vi.fn()
    render(<ErrorState onRetry={handleRetry} showRetry={false} />)

    expect(screen.queryByRole('button')).not.toBeInTheDocument()
  })

  it('renders children content', () => {
    render(
      <ErrorState>
        <div>Custom content</div>
      </ErrorState>
    )
    expect(screen.getByText('Custom content')).toBeInTheDocument()
  })

  it('applies correct icon for network variant', () => {
    render(<ErrorState variant="network" />)
    expect(screen.getByText('Network Error')).toBeInTheDocument()
    expect(screen.getByText('Please check your internet connection and try again.')).toBeInTheDocument()
  })

  it('applies correct content for server variant', () => {
    render(<ErrorState variant="server" />)
    expect(screen.getByText('Server Error')).toBeInTheDocument()
    expect(screen.getByText('Something went wrong on our end. Please try again later.')).toBeInTheDocument()
  })

  it('applies correct content for not-found variant', () => {
    render(<ErrorState variant="not-found" />)
    expect(screen.getByText('Not Found')).toBeInTheDocument()
    expect(screen.getByText('The page or resource you\'re looking for doesn\'t exist.')).toBeInTheDocument()
  })
})

describe('ErrorCard', () => {
  it('renders with default props', () => {
    render(<ErrorCard />)
    const card = screen.getByRole('alert')
    expect(card).toBeInTheDocument()
    expect(screen.getByText('Error')).toBeInTheDocument()
    expect(screen.getByText('Something went wrong')).toBeInTheDocument()
  })

  it('renders custom title and message', () => {
    render(<ErrorCard title="Custom Title" message="Custom message" />)
    expect(screen.getByText('Custom Title')).toBeInTheDocument()
    expect(screen.getByText('Custom message')).toBeInTheDocument()
  })

  it('shows dismiss button when dismissible', () => {
    const handleDismiss = vi.fn()
    render(<ErrorCard dismissible onDismiss={handleDismiss} />)

    const dismissButton = screen.getByRole('button')
    expect(dismissButton).toBeInTheDocument()

    dismissButton.click()
    expect(handleDismiss).toHaveBeenCalledOnce()
  })

  it('hides dismiss button when not dismissible', () => {
    render(<ErrorCard dismissible={false} />)
    expect(screen.queryByRole('button')).not.toBeInTheDocument()
  })
})

describe('FormError', () => {
  it('renders error message when error is provided', () => {
    render(<FormError error="Field is required" />)
    const error = screen.getByRole('alert')
    expect(error).toBeInTheDocument()
    expect(error).toHaveTextContent('Field is required')
    expect(error).toHaveClass('text-red-600')
  })

  it('renders nothing when no error', () => {
    const { container } = render(<FormError />)
    expect(container.firstChild).toBeNull()
  })

  it('renders nothing when error is empty', () => {
    const { container } = render(<FormError error="" />)
    expect(container.firstChild).toBeNull()
  })
})

describe('ErrorAlert', () => {
  it('renders with message', () => {
    render(<ErrorAlert message="Alert message" />)
    const alert = screen.getByRole('alert')
    expect(alert).toBeInTheDocument()
    expect(screen.getByText('Alert message')).toBeInTheDocument()
  })

  it('renders with title and message', () => {
    render(<ErrorAlert title="Alert Title" message="Alert message" />)
    expect(screen.getByText('Alert Title')).toBeInTheDocument()
    expect(screen.getByText('Alert message')).toBeInTheDocument()
  })

  it('applies warning variant styles', () => {
    render(<ErrorAlert variant="warning" message="Warning message" />)
    const alert = screen.getByRole('alert')
    expect(alert).toHaveClass('border-yellow-200')
  })

  it('shows close button when onClose is provided', () => {
    const handleClose = vi.fn()
    render(<ErrorAlert message="Alert" onClose={handleClose} />)

    const closeButton = screen.getByRole('button')
    expect(closeButton).toBeInTheDocument()

    closeButton.click()
    expect(handleClose).toHaveBeenCalledOnce()
  })
})

describe('NetworkError', () => {
  it('renders network error state', () => {
    render(<NetworkError />)
    expect(screen.getByText('Connection Problem')).toBeInTheDocument()
    expect(screen.getByText('Unable to connect to the server. Please check your internet connection.')).toBeInTheDocument()
  })

  it('shows retry button when onRetry is provided', () => {
    const handleRetry = vi.fn()
    render(<NetworkError onRetry={handleRetry} />)

    const retryButton = screen.getByRole('button', { name: /try again/i })
    expect(retryButton).toBeInTheDocument()

    retryButton.click()
    expect(handleRetry).toHaveBeenCalledOnce()
  })
})

describe('NotFoundError', () => {
  it('renders not found error state with default resource', () => {
    render(<NotFoundError />)
    expect(screen.getByText('Not Found')).toBeInTheDocument()
    expect(screen.getByText('The page you\'re looking for doesn\'t exist or has been moved.')).toBeInTheDocument()
  })

  it('renders with custom resource', () => {
    render(<NotFoundError resource="product" />)
    expect(screen.getByText('The product you\'re looking for doesn\'t exist or has been moved.')).toBeInTheDocument()
  })

  it('shows go back button when onGoBack is provided', () => {
    const handleGoBack = vi.fn()
    render(<NotFoundError onGoBack={handleGoBack} />)

    const goBackButton = screen.getByRole('button', { name: /go back/i })
    expect(goBackButton).toBeInTheDocument()

    goBackButton.click()
    expect(handleGoBack).toHaveBeenCalledOnce()
  })

  it('hides button when no onGoBack provided', () => {
    render(<NotFoundError />)
    expect(screen.queryByRole('button')).not.toBeInTheDocument()
  })
})