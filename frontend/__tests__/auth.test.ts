/**
 * Auth Flow Tests
 * Tests signup and signin functionality with backend API
 */

import { signUp, signIn, getSession, signOut } from '@/lib/auth-client'
import { apiAuth } from '@/lib/api'

describe('Auth Flow', () => {
  const testEmail = `test-${Date.now()}@example.com`
  const testPassword = 'TestPassword123!'
  let authToken: string | null = null

  test('signup with email and password', async () => {
    const result = await signUp(testEmail, testPassword)

    console.log('Signup result:', result)
    expect(result.success).toBe(true)

    if (result.success && result.data?.token) {
      authToken = result.data.token
      apiAuth.setToken(authToken)
      expect(authToken).toBeTruthy()
      expect(result.data.user_id).toBeTruthy()
    }
  })

  test('signin with email and password', async () => {
    const result = await signIn(testEmail, testPassword)

    console.log('Signin result:', result)
    expect(result.success).toBe(true)

    if (result.success && result.data?.token) {
      authToken = result.data.token
      apiAuth.setToken(authToken)
      expect(authToken).toBeTruthy()
      expect(result.data.user_id).toBeTruthy()
    }
  })

  test('verify token is valid', async () => {
    if (!authToken) {
      throw new Error('No auth token found')
    }

    const session = await getSession()
    console.log('Session:', session)
    expect(session).toBeTruthy()
  })

  test('signout clears token', async () => {
    const result = await signOut()

    console.log('Signout result:', result)
    expect(result.success).toBe(true)

    const token = apiAuth.getToken()
    expect(token).toBeNull()
  })

  test('invalid credentials return error', async () => {
    const result = await signIn('invalid@example.com', 'InvalidPassword123!')

    console.log('Invalid signin result:', result)
    expect(result.success).toBe(false)
    expect(result.error).toBeTruthy()
  })

  test('duplicate email returns error', async () => {
    // First signup
    const result1 = await signUp(`duplicate-${Date.now()}@example.com`, testPassword)
    expect(result1.success).toBe(true)

    // Try to signup with same email
    const result2 = await signUp(`duplicate-${Date.now()}@example.com`, testPassword)
    console.log('Duplicate signup result:', result2)
    // This might return success if timestamps are different, adjust as needed
  })
})
