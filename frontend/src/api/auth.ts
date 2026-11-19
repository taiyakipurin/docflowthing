import type { UserResponse } from './types'

interface TokenResponse
{
    access_token: string
    token_type: string
}

let accessToken: string | null = null

export function getAccessToken(): string | null
{
    return accessToken
}

export async function login(
    username: string,
    password: string
): Promise<void>
{
    const response = await fetch('/api/v1/auth/login',
    {
        method: 'POST',
        headers:
        {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(
        {
            username,
            password
        })
    })

    const data: TokenResponse = await response.json()

    if (!response.ok)
    {
        throw new Error(
            'detail' in data ? data.detail : 'Authorization error'
        )
    }

    accessToken = data.access_token
}

export async function getMe(): Promise<UserResponse>
{
    const accessToken = getAccessToken()

    if (!accessToken)
    {
        throw new Error('Access token is missing')
    }

    const response = await fetch('/api/v1/auth/me',
    {
        method: 'GET',
        headers:
        {
            'Authorization': `Bearer ${accessToken}`
        }
    })

    const data = await response.json()

    if (!response.ok)
    {
        throw new Error(data.detail || 'failed to get user information')

    }

    return data as UserResponse

}

export async function logout(): Promise<void>
{
    try
    {
        const response = await fetch('/api/v1/auth/logout',
        {
            method: 'POST',
            credentials: 'include'
        })

        if (!response.ok)
        {
            throw new Error('logout failed')
        }
    }
    finally
    {
        accessToken = null
    }


}
