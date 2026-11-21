<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import type { UserResponse, RoleResponse } from '../api/types'
import {
    getUsers,
    createUser,
    updateUser,
    updateUserRoles
} from '../api/user'
import { getRoles } from '../api/role'

type UserRole = 'INITIATOR' | 'APPROVER' | 'SYSADMIN' | 'ADMIN' | 'AUDITOR'
type UserStatus = 'ACTIVE' | 'BLOCKED'

const users = ref<UserResponse[]>([])
const roles = ref<RoleResponse[]>([])
const isLoading = ref(false)
const isSaving = ref(false)
const errorMessage = ref('')

const searchQuery = ref('')
const selectedRole = ref('ALL')
const selectedStatus = ref('ALL')

const selectedUser = ref<UserResponse | null>(null)

const isModalOpen = ref(false)
const editingUserId = ref<number | null>(null)

const form = ref(
{
    username: '',
    first_name: '',
    second_name: '',
    email: '',
    roles_ids: [] as number[]
})

onMounted(async () =>
{
    isLoading.value = true
    errorMessage.value = ''

    try
    {
        users.value = await getUsers()

        if (users.value.length > 0)
        {
            selectedUser.value = users.value[0]
        }
    }
    catch (error)
    {
        errorMessage.value = error instanceof Error
            ? error.message
            : "An error occurred while loading users"
    }
    finally
    {
        isLoading.value = false
    }

})

onMounted(async () =>
{
    isLoading.value = true
    errorMessage.value = ''

    try
    {
        const [usersData, rolesData] = await Promise.all(
        [
            getUsers(),
            getRoles()
        ])

        users.value = usersData
        roles.value = rolesData

        if (users.value.length > 0)
        {
            selectedUser.value = users.value[0]
        }
    }
    catch (error)
    {
        errorMessage.value = error instanceof Error
            ? error.message
            : 'An error occurred while loading data'
    }
    finally
    {
        isLoading.value = false
    }
})

const filteredUsers = computed(() =>
{
    const query = searchQuery.value.toLowerCase().trim()

    return users.value.filter(user =>
    {
        const fullName =
            `${user.first_name} ${user.last_name}`.toLowerCase()

        const matchesSearch =
            user.username.toLowerCase().includes(query) ||
            user.first_name.toLowerCase().includes(query) ||
            user.last_name.toLowerCase().includes(query) ||
            user.email.toLowerCase().includes(query) ||
            fullName.includes(query)

        const matchesRole =
            selectedRole.value === 'ALL' ||
            user.roles.some(role => role.code === selectedRole.value)

        const matchesStatus =
            selectedStatus.value === 'ALL' ||
            (selectedStatus.value === 'ACTIVE' && user.is_active) ||
            (selectedStatus.value === 'BLOCKED' && !user.is_active)

        return matchesSearch && matchesRole && matchesStatus
    })
})

function getFullName(user: UserResponse): string
{
    return `${user.first_name} ${user.last_name}`
}

function getRoleLabel(userRoles: RoleResponse[]): string
{
    return userRoles.map(role => role.name).join(', ')
}

function getStatusLabel(isActive: boolean): string
{
    return isActive ? 'Активен' : 'Заблокирован'
}

function formatDate(date: string): string
{
    return new Date(date).toLocaleDateString('ru-RU')
}

function selectUser(user: UserResponse)
{
    selectedUser.value = user
}

function openCreateModal()
{
    editingUserId.value = null

    form.value =
    {
        username: '',
        password: '',
        first_name: '',
        last_name: '',
        email: '',
        roles_ids: []
    }

    isModalOpen.value = true
}

function openEditModal(user: UserResponse)
{
    editingUserId.value = user.id

    form.value =
    {
        username: user.username,
        password: '',
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email,
        roles_ids: user.roles.map(role => role.id)
    }

    isModalOpen.value = true
}

