<script setup lang="ts">
import { computed, ref } from 'vue'

type ExecutionStatus =
    'QUEUED' |
    'RUNNING' |
    'SUCCESS' |
    'PARTIAL_SUCCESS' |
    'FAILED'

type ServerResultStatus =
    'SUCCESS' |
    'FAILED' |
    'SKIPPED' |
    'RUNNING'

interface ServerResult
{
    hostname: string
    status: ServerResultStatus
    message: string
    duration: string
}

interface Execution
{
    id: number
    number: string
    documentNumber: string
    documentTitle: string
    scenario: string
    initiator: string
    startedAt: string
    finishedAt: string | null
    status: ExecutionStatus
    servers: ServerResult[]
    logs: string[]
}

const executions = ref<Execution[]>([
    {
        id: 1,
        number: 'EXEC-0001',
        documentNumber: 'DOC-0001',
        documentTitle: 'Обновление Nginx',
        scenario: 'nginx_update',
        initiator: 'Администратор',
        startedAt: '05.11.2026 13:00',
        finishedAt: '05.11.2026 13:02',
        status: 'SUCCESS',
        servers: [
            {
                hostname: 'web-01',
                status: 'SUCCESS',
                message: 'Nginx успешно обновлён.',
                duration: '45 сек.'
            },
            {
                hostname: 'web-02',
                status: 'SUCCESS',
                message: 'Nginx успешно обновлён.',
                duration: '51 сек.'
            }
        ],
        logs: [
            '[13:00:01] Starting Ansible Runner',
            '[13:00:02] Loading inventory',
            '[13:00:05] Connecting to web-01',
            '[13:00:32] Nginx package updated',
            '[13:00:33] Connecting to web-02',
            '[13:01:10] Nginx package updated',
            '[13:02:00] Execution completed successfully'
        ]
    },
    {
        id: 2,
        number: 'EXEC-0002',
        documentNumber: 'DOC-0005',
        documentTitle: 'Создание пользователя на сервере',
        scenario: 'create_user',
        initiator: 'Администратор',
        startedAt: '05.11.2026 14:10',
        finishedAt: '05.11.2026 14:11',
        status: 'PARTIAL_SUCCESS',
        servers: [
            {
                hostname: 'db-01',
                status: 'SUCCESS',
                message: 'Пользователь создан.',
                duration: '32 сек.'
            },
            {
                hostname: 'web-01',
                status: 'FAILED',
                message: 'Ошибка подключения по SSH.',
                duration: '60 сек.'
            }
        ],
        logs: [
            '[14:10:01] Starting Ansible Runner',
            '[14:10:04] Connecting to db-01',
            '[14:10:20] User created successfully',
            '[14:10:21] Connecting to web-01',
            '[14:11:00] SSH connection failed',
            '[14:11:02] Execution finished with errors'
        ]
    },
    {
        id: 3,
        number: 'EXEC-0003',
        documentNumber: 'DOC-0006',
        documentTitle: 'Обновление системных пакетов',
        scenario: 'package_update',
        initiator: 'Администратор',
        startedAt: '05.11.2026 15:30',
        finishedAt: null,
        status: 'RUNNING',
        servers: [
            {
                hostname: 'web-01',
                status: 'SUCCESS',
                message: 'Обновление завершено.',
                duration: '48 сек.'
            },
            {
                hostname: 'db-01',
                status: 'RUNNING',
                message: 'Выполняется обновление пакетов.',
                duration: '—'
            }
        ],
        logs: [
            '[15:30:01] Starting Ansible Runner',
            '[15:30:05] Connecting to web-01',
            '[15:30:53] Package update completed',
            '[15:30:54] Connecting to db-01',
            '[15:31:10] Installing packages...'
        ]
    },
    {
        id: 4,
        number: 'EXEC-0004',
        documentNumber: 'DOC-0008',
        documentTitle: 'Установка Nginx',
        scenario: 'nginx_install',
        initiator: 'Администратор',
        startedAt: '04.11.2026 16:00',
        finishedAt: '04.11.2026 16:01',
        status: 'FAILED',
        servers: [
            {
                hostname: 'app-01',
                status: 'FAILED',
                message: 'Не удалось установить пакет Nginx.',
                duration: '38 сек.'
            }
        ],
        logs: [
            '[16:00:01] Starting Ansible Runner',
            '[16:00:05] Connecting to app-01',
            '[16:00:20] Installing nginx',
            '[16:00:38] Package installation failed',
            '[16:01:00] Execution failed'
        ]
    }
])

