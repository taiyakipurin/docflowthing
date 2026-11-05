<script setup lang="ts">
import { computed, ref } from 'vue'

type AuditEvent =
{
    id: number
    timestamp: string
    actor: string
    actorRole: string
    action: string
    category: string
    entity: string
    entityId: string
    result: 'SUCCESS' | 'FAILURE'
    ipAddress: string
    description: string
    details: string
}

const events = ref<AuditEvent[]>(
[
    {
        id: 1,
        timestamp: '05.11.2026 09:42:18',
        actor: 'Иванов И.И.',
        actorRole: 'INITIATOR',
        action: 'Создание документа',
        category: 'DOCUMENT',
        entity: 'Документ DOC-0007',
        entityId: 'DOC-0007',
        result: 'SUCCESS',
        ipAddress: '192.168.1.105',
        description: 'Создан новый документ на изменение инфраструктуры.',
        details: 'Пользователь создал документ «Обновление Nginx на web-01».'
    },
    {
        id: 2,
        timestamp: '05.11.2026 09:45:03',
        actor: 'Иванов И.И.',
        actorRole: 'INITIATOR',
        action: 'Отправка на согласование',
        category: 'DOCUMENT',
        entity: 'Документ DOC-0007',
        entityId: 'DOC-0007',
        result: 'SUCCESS',
        ipAddress: '192.168.1.105',
        description: 'Документ отправлен на рассмотрение.',
        details: 'Статус документа изменён с DRAFT на PENDING_APPROVAL.'
    },
    {
        id: 3,
        timestamp: '05.11.2026 10:12:41',
        actor: 'Петров П.П.',
        actorRole: 'APPROVER',
        action: 'Согласование документа',
        category: 'APPROVAL',
        entity: 'Документ DOC-0005',
        entityId: 'DOC-0005',
        result: 'SUCCESS',
        ipAddress: '192.168.1.110',
        description: 'Документ успешно согласован.',
        details: 'Статус документа изменён с PENDING_APPROVAL на APPROVED.'
    },
    {
        id: 4,
        timestamp: '05.11.2026 10:25:16',
        actor: 'Сидоров С.С.',
        actorRole: 'SYSADMIN',
        action: 'Запуск выполнения',
        category: 'EXECUTION',
        entity: 'Задание EXEC-0004',
        entityId: 'EXEC-0004',
        result: 'SUCCESS',
        ipAddress: '192.168.1.120',
        description: 'Запущен сценарий обновления системных пакетов.',
        details: 'Для выполнения задания использован документ DOC-0005. Целевой сервер: web-02.'
    },
    {
        id: 5,
        timestamp: '05.11.2026 10:28:52',
        actor: 'SYSTEM',
        actorRole: 'SYSTEM',
        action: 'Завершение выполнения',
        category: 'EXECUTION',
        entity: 'Задание EXEC-0004',
        entityId: 'EXEC-0004',
        result: 'FAILURE',
        ipAddress: '127.0.0.1',
        description: 'Выполнение задания завершилось с ошибкой.',
        details: 'Ansible вернул ненулевой код завершения. Подробности доступны в журнале выполнения.'
    },
    {
        id: 6,
        timestamp: '05.11.2026 10:35:09',
        actor: 'Сидоров С.С.',
        actorRole: 'SYSADMIN',
        action: 'Создание электронного акта',
        category: 'ACT',
        entity: 'Акт ACT-0003',
        entityId: 'ACT-0003',
        result: 'SUCCESS',
        ipAddress: '192.168.1.120',
        description: 'Сформирован электронный акт по результатам выполнения.',
        details: 'Создан акт ACT-0003 на основании документа DOC-0005 и задания EXEC-0004.'
    },
    {
        id: 7,
        timestamp: '05.11.2026 11:02:33',
        actor: 'Администратор',
        actorRole: 'ADMIN',
        action: 'Изменение роли пользователя',
        category: 'USER',
        entity: 'Пользователь user-004',
        entityId: 'user-004',
        result: 'SUCCESS',
        ipAddress: '192.168.1.100',
        description: 'Изменена роль пользователя.',
        details: 'Роль пользователя изменена с INITIATOR на SYSADMIN.'
    },
    {
        id: 8,
        timestamp: '05.11.2026 11:15:47',
        actor: 'Администратор',
        actorRole: 'ADMIN',
        action: 'Изменение сервера',
        category: 'SERVER',
        entity: 'Сервер web-01',
        entityId: 'web-01',
        result: 'SUCCESS',
        ipAddress: '192.168.1.100',
        description: 'Обновлены сведения об инфраструктурном объекте.',
        details: 'Изменено описание сервера web-01.'
    }
])

const searchQuery = ref('')
const selectedCategory = ref('ALL')
const selectedResult = ref('ALL')
const selectedEvent = ref<AuditEvent | null>(events.value[0])

const categories =
[
    { value: 'ALL', label: 'Все события' },
    { value: 'DOCUMENT', label: 'Документы' },
    { value: 'APPROVAL', label: 'Согласование' },
    { value: 'EXECUTION', label: 'Выполнение работ' },
    { value: 'ACT', label: 'Электронные акты' },
    { value: 'SERVER', label: 'Серверы' },
    { value: 'USER', label: 'Пользователи' }
]

const filteredEvents = computed(() =>
{
    const query = searchQuery.value.toLowerCase().trim()

    return events.value.filter(event =>
    {
        const matchesSearch =
            event.actor.toLowerCase().includes(query) ||
            event.action.toLowerCase().includes(query) ||
            event.entity.toLowerCase().includes(query) ||
            event.entityId.toLowerCase().includes(query)

        const matchesCategory =
            selectedCategory.value === 'ALL' ||
            event.category === selectedCategory.value

        const matchesResult =
            selectedResult.value === 'ALL' ||
            event.result === selectedResult.value

        return matchesSearch && matchesCategory && matchesResult
    })
})

