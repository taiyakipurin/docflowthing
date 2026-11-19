import { getAccessToken } from './auth'

export interface Document
{
    id: number
    author_id: number
    title: string
    description: string | null
    justification: string | null
    status: 'draft' | 'submitted' | 'approved' | 'rejected'
    created_at: string
    updated_at: string | null
}

export async function getDocuments(): Promise<Document[]>
{
    const response = await fetch('/api/v1/documents',
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
        throw new Error(data.detail || 'Failed to load documents')
    }

    return data
}


