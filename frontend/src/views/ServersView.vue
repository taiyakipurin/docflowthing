<script setup lang="ts">
import { computed, ref } from 'vue'

type ServerStatus = 'ACTIVE' | 'INACTIVE' | 'MAINTENANCE'
type ServerType = 'WEB' | 'DATABASE' | 'APPLICATION' | 'OTHER'

interface Server
{
    id: number
    hostname: string
    address: string
    type: ServerType
    os: string
    osVersion: string
    environment: string
    status: ServerStatus
    description: string
    cpu: number
    ram: number
    createdAt: string
}

const servers = ref<Server[]>([
    {
        id: 1,
        hostname: 'web-01',
        address: '192.168.1.10',
        type: 'WEB',
        os: 'Ubuntu',
        osVersion: '24.04 LTS',
        environment: 'PRODUCTION',
        status: 'ACTIVE',
        description: 'Основной веб-сервер предприятия.',
        cpu: 4,
        ram: 8,
        createdAt: '12.08.2026'
    },
    {
        id: 2,
        hostname: 'web-02',
        address: '192.168.1.11',
        type: 'WEB',
        os: 'Ubuntu',
        osVersion: '24.04 LTS',
        environment: 'PRODUCTION',
        status: 'ACTIVE',
        description: 'Дополнительный веб-сервер.',
        cpu: 4,
        ram: 8,
        createdAt: '12.08.2026'
    },
    {
        id: 3,
        hostname: 'db-01',
        address: '192.168.1.20',
        type: 'DATABASE',
        os: 'Debian',
        osVersion: '12',
        environment: 'PRODUCTION',
        status: 'ACTIVE',
        description: 'Основной сервер баз данных.',
        cpu: 8,
        ram: 32,
        createdAt: '15.08.2026'
    },
    {
        id: 4,
        hostname: 'app-01',
        address: '192.168.1.30',
        type: 'APPLICATION',
        os: 'Ubuntu',
        osVersion: '22.04 LTS',
        environment: 'TEST',
        status: 'MAINTENANCE',
        description: 'Сервер тестового окружения.',
        cpu: 4,
        ram: 16,
        createdAt: '20.08.2026'
    },
    {
        id: 5,
        hostname: 'backup-01',
        address: '192.168.1.40',
        type: 'OTHER',
        os: 'Debian',
        osVersion: '12',
        environment: 'PRODUCTION',
        status: 'INACTIVE',
        description: 'Сервер резервного копирования.',
        cpu: 4,
        ram: 16,
        createdAt: '25.08.2026'
    }
])

const searchQuery = ref('')
const selectedType = ref('')
const selectedStatus = ref('')
const selectedServerId = ref<number | null>(1)

const showForm = ref(false)
const editingServerId = ref<number | null>(null)

const form = ref({
    hostname: '',
    address: '',
    type: 'WEB' as ServerType,
    os: 'Ubuntu',
    osVersion: '',
    environment: 'PRODUCTION',
    status: 'ACTIVE' as ServerStatus,
    description: '',
    cpu: 4,
    ram: 8
})

const filteredServers = computed(() =>
{
    const query = searchQuery.value.toLowerCase()

    return servers.value.filter(server =>
    {
        const matchesSearch =
            server.hostname.toLowerCase().includes(query) ||
            server.address.toLowerCase().includes(query) ||
            server.os.toLowerCase().includes(query)

        const matchesType =
            !selectedType.value || server.type === selectedType.value

        const matchesStatus =
            !selectedStatus.value || server.status === selectedStatus.value

        return matchesSearch && matchesType && matchesStatus
    })
})

const selectedServer = computed(() =>
{
    return servers.value.find(
        server => server.id === selectedServerId.value
    ) ?? null
})

function getTypeLabel(type: ServerType)
{
    const labels: Record<ServerType, string> = {
        WEB: 'Веб-сервер',
        DATABASE: 'Сервер БД',
        APPLICATION: 'Сервер приложений',
        OTHER: 'Другой'
    }

    return labels[type]
}

