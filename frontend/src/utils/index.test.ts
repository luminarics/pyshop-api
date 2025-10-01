import { describe, it, expect } from 'vitest'
import {
  formatCurrency,
  formatDate,
  formatDateTime,
  truncateText,
  capitalizeFirst,
  generateId,
  sleep,
} from './index'

describe('formatCurrency', () => {
  it('formats USD currency by default', () => {
    const result = formatCurrency(123.45)
    expect(result).toBe('$123.45')
  })

  it('formats different currencies', () => {
    const result = formatCurrency(123.45, 'EUR')
    expect(result).toBe('€123.45')
  })

  it('handles zero amount', () => {
    const result = formatCurrency(0)
    expect(result).toBe('$0.00')
  })

  it('handles negative amounts', () => {
    const result = formatCurrency(-50.25)
    expect(result).toBe('-$50.25')
  })

  it('rounds to 2 decimal places', () => {
    const result = formatCurrency(123.456)
    expect(result).toBe('$123.46')
  })
})

describe('formatDate', () => {
  it('formats Date objects', () => {
    const date = new Date('2023-12-25')
    const result = formatDate(date)
    expect(result).toBe('December 25, 2023')
  })

  it('formats date strings', () => {
    const result = formatDate('2023-12-25')
    expect(result).toBe('December 25, 2023')
  })

  it('handles ISO date strings', () => {
    const result = formatDate('2023-12-25T10:30:00Z')
    expect(result).toBe('December 25, 2023')
  })
})

describe('formatDateTime', () => {
  it('formats Date objects with time', () => {
    const date = new Date('2023-12-25T15:30:00')
    const result = formatDateTime(date)
    expect(result).toMatch(/Dec 25, 2023.+3:30.+PM/)
  })

  it('formats date strings with time', () => {
    const result = formatDateTime('2023-12-25T15:30:00')
    expect(result).toMatch(/Dec 25, 2023.+3:30.+PM/)
  })
})

describe('truncateText', () => {
  it('truncates text longer than maxLength', () => {
    const result = truncateText('This is a long text', 10)
    expect(result).toBe('This is a ...')
  })

  it('returns original text if shorter than maxLength', () => {
    const result = truncateText('Short text', 20)
    expect(result).toBe('Short text')
  })

  it('returns original text if exactly maxLength', () => {
    const result = truncateText('Exact length', 12)
    expect(result).toBe('Exact length')
  })

  it('handles empty string', () => {
    const result = truncateText('', 10)
    expect(result).toBe('')
  })

  it('handles maxLength of 0', () => {
    const result = truncateText('Hello', 0)
    expect(result).toBe('...')
  })
})

describe('capitalizeFirst', () => {
  it('capitalizes first letter of lowercase string', () => {
    const result = capitalizeFirst('hello world')
    expect(result).toBe('Hello world')
  })

  it('handles already capitalized string', () => {
    const result = capitalizeFirst('Hello World')
    expect(result).toBe('Hello world')
  })

  it('handles single character', () => {
    const result = capitalizeFirst('a')
    expect(result).toBe('A')
  })

  it('handles empty string', () => {
    const result = capitalizeFirst('')
    expect(result).toBe('')
  })

  it('handles string with numbers', () => {
    const result = capitalizeFirst('123hello')
    expect(result).toBe('123hello')
  })

  it('converts rest to lowercase', () => {
    const result = capitalizeFirst('HELLO WORLD')
    expect(result).toBe('Hello world')
  })
})

describe('generateId', () => {
  it('generates a string', () => {
    const result = generateId()
    expect(typeof result).toBe('string')
    expect(result.length).toBeGreaterThan(0)
  })

  it('generates unique IDs', () => {
    const id1 = generateId()
    const id2 = generateId()
    expect(id1).not.toBe(id2)
  })

  it('generates IDs with expected pattern', () => {
    const result = generateId()
    // Should contain alphanumeric characters
    expect(result).toMatch(/^[a-z0-9]+$/)
  })
})

describe('sleep', () => {
  it('returns a Promise', () => {
    const result = sleep(100)
    expect(result).toBeInstanceOf(Promise)
  })

  it('resolves after specified time', async () => {
    const start = Date.now()
    await sleep(100)
    const end = Date.now()
    const duration = end - start

    // Allow some tolerance for timing
    expect(duration).toBeGreaterThanOrEqual(90)
    expect(duration).toBeLessThan(200)
  })

  it('resolves with undefined', async () => {
    const result = await sleep(10)
    expect(result).toBeUndefined()
  })
})