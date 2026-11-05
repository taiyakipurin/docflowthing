<script setup lang="ts">
</script>

<template>
    <header class="app-header">
        <div class="header-breadcrumb">
            Информационная система / Документооборот
        </div>

        <div class="header-user">
            <span class="user-name">Тестовый пользователь</span>
            <span class="user-role">Инициатор</span>
        </div>
    </header>
</template>

<style scoped>
.app-header
{
    height: 58px;
    min-height: 58px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 24px;

    background: var(--color-background);
    border-bottom: 1px solid var(--color-border);
}

.header-breadcrumb
{
    font-size: 12px;
    color: var(--color-muted);
}

.header-user
{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 3px;
}

.user-name
{
    font-size: 12px;
    font-weight: bold;
}

.user-role
{
    font-size: 11px;
    color: var(--color-muted);
}
</style>
