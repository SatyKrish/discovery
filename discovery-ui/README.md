This UI uses Next.js and integrates Azure AD single sign-on via [NextAuth](https://next-auth.js.org/).

## Getting Started

Set the following environment variables to enable Azure AD login:

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

Open [http://localhost:3000](http://localhost:3000) to access the chat interface. Users must sign in with Azure AD before interacting with the chat.

## Learn More

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [NextAuth Azure AD Provider](https://next-auth.js.org/providers/azure-ad) - authentication setup details.
