# web/Dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN npm ci || yarn || pnpm i
COPY . .
RUN npm run build || yarn build || pnpm build

FROM nginx:alpine
# Nginx listens on 8080 for consistency with compose
EXPOSE 8080
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY dist /usr/share/nginx/html