async function saveUser()
{
    if (form.value.roles_ids.length === 0)
    {
        errorMessage.value = 'Необходимо назначить хотя бы одну роль.'
        return
    }

    isSaving.value = true
    errorMessage.value = ''

    try
    {
        let savedUser: UserResponse

        if (editingUserId.value !== null)
        {
            const userId = editingUserId.value

            await updateUser(userId,
            {
                first_name: form.value.first_name,
                last_name: form.value.last_name,
                email: form.value.email
            })

            savedUser = await updateUserRoles(userId,
            {
                roles_ids: form.value.roles_ids
            })
        }
        else
        {
            savedUser = await createUser(
            {
                username: form.value.username,
                password: form.value.password,
                first_name: form.value.first_name,
                last_name: form.value.last_name,
                email: form.value.email
            })

            savedUser = await updateUserRoles(savedUser.id,
            {
                roles_ids: form.value.roles_ids
            })
        }

        const existingIndex = users.value.findIndex(
            user => user.id === savedUser.id
        )

        if (existingIndex !== -1)
        {
            users.value[existingIndex] = savedUser
        }
        else
        {
            users.value.unshift(savedUser)
        }

        selectedUser.value = savedUser
        isModalOpen.value = false
    }
    catch (error)
    {
        errorMessage.value = error instanceof Error
            ? error.message
            : 'Не удалось сохранить пользователя'
    }
    finally
    {
        isSaving.value = false
    }
}

async function toggleUserStatus(user: UserResponse)
{
    errorMessage.value = ''

    try
    {
        const updatedUser = await updateUser(user.id,
        {
            is_active: !user.is_active
        })

        const index = users.value.findIndex(
            item => item.id === updatedUser.id
        )

        if (index !== -1)
        {
            users.value[index] = updatedUser
        }

        selectedUser.value = updatedUser
    }
    catch (error)
    {
        errorMessage.value = error instanceof Error
            ? error.message
            : 'Не удалось изменить статус пользователя'
    }
}
</script>

