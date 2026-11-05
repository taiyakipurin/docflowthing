<script setup lang="ts">
import { computed, ref } from 'vue'

type ActStatus = 'COMPLETED' | 'PARTIAL' | 'FAILED'

interface ActServerResult
{
    hostname: string
    result: 'SUCCESS' | 'FAILED' | 'SKIPPED'
    description: string
}

interface ExecutionAct
{
    id: number
    number: string
    documentNumber: string
    documentTitle: string
    executionNumber: string
    scenario: string
    createdAt: string
    author: string
    status: ActStatus
    summary: string
    servers: ActServerResult[]
    fileName: string
}

const acts = ref<ExecutionAct[]>([
    {
        id: 1,
        number: 'ACT-0001',
        documentNumber: 'DOC-0001',
        documentTitle: 'Обновление Nginx',
        executionNumber: 'EXEC-0001',
        scenario: 'nginx_update',
        createdAt: '05.11.2026 13:05',
        author: 'Администратор',
        status: 'COMPLETED',
        summary: 'Обновление Nginx успешно выполнено на всех целевых серверах.',
        servers: [
            {
                hostname: 'web-01',
                result: 'SUCCESS',
                description: 'Nginx успешно обновлён.'
            },
            {
                hostname: 'web-02',
                result: 'SUCCESS',
                description: 'Nginx успешно обновлён.'
            }
        ],
        fileName: 'ACT-0001.pdf'
    },
    {
        id: 2,
        number: 'ACT-0002',
        documentNumber: 'DOC-0005',
        documentTitle: 'Создание пользователя на сервере',
        executionNumber: 'EXEC-0002',
        scenario: 'create_user',
        createdAt: '05.11.2026 14:15',
        author: 'Администратор',
        status: 'PARTIAL',
        summary: 'Пользователь создан на одном сервере. На втором сервере выполнение завершилось ошибкой подключения.',
        servers: [
            {
                hostname: 'db-01',
                result: 'SUCCESS',
                description: 'Пользователь успешно создан.'
            },
            {
                hostname: 'web-01',
                result: 'FAILED',
                description: 'Не удалось установить SSH-соединение.'
            }
        ],
        fileName: 'ACT-0002.pdf'
    },
    {
        id: 3,
        number: 'ACT-0003',
        documentNumber: 'DOC-0008',
        documentTitle: 'Установка Nginx',
        executionNumber: 'EXEC-0004',
        scenario: 'nginx_install',
        createdAt: '04.11.2026 16:05',
        author: 'Администратор',
        status: 'FAILED',
        summary: 'Установка Nginx завершилась ошибкой. Работы не выполнены.',
        servers: [
            {
                hostname: 'app-01',
                result: 'FAILED',
                description: 'Не удалось установить пакет Nginx.'
            }
        ],
        fileName: 'ACT-0003.pdf'
    }
])

const searchQuery = ref('')
const selectedStatus = ref('')
const selectedActId = ref<number | null>(1)

const filteredActs = computed(() =>
{
    const query = searchQuery.value.toLowerCase()

    return acts.value.filter(act =>
    {
        const matchesSearch =
            act.number.toLowerCase().includes(query) ||
            act.documentNumber.toLowerCase().includes(query) ||
            act.documentTitle.toLowerCase().includes(query) ||
            act.executionNumber.toLowerCase().includes(query)

        const matchesStatus =
            !selectedStatus.value || act.status === selectedStatus.value

        return matchesSearch && matchesStatus
    })
})

const selectedAct = computed(() =>
{
    return acts.value.find(
        act => act.id === selectedActId.value
    ) ?? null
})

function selectAct(id: number)
{
    selectedActId.value = id
}

function getActStatusLabel(status: ActStatus)
{
    const labels: Record<ActStatus, string> = {
        COMPLETED: 'Выполнено',
        PARTIAL: 'Частично выполнено',
        FAILED: 'Не выполнено'
    }

    return labels[status]
}

function getResultLabel(result: ActServerResult['result'])
{
    const labels: Record<ActServerResult['result'], string> = {
        SUCCESS: 'Успешно',
        FAILED: 'Ошибка',
        SKIPPED: 'Пропущено'
    }

    return labels[result]
}

function openActFile(act: ExecutionAct)
{
    console.log('Запрос файла акта:', act.fileName)
}
</script>

