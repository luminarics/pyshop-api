import { describe, it, expect, beforeEach, vi } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import {
  useBreakpoint,
  useMediaQuery,
  useBreakpointValue,
  useDeviceType,
  useResponsiveValue,
  useWindowSize,
  useIsMobile,
  useIsTablet,
  useIsDesktop,
  useResponsiveColumns,
} from './useBreakpoint'
import { mockBreakpoint } from '@/test/utils'

// Mock window.matchMedia for consistent testing
const mockMatchMedia = (matches: boolean) => {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: vi.fn().mockImplementation(query => ({
      matches,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  })
}

describe('useBreakpoint', () => {
  beforeEach(() => {
    mockMatchMedia(false)
  })

  it('returns default breakpoint when no matches', () => {
    const { result } = renderHook(() => useBreakpoint())
    expect(result.current).toBe('sm')
  })

  it('returns correct breakpoint for xl screens', () => {
    mockBreakpoint('xl')
    const { result } = renderHook(() => useBreakpoint())
    expect(['xl', '2xl']).toContain(result.current)
  })
})

describe('useMediaQuery', () => {
  it('returns false when media query does not match', () => {
    mockMatchMedia(false)
    const { result } = renderHook(() => useMediaQuery('(min-width: 768px)'))
    expect(result.current).toBe(false)
  })

  it('returns true when media query matches', () => {
    mockMatchMedia(true)
    const { result } = renderHook(() => useMediaQuery('(min-width: 768px)'))
    expect(result.current).toBe(true)
  })
})

describe('useBreakpointValue', () => {
  it('returns false when breakpoint is not active', () => {
    mockMatchMedia(false)
    const { result } = renderHook(() => useBreakpointValue('lg'))
    expect(result.current).toBe(false)
  })

  it('returns true when breakpoint is active', () => {
    mockMatchMedia(true)
    const { result } = renderHook(() => useBreakpointValue('lg'))
    expect(result.current).toBe(true)
  })
})

describe('useDeviceType', () => {
  it('returns mobile for small screens', () => {
    mockBreakpoint('xs')
    const { result } = renderHook(() => useDeviceType())
    expect(result.current).toBe('mobile')
  })

  it('returns desktop for large screens', () => {
    mockBreakpoint('lg')
    const { result } = renderHook(() => useDeviceType())
    expect(result.current).toBe('desktop')
  })
})

describe('useResponsiveValue', () => {
  it('returns value for current breakpoint', () => {
    mockBreakpoint('md')
    const values = {
      sm: 'small',
      md: 'medium',
      lg: 'large',
    }
    const { result } = renderHook(() => useResponsiveValue(values))
    expect(result.current).toBe('medium')
  })

  it('falls back to smaller breakpoint when current not available', () => {
    mockBreakpoint('lg')
    const values = {
      sm: 'small',
      md: 'medium',
      // lg not defined
    }
    const { result } = renderHook(() => useResponsiveValue(values))
    expect(result.current).toBe('medium')
  })

  it('returns undefined when no matching values', () => {
    mockBreakpoint('xs')
    const values = {
      lg: 'large',
      xl: 'extra-large',
    }
    const { result } = renderHook(() => useResponsiveValue(values))
    expect(result.current).toBeUndefined()
  })
})

describe('useWindowSize', () => {
  beforeEach(() => {
    // Mock window dimensions
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 1024,
    })
    Object.defineProperty(window, 'innerHeight', {
      writable: true,
      configurable: true,
      value: 768,
    })
  })

  it('returns current window dimensions', () => {
    const { result } = renderHook(() => useWindowSize())
    expect(result.current.width).toBe(1024)
    expect(result.current.height).toBe(768)
  })

  it('updates when window is resized', () => {
    const { result } = renderHook(() => useWindowSize())

    act(() => {
      // Simulate window resize
      Object.defineProperty(window, 'innerWidth', { value: 1280 })
      Object.defineProperty(window, 'innerHeight', { value: 1024 })

      // Trigger resize event
      const resizeEvent = new Event('resize')
      window.dispatchEvent(resizeEvent)
    })

    expect(result.current.width).toBe(1280)
    expect(result.current.height).toBe(1024)
  })
})

describe('useIsMobile', () => {
  it('returns true for mobile screens', () => {
    mockBreakpoint('xs')
    const { result } = renderHook(() => useIsMobile())
    expect(result.current).toBe(true)
  })

  it('returns false for desktop screens', () => {
    mockBreakpoint('lg')
    const { result } = renderHook(() => useIsMobile())
    expect(result.current).toBe(false)
  })
})

describe('useIsTablet', () => {
  it('returns true for tablet screens', () => {
    mockBreakpoint('md')
    const { result } = renderHook(() => useIsTablet())
    expect(result.current).toBe(true)
  })

  it('returns false for mobile screens', () => {
    mockBreakpoint('xs')
    const { result } = renderHook(() => useIsTablet())
    expect(result.current).toBe(false)
  })
})

describe('useIsDesktop', () => {
  it('returns true for desktop screens', () => {
    mockBreakpoint('lg')
    const { result } = renderHook(() => useIsDesktop())
    expect(result.current).toBe(true)
  })

  it('returns false for mobile screens', () => {
    mockBreakpoint('xs')
    const { result } = renderHook(() => useIsDesktop())
    expect(result.current).toBe(false)
  })
})

describe('useResponsiveColumns', () => {
  it('returns mobile columns for small screens', () => {
    mockBreakpoint('xs')
    const { result } = renderHook(() => useResponsiveColumns(1, 2, 3, 4))
    expect(result.current).toBe(1)
  })

  it('returns tablet columns for medium screens', () => {
    mockBreakpoint('md')
    const { result } = renderHook(() => useResponsiveColumns(1, 2, 3, 4))
    expect(result.current).toBe(2)
  })

  it('returns desktop columns for large screens', () => {
    mockBreakpoint('lg')
    const { result } = renderHook(() => useResponsiveColumns(1, 2, 3, 4))
    expect(result.current).toBe(3)
  })

  it('returns wide columns for xl screens', () => {
    mockBreakpoint('xl')
    const { result } = renderHook(() => useResponsiveColumns(1, 2, 3, 4))
    expect(result.current).toBe(4)
  })
})