<template>
    <div class="page">
        <div class="page-header">
            <div>
                <h1>Пользователи</h1>
                <p>Управление учётными записями и ролями пользователей</p>
            </div>

            <button class="primary-button" @click="openCreateModal">
                Добавить пользователя
            </button>
        </div>

        <p v-if="errorMessage" class="error-message">
            {{ errorMessage }}
        </p>

        <p v-if="isLoading">
            Загрузка пользователей...
        </p>

        <div class="filters">
            <input
                v-model="searchQuery"
                type="text"
                placeholder="Поиск по имени или электронной почте"
            >

            <select v-model="selectedRole">
                <option value="ALL">Все роли</option>
                <option
                    v-for="role in roles"
                    :key="role.id"
                    :value="role.code"
                >
                    {{ role.name }}
                </option>
            </select>

            <select v-model="selectedStatus">
                <option value="ALL">Все статусы</option>
                <option value="ACTIVE">Активные</option>
                <option value="BLOCKED">Заблокированные</option>
            </select>
        </div>

        <div class="users-layout">
            <section class="users-section">
                <div class="section-header">
                    <h2>Учётные записи</h2>
                    <span>Найдено: {{ filteredUsers.length }}</span>
                </div>

                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Пользователь</th>
                                <th>Электронная почта</th>
                                <th>Роль</th>
                                <th>Статус</th>
                                <th>Дата регистрации</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr
                                v-for="user in filteredUsers"
                                :key="user.id"
                                :class="{
                                    selected: selectedUser?.id === user.id
                                }"
                                @click="selectUser(user)"
                            >
                                <td>{{ getFullName(user) }}</td>
                                <td>{{ user.email }}</td>
                                <td>{{ getRoleLabel(user.roles) }}</td>
                                <td>
                                    <span
                                        class="status"
                                        :class="user.is_active ? 'active' : 'blocked'"
                                    >
                                        {{ getStatusLabel(user.is_active) }}
                                    </span>
                                </td>
                                <td>{{ formatDate(user.created_at) }}</td>
                            </tr>

                            <tr v-if="filteredUsers.length === 0">
                                <td colspan="5" class="empty-state">
                                    Пользователи не найдены
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <aside class="details-panel">
                <div class="section-header">
                    <h2>Информация о пользователе</h2>
                </div>

                <template v-if="selectedUser">
                    <div class="user-details">
                        <div class="user-name">
                            {{ getFullName(selectedUser) }}
                        </div>

                        <div class="detail-field">
                            <span>Идентификатор</span>
                            <strong>{{ selectedUser.id }}</strong>
                        </div>

                        <div class="detail-field">
                            <span>Имя пользователя</span>
                            <strong>{{ selectedUser.username }}</strong>
                        </div>

                        <div class="detail-field">
                            <span>Электронная почта</span>
                            <strong>{{ selectedUser.email }}</strong>
                        </div>

                        <div class="detail-field">
                            <span>Ролb</span>
                            <strong>{{ getRoleLabel(selectedUser.roles) }}</strong>
                        </div>

                        <div class="detail-field">
                            <span>Статус учётной записи</span>
                            <strong
                                :class="selectedUser.is_active ? 'active' : 'blocked'"
                            >
                                {{ getStatusLabel(selectedUser.is_active) }}
                            </strong>
                        </div>

                        <div class="detail-field">
                            <span>Дата регистрации</span>
                            <strong>{{ formatDate(selectedUser.created_at) }}</strong>
                        </div>
                    </div>

                    <div class="panel-actions">
                        <button
                            class="primary-button"
                            @click="openEditModal(selectedUser)"
                        >
                            Редактировать
                        </button>

                        <button
                            class="secondary-button"
                            @click="toggleUserStatus(selectedUser)"
                        >
                            {{
                                selectedUser.is_active
                                    ? 'Заблокировать'
                                    : 'Активировать'
                            }}
                        </button>
                    </div>
                </template>

                <div v-else class="empty-details">
                    Выберите пользователя из списка.
                </div>
            </aside>
        </div>

        <div
            v-if="isModalOpen"
            class="modal-overlay"
            @click.self="isModalOpen = false"
        >
            <div class="modal">
                <div class="modal-header">
                    <h2>
                        {{
                            editingUserId !== null
                                ? 'Редактирование пользователя'
                                : 'Новый пользователь'
                        }}
                    </h2>

                    <button
                        class="close-button"
                        @click="isModalOpen = false"
                    >
                        ×
                    </button>
                </div>

                <form @submit.prevent="saveUser">
                    <div class="form-field">
                        <label for="username">Имя пользователя</label>
                        <input
                            id="username"
                            v-model="form.username"
                            type="text"
                            minlength="3"
                            maxlength="100"
                            :disabled="editingUserId !== null"
                            required
                        >
                    </div>

                    <div
                        v-if="editingUserId === null"
                        class="form-field"
                    >
                        <label for="password">Пароль</label>
                        <input
                            id="password"
                            v-model="form.password"
                            type="password"
                            minlength="8"
                            maxlength="120"
                            required
                        >
                    </div>

                    <div class="form-field">
                        <label for="firstName">Имя</label>
                        <input
                            id="firstName"
                            v-model="form.first_name"
                            type="text"
                            maxlength="50"
                            required
                        >
                    </div>

                    <div class="form-field">
                        <label for="lastName">Фамилия</label>
                        <input
                            id="lastName"
                            v-model="form.last_name"
                            type="text"
                            maxlength="50"
                            required
                        >
                    </div>

                    <div class="form-field">
                        <label for="email">Электронная почта</label>
                        <input
                            id="email"
                            v-model="form.email"
                            type="email"
                            maxlength="100"
                            required
                        >
                    </div>

                    <div class="form-field">
                        <label for="roles">Роли</label>
                        <select
                            id="roles"
                            v-model="form.roles_ids"
                            multiple
                            required
                        >
                            <option
                                v-for="role in roles"
                                :key="role.id"
                                :value="role.id"
                            >
                                {{ role.name }}
                            </option>
                        </select>
                    </div>

                    <div class="modal-actions">
                        <button
                            type="button"
                            class="secondary-button"
                            @click="isModalOpen = false"
                        >
                            Отмена
                        </button>

                        <button
                            type="submit"
                            class="primary-button"
                            :disabled="isSaving"
                        >
                            {{ isSaving ? 'Сохранение...' : 'Сохранить' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.page
{
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.page-header
{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.page-header h1
{
    margin: 0 0 6px;
    font-size: 24px;
    font-weight: 600;
}

.page-header p
{
    margin: 0;
    color: var(--color-muted);
    font-size: 14px;
}



.filters
{
    display: flex;
    gap: 10px;
}

.filters input
{
    flex: 1;
    min-width: 250px;
}

.filters select
{
    width: 190px;
    background: white;
}

.filters input,
.filters select
{
    height: 38px;
}

.primary-button,
.secondary-button
{
    min-height: 36px;
    padding: 8px 13px;
    font-size: 13px;
}

.primary-button
{
    color: white;
    background: var(--color-primary);
    border: 1px solid var(--color-primary);
}

.primary-button:hover
{
    background: #46515d;
}

.secondary-button
{
    color: var(--color-text);
    background: white;
}

.secondary-button:hover
{
    background: #f0f1f2;
}

.users-layout
{
    display: grid;
    grid-template-columns: minmax(0, 1fr) 340px;
    gap: 16px;
    align-items: start;
}

.users-section,
.details-panel
{
    background: white;
    border: 1px solid var(--color-border);
}

.section-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px;
    border-bottom: 1px solid var(--color-border);
}

.section-header h2
{
    margin: 0;
    font-size: 16px;
    font-weight: 600;
}

.section-header span
{
    color: var(--color-muted);
    font-size: 13px;
}

.table-wrapper
{
    overflow-x: auto;
}

table
{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

th
{
    padding: 11px 12px;
    text-align: left;
    color: var(--color-muted);
    background: #f3f4f5;
    font-weight: 600;
    white-space: nowrap;
}

td
{
    padding: 12px;
    border-top: 1px solid #e3e5e8;
    white-space: nowrap;
}

tbody tr
{
    cursor: pointer;
}

tbody tr:hover
{
    background: #f5f6f7;
}

tbody tr.selected
{
    background: #e9edf1;
}

.status
{
    display: inline-block;
    padding: 4px 7px;
    border: 1px solid;
    font-size: 12px;
}

.status.active
{
    color: #28633c;
    border-color: #a8c9b2;
    background: #edf5ef;
}

.status.blocked
{
    color: #963d3d;
    border-color: #d9aaaa;
    background: #f9eeee;
}

.empty-state
{
    padding: 30px;
    text-align: center;
    color: var(--color-muted);
}

.user-details
{
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.user-name
{
    padding-bottom: 14px;
    border-bottom: 1px solid var(--color-border);
    font-size: 17px;
    font-weight: 600;
}

.detail-field
{
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.detail-field span
{
    color: var(--color-muted);
    font-size: 12px;
}

.detail-field strong
{
    font-size: 13px;
    font-weight: 600;
    overflow-wrap: anywhere;
}

.detail-field strong.active
{
    color: #28633c;
}

.detail-field strong.blocked
{
    color: #963d3d;
}

.panel-actions
{
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 0 16px 16px;
}

.empty-details
{
    padding: 20px 16px;
    color: var(--color-muted);
    font-size: 13px;
}

.modal-overlay
{
    position: fixed;
    inset: 0;
    z-index: 100;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    background: rgba(0, 0, 0, 0.45);
}

.modal
{
    width: 100%;
    max-width: 480px;
    background: white;
    border: 1px solid var(--color-border);
}

.modal-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid var(--color-border);
}

.modal-header h2
{
    margin: 0;
    font-size: 17px;
    font-weight: 600;
}

.close-button
{
    padding: 0 5px;
    border: none;
    background: transparent;
    font-size: 24px;
    color: var(--color-muted);
}

.modal form
{
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 20px;
}

.form-field
{
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.form-field label
{
    font-size: 13px;
    font-weight: 600;
}

.form-field input,
.form-field select[multiple]
{
    width: 100%;
    min-height: 110px;
    background: white;
}

.modal-actions
{
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    padding-top: 10px;
    border-top: 1px solid var(--color-border);
}

.error-message
{
    color: #963d3d;
    font-size: 13px;
}

@media (max-width: 1200px)
{
    .users-layout
    {
        grid-template-columns: 1fr;
    }
}
</style>