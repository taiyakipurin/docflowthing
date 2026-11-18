<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api/auth'

const router = useRouter()

const username = ref('')
const password = ref('')
const isSubmitting = ref(false)
const errorMessage = ref('')

async function handleSubmit()
{
    if (!username.value || !password.value)
    {
        return
    }

    isSubmitting.value = true
    errorMessage.value = ''

    try
    {
        await login(username.value, password.value)
        await router.replace({ name: 'documents' })
    }
    catch (error)
    {
        if (error instanceof Error)
        {
            errorMessage.value = error.message
        }
        else
        {
            errorMessage.value = 'Error occurred while connecting to the server'
        }
    }

    finally
    {
        isSubmitting.value = false
    }
}
</script>

<template>
    <main class="login-page">
        <section class="login-panel">
            <header class="login-header">
                <div class="system-name">DOCFLOW</div>
                <h1>Вход в систему</h1>
                <p>Введите учётные данные для продолжения</p>
            </header>

            <form class="login-form" @submit.prevent="handleSubmit">
                <div class="form-field">
                    <label for="username">Имя пользователя</label>
                    <input
                        id="username"
                        v-model="username"
                        type="text"
                        autocomplete="username"
                        placeholder="Введите имя пользователя"
                        required
                    >
                </div>

                <div class="form-field">
                    <label for="password">Пароль</label>
                    <input
                        id="password"
                        v-model="password"
                        type="password"
                        autocomplete="current-password"
                        placeholder="Введите пароль"
                        required
                    >
                </div>

                <p v-if="errorMessage" class="login-error">
                    {{ errorMessage }}
                </p>

                <button type="submit" :disabled="isSubmitting">
                    {{ isSubmitting ? 'Вход...' : 'Войти' }}
                </button>
            </form>

            <footer class="login-footer">
                DOCFLOW — система документооборота предприятия
            </footer>
        </section>
    </main>
</template>

<style scoped>
.login-page
{
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    background: #e9e9e9;
    color: #222;
    font-family: Arial, sans-serif;
}

.login-panel
{
    width: 100%;
    max-width: 420px;
    padding: 40px;
    background: #fff;
    border: 1px solid #bdbdbd;
}

.login-header
{
    margin-bottom: 32px;
}

.system-name
{
    margin-bottom: 28px;
    color: #555;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
}

.login-header h1
{
    margin: 0 0 10px;
    font-size: 25px;
    font-weight: 600;
}

.login-header p
{
    margin: 0;
    color: #777;
    font-size: 14px;
    line-height: 1.5;
}

.login-form
{
    display: flex;
    flex-direction: column;
    gap: 22px;
}

.form-field
{
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-field label
{
    font-size: 14px;
    font-weight: 600;
}

.form-field input
{
    width: 100%;
    height: 42px;
    box-sizing: border-box;
    padding: 0 12px;
    border: 1px solid #aaa;
    border-radius: 0;
    outline: none;
    background: #fff;
    color: #222;
    font-size: 14px;
}

.form-field input:focus
{
    border-color: #333;
}

.form-field input::placeholder
{
    color: #999;
}

.login-form button
{
    height: 42px;
    margin-top: 4px;
    border: 1px solid #222;
    border-radius: 0;
    background: #333;
    color: #fff;
    font-size: 14px;
    cursor: pointer;
}

.login-form button:hover
{
    background: #222;
}

.login-form button:disabled
{
    background: #777;
    cursor: default;
}

.login-footer
{
    margin-top: 32px;
    padding-top: 18px;
    border-top: 1px solid #ddd;
    color: #888;
    font-size: 11px;
    line-height: 1.5;
}

.login-error
{
    margin: 0;
    color: #b42318;
    font-size: 13px;
}

@media (max-width: 480px)
{
    .login-panel
    {
        padding: 28px 22px;
    }
}
</style>