<template>
  <div id="app">
    <header>
      <img src="@/assets/TailorLink.png" alt="Logo" class="logo" />
      <nav>
        <RouterLink to="#Home">홈</RouterLink>
        <RouterLink to="#사용방법">사용방법</RouterLink>
        <RouterLink to="#체험">체험</RouterLink>
        <RouterLink to="#????s>????</RouterLink>
        <RouterLink to="#계정">계정</RouterLink>
        <RouterLink to="#로그인">Log-in</RouterLink>
      </nav>
    </header>
    <!-- 다른 콘텐츠가 있다면 여기에 추가 -->
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style>
header {
  background-color: #FFFDF5;
  padding: 1rem 0;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  display: flex;
  align-items: center;
  z-index: 1000;
}

.logo {
  height: 30px;
  margin-right: 0.3rem;
  margin-left: 1.5rem;
}

nav {
  display: flex;
  justify-content: center;
  gap: 3.0rem;
  flex-grow: 1;
}

nav a {
  color: #000000;
  text-decoration: none;
  font-weight: bold;
}

nav a:hover {
  text-decoration: underline;
}

#app {
  padding-top: 60px; /* 헤더 높이만큼 여백 추가 */
  background-image: url('@/assets/BackGround.png'); /* 배경 이미지 추가 */
  background-size: cover; /* 이미지가 화면을 채우도록 조정 */
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed; /* 스크롤 시 배경 고정 */
  width: 100vw; /* 전체 너비 차지 */
  min-height: 100vh; /* 전체 높이 차지 */
  overflow-x: hidden; /* 가로 스크롤 제거 */
}
</style>
