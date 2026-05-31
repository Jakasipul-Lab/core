# Step 1: Use an official, secure Node image to build the app
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Step 2: Create the production runner to keep the final image tiny and fast
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built assets from step 1
COPY --from:builder /app/public ./public
COPY --from:builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from:builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000

CMD ["node", "server.js"]
