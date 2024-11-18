<template>
  <div id="app">
    <header>
      <div class="nav-container">
        <!-- 로고 영역 -->
        <div class="logo">
          <RouterLink to="/">
            <img src="@/assets/TailorLink.png" alt="TailorLink Logo" />
          </RouterLink>
        </div>

        <!-- 메인 네비게이션 -->
        <nav class="main-nav">
          <RouterLink to="/">홈</RouterLink>
          <RouterLink to="/how-to">사용방법</RouterLink>
          <RouterLink to="/experience">체험</RouterLink>
          <RouterLink to="/support">고객센터</RouterLink>
        </nav>

        <!-- 로그인 및 회원가입 버튼 -->
        <div class="nav2">
          <RouterLink to="/login">Log-in</RouterLink>
          <RouterLink to="/join" class="join-button">Sign-up</RouterLink>
        </div>
      </div>
    </header>

    <!-- 라우터에서 렌더링되는 콘텐츠 -->
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>

<style>
/* 초기화 스타일 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

#app {
  padding-top: 70px; /* 헤더 높이만큼 여백 */
  min-height: 100vh;
  background-color: aliceblue;
}

/* 헤더 스타일 */
header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: #ffffff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

/* 로고 스타일 */
.logo {
  display: flex;
  align-items: center;
}

.logo img {
  height: 40px; /* 로고 크기 */
  cursor: pointer;
}

/* 메인 네비게이션 */
.main-nav {
  display: flex;
  gap: 2rem;
}

.main-nav a {
  text-decoration: none;
  color: #333333;
  font-weight: bold;
  font-size: 1rem;
}

.main-nav a:hover {
  text-decoration: underline;
}

/* 로그인 및 회원가입 버튼 영역 */
.nav2 {
  display: flex;
  align-items: center;
  gap: 1rem; /* 버튼 간격 추가 */
}

.nav2 a {
  text-decoration: none;
  color: #007bff;
  font-weight: bold;
  font-size: 1rem;
}

.nav2 a:hover {
  text-decoration: underline;
}

/* 회원가입 버튼 스타일 */
.join-button {
  color: #28a745; /* 초록색으로 설정 */
}

.join-button:hover {
  color: #1e7e34; /* 호버 시 더 진한 초록색 */
}

/* 메인 콘텐츠 */
main {
  margin-top: 1rem;
  padding: 2rem;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .main-nav {
    gap: 1rem;
  }

  .logo img {
    height: 30px; /* 모바일에서 로고 크기 조정 */
  }

  .nav-container {
    padding: 0 1rem;
  }
}
</style>
