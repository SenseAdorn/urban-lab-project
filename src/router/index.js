import { createRouter, createWebHistory } from 'vue-router';

// Import components for routing
import LoginPage from '../pages/LoginPage.vue';
import DashboardPage from '../pages/DashboardPage.vue';
import StudentsPage from '../pages/StudentsPage.vue';
import ContactsPage from '../pages/ContactsPage.vue';
import EventsPage from '../pages/EventsPage.vue';
import GrantsPage from '../pages/GrantsPage.vue';
import InteractionsPage from '../pages/InteractionsPage.vue';
import RegisterPage from '../pages/RegisterPage.vue';
import NotFoundPage from '../pages/NotFoundPage.vue'; // 404 Page Component
import AddData from '../pages/AddData.vue';

// Define routes
const routes = [
    { path: '/', redirect: '/login' }, // Default route redirects to /login
    { path: '/login', component: LoginPage },
    { path: '/dashboard', component: DashboardPage },
    { path: '/students', component: StudentsPage },
    { path: '/contacts', component: ContactsPage },
    { path: '/events', component: EventsPage },
    { path: '/grants', component: GrantsPage },
    { path: '/interactions', component: InteractionsPage },
    { path: '/register', component: RegisterPage },
    { path: '/:pathMatch(.*)*', component: NotFoundPage },
    { path: '/add-data', component: AddData }, // Catch-all 404 route
];

// Create router instance
const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Navigation guards
router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('access_token');

    if (to.path !== '/login' && !isAuthenticated) {
        // If not authenticated, redirect to login
        next('/login');
    } else if (to.path === '/login' && isAuthenticated) {
        // Prevent authenticated users from accessing login page
        next('/dashboard');
    } else {
        // Proceed to the route
        next();
    }
});

export default router;
