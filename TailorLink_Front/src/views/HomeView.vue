<template>
  <div class="home-page">
    <main class="home-content">
      <section>
        <h2>공지사항</h2>
        <p>최신 소식과 업데이트 내용을 확인하세요.</p>
      </section>
      <section>
        <h2>기능 탐색</h2>
        <p>다양한 기능과 서비스를 확인하고 이용해보세요.</p>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
// 현재 페이지는 별도의 스크립트 로직이 필요하지 않습니다.
</script>

<style scoped>
/* 홈 페이지 전체 레이아웃 */
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100vh;
  background-color: #f9fafc;
  padding: 1rem;
}

.home-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  width: 100%;
  max-width: 800px;
}

.home-content section {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.home-content h2 {
  font-size: 1.5rem;
  color: #007bff;
}

.home-content p {
  font-size: 1rem;
  color: #555555;
}
</style>
