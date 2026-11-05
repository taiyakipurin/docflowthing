<script setup lang="ts">
import { computed, ref } from 'vue'

interface ApprovalDocument
{
    id: number
    number: string
    title: string
    author: string
    createdAt: string
    justification: string
    description: string
    servers: string[]
    status: 'PENDING_APPROVAL' | 'APPROVED' | 'REJECTED'
}

const documents = ref<ApprovalDocument[]>([
    {
        id: 1,
        number: 'DOC-0001',
        title: 'Обновление Nginx',
        author: 'Иванов И.И.',
        createdAt: '05.11.2026 10:30',
        justification: 'Необходимо обновить Nginx для устранения обнаруженных проблем.',
        description: 'Обновление Nginx до актуальной версии с последующей проверкой доступности веб-сервисов.',
        servers: ['web-01', 'web-02'],
        status: 'PENDING_APPROVAL'
    },
    {
        id: 2,
        number: 'DOC-0005',
        title: 'Создание пользователя на сервере',
        author: 'Петров П.П.',
        createdAt: '05.11.2026 11:15',
        justification: 'Необходимо предоставить сотруднику доступ к серверу.',
        description: 'Создать системную учётную запись с ограниченными привилегиями.',
        servers: ['db-01'],
        status: 'PENDING_APPROVAL'
    },
    {
        id: 3,
        number: 'DOC-0006',
        title: 'Обновление системных пакетов',
        author: 'Сидоров С.С.',
        createdAt: '05.11.2026 12:00',
        justification: 'Требуется установить актуальные обновления системы.',
        description: 'Выполнить обновление системных пакетов на выбранных серверах.',
        servers: ['web-01', 'db-01'],
        status: 'PENDING_APPROVAL'
    }
])

const searchQuery = ref('')
const selectedDocumentId = ref<number | null>(1)
const rejectionReason = ref('')

const filteredDocuments = computed(() =>
{
    const query = searchQuery.value.toLowerCase()

    return documents.value.filter(document =>
    {
        const matchesSearch =
            document.number.toLowerCase().includes(query) ||
            document.title.toLowerCase().includes(query) ||
            document.author.toLowerCase().includes(query)

        return matchesSearch &&
            document.status === 'PENDING_APPROVAL'
    })
})

const selectedDocument = computed(() =>
{
    return documents.value.find(
        document => document.id === selectedDocumentId.value
    ) ?? null
})

function selectDocument(id: number)
{
    selectedDocumentId.value = id
    rejectionReason.value = ''
}

function approveDocument()
{
    if (!selectedDocument.value)
    {
        return
    }

    selectedDocument.value.status = 'APPROVED'

    console.log(
        'Документ согласован:',
        selectedDocument.value.number
    )

    selectedDocumentId.value = null
}

function rejectDocument()
{
    if (!selectedDocument.value || !rejectionReason.value.trim())
    {
        return
    }

    selectedDocument.value.status = 'REJECTED'

    console.log('Документ отклонён:', {
        document: selectedDocument.value.number,
        reason: rejectionReason.value
    })

    selectedDocumentId.value = null
}

function getStatusLabel(status: string)
{
    const statuses: Record<string, string> = {
        PENDING_APPROVAL: 'На согласовании',
        APPROVED: 'Согласован',
        REJECTED: 'Отклонён'
    }

    return statuses[status] ?? status
}
</script>

