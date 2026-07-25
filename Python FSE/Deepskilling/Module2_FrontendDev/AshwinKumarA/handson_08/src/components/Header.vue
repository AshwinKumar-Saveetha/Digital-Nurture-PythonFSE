<template>
  <header class="site-header">
    <div class="header-container">
      <RouterLink class="site-title" to="/">
        Student Portal
      </RouterLink>

      <nav aria-label="Main navigation">
        <RouterLink to="/">Home</RouterLink>

        <RouterLink to="/courses">
          Courses
        </RouterLink>

        <RouterLink to="/profile">
          Profile
          <span class="enrollment-count">
            {{ store.enrolledCourses.length }}
          </span>
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()
</script>

<style scoped>
.site-header {
  background-color: #bfd42f;
  color: #20251a;
  border-bottom: 4px solid #718000;
  box-shadow: 0 3px 10px rgb(32 37 26 / 14%);
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
}

.site-title {
  color: #20251a;
  font-size: 2rem;
  font-weight: 700;
  text-decoration: none;
  letter-spacing: 0.3px;
}

nav {
  display: flex;
  align-items: center;
  gap: 10px;
}

nav a {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 9px 13px;
  border-radius: 6px;
  color: #20251a;
  font-weight: 700;
  text-decoration: none;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
}

nav a:hover {
  background-color: #eff5c7;
  color: #4d5900;
}

nav a.router-link-exact-active {
  background-color: #4d5900;
  color: #ffffff;
}

.enrollment-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 7px;
  border-radius: 20px;
  background-color: #ffffff;
  color: #4d5900;
  font-size: 0.8rem;
  line-height: 1;
}

nav a.router-link-exact-active .enrollment-count {
  background-color: #bfd42f;
  color: #20251a;
}

@media (max-width: 650px) {
  .header-container {
    flex-direction: column;
    gap: 15px;
  }

  .site-title {
    font-size: 1.7rem;
  }

  nav {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>