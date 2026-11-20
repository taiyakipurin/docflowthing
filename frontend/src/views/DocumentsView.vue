<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getDocuments, type Document } from '../api/document'

const router = useRouter()

const documents = ref<Document[]>([])
const searchQuery = ref('')
const selectedStatus = ref('ALL')

const isLoading = ref(false)
const errorMessage = ref('')

onMounted(async () =>
{
    isLoading.value = true

    try
    {
        documents.value = await getDocuments()
    }
    catch (error)
    {
        if (error instanceof Error)
        {
            errorMessage.value = error.message
        }
        else
        {
            errorMessage.value = 'Failed to load documents'
        }
    }
    finally
    {
        isLoading.value = false
    }

})

const filteredDocuments = computed(() =>
{
    return documents.value.filter((document) =>
    {
        const query = searchQuery.value.toLowerCase()

        const matchesSearch =
            document.title.toLowerCase().includes(query) ||
            String(document.author_id).includes(query) ||
            String(document.id).includes(query)

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
        draft: 'Черновик',
        submitted: 'На согласовании',
        approved: 'Одобрен',
        rejected: 'Отклонён'
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

function formatDate(date: string): string
{
    return new Date(date).toLocaleString('ru-RU')
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
                <option value="draft">Черновик</option>
                <option value="submitted">На согласовании</option>
                <option value="approved">Одобрен</option>
                <option value="rejected">Отклонён</option>
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
                        <td>{{ document.id }}</td>
                        <td>{{ document.title }}</td>
                        <td>{{ document.author_name }}</td>
                        <td>{{ getStatusLabel(document.status) }}</td>
                        <td>{{ formatDate(document.created_at) }}</td>
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
