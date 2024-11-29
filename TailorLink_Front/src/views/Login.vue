<template>
  <div class="login-page">
    <form @submit.prevent="handleLogin" class="login-form">
      <h1>로그인</h1>
      <div class="form-group">
        <label for="email">이메일</label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="이메일을 입력하세요"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">비밀번호</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="비밀번호를 입력하세요"
          required
        />
      </div>
      <div class="button-container">
        <button type="submit" class="login-button">로그인</button>
        <button type="button" class="join-button" @click="goToJoin">회원가입</button>
      </div>
    </form>

    <!-- 간편 로그인 버튼 -->
    <div class="social-login">
      <button class="social-button facebook" @click="loginWithFacebook">
        Facebook 로그인
      </button>
      <button class="social-button kakao" @click="loginWithKakao">
        카카오 로그인
      </button>
      <button class="social-button naver" @click="loginWithNaver">
        네이버 로그인
      </button>
      <button class="social-button google" @click="loginWithGoogle">
        Google 로그인
      </button>
    </div>
    <footer class="footer">
      <p>이용약관 | 개인정보 처리방침</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const router = useRouter();

const handleLogin = () => {
  if (email.value && password.value) {
    console.log('로그인 시도:', { email: email.value, password: password.value });
    alert('로그인 성공!');
    router.push('/'); // 성공 시 홈 페이지로 이동
  } else {
    alert('모든 필드를 채워주세요.');
  }
};

const goToJoin = () => {
  router.push('/join'); // 회원가입 페이지로 이동
};

const loginWithFacebook = () => {
  alert('Facebook 로그인 기능은 준비 중입니다.');
};

const loginWithKakao = () => {
  alert('Kakao 로그인 기능은 준비 중입니다.');
};

const loginWithNaver = () => {
  alert('Naver 로그인 기능은 준비 중입니다.');
};

const loginWithGoogle = () => {
  alert('Google 로그인 기능은 준비 중입니다.');
};
</script>

<style scoped>
.login-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f4f8;
  padding: 1rem;
}

.login-form {
  background: #ffffff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333333;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #555555;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  border-color: #007bff;
  outline: none;
}

.button-container {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

button {
  flex: 1;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button {
  background-color: #007bff;
  color: #ffffff;
}

.login-button:hover {
  background-color: #0056b3;
}

.join-button {
  background-color: #28a745;
  color: #ffffff;
}

.join-button:hover {
  background-color: #218838;
}

/* 간편 로그인 스타일 */
.social-login {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: 100%;
  max-width: 400px;
}

.social-button {
  width: 100%;
  max-width: 300px;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  text-align: center;
}

.facebook {
  background-color: #4267b2;
  color: #ffffff;
}

.facebook:hover {
  background-color: #365899;
}

.kakao {
  background-color: #fee500;
  color: #000000;
}

.kakao:hover {
  background-color: #ffd700;
}

.naver {
  background-color: #03c75a;
  color: #ffffff;
}

.naver:hover {
  background-color: #02a64f;
}

.google {
  background-color: #db4437;
  color: #ffffff;
}

.google:hover {
  background-color: #c33c28;
}

/* 푸터 스타일 */
.footer {
  margin-top: 2rem;
  font-size: 0.875rem;
  text-align: center;
  color: #888888;
}
</style>
