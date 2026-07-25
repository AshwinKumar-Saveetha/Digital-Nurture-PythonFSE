<template>
  <main class="home-view">
    <section class="hero-section">
      <p class="welcome-label">Welcome</p>

      <h1>Student Portal</h1>

      <p class="hero-description">
        View your courses, check course details, and manage your student profile.
      </p>

      <RouterLink class="courses-button" to="/courses">
        Explore Courses
      </RouterLink>
    </section>
  </main>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.home-view {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 84px);
  padding: 40px 20px;
  background: linear-gradient(
    135deg,
    #f8faea 0%,
    #eff5c7 50%,
    #f4f6ee 100%
  );
}

.hero-section {
  width: 100%;
  max-width: 760px;
  padding: 55px 30px;
  border: 1px solid #d8ddc5;
  border-radius: 16px;
  background-color: #ffffff;
  text-align: center;
  box-shadow: 0 10px 30px rgb(32 37 26 / 12%);
}

.welcome-label {
  margin-bottom: 10px;
  color: #718000;
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.hero-section h1 {
  margin-bottom: 18px;
  color: #20251a;
  font-size: clamp(2rem, 5vw, 3.2rem);
}

.hero-description {
  max-width: 600px;
  margin: 0 auto 28px;
  color: #596048;
  font-size: 1.1rem;
  line-height: 1.7;
}

.courses-button {
  display: inline-block;
  padding: 13px 22px;
  border-radius: 7px;
  background-color: #bfd42f;
  color: #20251a;
  font-weight: 700;
  text-decoration: none;
  transition:
    background-color 0.2s ease,
    transform 0.2s ease;
}

.courses-button:hover {
  background-color: #aabd20;
  color: #20251a;
  transform: translateY(-2px);
}

.courses-button:focus {
  outline: 3px solid #718000;
  outline-offset: 3px;
}
</style>