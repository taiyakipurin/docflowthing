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


export interface ServerResponse
{
    id: number
    hostname: string
    ip_address: string
    server_type?: string | null
    os?: string | null
    os_version?: string | null
    environment?: string | null
    cpu?: int | null
    ram?: int | null
    description?: string | null
    status: string
    created_at: string
}

export interface ServerCreate
{
    hostname: string
    ip_address: string
    server_type?: string | null
    os?: string | null
    os_version?: string | null
    environment?: string | null
    cpu?: number | null
    ram?: number | null
    description?: string | null
}

export interface ServerUpdate
{
    hostname?: string
    ip_address?: string
    server_type?: string | null
    os?: string | null
    os_version?: string | null
    environment?: string | null
    cpu?: number | null
    ram?: number | null
    description?: string | null
    status?: string
}