function getStatusLabel(status: ServerStatus)
{
    const labels: Record<ServerStatus, string> = {
        ACTIVE: 'Активен',
        INACTIVE: 'Неактивен',
        MAINTENANCE: 'На обслуживании'
    }

    return labels[status]
}

function getEnvironmentLabel(environment: string)
{
    const labels: Record<string, string> = {
        PRODUCTION: 'Продуктивное',
        TEST: 'Тестовое',
        DEVELOPMENT: 'Разработка'
    }

    return labels[environment] ?? environment
}

function resetForm()
{
    form.value = {
        hostname: '',
        address: '',
        type: 'WEB',
        os: 'Ubuntu',
        osVersion: '',
        environment: 'PRODUCTION',
        status: 'ACTIVE',
        description: '',
        cpu: 4,
        ram: 8
    }

    editingServerId.value = null
}

function openCreateForm()
{
    resetForm()
    showForm.value = true
}

function openEditForm(server: Server)
{
    editingServerId.value = server.id

    form.value = {
        hostname: server.hostname,
        address: server.address,
        type: server.type,
        os: server.os,
        osVersion: server.osVersion,
        environment: server.environment,
        status: server.status,
        description: server.description,
        cpu: server.cpu,
        ram: server.ram
    }

    showForm.value = true
}

function saveServer()
{
    if (
        !form.value.hostname.trim() ||
        !form.value.address.trim() ||
        !form.value.osVersion.trim()
    )
    {
        return
    }

    if (editingServerId.value !== null)
    {
        const server = servers.value.find(
            item => item.id === editingServerId.value
        )

        if (server)
        {
            Object.assign(server, form.value)
            selectedServerId.value = server.id
        }
    }
    else
    {
        const id = Math.max(0, ...servers.value.map(server => server.id)) + 1

        servers.value.push({
            id,
            ...form.value,
            createdAt: new Date().toLocaleDateString('ru-RU')
        })

        selectedServerId.value = id
    }

    showForm.value = false
    resetForm()
}

function cancelForm()
{
    showForm.value = false
    resetForm()
}
</script>

