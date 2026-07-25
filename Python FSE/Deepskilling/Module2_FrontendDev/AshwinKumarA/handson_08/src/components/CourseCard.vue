<template>
  <article class="course-card">
    <h2>{{ name }}</h2>

    <p>
      <strong>Course Code:</strong>
      {{ code }}
    </p>

    <p>
      <strong>Credits:</strong>
      {{ credits }}
    </p>

    <p>
      <strong>Grade:</strong>
      {{ grade }}
    </p>

    <span class="details-text">View Course Details</span>
  </article>
</template>

<script setup>
defineProps({
  name: String,
  code: String,
  credits: Number,
  grade: String,
})
</script>

<style scoped>
.course-card {
  height: 100%;
  padding: 22px;
  border: 1px solid #d8ddc5;
  border-top: 5px solid #bfd42f;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgb(32 37 26 / 8%);
  transition:
    transform 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.course-card:hover {
  transform: translateY(-3px);
  border-color: #bfd42f;
  box-shadow: 0 6px 18px rgb(32 37 26 / 12%);
}

.course-card h2 {
  margin-bottom: 16px;
  color: #4d5900;
  font-size: 1.3rem;
  line-height: 1.35;
}

.course-card p {
  margin-bottom: 10px;
  color: #454b39;
  line-height: 1.5;
}

.course-card strong {
  color: #20251a;
}

.details-text {
  display: inline-block;
  margin-top: 10px;
  color: #4d5900;
  font-weight: 700;
}
</style>