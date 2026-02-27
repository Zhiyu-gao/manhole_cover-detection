# Frontend (Vue 3)

This frontend is part of the manhole-cover detection system.

## Scripts

```bash
npm install
npm run serve
npm run build
npm run lint
```

## Notes

- API base URL can be overridden by `VUE_APP_API_BASE_URL`.
- Route-level auth guard is configured in `src/router/index.js`.
- Shared defect-category constants are in `src/constants/categories.js`.