const searchQuery = ref('')
const selectedStatus = ref('')
const selectedExecutionId = ref<number | null>(1)

const filteredExecutions = computed(() =>
{
    const query = searchQuery.value.toLowerCase()

    return executions.value.filter(execution =>
    {
        const matchesSearch =
            execution.number.toLowerCase().includes(query) ||
            execution.documentNumber.toLowerCase().includes(query) ||
            execution.documentTitle.toLowerCase().includes(query) ||
            execution.scenario.toLowerCase().includes(query)

        const matchesStatus =
            !selectedStatus.value ||
            execution.status === selectedStatus.value

        return matchesSearch && matchesStatus
    })
})

const selectedExecution = computed(() =>
{
    return executions.value.find(
        execution => execution.id === selectedExecutionId.value
    ) ?? null
})

function selectExecution(id: number)
{
    selectedExecutionId.value = id
}

function getExecutionStatusLabel(status: ExecutionStatus)
{
    const labels: Record<ExecutionStatus, string> = {
        QUEUED: 'В очереди',
        RUNNING: 'Выполняется',
        SUCCESS: 'Успешно',
        PARTIAL_SUCCESS: 'Частично выполнено',
        FAILED: 'Ошибка'
    }

    return labels[status]
}

function getServerStatusLabel(status: ServerResultStatus)
{
    const labels: Record<ServerResultStatus, string> = {
        SUCCESS: 'Успешно',
        FAILED: 'Ошибка',
        SKIPPED: 'Пропущено',
        RUNNING: 'Выполняется'
    }

    return labels[status]
}
</script>

