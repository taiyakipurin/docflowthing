<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const title = ref('')
const justification = ref('')
const description = ref('')
const selectedServers = ref<number[]>([])
const attachments = ref<File[]>([])

const servers = [
    { id: 1, hostname: 'web-01', address: '192.168.1.10', os: 'Ubuntu 24.04' },
    { id: 2, hostname: 'web-02', address: '192.168.1.11', os: 'Ubuntu 24.04' },
    { id: 3, hostname: 'db-01', address: '192.168.1.20', os: 'Debian 12' },
]

function toggleServer(id: number)
{
    if (selectedServers.value.includes(id))
    {
        selectedServers.value = selectedServers.value.filter(
            serverId => serverId !== id
        )
    }
    else
    {
        selectedServers.value.push(id)
    }
}

function handleFiles(event: Event)
{
    const target = event.target as HTMLInputElement

    if (target.files)
    {
        attachments.value = Array.from(target.files)
    }
}

function saveDocument(status: 'DRAFT' | 'PENDING_APPROVAL')
{
    console.log({
        title: title.value,
        justification: justification.value,
        description: description.value,
        servers: selectedServers.value,
        attachments: attachments.value,
        status
    })

    router.push('/documents')
}

function cancel()
{
    router.push('/documents')
}
</script>

<template>
    <div class="document-create">
        <div class="page-heading">
            <div>
                <h1>Создание документа</h1>
                <p>Заявка на изменение конфигурации серверной инфраструктуры</p>
            </div>
        </div>

        <section class="form-section">
            <h2>Основная информация</h2>

            <div class="form-group">
                <label for="title">Название документа</label>
                <input
                    id="title"
                    v-model="title"
                    type="text"
                    placeholder="Например: Обновление Nginx"
                >
            </div>

            <div class="form-group">
                <label for="justification">Обоснование</label>
                <textarea
                    id="justification"
                    v-model="justification"
                    rows="3"
                    placeholder="Почему необходимо выполнить изменение?"
                ></textarea>
            </div>

            <div class="form-group">
                <label for="description">Описание работ</label>
                <textarea
                    id="description"
                    v-model="description"
                    rows="5"
                    placeholder="Опишите планируемые изменения..."
                ></textarea>
            </div>
        </section>

        <section class="form-section">
            <h2>Целевые серверы</h2>
            <p class="section-description">
                Выберите серверы, конфигурация которых должна быть изменена.
            </p>

            <table class="server-table">
                <thead>
                    <tr>
                        <th></th>
                        <th>Имя</th>
                        <th>IP-адрес</th>
                        <th>Операционная система</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="server in servers" :key="server.id">
                        <td>
                            <input
                                type="checkbox"
                                :checked="selectedServers.includes(server.id)"
                                @change="toggleServer(server.id)"
                            >
                        </td>
                        <td>{{ server.hostname }}</td>
                        <td>{{ server.address }}</td>
                        <td>{{ server.os }}</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <section class="form-section">
            <h2>Вложения</h2>

            <div class="form-group">
                <label for="attachments">Прикрепить файлы</label>
                <input
                    id="attachments"
                    type="file"
                    multiple
                    @change="handleFiles"
                >
            </div>

            <ul v-if="attachments.length" class="file-list">
                <li v-for="file in attachments" :key="file.name">
                    {{ file.name }}
                </li>
            </ul>
        </section>

        <div class="form-actions">
            <button class="button-secondary" @click="cancel">
                Отмена
            </button>

            <button
                class="button-secondary"
                @click="saveDocument('DRAFT')"
            >
                Сохранить черновик
            </button>

            <button
                class="button-primary"
                @click="saveDocument('PENDING_APPROVAL')"
            >
                Отправить на согласование
            </button>
        </div>
    </div>
</template>

<style scoped>
.document-create
{
    max-width: 1100px;
}

.page-heading
{
    margin-bottom: 24px;
}

.page-heading h1
{
    margin: 0 0 8px;
    font-size: 24px;
    font-weight: 600;
}

.page-heading p,
.section-description
{
    color: var(--color-muted);
    font-size: 14px;
}

.form-section
{
    background: var(--color-background);
    border: 1px solid var(--color-border);
    padding: 20px;
    margin-bottom: 20px;
}

.form-section h2
{
    margin: 0 0 20px;
    font-size: 17px;
    font-weight: 600;
}

.form-group
{
    display: flex;
    flex-direction: column;
    gap: 7px;
    margin-bottom: 18px;
}

.form-group:last-child
{
    margin-bottom: 0;
}

.form-group label
{
    font-size: 14px;
    font-weight: 600;
}

.form-group input,
.form-group textarea
{
    width: 100%;
    background: #fff;
}

.form-group textarea
{
    resize: vertical;
}

.server-table
{
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}

.server-table th,
.server-table td
{
    padding: 11px 12px;
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

.server-table th
{
    background: #f0f1f2;
    font-weight: 600;
}

.server-table input
{
    width: 15px;
    height: 15px;
}

.file-list
{
    padding-left: 20px;
    font-size: 14px;
}

.form-actions
{
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 24px;
}

.form-actions button
{
    padding: 9px 16px;
}

.button-primary
{
    background: var(--color-primary);
    color: white;
    border: 1px solid var(--color-primary);
}

.button-secondary
{
    background: white;
    color: var(--color-text);
}
</style>
