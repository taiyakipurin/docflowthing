<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface Document
{
    id: number
    number: string
    title: string
    author: string
    status: string
    createdAt: string
}

const documents = ref<Document[]>(
[
    {
        id: 1,
        number: 'DOC-0001',
        title: 'Обновление Nginx',
        author: 'Иванов И.И.',
        status: 'PENDING_APPROVAL',
        createdAt: '05.11.2026'
    },
    {
        id: 2,
        number: 'DOC-0002',
        title: 'Создание пользователя на сервере',
        author: 'Петров П.П.',
        status: 'APPROVED',
        createdAt: '04.11.2026'
    },
    {
        id: 3,
        number: 'DOC-0003',
        title: 'Обновление системных пакетов',
        author: 'Сидоров С.С.',
        status: 'REJECTED',
        createdAt: '03.11.2026'
    },
    {
        id: 4,
        number: 'DOC-0004',
        title: 'Установка PostgreSQL',
        author: 'Иванов И.И.',
        status: 'DRAFT',
        createdAt: '02.11.2026'
    }
])

const searchQuery = ref('')
const selectedStatus = ref('ALL')

const filteredDocuments = computed(() =>
{
    return documents.value.filter((document) =>
    {
        const query = searchQuery.value.toLowerCase()

        const matchesSearch =
            document.number.toLowerCase().includes(query) ||
            document.title.toLowerCase().includes(query) ||
            document.author.toLowerCase().includes(query)

        const matchesStatus =
            selectedStatus.value === 'ALL' ||
            document.status === selectedStatus.value

        return matchesSearch && matchesStatus
    })
})

function getStatusLabel(status: string): string
{
    const labels: Record<string, string> =
    {
        DRAFT: 'Черновик',
        PENDING_APPROVAL: 'На согласовании',
        APPROVED: 'Одобрен',
        REJECTED: 'Отклонён'
    }

    return labels[status] ?? status
}

function openDocument(id: number): void
{
    router.push(`/documents/${id}`)
}

function createDocument(): void
{
    router.push('/documents/new')
}
</script>

<template>
    <section class="documents-page">
        <div class="page-heading">
            <div>
                <h1>Документы</h1>
                <p>Просмотр и управление документами</p>
            </div>

            <button
                class="primary-button"
                @click="createDocument"
            >
                Создать документ
            </button>
        </div>

        <div class="document-filters">
            <input
                v-model="searchQuery"
                type="text"
                placeholder="Поиск по номеру, названию или автору"
            >

            <select v-model="selectedStatus">
                <option value="ALL">Все статусы</option>
                <option value="DRAFT">Черновик</option>
                <option value="PENDING_APPROVAL">На согласовании</option>
                <option value="APPROVED">Одобрен</option>
                <option value="REJECTED">Отклонён</option>
            </select>
        </div>

        <div class="table-container">
            <table class="documents-table">
                <thead>
                    <tr>
                        <th>Номер</th>
                        <th>Название</th>
                        <th>Автор</th>
                        <th>Статус</th>
                        <th>Дата создания</th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="document in filteredDocuments"
                        :key="document.id"
                        @click="openDocument(document.id)"
                    >
                        <td>{{ document.number }}</td>
                        <td>{{ document.title }}</td>
                        <td>{{ document.author }}</td>
                        <td>
                            <span class="status-label">
                                {{ getStatusLabel(document.status) }}
                            </span>
                        </td>
                        <td>{{ document.createdAt }}</td>
                    </tr>

                    <tr v-if="filteredDocuments.length === 0">
                        <td colspan="5" class="empty-message">
                            Документы не найдены
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="table-footer">
            Найдено документов: {{ filteredDocuments.length }}
        </div>
    </section>
</template>

<style scoped>
.documents-page
{
    width: 100%;
}

.page-heading
{
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 24px;
}

.page-heading h1
{
    margin: 0;
    font-size: 24px;
    font-weight: 600;
}

.page-heading p
{
    margin: 6px 0 0;
    font-size: 12px;
    color: var(--color-muted);
}

.primary-button
{
    padding: 9px 16px;
    background: var(--color-primary);
    color: #ffffff;
    border: 1px solid var(--color-primary);
}

.primary-button:hover
{
    background: #414c58;
}

.document-filters
{
    display: flex;
    gap: 10px;
    margin-bottom: 16px;
}

.document-filters input
{
    width: 350px;
}

.document-filters select
{
    min-width: 180px;
    background: #ffffff;
}

.table-container
{
    overflow-x: auto;
    border: 1px solid var(--color-border);
    background: #ffffff;
}

.documents-table
{
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

.documents-table th
{
    padding: 12px;
    background: #eceef0;
    border-bottom: 1px solid var(--color-border);

    font-size: 11px;
    font-weight: 600;
    color: #555b62;
}

.documents-table td
{
    padding: 13px 12px;
    border-bottom: 1px solid #e5e6e8;
    font-size: 13px;
}

.documents-table tbody tr
{
    cursor: pointer;
}

.documents-table tbody tr:hover
{
    background: #f1f3f5;
}

.status-label
{
    font-size: 12px;
}

.empty-message
{
    text-align: center;
    color: var(--color-muted);
    padding: 28px !important;
}

.table-footer
{
    margin-top: 12px;
    font-size: 12px;
    color: var(--color-muted);
}
</style>
