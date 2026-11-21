import type { RoleResponse } from './types'
import { getAccessToken } from './auth'

async function apiRequest<T>(
    path: string,
    options: RequestInit = {}
): Promise<T>
{
    const headers = new Headers(options.headers)
    const token = getAccessToken()

    if (token)
    {
        headers.set('Authorization', `Bearer ${token}`)
    }
    if (options.body)
    {
        headers.set('Content-Type', 'application/json')
    }

    const response = await fetch(`/api/v1/${path}`,
    {
        ...options,
        headers
    })

    const data = await response.json()

    if (!response.ok)
    {
        throw new Error(data.detail || 'API request failed')
    }

    return data as T
}

export async function getRoles(): Promise<RoleResponse[]>
{
    return apiRequest<RoleResponse[]>('roles/')
}