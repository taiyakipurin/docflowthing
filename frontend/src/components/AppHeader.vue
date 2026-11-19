<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getMe, logout } from '../api/auth'
import type { UserResponse } from '../api/types'
import { useRouter } from 'vue-router'


const router = useRouter()
const user = ref<UserResponse | null>(null)
const isMenuOpen = ref(false)

onMounted(async () =>
{
    try
    {
        user.value = await getMe()
    }
    catch (error)
    {
        console.error('failed to load user:', error)
        await router.replace({ name: 'login' })
    }
})

const avatarInitials = computed(() =>
{
    if (!user.value)
    {
        return '?'
    }

    const name = user.value.full_name || user.value.username

    return name
        .split(' ')
        .filter(Boolean)
        .slice(0, 2)
        .map(part => part[0].toUpperCase())
        .join('')
})

function toggleMenu()
{
    isMenuOpen.value = !isMenuOpen.value
}

async function handleLogout()
{
    isMenuOpen.value = false

    try
    {
        await logout()
    }
    catch (error)
    {
        console.error('Logout error:', error)
    }
    finally
    {
        await router.replace({name: 'login'})
    }

}


</script>

<template>
    <header class="app-header">
        <div class="header-breadcrumb">
            Информационная система / Документооборот
        </div>

        <div class="header-user-container">
            <button
                class="header-user"
                type="button"
                @click="toggleMenu"
                :aria-expanded="isMenuOpen"
                aria-haspopup="true"
            >
                <div class="user-info">
                    <span class="user-name">
                        {{ user?.full_name || user?.username || 'Loading...' }}
                    </span>

                    <span class="user-role">
                        {{
                            !user
                                ? 'Loading...'
                                : user.roles.length > 0
                                    ? user.roles.map(role => role.name).join(', ')
                                    : 'No roles assigned'
                        }}
                    </span>
                </div>

                <div class="user-avatar">
                    {{ avatarInitials }}
                </div>
            </button>

            <div v-if="isMenuOpen" class="user-dropdown">
                <button
                    class="dropdown-item"
                    type="button"
                    disabled
                >
                    Настройки
                </button>

                <div class="dropdown-divider"></div>

                <button
                    class="dropdown-item logout-item"
                    type="button"
                    @click="handleLogout"
                >
                    Выйти
                </button>
            </div>
        </div>
    </header>
</template>

<style scoped>
    .app-header
    {
        height: 58px;
        min-height: 58px;

        display: flex;
        align-items: center;
        justify-content: space-between;

        padding: 0 24px;

        background: var(--color-background);
        border-bottom: 1px solid var(--color-border);
    }

    .header-breadcrumb
    {
        font-size: 12px;
        color: var(--color-muted);
    }

    .header-user-container
    {
        position: relative;
    }

    .header-user
    {
        display: flex;
        align-items: center;
        gap: 12px;

        padding: 4px;
        border: none;
        background: transparent;
        color: inherit;
        font-family: inherit;
        text-align: right;
        cursor: pointer;
    }

    .header-user:hover
    {
        background: var(--color-background-secondary);
    }

    .user-info
    {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 3px;
    }

    .user-dropdown
    {
        position: absolute;
        top: calc(100% + 8px);
        right: 0;

        width: 180px;

        background: var(--color-background);
        border: 1px solid var(--color-border);
        z-index: 100;
    }

    .dropdown-item
    {
        width: 100%;
        padding: 11px 14px;
        display: block;
        border: none;
        background: transparent;
        color: var(--color-text);
        font-family: inherit;
        font-size: 12px;
        text-align: left;
        cursor: pointer;
    }

    .dropdown-item:hover:not(:disabled)
    {
        background: var(--color-background-secondary);
    }

    .dropdown-item:disabled
    {
        color: var(--color-muted);
        cursor: default;
    }

    .logout-item
    {
        color: #b42318;
    }

    .dropdown-divider
    {
        height: 1px;
        background: var(--color-border);
    }

    .user-avatar
    {
        width: 36px;
        height: 36px;
        flex-shrink: 0;

        display: flex;
        align-items: center;
        justify-content: center;

        border: 1px solid var(--color-border);
        background: #e9e9e9;
        color: #333;

        font-size: 12px;
        font-weight: bold;
    }

    .user-name
    {
        font-size: 12px;
        font-weight: bold;
    }

    .user-role
    {
        font-size: 11px;
        color: var(--color-muted);
    }
</style>
