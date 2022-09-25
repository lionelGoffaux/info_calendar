FROM node:latest as builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

FROM httpd:2
COPY --from=builder /app/dist/ /usr/local/apache2/htdocs/
