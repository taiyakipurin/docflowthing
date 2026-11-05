<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

const navigation = [
    {
        title: 'ДОКУМЕНТООБОРОТ',
        items: [
            { label: 'Документы', path: '/documents' },
            { label: 'Согласование', path: '/approvals' }
        ]
    },
    {
        title: 'ИНФРАСТРУКТУРА',
        items: [
            { label: 'Серверы', path: '/servers' },
            { label: 'Выполнение работ', path: '/executions' }
        ]
    },
    {
        title: 'УЧЁТ',
        items: [
            { label: 'Электронные акты', path: '/acts' },
            { label: 'Журнал аудита', path: '/audit' }
        ]
    },
    {
        title: 'АДМИНИСТРИРОВАНИЕ',
        items: [
            { label: 'Пользователи', path: '/users' }
        ]
    }
]

function isActive(path: string): boolean
{
    if (path === '/documents')
    {
        return route.path === path ||
            route.path.startsWith('/documents/')
    }

    return route.path === path
}
</script>

<template>
    <aside class="sidebar">
        <div class="sidebar-brand">
            <span class="brand-name">DOCFLOW</span>
            <span class="brand-description">Enterprise system</span>
        </div>

        <nav class="sidebar-navigation">
            <section
                v-for="group in navigation"
                :key="group.title"
                class="navigation-group"
            >
                <h3 class="navigation-title">
                    {{ group.title }}
                </h3>

                <RouterLink
                    v-for="item in group.items"
                    :key="item.path"
                    :to="item.path"
                    class="navigation-link"
                    :class="{ active: isActive(item.path) }"
                >
                    {{ item.label }}
                </RouterLink>
            </section>
        </nav>

        <div class="sidebar-footer">
            DOCFLOW v0.1
        </div>
    </aside>
</template>

<style scoped>
.sidebar
{
    width: var(--sidebar-width);
    min-width: var(--sidebar-width);
    height: 100vh;

    display: flex;
    flex-direction: column;

    background: var(--color-sidebar);
    border-right: 1px solid var(--color-border);
}

.sidebar-brand
{
    display: flex;
    flex-direction: column;
    gap: 4px;

    padding: 20px 16px;
    border-bottom: 1px solid var(--color-border);
}

.brand-name
{
    font-size: 19px;
    font-weight: bold;
    letter-spacing: 1px;
}

.brand-description
{
    font-size: 11px;
    color: var(--color-muted);
}

.sidebar-navigation
{
    flex: 1;
    padding: 12px 8px;
}

.navigation-group
{
    margin-bottom: 24px;
}

.navigation-title
{
    margin: 0;
    padding: 8px;

    font-size: 10px;
    font-weight: bold;
    letter-spacing: 0.7px;
    color: var(--color-muted);
}

.navigation-link
{
    display: block;
    padding: 9px 10px;

    font-size: 13px;
    color: var(--color-text);

    border-left: 3px solid transparent;
}

.navigation-link:hover
{
    background: #dfe1e4;
}

.navigation-link.active
{
    background: #d4d8dc;
    border-left-color: var(--color-primary);
    font-weight: bold;
}

.sidebar-footer
{
    padding: 12px 16px;
    border-top: 1px solid var(--color-border);

    font-size: 10px;
    color: var(--color-muted);
}
</style>
