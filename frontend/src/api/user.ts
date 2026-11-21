import { getAccessToken } from './auth'
import type {
    UserResponse,
    UserCreate,
    UserUpdate,
    UserRolesUpdate
} from './types'

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

export async function getUser(userId: number): Promise<UserResponse>
{
    return apiRequest<UserResponse>(`users/${userId}`)
}

export async function getUsers(): Promise<UserResponse[]>
{
    return apiRequest<UserResponse[]>('users/')
}

export async function createUser(data: UserCreate): Promise<UserResponse>
{
    return apiRequest<UserResponse>('users/',
    {
        method: 'POST',
        body: JSON.stringify(data)
    })
}

export async function updateUser(userId: number, data: UserUpdate): Promise<UserResponse>
{
    return apiRequest<UserResponse>(`users/${userId}`,
    {
        method: 'PATCH',
        body: JSON.stringify(data)
    })
}

export async function updateUserRoles(
    userId: number,
    data: UserRolesUpdate
): Promise<UserResponse>
{
    return apiRequest<UserResponse>(`users/${userId}/roles`,
    {
        method: 'PATCH',
        body: JSON.stringify(data)
    })
}

export async function deleteUser(userId: number): Promise<UserResponse>
{
    return apiRequest<UserResponse>(`users/${userId}`,
    {
        method: 'DELETE',
    })
}