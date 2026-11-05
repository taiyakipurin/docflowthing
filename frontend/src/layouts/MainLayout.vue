<script setup lang="ts">
import AppSidebar from '../components/AppSidebar.vue'
import AppHeader from '../components/AppHeader.vue'
</script>

<template>
    <div class="app-layout">
        <AppSidebar />

        <div class="app-content">
            <AppHeader />

            <main class="main-content">
                <RouterView />
            </main>
        </div>
    </div>
</template>

<style scoped>
.app-layout
{
    display: flex;
    min-height: 100vh;
}

.app-content
{
    display: flex;
    flex-direction: column;
    flex: 1;
    min-width: 0;
}

.main-content
{
    flex: 1;
    padding: 24px;
    overflow-y: auto;
}
</style>
