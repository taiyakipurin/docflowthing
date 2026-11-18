import { createRouter, createWebHistory } from 'vue-router'

import MainLayout from '../layouts/MainLayout.vue'

import DocumentsView from '../views/DocumentsView.vue'

import LoginView from '../views/LoginView.vue'

const router = createRouter (
{
    history: createWebHistory(),

    routes:
    [
        {
            path: '/login',
            name: 'login',
            component: LoginView,
        },
        {
            path: '/',
            component: MainLayout,

            children:
            [
                {
                    path: '',
                    redirect: '/login'
                },
                {
                    name: 'documents',
                    path: 'documents',
                    component: DocumentsView
                },
                {
                    path: 'documents/new',
                    component: () => import('../views/DocumentCreateView.vue')
                },
                {
                    path: 'documents/:id',
                    component: () => import('../views/DocumentDetailView.vue')
                },
                {
                    path: 'approvals',
                    component: () => import('../views/ApprovalsView.vue')
                },
                {
                    path: 'servers',
                    component: () => import('../views/ServersView.vue')
                },
                {
                    path: 'executions',
                    component: () => import('../views/ExecutionsView.vue')
                },
                {
                    path: 'acts',
                    component: () => import('../views/ActsView.vue')
                },
                {
                    path: 'audit',
                    component: () => import('../views/AuditView.vue')
                },
                {
                    path: 'users',
                    component: () => import('../views/UsersView.vue')
                }
            ]
        },
    ]
})

export default router
