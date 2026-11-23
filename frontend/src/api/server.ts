import { getAccessToken } from './auth'
import type { ServerCreate, ServerUpdate, ServerResponse }  from './types'

export async function getServers(): Promise<ServerResponse[]>
{
    const response = await fetch('/api/v1/servers/',
    {
        method: 'GET',
        headers:
        {
            'Authorization': `Bearer ${getAccessToken()}`
        }
    })

    const data = await response.json()

    if (!response.ok)
    {
        throw new Error(data.detail || 'Failed to load servers')
    }

    return data
}

export async function getServer(serverId: number): Promise<ServerResponse>
{
    const response = await fetch(`/api/v1/servers/${serverId}`,
    {
        method: 'GET',
        headers:
        {
            'Authorization': `Bearer ${getAccessToken()}`
        }
    })

    const data = await response.json()

    if (!response.ok)
    {
        throw new Error(data.detail || 'Failed to load server')
    }

    return data
}

export async function createServer(data: ServerCreate): Promise<ServerResponse>
{
    const response = await fetch('/api/v1/servers/',
    {
        method: 'POST',
        headers:
        {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify(data)
    })

    const result = await response.json()

    if (!response.ok)
    {
        throw new Error(result.detail || 'Failed to create server')
    }

    return result
}

export async function updateServer(
    serverId: number,
    data: ServerUpdate
): Promise<ServerResponse>
{
    const response = await fetch(`/api/v1/servers/${serverId}`,
    {
        method: 'PATCH',
        headers:
        {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify(data)
    })

    const result = await response.json()

    if (!response.ok)
    {
        throw new Error(result.detail || 'Failed to update server')
    }

    return result
}

export async function deleteServer(serverId: number): Promise<ServerResponse>
{
    const response = await fetch(`/api/v1/servers/${serverId}`,
    {
        method: 'DELETE',
        headers:
        {
            'Authorization': `Bearer ${getAccessToken()}`
        }
    })

    const result = await response.json()

    if (!response.ok)
    {
        throw new Error(result.detail || 'Failed to delete server')
    }

    return result
}