<template>
    <div class="executions-view">
        <div class="page-heading">
            <div>
                <h1>Выполнение работ</h1>
                <p>Запуски сценариев автоматизации серверной инфраструктуры</p>
            </div>
        </div>

        <section class="filters-section">
            <input
                v-model="searchQuery"
                type="text"
                placeholder="Поиск по заданию, документу или сценарию..."
            >

            <select v-model="selectedStatus">
                <option value="">Все статусы</option>
                <option value="QUEUED">В очереди</option>
                <option value="RUNNING">Выполняется</option>
                <option value="SUCCESS">Успешно</option>
                <option value="PARTIAL_SUCCESS">Частично выполнено</option>
                <option value="FAILED">Ошибка</option>
            </select>
        </section>

        <div class="execution-layout">
            <section class="execution-list-section">
                <div class="section-heading">
                    <h2>История запусков</h2>
                    <span>{{ filteredExecutions.length }} записей</span>
                </div>

                <div v-if="filteredExecutions.length" class="execution-list">
                    <button
                        v-for="execution in filteredExecutions"
                        :key="execution.id"
                        class="execution-item"
                        :class="{
                            active: selectedExecutionId === execution.id
                        }"
                        @click="selectExecution(execution.id)"
                    >
                        <div class="execution-item-top">
                            <strong>{{ execution.number }}</strong>
                            <span>{{ execution.startedAt }}</span>
                        </div>

                        <div class="execution-title">
                            {{ execution.documentTitle }}
                        </div>

                        <div class="execution-item-bottom">
                            <span>{{ execution.scenario }}</span>
                            <span class="status">
                                {{ getExecutionStatusLabel(execution.status) }}
                            </span>
                        </div>
                    </button>
                </div>

                <div v-else class="empty-state">
                    Запуски не найдены.
                </div>
            </section>

            <section class="execution-details">
                <template v-if="selectedExecution">
                    <div class="details-heading">
                        <div>
                            <span class="execution-number">
                                {{ selectedExecution.number }}
                            </span>
                            <h2>{{ selectedExecution.documentTitle }}</h2>
                        </div>

                        <span class="status">
                            {{ getExecutionStatusLabel(selectedExecution.status) }}
                        </span>
                    </div>

                    <div class="details-content">
                        <section class="detail-section">
                            <h3>Информация о запуске</h3>

                            <div class="info-grid">
                                <div>
                                    <span>Исходный документ</span>
                                    <strong>{{ selectedExecution.documentNumber }}</strong>
                                </div>

                                <div>
                                    <span>Сценарий</span>
                                    <strong>{{ selectedExecution.scenario }}</strong>
                                </div>

                                <div>
                                    <span>Инициатор запуска</span>
                                    <strong>{{ selectedExecution.initiator }}</strong>
                                </div>

                                <div>
                                    <span>Начало выполнения</span>
                                    <strong>{{ selectedExecution.startedAt }}</strong>
                                </div>

                                <div>
                                    <span>Завершение</span>
                                    <strong>
                                        {{ selectedExecution.finishedAt ?? 'Не завершено' }}
                                    </strong>
                                </div>
                            </div>
                        </section>

                        <section class="detail-section">
                            <h3>Результаты по серверам</h3>

                            <table>
                                <thead>
                                    <tr>
                                        <th>Сервер</th>
                                        <th>Результат</th>
                                        <th>Время</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    <tr
                                        v-for="server in selectedExecution.servers"
                                        :key="server.hostname"
                                    >
                                        <td>{{ server.hostname }}</td>
                                        <td>
                                            {{ getServerStatusLabel(server.status) }}
                                        </td>
                                        <td>{{ server.duration }}</td>
                                        <td>{{ server.message }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </section>

                        <section class="detail-section">
                            <h3>Журнал выполнения</h3>

                            <div class="log-container">
                                <div
                                    v-for="(log, index) in selectedExecution.logs"
                                    :key="index"
                                    class="log-line"
                                >
                                    {{ log }}
                                </div>
                            </div>
                        </section>
                    </div>
                </template>

                <div v-else class="empty-details">
                    Выберите запуск из списка.
                </div>
            </section>
        </div>
    </div>
</template>

<style scoped>
.executions-view
{
    max-width: 1600px;
}

.page-heading
{
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
    min-width: 190px;
    background: white;
}

.execution-layout
{
    display: grid;
    grid-template-columns: 360px minmax(0, 1fr);
    gap: 20px;
    align-items: start;
}

.execution-list-section,
.execution-details
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

.execution-list
{
    display: flex;
    flex-direction: column;
}

.execution-item
{
    width: 100%;
    padding: 14px;
    text-align: left;
    background: white;
    border: none;
    border-bottom: 1px solid var(--color-border);
}

.execution-item.active
{
    background: #edf0f2;
    border-left: 3px solid var(--color-primary);
}

.execution-item-top,
.execution-item-bottom
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.execution-item-top
{
    margin-bottom: 10px;
    font-size: 12px;
}

.execution-item-top span,
.execution-item-bottom > span:first-child
{
    color: var(--color-muted);
}

.execution-title
{
    margin-bottom: 10px;
    font-size: 14px;
    font-weight: 600;
}

.execution-item-bottom
{
    font-size: 12px;
}

.status
{
    padding: 5px 8px;
    background: #edf0f2;
    border: 1px solid var(--color-border);
    font-size: 12px;
    white-space: nowrap;
}

.details-heading
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    padding: 20px;
    border-bottom: 1px solid var(--color-border);
}

.execution-number
{
    color: var(--color-muted);
    font-size: 13px;
}

.details-heading h2
{
    margin: 7px 0 0;
    font-size: 18px;
}

.details-content
{
    padding: 20px;
}

.detail-section
{
    margin-bottom: 26px;
}

.detail-section:last-child
{
    margin-bottom: 0;
}

.detail-section h3
{
    margin: 0 0 15px;
    font-size: 15px;
}

.info-grid
{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    padding: 16px;
    background: #f5f5f5;
    border: 1px solid var(--color-border);
}

.info-grid div
{
    display: flex;
    flex-direction: column;
    gap: 7px;
    font-size: 13px;
}

.info-grid span
{
    color: var(--color-muted);
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
    padding: 11px;
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

th
{
    background: #f0f1f2;
    font-weight: 600;
}

.log-container
{
    max-height: 300px;
    overflow-y: auto;
    padding: 15px;
    background: #20252a;
    border: 1px solid #111519;
    color: #d5dce2;
    font-family: Consolas, monospace;
    font-size: 12px;
    line-height: 1.8;
}

.log-line
{
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.empty-state,
.empty-details
{
    padding: 35px 15px;
    color: var(--color-muted);
    text-align: center;
    font-size: 14px;
}

.empty-details
{
    display: flex;
    min-height: 500px;
    align-items: center;
    justify-content: center;
}
</style>