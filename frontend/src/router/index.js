import { createRouter, createWebHistory } from "vue-router";
import { authState, loadCurrentIdentity, hasPermission } from "../state/auth";

const routes = [
  { path: "/", name: "landing", component: () => import("../pages/LandingPage.vue") },
  { path: "/login", name: "login", component: () => import("../pages/LoginPage.vue") },
  { path: "/register", name: "register", component: () => import("../pages/RegisterPage.vue") },
  { path: "/forgot-password", name: "forgot-password", component: () => import("../pages/ForgotPasswordPage.vue") },
  { path: "/reset-password", name: "reset-password", component: () => import("../pages/ResetPasswordPage.vue") },
  { path: "/verify-email", name: "verify-email", component: () => import("../pages/VerifyEmailPage.vue") },
  {
    path: "/home",
    name: "home",
    component: () => import("../pages/HomePage.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/profile",
    name: "profile",
    component: () => import("../pages/ProfilePage.vue"),
    meta: { requiresAuth: true, permission: "profile.view" },
  },
  {
    path: "/reports",
    name: "reports",
    component: () => import("../pages/ReportsPage.vue"),
    meta: { requiresAuth: true, permission: "reports.view" },
  },
  {
    path: "/search",
    name: "search",
    component: () => import("../pages/SearchPage.vue"),
    meta: { requiresAuth: true, permission: "search.execute" },
  },
  {
    path: "/files",
    name: "files",
    component: () => import("../pages/FilesPage.vue"),
    meta: { requiresAuth: true, permission: "file.view" },
  },
  {
    path: "/administration",
    name: "administration",
    component: () => import("../pages/AdministrationPage.vue"),
    meta: { requiresAuth: true, permission: "admin.access" },
  },
  { path: "/access-denied", name: "access-denied", component: () => import("../pages/AccessDeniedPage.vue") },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach(async (to) => {
  if (!authState.ready) {
    await loadCurrentIdentity();
  }

  // Authentication failure and authorization failure stay distinct, per the
  // application's security requirements: unauthenticated visitors go to
  // /login; authenticated visitors missing a permission go to /access-denied.
  if (to.meta.requiresAuth && !authState.subjectId) {
    return { name: "login", query: { next: to.fullPath } };
  }

  if (to.meta.permission && !hasPermission(to.meta.permission)) {
    return { name: "access-denied" };
  }

  return true;
});
