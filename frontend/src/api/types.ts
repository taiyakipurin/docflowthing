export interface RoleResponse
{
    code: string
    name: string
}

export interface UserResponse
{
    id: number
    username: string
    full_name: string
    is_active: boolean
    created_at: string
    roles: RoleResponse[]
}