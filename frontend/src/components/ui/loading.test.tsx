import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@/test/utils'
import {
  LoadingSpinner,
  LoadingDots,
  LoadingSkeleton,
  LoadingState,
  LoadingButton,
  LoadingCard,
} from './loading'

describe('LoadingSpinner', () => {
  it('renders with default props', () => {
    render(<LoadingSpinner />)
    const spinner = screen.getByRole('status')
    expect(spinner).toBeInTheDocument()
    expect(spinner).toHaveAttribute('aria-label', 'Loading')
  })

  it('applies correct size classes', () => {
    render(<LoadingSpinner size="lg" />)
    const spinner = screen.getByRole('status')
    expect(spinner).toHaveClass('w-8', 'h-8')
  })

  it('applies custom className', () => {
    render(<LoadingSpinner className="custom-class" />)
    const spinner = screen.getByRole('status')
    expect(spinner).toHaveClass('custom-class')
  })
})

describe('LoadingDots', () => {
  it('renders three dots', () => {
    render(<LoadingDots />)
    const container = screen.getByRole('status')
    expect(container).toBeInTheDocument()
    expect(container.children).toHaveLength(3)
  })

  it('applies correct size classes', () => {
    render(<LoadingDots size="lg" />)
    const container = screen.getByRole('status')
    const dots = container.children
    Array.from(dots).forEach(dot => {
      expect(dot).toHaveClass('w-3', 'h-3')
    })
  })
})

describe('LoadingSkeleton', () => {
  it('renders single skeleton by default', () => {
    render(<LoadingSkeleton />)
    const skeleton = screen.getByRole('status')
    expect(skeleton).toBeInTheDocument()
    expect(skeleton).toHaveClass('h-4', 'rounded')
  })

  it('renders multiple lines for text variant', () => {
    render(<LoadingSkeleton variant="text" lines={3} />)
    const container = screen.getByRole('status').parentElement
    expect(container?.children).toHaveLength(3)
  })

  it('applies correct variant classes', () => {
    render(<LoadingSkeleton variant="circle" />)
    const skeleton = screen.getByRole('status')
    expect(skeleton).toHaveClass('rounded-full', 'aspect-square')
  })
})

describe('LoadingState', () => {
  it('renders with default spinner', () => {
    render(<LoadingState />)
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders with custom text', () => {
    render(<LoadingState text="Please wait..." />)
    expect(screen.getByText('Please wait...')).toBeInTheDocument()
  })

  it('renders dots variant', () => {
    render(<LoadingState variant="dots" />)
    const container = screen.getByRole('status')
    expect(container.children).toHaveLength(3) // dots
  })

  it('renders children content', () => {
    render(
      <LoadingState>
        <div>Custom content</div>
      </LoadingState>
    )
    expect(screen.getByText('Custom content')).toBeInTheDocument()
  })
})

describe('LoadingButton', () => {
  it('renders children when not loading', () => {
    render(
      <LoadingButton isLoading={false}>
        Click me
      </LoadingButton>
    )
    expect(screen.getByText('Click me')).toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('shows spinner when loading', () => {
    render(
      <LoadingButton isLoading={true}>
        Click me
      </LoadingButton>
    )
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('is disabled when loading', () => {
    render(
      <LoadingButton isLoading={true}>
        Click me
      </LoadingButton>
    )
    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
  })

  it('calls onClick when not loading', () => {
    const handleClick = vi.fn()
    render(
      <LoadingButton isLoading={false} onClick={handleClick}>
        Click me
      </LoadingButton>
    )
    const button = screen.getByRole('button')
    button.click()
    expect(handleClick).toHaveBeenCalledOnce()
  })

  it('does not call onClick when loading', () => {
    const handleClick = vi.fn()
    render(
      <LoadingButton isLoading={true} onClick={handleClick}>
        Click me
      </LoadingButton>
    )
    const button = screen.getByRole('button')
    button.click()
    expect(handleClick).not.toHaveBeenCalled()
  })
})

describe('LoadingCard', () => {
  it('renders skeleton card with default props', () => {
    render(<LoadingCard />)
    const card = screen.getByRole('status').closest('div')
    expect(card).toHaveClass('p-6', 'border', 'rounded-lg')
  })

  it('shows image skeleton when showImage is true', () => {
    render(<LoadingCard showImage={true} />)
    const skeletons = screen.getAllByRole('status')
    expect(skeletons.length).toBeGreaterThan(1) // image + text lines
  })

  it('shows button skeleton when showButton is true', () => {
    render(<LoadingCard showButton={true} />)
    const skeletons = screen.getAllByRole('status')
    expect(skeletons.length).toBeGreaterThan(1) // text + button
  })

  it('renders correct number of text lines', () => {
    render(<LoadingCard lines={5} showImage={false} showButton={false} />)
    // Should have container with multiple line skeletons
    const container = screen.getByRole('status').parentElement
    expect(container).toBeInTheDocument()
  })
})