function getResultLabel(result: string)
{
    return result === 'SUCCESS' ? 'Успешно' : 'Ошибка'
}

function getCategoryLabel(category: string)
{
    const item = categories.find(item => item.value === category)
    return item?.label ?? category
}

function selectEvent(event: AuditEvent)
{
    selectedEvent.value = event
}
</script>

<template>
    <div class="page">
        <div class="page-header">
            <div>
                <h1>Журнал аудита</h1>
                <p>История действий и событий информационной системы</p>
            </div>
        </div>

        <div class="filters">
            <input
                v-model="searchQuery"
                type="text"
                placeholder="Поиск по пользователю, действию или объекту"
            >

            <select v-model="selectedCategory">
                <option
                    v-for="category in categories"
                    :key="category.value"
                    :value="category.value"
                >
                    {{ category.label }}
                </option>
            </select>

            <select v-model="selectedResult">
                <option value="ALL">Любой результат</option>
                <option value="SUCCESS">Успешно</option>
                <option value="FAILURE">Ошибка</option>
            </select>
        </div>

        <div class="audit-layout">
            <section class="events-section">
                <div class="section-header">
                    <h2>События</h2>
                    <span>Найдено: {{ filteredEvents.length }}</span>
                </div>

                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Дата и время</th>
                                <th>Пользователь</th>
                                <th>Действие</th>
                                <th>Объект</th>
                                <th>Результат</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr
                                v-for="event in filteredEvents"
                                :key="event.id"
                                :class="{ selected: selectedEvent?.id === event.id }"
                                @click="selectEvent(event)"
                            >
                                <td class="date-cell">{{ event.timestamp }}</td>
                                <td>{{ event.actor }}</td>
                                <td>{{ event.action }}</td>
                                <td>{{ event.entity }}</td>
                                <td>
                                    <span
                                        class="result"
                                        :class="event.result.toLowerCase()"
                                    >
                                        {{ getResultLabel(event.result) }}
                                    </span>
                                </td>
                            </tr>

                            <tr v-if="filteredEvents.length === 0">
                                <td colspan="5" class="empty-state">
                                    События не найдены
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <aside class="details-panel">
                <div class="section-header">
                    <h2>Информация о событии</h2>
                </div>

                <div v-if="selectedEvent" class="event-details">
                    <div class="detail-field">
                        <span>Дата и время</span>
                        <strong>{{ selectedEvent.timestamp }}</strong>
                    </div>

                    <div class="detail-field">
                        <span>Пользователь</span>
                        <strong>{{ selectedEvent.actor }}</strong>
                    </div>

                    <div class="detail-field">
                        <span>Роль</span>
                        <strong>{{ selectedEvent.actorRole }}</strong>
                    </div>

                    <div class="detail-field">
                        <span>Действие</span>
                        <strong>{{ selectedEvent.action }}</strong>
                    </div>

                    <div class="detail-field">
                        <span>Категория</span>
                        <strong>{{ getCategoryLabel(selectedEvent.category) }}</strong>
                    </div>

                    <div class="detail-field">
                        <span>Объект</span>
                        <strong>{{ selectedEvent.entity }}</strong>
                    </div>

                    <div class="detail-field">
                        <span>Идентификатор объекта</span>
                        <strong>{{ selectedEvent.entityId }}</strong>
                    </div>

                    <div class="detail-field">
                        <span>Результат</span>
                        <strong
                            :class="selectedEvent.result.toLowerCase()"
                        >
                            {{ getResultLabel(selectedEvent.result) }}
                        </strong>
                    </div>

                    <div class="detail-field">
                        <span>IP-адрес</span>
                        <strong>{{ selectedEvent.ipAddress }}</strong>
                    </div>

                    <div class="detail-field description-field">
                        <span>Описание</span>
                        <p>{{ selectedEvent.description }}</p>
                    </div>

                    <div class="detail-field description-field">
                        <span>Подробности</span>
                        <p>{{ selectedEvent.details }}</p>
                    </div>
                </div>

                <div v-else class="empty-details">
                    Выберите событие из списка.
                </div>

                <div class="readonly-note">
                    Журнал аудита доступен только для просмотра.
                    Записи не могут быть изменены или удалены через интерфейс.
                </div>
            </aside>
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

.audit-layout
{
    display: grid;
    grid-template-columns: minmax(0, 1fr) 350px;
    gap: 16px;
    align-items: start;
}

.events-section,
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

.date-cell
{
    white-space: nowrap;
}

.result
{
    display: inline-block;
    padding: 4px 7px;
    font-size: 12px;
    border: 1px solid;
    white-space: nowrap;
}

.result.success
{
    color: #28633c;
    border-color: #a8c9b2;
    background: #edf5ef;
}

.result.failure
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

.event-details
{
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 15px;
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

.detail-field p
{
    margin: 0;
    font-size: 13px;
    line-height: 1.5;
}

.detail-field strong.success
{
    color: #28633c;
}

.detail-field strong.failure
{
    color: #963d3d;
}

.readonly-note
{
    margin: 0 16px 16px;
    padding: 10px;
    border: 1px solid var(--color-border);
    background: #f3f4f5;
    color: var(--color-muted);
    font-size: 12px;
    line-height: 1.5;
}

.empty-details
{
    padding: 20px 16px;
    color: var(--color-muted);
    font-size: 13px;
}

@media (max-width: 1200px)
{
    .audit-layout
    {
        grid-template-columns: 1fr;
    }
}
</style>