<template>
    <div class="approvals-view">
        <div class="page-heading">
            <div>
                <h1>Согласование документов</h1>
                <p>Рассмотрение заявок на изменение серверной инфраструктуры</p>
            </div>
        </div>

        <div class="approval-layout">
            <section class="queue-section">
                <div class="section-heading">
                    <h2>Очередь согласования</h2>
                    <span class="counter">
                        {{ filteredDocuments.length }}
                    </span>
                </div>

                <input
                    v-model="searchQuery"
                    class="search-input"
                    type="text"
                    placeholder="Поиск документов..."
                >

                <div v-if="filteredDocuments.length" class="document-list">
                    <button
                        v-for="document in filteredDocuments"
                        :key="document.id"
                        class="document-item"
                        :class="{
                            active: selectedDocumentId === document.id
                        }"
                        @click="selectDocument(document.id)"
                    >
                        <div class="document-item-top">
                            <strong>{{ document.number }}</strong>
                            <span>{{ document.createdAt }}</span>
                        </div>

                        <div class="document-title">
                            {{ document.title }}
                        </div>

                        <div class="document-author">
                            Автор: {{ document.author }}
                        </div>
                    </button>
                </div>

                <div v-else class="empty-state">
                    Нет документов, ожидающих согласования.
                </div>
            </section>

            <section class="details-section">
                <template v-if="selectedDocument">
                    <div class="details-heading">
                        <div>
                            <span class="document-number">
                                {{ selectedDocument.number }}
                            </span>

                            <h2>{{ selectedDocument.title }}</h2>
                        </div>

                        <span class="status">
                            {{ getStatusLabel(selectedDocument.status) }}
                        </span>
                    </div>

                    <div class="details-content">
                        <div class="info-grid">
                            <div>
                                <span>Автор</span>
                                <strong>{{ selectedDocument.author }}</strong>
                            </div>

                            <div>
                                <span>Дата создания</span>
                                <strong>{{ selectedDocument.createdAt }}</strong>
                            </div>
                        </div>

                        <div class="detail-block">
                            <h3>Обоснование</h3>
                            <p>{{ selectedDocument.justification }}</p>
                        </div>

                        <div class="detail-block">
                            <h3>Описание работ</h3>
                            <p>{{ selectedDocument.description }}</p>
                        </div>

                        <div class="detail-block">
                            <h3>Целевые серверы</h3>

                            <ul>
                                <li
                                    v-for="server in selectedDocument.servers"
                                    :key="server"
                                >
                                    {{ server }}
                                </li>
                            </ul>
                        </div>

                        <div class="decision-section">
                            <h3>Решение по документу</h3>

                            <div class="form-group">
                                <label for="rejection-reason">
                                    Причина отклонения
                                </label>

                                <textarea
                                    id="rejection-reason"
                                    v-model="rejectionReason"
                                    rows="3"
                                    placeholder="Укажите причину, если отклоняете документ..."
                                ></textarea>
                            </div>

                            <div class="decision-actions">
                                <button
                                    class="button-reject"
                                    :disabled="!rejectionReason.trim()"
                                    @click="rejectDocument"
                                >
                                    Отклонить
                                </button>

                                <button
                                    class="button-approve"
                                    @click="approveDocument"
                                >
                                    Согласовать
                                </button>
                            </div>
                        </div>
                    </div>
                </template>

                <div v-else class="empty-details">
                    Выберите документ из очереди согласования.
                </div>
            </section>
        </div>
    </div>
</template>

<style scoped>
.approvals-view
{
    max-width: 1500px;
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

.approval-layout
{
    display: grid;
    grid-template-columns: 360px minmax(0, 1fr);
    gap: 20px;
    align-items: start;
}

.queue-section,
.details-section
{
    background: white;
    border: 1px solid var(--color-border);
}

.queue-section
{
    padding: 16px;
}

.section-heading
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.section-heading h2,
.details-heading h2
{
    margin: 0;
    font-size: 17px;
}

.counter
{
    padding: 3px 8px;
    background: #e8e9eb;
    font-size: 13px;
}

.search-input
{
    width: 100%;
    margin-bottom: 14px;
}

.document-list
{
    display: flex;
    flex-direction: column;
}

.document-item
{
    width: 100%;
    padding: 13px;
    text-align: left;
    background: white;
    border: 1px solid var(--color-border);
    border-bottom: none;
}

.document-item:last-child
{
    border-bottom: 1px solid var(--color-border);
}

.document-item.active
{
    background: #edf0f2;
    border-left: 3px solid var(--color-primary);
}

.document-item-top
{
    display: flex;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 9px;
    font-size: 12px;
}

.document-item-top span,
.document-author
{
    color: var(--color-muted);
}

.document-title
{
    margin-bottom: 7px;
    font-size: 14px;
    font-weight: 600;
}

.document-author
{
    font-size: 12px;
}

.details-section
{
    min-height: 500px;
}

.details-heading
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid var(--color-border);
}

.document-number
{
    display: block;
    margin-bottom: 8px;
    color: var(--color-muted);
    font-size: 13px;
}

.status
{
    padding: 6px 9px;
    background: #fff1d6;
    border: 1px solid #e2c58c;
    font-size: 12px;
    white-space: nowrap;
}

.details-content
{
    padding: 20px;
}

.info-grid
{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--color-border);
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

.detail-block
{
    padding: 18px 0;
    border-bottom: 1px solid var(--color-border);
}

.detail-block h3,
.decision-section h3
{
    margin: 0 0 12px;
    font-size: 14px;
}

.detail-block p,
.detail-block li
{
    font-size: 14px;
    line-height: 1.6;
}

.decision-section
{
    padding-top: 20px;
}

.form-group
{
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 16px;
}

.form-group label
{
    font-size: 13px;
    font-weight: 600;
}

.form-group textarea
{
    width: 100%;
    resize: vertical;
}

.decision-actions
{
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 16px;
}

.decision-actions button
{
    padding: 9px 18px;
}

.button-approve
{
    color: white;
    background: var(--color-primary);
    border-color: var(--color-primary);
}

.button-reject
{
    color: #a22d2d;
    background: white;
    border-color: #c98b8b;
}

.button-reject:disabled
{
    opacity: 0.45;
    cursor: not-allowed;
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