<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const document = {
    number: 'DOC-0001',
    title: 'Обновление Nginx',
    status: 'PENDING_APPROVAL',
    author: 'Иванов Иван Иванович',
    createdAt: '05.11.2026 10:30',
    justification: 'Необходимо обновить Nginx для устранения обнаруженных проблем и получения актуальных исправлений.',
    description: 'Обновить Nginx до актуальной версии на веб-серверах. После обновления проверить доступность сервиса и корректность конфигурации.',
    servers: [
        {
            hostname: 'web-01',
            address: '192.168.1.10',
            os: 'Ubuntu 24.04'
        },
        {
            hostname: 'web-02',
            address: '192.168.1.11',
            os: 'Ubuntu 24.04'
        }
    ],
    attachments: [
        'nginx-update-plan.pdf'
    ]
}

function getStatusLabel(status: string)
{
    const statuses: Record<string, string> = {
        DRAFT: 'Черновик',
        PENDING_APPROVAL: 'На согласовании',
        APPROVED: 'Согласован',
        REJECTED: 'Отклонён'
    }

    return statuses[status] ?? status
}

function goBack()
{
    router.push('/documents')
}
</script>

<template>
    <div class="document-detail">
        <div class="page-heading">
            <div>
                <div class="breadcrumbs">
                    <a @click="goBack">Документы</a>
                    <span>/</span>
                    <span>{{ document.number }}</span>
                </div>

                <h1>{{ document.title }}</h1>
                <p>{{ document.number }}</p>
            </div>

            <div class="heading-actions">
                <span class="status">
                    {{ getStatusLabel(document.status) }}
                </span>

                <button @click="goBack">
                    Назад
                </button>
            </div>
        </div>

        <div class="detail-grid">
            <div class="main-column">
                <section class="detail-section">
                    <h2>Основная информация</h2>

                    <div class="info-row">
                        <span>Автор</span>
                        <strong>{{ document.author }}</strong>
                    </div>

                    <div class="info-row">
                        <span>Дата создания</span>
                        <strong>{{ document.createdAt }}</strong>
                    </div>
                </section>

                <section class="detail-section">
                    <h2>Обоснование</h2>
                    <p>{{ document.justification }}</p>
                </section>

                <section class="detail-section">
                    <h2>Описание работ</h2>
                    <p>{{ document.description }}</p>
                </section>

                <section class="detail-section">
                    <h2>Целевые серверы</h2>

                    <table>
                        <thead>
                            <tr>
                                <th>Имя сервера</th>
                                <th>IP-адрес</th>
                                <th>Операционная система</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="server in document.servers"
                                :key="server.hostname">
                                <td>{{ server.hostname }}</td>
                                <td>{{ server.address }}</td>
                                <td>{{ server.os }}</td>
                            </tr>
                        </tbody>
                    </table>
                </section>

                <section class="detail-section">
                    <h2>Вложения</h2>

                    <ul v-if="document.attachments.length">
                        <li v-for="file in document.attachments" :key="file">
                            {{ file }}
                        </li>
                    </ul>

                    <p v-else>Вложения отсутствуют.</p>
                </section>
            </div>

            <aside class="side-column">
                <section class="detail-section">
                    <h2>Согласование</h2>

                    <div class="timeline">
                        <div class="timeline-item">
                            <strong>Документ создан</strong>
                            <span>05.11.2026 10:30</span>
                            <p>Иванов Иван Иванович</p>
                        </div>

                        <div class="timeline-item pending">
                            <strong>Ожидает согласования</strong>
                            <span>Текущее состояние</span>
                        </div>
                    </div>
                </section>

                <section class="detail-section">
                    <h2>Дальнейшие действия</h2>

                    <p class="muted">
                        Документ ожидает рассмотрения согласующим лицом.
                    </p>
                </section>
            </aside>
        </div>
    </div>
</template>

<style scoped>
.document-detail
{
    max-width: 1400px;
}

.page-heading
{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 24px;
}

.page-heading h1
{
    margin: 12px 0 5px;
    font-size: 24px;
}

.page-heading p
{
    margin: 0;
    color: var(--color-muted);
    font-size: 13px;
}

.breadcrumbs
{
    display: flex;
    gap: 9px;
    font-size: 13px;
    color: var(--color-muted);
}

.breadcrumbs a
{
    cursor: pointer;
    text-decoration: underline;
}

.heading-actions
{
    display: flex;
    align-items: center;
    gap: 12px;
}

.heading-actions button
{
    background: white;
    padding: 8px 14px;
}

.status
{
    padding: 7px 10px;
    background: #fff1d6;
    border: 1px solid #e2c58c;
    font-size: 13px;
}

.detail-grid
{
    display: grid;
    grid-template-columns: minmax(0, 2fr) minmax(260px, 1fr);
    gap: 20px;
    align-items: start;
}

.detail-section
{
    background: white;
    border: 1px solid var(--color-border);
    padding: 20px;
    margin-bottom: 18px;
}

.detail-section h2
{
    margin: 0 0 18px;
    font-size: 16px;
}

.detail-section p
{
    font-size: 14px;
    line-height: 1.6;
}

.info-row
{
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #e5e6e8;
    font-size: 14px;
}

.info-row:last-child
{
    border-bottom: none;
}

.info-row span,
.muted
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
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

th
{
    background: #f0f1f2;
}

.timeline
{
    border-left: 2px solid var(--color-border);
    margin-left: 5px;
    padding-left: 18px;
}

.timeline-item
{
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 24px;
    font-size: 13px;
}

.timeline-item::before
{
    content: '';
    position: absolute;
    left: -25px;
    top: 3px;
    width: 10px;
    height: 10px;
    background: #737b84;
    border: 2px solid white;
}

.timeline-item span,
.timeline-item p
{
    color: var(--color-muted);
    margin: 0;
}

.timeline-item.pending::before
{
    background: #d69b31;
}
</style>