<template>
  <div class="join-page">
    <form @submit.prevent="handleJoin" class="join-form">
      <h1>회원가입</h1>
      <div class="form-group">
        <label for="name">이름</label>
        <input
          type="text"
          id="name"
          v-model="name"
          placeholder="이름을 입력하세요"
          required
        />
      </div>
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
      <button type="submit" class="join-button">회원가입</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const name = ref('');
const email = ref('');
const password = ref('');
const router = useRouter();

const handleJoin = () => {
  if (name.value && email.value && password.value) {
    console.log('회원가입 정보:', { name: name.value, email: email.value, password: password.value });
    alert('회원가입 성공!');
    router.push('/login'); // 회원가입 완료 후 로그인 페이지로 이동
  } else {
    alert('모든 필드를 채워주세요.');
  }
};
</script>

<style scoped>
.join-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f9fafc;
  padding: 1rem;
}

.join-form {
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

.join-button {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.join-button:hover {
  background-color: #0056b3;
}
</style>
