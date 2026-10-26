
<script setup lang="ts">
import { ref } from 'vue'

type DocumentStatus =
    | 'На согласовании'
    | 'Согласован'
    | 'На исполнении'
    | 'Исполнен'
    | 'Отклонён'

interface DocumentItem
{
    id: string
    title: string
    status: DocumentStatus
    date: string
}

const documents = ref<DocumentItem[]>([
    {
        id: 'ДОК-2026-014',
        title: 'Настройка веб-сервера',
        status: 'На согласовании',
        date: '21.10.2026',
    },
    {
        id: 'ДОК-2026-011',
        title: 'Обновление пакетов ОС',
        status: 'На исполнении',
        date: '19.10.2026',
    },
    {
        id: 'ДОК-2026-008',
        title: 'Развёртывание PostgreSQL',
        status: 'Исполнен',
        date: '16.10.2026',
    },
])

const activeSection = ref('Главная')
const notice = ref('')

function navigate(section: string)
{
    activeSection.value = section

    if (section !== 'Главная')
    {
        notice.value = `Раздел «${section}» будет реализован отдельно.`
    }
    else
    {
        notice.value = ''
    }
}

function createDocument()
{
    notice.value = 'Форма создания документа будет реализована следующим этапом.'
}

function openDocument(document: DocumentItem)
{
    notice.value = `Открытие документа ${document.id} будет реализовано следующим этапом.`
}

function statusClass(status: DocumentStatus): string
{
    const classes: Record<DocumentStatus, string> = {
        'На согласовании': 'status-review',
        'Согласован': 'status-approved',
        'На исполнении': 'status-execution',
        'Исполнен': 'status-completed',
        'Отклонён': 'status-rejected',
    }

    return classes[status]
}
</script>

<template>
    <div class="app-shell">
        <header class="topbar">
            <div class="brand">
                <div class="brand-mark">ID</div>

                <div class="brand-text">
                    <div class="brand-name">TITLE*</div>
                    <div class="brand-caption">Система документооборота</div>
                </div>
            </div>

            <div class="user-area">
                <div class="user-info">
                    <span class="user-name">Иванов И. И.</span>
                    <span class="user-role">Инициатор</span>
                </div>

                <button
                    class="logout-button"
                    type="button"
                    @click="notice = 'Выход из системы будет подключён вместе с авторизацией.'"
                >
                    Выйти
                </button>
            </div>
        </header>

        <div class="app-body">
            <aside class="sidebar">
                <div class="sidebar-heading">НАВИГАЦИЯ</div>

                <nav class="navigation" aria-label="Основная навигация">
                    <button
                        v-for="section in [
                            'Главная',
                            'Мои документы',
                            'Создать документ',
                            'Согласования',
                            'Серверы',
                        ]"
                        :key="section"
                        class="nav-item"
                        :class="{
                            'nav-item-active': activeSection === section,
                        }"
                        type="button"
                        @click="
                            section === 'Создать документ'
                                ? createDocument()
                                : navigate(section)
                        "
                    >
                        <span class="nav-marker"></span>
                        {{ section }}
                    </button>
                </nav>

                <div class="sidebar-footer">
                    <div>TITLE*</div>
                    <div>Внутренняя система</div>
                </div>
            </aside>

            <main class="main-content">
                <div class="page-heading">
                    <div>
                        <div class="eyebrow">РАБОЧЕЕ ПРОСТРАНСТВО</div>
                        <h1>Главная</h1>
                        <p class="page-description">
                            Документы и конфигурационные работы
                        </p>
                    </div>

                    <button
                        class="primary-button"
                        type="button"
                        @click="createDocument"
                    >
                        <span class="button-plus">+</span>
                        Создать документ
                    </button>
                </div>

                <div v-if="notice" class="notice" role="status">
                    <span>{{ notice }}</span>

                    <button
                        class="notice-close"
                        type="button"
                        aria-label="Закрыть уведомление"
                        @click="notice = ''"
                    >
                        ×
                    </button>
                </div>

                <section class="quick-section">
                    <div class="section-heading">
                        <h2>Быстрые действия</h2>
                    </div>

                    <div class="quick-actions">
                        <button
                            class="action-card"
                            type="button"
                            @click="createDocument"
                        >
                            <span class="action-symbol">+</span>
                            <span class="action-content">
                                <span class="action-title">
                                    Создать документ
                                </span>
                                <span class="action-description">
                                    Оформить запрос на проведение работ
                                </span>
                            </span>
                            <span class="action-arrow">→</span>
                        </button>

                        <button
                            class="action-card"
                            type="button"
                            @click="navigate('Мои документы')"
                        >
                            <span class="action-symbol action-symbol-list">
                                ≡
                            </span>
                            <span class="action-content">
                                <span class="action-title">
                                    Мои документы
                                </span>
                                <span class="action-description">
                                    Просмотреть созданные документы
                                </span>
                            </span>
                            <span class="action-arrow">→</span>
                        </button>
                    </div>
                </section>

                <section class="documents-section">
                    <div class="section-heading documents-heading">
                        <div>
                            <h2>Последние документы</h2>
                        </div>

                        <button
                            class="text-button"
                            type="button"
                            @click="navigate('Мои документы')"
                        >
                            Все документы →
                        </button>
                    </div>

                    <div class="table-wrapper">
                        <table class="documents-table">
                            <thead>
                                <tr>
                                    <th>Регистрационный номер</th>
                                    <th>Название</th>
                                    <th>Статус</th>
                                    <th>Дата</th>
                                    <th>
                                        <span class="visually-hidden">
                                            Действия
                                        </span>
                                    </th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr
                                    v-for="document in documents"
                                    :key="document.id"
                                >
                                    <td class="document-id">
                                        {{ document.id }}
                                    </td>

                                    <td class="document-title">
                                        {{ document.title }}
                                    </td>

                                    <td>
                                        <span
                                            class="status"
                                            :class="statusClass(document.status)"
                                        >
                                            {{ document.status }}
                                        </span>
                                    </td>

                                    <td class="document-date">
                                        {{ document.date }}
                                    </td>

                                    <td class="document-action">
                                        <button
                                            class="open-button"
                                            type="button"
                                            :aria-label="`Открыть ${document.id}`"
                                            @click="openDocument(document)"
                                        >
                                            →
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>

                <footer class="page-footer">
                    INFRA-DOCFLOW
                    <span>Система управления документами и инфраструктурой</span>
                </footer>
            </main>
        </div>
    </div>
</template>

<style src="../styles/home.css"></style>
