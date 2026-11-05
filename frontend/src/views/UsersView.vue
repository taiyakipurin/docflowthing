<script setup lang="ts">
import { computed, ref } from 'vue'

type UserRole = 'INITIATOR' | 'APPROVER' | 'SYSADMIN' | 'ADMIN' | 'AUDITOR'
type UserStatus = 'ACTIVE' | 'BLOCKED'

interface User
{
    id: number
    fullName: string
    email: string
    role: UserRole
    status: UserStatus
    createdAt: string
}

const users = ref<User[]>(
[
    {
        id: 1,
        fullName: 'Иванов Иван Иванович',
        email: 'ivanov@company.local',
        role: 'INITIATOR',
        status: 'ACTIVE',
        createdAt: '01.10.2026'
    },
    {
        id: 2,
        fullName: 'Петров Пётр Петрович',
        email: 'petrov@company.local',
        role: 'APPROVER',
        status: 'ACTIVE',
        createdAt: '01.10.2026'
    },
    {
        id: 3,
        fullName: 'Сидоров Сергей Сергеевич',
        email: 'sidorov@company.local',
        role: 'SYSADMIN',
        status: 'ACTIVE',
        createdAt: '03.10.2026'
    },
    {
        id: 4,
        fullName: 'Администратор системы',
        email: 'admin@company.local',
        role: 'ADMIN',
        status: 'ACTIVE',
        createdAt: '28.09.2026'
    },
    {
        id: 5,
        fullName: 'Кузнецова Анна Викторовна',
        email: 'kuznetsova@company.local',
        role: 'AUDITOR',
        status: 'ACTIVE',
        createdAt: '05.10.2026'
    },
    {
        id: 6,
        fullName: 'Смирнов Алексей Олегович',
        email: 'smirnov@company.local',
        role: 'INITIATOR',
        status: 'BLOCKED',
        createdAt: '10.10.2026'
    }
])

const roles =
[
    { value: 'INITIATOR', label: 'Инициатор' },
    { value: 'APPROVER', label: 'Согласующий' },
    { value: 'SYSADMIN', label: 'Системный администратор' },
    { value: 'ADMIN', label: 'Администратор' },
    { value: 'AUDITOR', label: 'Аудитор' }
]

const searchQuery = ref('')
const selectedRole = ref('ALL')
const selectedStatus = ref('ALL')

const selectedUser = ref<User | null>(users.value[0])

const isModalOpen = ref(false)
const editingUserId = ref<number | null>(null)

const form = ref(
{
    fullName: '',
    email: '',
    role: 'INITIATOR' as UserRole,
    status: 'ACTIVE' as UserStatus
})

const filteredUsers = computed(() =>
{
    const query = searchQuery.value.toLowerCase().trim()

    return users.value.filter(user =>
    {
        const matchesSearch =
            user.fullName.toLowerCase().includes(query) ||
            user.email.toLowerCase().includes(query)

        const matchesRole =
            selectedRole.value === 'ALL' ||
            user.role === selectedRole.value

        const matchesStatus =
            selectedStatus.value === 'ALL' ||
            user.status === selectedStatus.value

        return matchesSearch && matchesRole && matchesStatus
    })
})

function getRoleLabel(role: UserRole)
{
    const item = roles.find(item => item.value === role)
    return item?.label ?? role
}

function getStatusLabel(status: UserStatus)
{
    return status === 'ACTIVE' ? 'Активен' : 'Заблокирован'
}

function selectUser(user: User)
{
    selectedUser.value = user
}

function openCreateModal()
{
    editingUserId.value = null

    form.value =
    {
        fullName: '',
        email: '',
        role: 'INITIATOR',
        status: 'ACTIVE'
    }

    isModalOpen.value = true
}

function openEditModal(user: User)
{
    editingUserId.value = user.id

    form.value =
    {
        fullName: user.fullName,
        email: user.email,
        role: user.role,
        status: user.status
    }

    isModalOpen.value = true
}