<template>
    <div class="servers-view">
        <div class="page-heading">
            <div>
                <h1>Серверная инфраструктура</h1>
                <p>Управление инвентаризацией серверов предприятия</p>
            </div>

            <button class="button-primary" @click="openCreateForm">
                Добавить сервер
            </button>
        </div>

        <section class="filters-section">
            <input
                v-model="searchQuery"
                type="text"
                placeholder="Поиск по имени, IP или ОС..."
            >

            <select v-model="selectedType">
                <option value="">Все типы серверов</option>
                <option value="WEB">Веб-сервер</option>
                <option value="DATABASE">Сервер БД</option>
                <option value="APPLICATION">Сервер приложений</option>
                <option value="OTHER">Другой</option>
            </select>

            <select v-model="selectedStatus">
                <option value="">Все состояния</option>
                <option value="ACTIVE">Активен</option>
                <option value="INACTIVE">Неактивен</option>
                <option value="MAINTENANCE">На обслуживании</option>
            </select>
        </section>

        <div class="servers-layout">
            <section class="server-list-section">
                <div class="section-heading">
                    <h2>Список серверов</h2>
                    <span>{{ filteredServers.length }} записей</span>
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>Имя</th>
                            <th>IP-адрес</th>
                            <th>Тип</th>
                            <th>ОС</th>
                            <th>Состояние</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr
                            v-for="server in filteredServers"
                            :key="server.id"
                            :class="{
                                selected: selectedServerId === server.id
                            }"
                            @click="selectedServerId = server.id"
                        >
                            <td>{{ server.hostname }}</td>
                            <td>{{ server.address }}</td>
                            <td>{{ getTypeLabel(server.type) }}</td>
                            <td>{{ server.os }} {{ server.osVersion }}</td>
                            <td>
                                {{ getStatusLabel(server.status) }}
                            </td>
                        </tr>

                        <tr v-if="!filteredServers.length">
                            <td colspan="5" class="empty-row">
                                Серверы не найдены.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </section>

            <aside class="server-details">
                <template v-if="selectedServer">
                    <div class="details-heading">
                        <div>
                            <span>Информация о сервере</span>
                            <h2>{{ selectedServer.hostname }}</h2>
                        </div>

                        <button @click="openEditForm(selectedServer)">
                            Изменить
                        </button>
                    </div>

                    <div class="details-content">
                        <div class="detail-row">
                            <span>IP-адрес</span>
                            <strong>{{ selectedServer.address }}</strong>
                        </div>

                        <div class="detail-row">
                            <span>Тип</span>
                            <strong>{{ getTypeLabel(selectedServer.type) }}</strong>
                        </div>

                        <div class="detail-row">
                            <span>Операционная система</span>
                            <strong>
                                {{ selectedServer.os }} {{ selectedServer.osVersion }}
                            </strong>
                        </div>

                        <div class="detail-row">
                            <span>Окружение</span>
                            <strong>
                                {{ getEnvironmentLabel(selectedServer.environment) }}
                            </strong>
                        </div>

                        <div class="detail-row">
                            <span>Состояние</span>
                            <strong>
                                {{ getStatusLabel(selectedServer.status) }}
                            </strong>
                        </div>

                        <div class="detail-row">
                            <span>Процессор</span>
                            <strong>{{ selectedServer.cpu }} vCPU</strong>
                        </div>

                        <div class="detail-row">
                            <span>Оперативная память</span>
                            <strong>{{ selectedServer.ram }} GB</strong>
                        </div>

                        <div class="detail-row">
                            <span>Дата регистрации</span>
                            <strong>{{ selectedServer.createdAt }}</strong>
                        </div>

                        <div class="description-block">
                            <span>Описание</span>
                            <p>{{ selectedServer.description || 'Описание отсутствует.' }}</p>
                        </div>
                    </div>
                </template>

                <div v-else class="empty-details">
                    Выберите сервер из списка.
                </div>
            </aside>
        </div>

        <div v-if="showForm" class="modal-overlay">
            <div class="server-modal">
                <div class="modal-heading">
                    <h2>
                        {{ editingServerId ? 'Редактирование сервера' : 'Добавление сервера' }}
                    </h2>

                    <button class="close-button" @click="cancelForm">
                        ×
                    </button>
                </div>

                <form @submit.prevent="saveServer">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="hostname">Имя сервера</label>
                            <input
                                id="hostname"
                                v-model="form.hostname"
                                required
                            >
                        </div>

                        <div class="form-group">
                            <label for="address">IP-адрес</label>
                            <input
                                id="address"
                                v-model="form.address"
                                required
                            >
                        </div>

                        <div class="form-group">
                            <label for="type">Тип сервера</label>
                            <select id="type" v-model="form.type">
                                <option value="WEB">Веб-сервер</option>
                                <option value="DATABASE">Сервер БД</option>
                                <option value="APPLICATION">Сервер приложений</option>
                                <option value="OTHER">Другой</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="os">Операционная система</label>
                            <select id="os" v-model="form.os">
                                <option value="Ubuntu">Ubuntu</option>
                                <option value="Debian">Debian</option>
                                <option value="Rocky Linux">Rocky Linux</option>
                                <option value="Windows Server">Windows Server</option>
                                <option value="Other">Другая</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="os-version">Версия ОС</label>
                            <input
                                id="os-version"
                                v-model="form.osVersion"
                                required
                            >
                        </div>

                        <div class="form-group">
                            <label for="environment">Окружение</label>
                            <select id="environment" v-model="form.environment">
                                <option value="PRODUCTION">Продуктивное</option>
                                <option value="TEST">Тестовое</option>
                                <option value="DEVELOPMENT">Разработка</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="status">Состояние</label>
                            <select id="status" v-model="form.status">
                                <option value="ACTIVE">Активен</option>
                                <option value="INACTIVE">Неактивен</option>
                                <option value="MAINTENANCE">На обслуживании</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="cpu">Количество vCPU</label>
                            <input
                                id="cpu"
                                v-model.number="form.cpu"
                                type="number"
                                min="1"
                                required
                            >
                        </div>

                        <div class="form-group">
                            <label for="ram">Оперативная память (GB)</label>
                            <input
                                id="ram"
                                v-model.number="form.ram"
                                type="number"
                                min="1"
                                required
                            >
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="description">Описание</label>
                        <textarea
                            id="description"
                            v-model="form.description"
                            rows="3"
                        ></textarea>
                    </div>

                    <div class="modal-actions">
                        <button
                            type="button"
                            class="button-secondary"
                            @click="cancelForm"
                        >
                            Отмена
                        </button>

                        <button type="submit" class="button-primary">
                            Сохранить
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.servers-view
{
    max-width: 1600px;
}

