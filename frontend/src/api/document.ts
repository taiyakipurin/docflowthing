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
    author_name: string
}

export async function getDocuments(): Promise<Document[]>
{
    const response = await fetch('/api/v1/documents/',
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

export interface DocumentCreate
{
    title: string
    description: string | null
    justification: string | null

}

export async function createDocument(data: DocumentCreate): Promise<Document>
{
    const response = await fetch('/api/v1/documents/',
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
            throw new Error(result.detail || 'Failed to create document')
        }

    return result
}

export async function submitDocument(documentId: number): Promise<Document>
{
    const response = await fetch(`/api/v1/documents/${documentId}/submit`,
    {
        method: 'POST',
        headers:
        {
            'Authorization': `Bearer ${getAccessToken()}`
        }
    })

    const result = await response.json()

    if (!response.ok)
    {
        throw new Error(result.detail || 'Failed to submit document')
    }

    return result
}

export async function approveDocumentRequest(documentId: number): Promise<Document>
{
    const response = await fetch(`/api/v1/documents/${documentId}/approve`,
    {
        method: 'POST',
        headers:
        {
            'Authorization': `Bearer ${getAccessToken()}`
        }
    })

    const result = await response.json()

    if (!response.ok)
    {
        throw new Error(result.detail || 'Failed to approve document')
    }

    return result
}

export async function rejectDocumentRequest(documentId: number): Promise<Document>
{
    const response = await fetch(`/api/v1/documents/${documentId}/reject`,
    {
        method: 'POST',
        headers:
        {
            'Authorization': `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify(
        {
            reason
        })
    })

    const result = await response.json()

    if (!response.ok)
    {
        throw new Error(result.detail || 'Failed to reject document')
    }

    return result
}