function saveUser()
{
    const fullName = form.value.fullName.trim()
    const email = form.value.email.trim()

    if (!fullName || !email)
    {
        return
    }

    const emailExists = users.value.some(user =>
        user.email.toLowerCase() === email.toLowerCase() &&
        user.id !== editingUserId.value
    )

    if (emailExists)
    {
        alert('Пользователь с таким адресом электронной почты уже существует.')
        return
    }

    if (editingUserId.value !== null)
    {
        const user = users.value.find(
            user => user.id === editingUserId.value
        )

        if (user)
        {
            user.fullName = fullName
            user.email = email
            user.role = form.value.role
            user.status = form.value.status
            selectedUser.value = user
        }
    }
    else
    {
        const newUser: User =
        {
            id: Math.max(0, ...users.value.map(user => user.id)) + 1,
            fullName,
            email,
            role: form.value.role,
            status: form.value.status,
            createdAt: new Date().toLocaleDateString('ru-RU')
        }

        users.value.unshift(newUser)
        selectedUser.value = newUser
    }

    isModalOpen.value = false
}

function toggleUserStatus(user: User)
{
    user.status = user.status === 'ACTIVE' ? 'BLOCKED' : 'ACTIVE'
    selectedUser.value = user
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
                    :key="role.value"
                    :value="role.value"
                >
                    {{ role.label }}
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
                                <td>{{ user.fullName }}</td>
                                <td>{{ user.email }}</td>
                                <td>{{ getRoleLabel(user.role) }}</td>
                                <td>
                                    <span
                                        class="status"
                                        :class="user.status.toLowerCase()"
                                    >
                                        {{ getStatusLabel(user.status) }}
                                    </span>
                                </td>
                                <td>{{ user.createdAt }}</td>
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
                            {{ selectedUser.fullName }}
                        </div>

                        <div class="detail-field">
                            <span>Идентификатор</span>
                            <strong>{{ selectedUser.id }}</strong>
                        </div>

                        <div class="detail-field">
                            <span>Электронная почта</span>
                            <strong>{{ selectedUser.email }}</strong>
                        </div>

                        <div class="detail-field">
                            <span>Роль</span>
                            <strong>{{ getRoleLabel(selectedUser.role) }}</strong>
                        </div>

                        <div class="detail-field">
                            <span>Статус учётной записи</span>
                            <strong
                                :class="selectedUser.status.toLowerCase()"
                            >
                                {{ getStatusLabel(selectedUser.status) }}
                            </strong>
                        </div>

                        <div class="detail-field">
                            <span>Дата регистрации</span>
                            <strong>{{ selectedUser.createdAt }}</strong>
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
                                selectedUser.status === 'ACTIVE'
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
                        <label for="fullName">ФИО</label>
                        <input
                            id="fullName"
                            v-model="form.fullName"
                            type="text"
                            placeholder="Иванов Иван Иванович"
                            required
                        >
                    </div>

                    <div class="form-field">
                        <label for="email">Электронная почта</label>
                        <input
                            id="email"
                            v-model="form.email"
                            type="email"
                            placeholder="user@company.local"
                            required
                        >
                    </div>

                    <div class="form-field">
                        <label for="role">Роль</label>
                        <select id="role" v-model="form.role">
                            <option
                                v-for="role in roles"
                                :key="role.value"
                                :value="role.value"
                            >
                                {{ role.label }}
                            </option>
                        </select>
                    </div>

                    <div class="form-field">
                        <label for="status">Статус учётной записи</label>
                        <select id="status" v-model="form.status">
                            <option value="ACTIVE">Активен</option>
                            <option value="BLOCKED">Заблокирован</option>
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

                        <button type="submit" class="primary-button">
                            Сохранить
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
.form-field select
{
    width: 100%;
    min-height: 38px;
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

@media (max-width: 1200px)
{
    .users-layout
    {
        grid-template-columns: 1fr;
    }
}
</style>