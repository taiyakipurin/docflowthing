export interface RoleResponse
{
    id: number
    code: string
    name: string
}

export interface UserResponse
{
    id: number
    username: string
    first_name: string
    last_name: string
    email: string
    is_active: boolean
    created_at: string
    roles: RoleResponse[]
}

export interface UserCreate
{
    username: string
    password: string
    first_name: string
    last_name: string
    email: string
}

export interface UserUpdate
{
    first_name?: string
    last_name?: string
    email?: string
    is_active?: boolean
}

export interface UserRolesUpdate
{
    roles_ids: number[]
}