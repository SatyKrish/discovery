This UI uses Next.js and integrates Azure AD single sign-on via [NextAuth](https://next-auth.js.org/). The interface defaults to the Inter typeface and smoothly fades between light and dark themes (respecting `prefers-reduced-motion`).

## Getting Started

During development (`npm run dev`) the chat is available without authentication. Copy `.env.example` to `.env.local` and adjust as needed. Key variable:

```bash
# For Next.js API route proxies to the agent backend
BACKEND_BASE_URL="http://localhost:8000"
```

Azure AD login is enabled only in production builds (`npm start`), where the following environment variables must be provided:

```bash
AZURE_AD_CLIENT_ID="..."
AZURE_AD_CLIENT_SECRET="..."
AZURE_AD_TENANT_ID="..."
NEXTAUTH_SECRET="...long-random-string..."
NEXTAUTH_URL="http://localhost:3000"
```

Then run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to access the chat interface.

## Styling

- Uses the [Inter](https://fonts.google.com/specimen/Inter) font with a `system-ui` fallback.
- Light/dark theme toggles fade using `transition-colors` and honor the user's `prefers-reduced-motion` setting.

## Learn More

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [NextAuth Azure AD Provider](https://next-auth.js.org/providers/azure-ad) - authentication setup details.
