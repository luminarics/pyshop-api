import { describe, it, expect } from 'vitest'

describe('Vitest Setup', () => {
  it('should run basic tests', () => {
    expect(1 + 1).toBe(2)
  })

  it('should handle string operations', () => {
    expect('hello'.toUpperCase()).toBe('HELLO')
  })

  it('should work with arrays', () => {
    const arr = [1, 2, 3]
    expect(arr).toHaveLength(3)
    expect(arr).toContain(2)
  })

  it('should handle async operations', async () => {
    const promise = Promise.resolve('success')
    await expect(promise).resolves.toBe('success')
  })
})

describe('Math utilities', () => {
  it('should calculate correctly', () => {
    const add = (a: number, b: number) => a + b
    expect(add(2, 3)).toBe(5)
  })
})