<template>
    <div class="acts-view">
        <div class="page-heading">
            <div>
                <h1>Электронные акты</h1>
                <p>Учёт результатов выполнения работ по документам</p>
            </div>
        </div>

        <section class="filters-section">
            <input
                v-model="searchQuery"
                type="text"
                placeholder="Поиск по номеру акта, документа или заданию..."
            >

            <select v-model="selectedStatus">
                <option value="">Все результаты</option>
                <option value="COMPLETED">Выполнено</option>
                <option value="PARTIAL">Частично выполнено</option>
                <option value="FAILED">Не выполнено</option>
            </select>
        </section>

        <div class="acts-layout">
            <section class="acts-list-section">
                <div class="section-heading">
                    <h2>Реестр актов</h2>
                    <span>{{ filteredActs.length }} записей</span>
                </div>

                <div v-if="filteredActs.length" class="acts-list">
                    <button
                        v-for="act in filteredActs"
                        :key="act.id"
                        class="act-item"
                        :class="{
                            active: selectedActId === act.id
                        }"
                        @click="selectAct(act.id)"
                    >
                        <div class="act-item-top">
                            <strong>{{ act.number }}</strong>
                            <span>{{ act.createdAt }}</span>
                        </div>

                        <div class="act-title">
                            {{ act.documentTitle }}
                        </div>

                        <div class="act-item-bottom">
                            <span>{{ act.documentNumber }}</span>
                            <span class="status">
                                {{ getActStatusLabel(act.status) }}
                            </span>
                        </div>
                    </button>
                </div>

                <div v-else class="empty-state">
                    Акты не найдены.
                </div>
            </section>

            <section class="act-details">
                <template v-if="selectedAct">
                    <div class="details-heading">
                        <div>
                            <span class="act-number">
                                {{ selectedAct.number }}
                            </span>
                            <h2>Акт выполненных работ</h2>
                        </div>

                        <button
                            class="button-primary"
                            @click="openActFile(selectedAct)"
                        >
                            Просмотреть файл
                        </button>
                    </div>

                    <div class="details-content">
                        <section class="detail-section">
                            <h3>Общие сведения</h3>

                            <div class="info-grid">
                                <div>
                                    <span>Номер акта</span>
                                    <strong>{{ selectedAct.number }}</strong>
                                </div>

                                <div>
                                    <span>Дата формирования</span>
                                    <strong>{{ selectedAct.createdAt }}</strong>
                                </div>

                                <div>
                                    <span>Ответственный</span>
                                    <strong>{{ selectedAct.author }}</strong>
                                </div>

                                <div>
                                    <span>Результат работ</span>
                                    <strong>
                                        {{ getActStatusLabel(selectedAct.status) }}
                                    </strong>
                                </div>
                            </div>
                        </section>

                        <section class="detail-section">
                            <h3>Связанные объекты</h3>

                            <div class="info-grid">
                                <div>
                                    <span>Исходный документ</span>
                                    <strong>{{ selectedAct.documentNumber }}</strong>
                                </div>

                                <div>
                                    <span>Запуск автоматизации</span>
                                    <strong>{{ selectedAct.executionNumber }}</strong>
                                </div>

                                <div>
                                    <span>Сценарий Ansible</span>
                                    <strong>{{ selectedAct.scenario }}</strong>
                                </div>
                            </div>
                        </section>

                        <section class="detail-section">
                            <h3>Описание результата</h3>
                            <p>{{ selectedAct.summary }}</p>
                        </section>

                        <section class="detail-section">
                            <h3>Результаты по серверам</h3>

                            <table>
                                <thead>
                                    <tr>
                                        <th>Сервер</th>
                                        <th>Результат</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    <tr
                                        v-for="server in selectedAct.servers"
                                        :key="server.hostname"
                                    >
                                        <td>{{ server.hostname }}</td>
                                        <td>
                                            {{ getResultLabel(server.result) }}
                                        </td>
                                        <td>{{ server.description }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </section>

                        <section class="detail-section">
                            <h3>Файл акта</h3>

                            <div class="file-entry">
                                <span>{{ selectedAct.fileName }}</span>

                                <button
                                    @click="openActFile(selectedAct)"
                                >
                                    Просмотреть
                                </button>
                            </div>
                        </section>
                    </div>
                </template>

                <div v-else class="empty-details">
                    Выберите акт из реестра.
                </div>
            </section>
        </div>
    </div>
</template>

<style scoped>
.acts-view
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

.acts-layout
{
    display: grid;
    grid-template-columns: 360px minmax(0, 1fr);
    gap: 20px;
    align-items: start;
}

.acts-list-section,
.act-details
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

.acts-list
{
    display: flex;
    flex-direction: column;
}

.act-item
{
    width: 100%;
    padding: 14px;
    text-align: left;
    background: white;
    border: none;
    border-bottom: 1px solid var(--color-border);
}

.act-item.active
{
    background: #edf0f2;
    border-left: 3px solid var(--color-primary);
}

.act-item-top,
.act-item-bottom
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.act-item-top
{
    margin-bottom: 10px;
    font-size: 12px;
}

.act-item-top span,
.act-item-bottom > span:first-child
{
    color: var(--color-muted);
}

.act-title
{
    margin-bottom: 10px;
    font-size: 14px;
    font-weight: 600;
}

.act-item-bottom
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
    gap: 15px;
    padding: 20px;
    border-bottom: 1px solid var(--color-border);
}

.act-number
{
    color: var(--color-muted);
    font-size: 13px;
}

.details-heading h2
{
    margin: 7px 0 0;
    font-size: 18px;
}

button
{
    padding: 8px 13px;
    background: white;
    border: 1px solid var(--color-border);
}

.button-primary
{
    color: white;
    background: var(--color-primary);
    border-color: var(--color-primary);
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

.detail-section > p
{
    font-size: 14px;
    line-height: 1.6;
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

.file-entry
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    border: 1px solid var(--color-border);
    font-size: 13px;
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