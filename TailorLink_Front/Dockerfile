FROM node:18

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install -g pnpm

# 환경 변수 설정
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
ENV ESLINT_NO_DEV_ERRORS=true

# 나머지 소스 코드 복사
COPY . .

# 빌드
RUN pnpm run dev

EXPOSE 3000

CMD ["pnpm", "start"]