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
            (data as any).detail || 'Authorization error'
        )
    }

    accessToken = data.access_token
}