.page-heading
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.page-heading h1
{
    margin: 0 0 8px;
    font-size: 24px;
}

.page-heading p
{
    margin: 0;
    color: var(--color-muted);
    font-size: 14px;
}

button
{
    padding: 8px 13px;
    background: white;
}

.button-primary
{
    color: white;
    background: var(--color-primary);
    border-color: var(--color-primary);
}

.button-secondary
{
    background: white;
}

.filters-section
{
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    padding: 14px;
    background: white;
    border: 1px solid var(--color-border);
}

.filters-section input
{
    flex: 1;
    min-width: 180px;
}

.filters-section select
{
    min-width: 170px;
    background: white;
}

.servers-layout
{
    display: grid;
    grid-template-columns: minmax(0, 1.8fr) minmax(300px, 1fr);
    gap: 20px;
    align-items: start;
}

.server-list-section,
.server-details
{
    background: white;
    border: 1px solid var(--color-border);
}

.section-heading
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid var(--color-border);
}

.section-heading h2
{
    margin: 0;
    font-size: 16px;
}

.section-heading span
{
    color: var(--color-muted);
    font-size: 13px;
}

table
{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

th,
td
{
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

th
{
    background: #f0f1f2;
    font-weight: 600;
}

tbody tr
{
    cursor: pointer;
}

tbody tr:hover
{
    background: #f4f5f6;
}

tbody tr.selected
{
    background: #e9edf0;
}

.empty-row
{
    padding: 25px;
    color: var(--color-muted);
    text-align: center;
}

.details-heading
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    padding: 16px;
    border-bottom: 1px solid var(--color-border);
}

.details-heading span
{
    color: var(--color-muted);
    font-size: 12px;
}

.details-heading h2
{
    margin: 6px 0 0;
    font-size: 18px;
}

.details-content
{
    padding: 16px;
}

.detail-row
{
    display: flex;
    justify-content: space-between;
    gap: 15px;
    padding: 11px 0;
    border-bottom: 1px solid #e5e6e8;
    font-size: 13px;
}

.detail-row span,
.description-block span
{
    color: var(--color-muted);
}

.detail-row strong
{
    text-align: right;
}

.description-block
{
    padding-top: 18px;
    font-size: 13px;
}

.description-block p
{
    line-height: 1.6;
}

.empty-details
{
    padding: 40px 15px;
    color: var(--color-muted);
    text-align: center;
    font-size: 14px;
}

.modal-overlay
{
    position: fixed;
    inset: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: rgba(0, 0, 0, 0.4);
}

.server-modal
{
    width: 100%;
    max-width: 720px;
    max-height: 90vh;
    overflow-y: auto;
    background: white;
    border: 1px solid var(--color-border);
}

.modal-heading
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 20px;
    border-bottom: 1px solid var(--color-border);
}

.modal-heading h2
{
    margin: 0;
    font-size: 18px;
}

.close-button
{
    border: none;
    font-size: 24px;
}

.server-modal form
{
    padding: 20px;
}

.form-grid
{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.form-group
{
    display: flex;
    flex-direction: column;
    gap: 7px;
    margin-bottom: 16px;
}

.form-group label
{
    font-size: 13px;
    font-weight: 600;
}

.form-group input,
.form-group select,
.form-group textarea
{
    width: 100%;
    background: white;
}

.form-group textarea
{
    resize: vertical;
}

.modal-actions
{
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
}
</style>