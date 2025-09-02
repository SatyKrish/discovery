================================================
FILE: README.md
================================================
<a href="https://chat.vercel.ai/">
  <img alt="Next.js 14 and App Router-ready AI chatbot." src="app/(chat)/opengraph-image.png">
  <h1 align="center">Chat SDK</h1>
</a>

<p align="center">
    Chat SDK is a free, open-source template built with Next.js and the AI SDK that helps you quickly build powerful chatbot applications.
</p>

<p align="center">
  <a href="https://chat-sdk.dev"><strong>Read Docs</strong></a> ·
  <a href="#features"><strong>Features</strong></a> ·
  <a href="#model-providers"><strong>Model Providers</strong></a> ·
  <a href="#deploy-your-own"><strong>Deploy Your Own</strong></a> ·
  <a href="#running-locally"><strong>Running locally</strong></a>
</p>
<br/>

## Features

- [Next.js](https://nextjs.org) App Router
  - Advanced routing for seamless navigation and performance
  - React Server Components (RSCs) and Server Actions for server-side rendering and increased performance
- [AI SDK](https://sdk.vercel.ai/docs)
  - Unified API for generating text, structured objects, and tool calls with LLMs
  - Hooks for building dynamic chat and generative user interfaces
  - Supports xAI (default), OpenAI, Fireworks, and other model providers
- [shadcn/ui](https://ui.shadcn.com)
  - Styling with [Tailwind CSS](https://tailwindcss.com)
  - Component primitives from [Radix UI](https://radix-ui.com) for accessibility and flexibility
- Data Persistence
  - [Neon Serverless Postgres](https://vercel.com/marketplace/neon) for saving chat history and user data
  - [Vercel Blob](https://vercel.com/storage/blob) for efficient file storage
- [Auth.js](https://authjs.dev)
  - Simple and secure authentication

## Model Providers

This template uses the [Vercel AI Gateway](https://vercel.com/docs/ai-gateway) to access multiple AI models through a unified interface. The default configuration includes [xAI](https://x.ai) models (`grok-2-vision-1212`, `grok-3-mini-beta`) routed through the gateway.

### AI Gateway Authentication

**For Vercel deployments**: Authentication is handled automatically via OIDC tokens.

**For non-Vercel deployments**: You need to provide an AI Gateway API key by setting the `AI_GATEWAY_API_KEY` environment variable in your `.env.local` file.

With the [AI SDK](https://ai-sdk.dev/docs/introduction), you can also switch to direct LLM providers like [OpenAI](https://openai.com), [Anthropic](https://anthropic.com), [Cohere](https://cohere.com/), and [many more](https://ai-sdk.dev/providers/ai-sdk-providers) with just a few lines of code.

## Deploy Your Own

You can deploy your own version of the Next.js AI Chatbot to Vercel with one click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fai-chatbot&env=AUTH_SECRET&envDescription=Learn+more+about+how+to+get+the+API+Keys+for+the+application&envLink=https%3A%2F%2Fgithub.com%2Fvercel%2Fai-chatbot%2Fblob%2Fmain%2F.env.example&demo-title=AI+Chatbot&demo-description=An+Open-Source+AI+Chatbot+Template+Built+With+Next.js+and+the+AI+SDK+by+Vercel.&demo-url=https%3A%2F%2Fchat.vercel.ai&products=%5B%7B%22type%22%3A%22integration%22%2C%22protocol%22%3A%22ai%22%2C%22productSlug%22%3A%22grok%22%2C%22integrationSlug%22%3A%22xai%22%7D%2C%7B%22type%22%3A%22integration%22%2C%22protocol%22%3A%22storage%22%2C%22productSlug%22%3A%22neon%22%2C%22integrationSlug%22%3A%22neon%22%7D%2C%7B%22type%22%3A%22integration%22%2C%22protocol%22%3A%22storage%22%2C%22productSlug%22%3A%22upstash-kv%22%2C%22integrationSlug%22%3A%22upstash%22%7D%2C%7B%22type%22%3A%22blob%22%7D%5D)

## Running locally

You will need to use the environment variables [defined in `.env.example`](.env.example) to run Next.js AI Chatbot. It's recommended you use [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables) for this, but a `.env` file is all that is necessary.

> Note: You should not commit your `.env` file or it will expose secrets that will allow others to control access to your various AI and authentication provider accounts.

1. Install Vercel CLI: `npm i -g vercel`
2. Link local instance with Vercel and GitHub accounts (creates `.vercel` directory): `vercel link`
3. Download your environment variables: `vercel env pull`

```bash
pnpm install
pnpm dev
```

Your app template should now be running on [localhost:3000](http://localhost:3000).



================================================
FILE: biome.jsonc
================================================
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "files": {
    "ignoreUnknown": false,
    "ignore": [
      "**/pnpm-lock.yaml",
      "lib/db/migrations",
      "lib/editor/react-renderer.tsx",
      "node_modules",
      ".next",
      "public",
      ".vercel"
    ]
  },
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "defaultBranch": "main",
    "useIgnoreFile": true
  },
  "formatter": {
    "enabled": true,
    "formatWithErrors": false,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineEnding": "lf",
    "lineWidth": 80,
    "attributePosition": "auto"
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "a11y": {
        "useHtmlLang": "warn", // Not in recommended ruleset, turning on manually
        "noHeaderScope": "warn", // Not in recommended ruleset, turning on manually
        "useValidAriaRole": {
          "level": "warn",
          "options": {
            "ignoreNonDom": false,
            "allowInvalidRoles": ["none", "text"]
          }
        },
        "useSemanticElements": "off", // Rule is buggy, revisit later
        "noSvgWithoutTitle": "off", // We do not intend to adhere to this rule
        "useMediaCaption": "off", // We would need a cultural change to turn this on
        "noAutofocus": "off", // We're highly intentional about when we use autofocus
        "noBlankTarget": "off", // Covered by Conformance
        "useFocusableInteractive": "off", // Disable focusable interactive element requirement
        "useAriaPropsForRole": "off", // Disable required ARIA attributes check
        "useKeyWithClickEvents": "off" // Disable keyboard event requirement with click events
      },
      "complexity": {
        "noUselessStringConcat": "warn", // Not in recommended ruleset, turning on manually
        "noForEach": "off", // forEach is too familiar to ban
        "noUselessSwitchCase": "off", // Turned off due to developer preferences
        "noUselessThisAlias": "off", // Turned off due to developer preferences
        "noBannedTypes": "off"
      },
      "correctness": {
        "noUnusedImports": "warn", // Not in recommended ruleset, turning on manually
        "useArrayLiterals": "warn", // Not in recommended ruleset, turning on manually
        "noNewSymbol": "warn", // Not in recommended ruleset, turning on manually
        "useJsxKeyInIterable": "off", // Rule is buggy, revisit later
        "useExhaustiveDependencies": "off", // Community feedback on this rule has been poor, we will continue with ESLint
        "noUnnecessaryContinue": "off" // Turned off due to developer preferences
      },
      "security": {
        "noDangerouslySetInnerHtml": "off" // Covered by Conformance
      },
      "style": {
        "useFragmentSyntax": "warn", // Not in recommended ruleset, turning on manually
        "noYodaExpression": "warn", // Not in recommended ruleset, turning on manually
        "useDefaultParameterLast": "warn", // Not in recommended ruleset, turning on manually
        "useExponentiationOperator": "off", // Obscure and arguably not easily readable
        "noUnusedTemplateLiteral": "off", // Stylistic opinion
        "noUselessElse": "off" // Stylistic opinion
      },
      "suspicious": {
        "noExplicitAny": "off" // We trust Vercelians to use any only when necessary
      },
      "nursery": {
        "noStaticElementInteractions": "warn",
        "noHeadImportInDocument": "warn",
        "noDocumentImportInPage": "warn",
        "noDuplicateElseIf": "warn",
        "noIrregularWhitespace": "warn",
        "useValidAutocomplete": "warn"
      }
    }
  },
  "javascript": {
    "jsxRuntime": "reactClassic",
    "formatter": {
      "jsxQuoteStyle": "double",
      "quoteProperties": "asNeeded",
      "trailingCommas": "all",
      "semicolons": "always",
      "arrowParentheses": "always",
      "bracketSpacing": true,
      "bracketSameLine": false,
      "quoteStyle": "single",
      "attributePosition": "auto"
    }
  },
  "json": {
    "formatter": {
      "enabled": true,
      "trailingCommas": "none"
    },
    "parser": {
      "allowComments": true,
      "allowTrailingCommas": false
    }
  },
  "css": {
    "formatter": { "enabled": false },
    "linter": { "enabled": false }
  },
  "organizeImports": { "enabled": false },
  "overrides": [
    // Playwright requires an object destructure, even if empty
    // https://github.com/microsoft/playwright/issues/30007
    {
      "include": ["playwright/**"],
      "linter": {
        "rules": {
          "correctness": {
            "noEmptyPattern": "off"
          }
        }
      }
    }
  ]
}



================================================
FILE: components.json
================================================
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}



================================================
FILE: drizzle.config.ts
================================================
import { config } from 'dotenv';
import { defineConfig } from 'drizzle-kit';

config({
  path: '.env.local',
});

export default defineConfig({
  schema: './lib/db/schema.ts',
  out: './lib/db/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    // biome-ignore lint: Forbidden non-null assertion.
    url: process.env.POSTGRES_URL!,
  },
});



================================================
FILE: instrumentation.ts
================================================
import { registerOTel } from '@vercel/otel';

export function register() {
  registerOTel({ serviceName: 'ai-chatbot' });
}



================================================
FILE: LICENSE
================================================
Copyright 2024 Vercel, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


================================================
FILE: middleware.ts
================================================
import { NextResponse, type NextRequest } from 'next/server';
import { getToken } from 'next-auth/jwt';
import { guestRegex, isDevelopmentEnvironment } from './lib/constants';

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  /*
   * Playwright starts the dev server and requires a 200 status to
   * begin the tests, so this ensures that the tests can start
   */
  if (pathname.startsWith('/ping')) {
    return new Response('pong', { status: 200 });
  }

  if (pathname.startsWith('/api/auth')) {
    return NextResponse.next();
  }

  const token = await getToken({
    req: request,
    secret: process.env.AUTH_SECRET,
    secureCookie: !isDevelopmentEnvironment,
  });

  if (!token) {
    const redirectUrl = encodeURIComponent(request.url);

    return NextResponse.redirect(
      new URL(`/api/auth/guest?redirectUrl=${redirectUrl}`, request.url),
    );
  }

  const isGuest = guestRegex.test(token?.email ?? '');

  if (token && !isGuest && ['/login', '/register'].includes(pathname)) {
    return NextResponse.redirect(new URL('/', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/',
    '/chat/:id',
    '/api/:path*',
    '/login',
    '/register',

    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico, sitemap.xml, robots.txt (metadata files)
     */
    '/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
  ],
};



================================================
FILE: next-env.d.ts
================================================
/// <reference types="next" />
/// <reference types="next/image-types/global" />

// NOTE: This file should not be edited
// see https://nextjs.org/docs/app/api-reference/config/typescript for more information.



================================================
FILE: next.config.ts
================================================
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  experimental: {
    ppr: true,
  },
  images: {
    remotePatterns: [
      {
        hostname: 'avatar.vercel.sh',
      },
    ],
  },
};

export default nextConfig;



================================================
FILE: package.json
================================================
{
  "name": "ai-chatbot",
  "version": "3.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev --turbo",
    "build": "tsx lib/db/migrate && next build",
    "start": "next start",
    "lint": "next lint && biome lint --write --unsafe",
    "lint:fix": "next lint --fix && biome lint --write --unsafe",
    "format": "biome format --write",
    "db:generate": "drizzle-kit generate",
    "db:migrate": "npx tsx lib/db/migrate.ts",
    "db:studio": "drizzle-kit studio",
    "db:push": "drizzle-kit push",
    "db:pull": "drizzle-kit pull",
    "db:check": "drizzle-kit check",
    "db:up": "drizzle-kit up",
    "test": "export PLAYWRIGHT=True && pnpm exec playwright test"
  },
  "dependencies": {
    "@ai-sdk/gateway": "^1.0.15",
    "@ai-sdk/provider": "2.0.0",
    "@ai-sdk/react": "2.0.26",
    "@ai-sdk/xai": "2.0.13",
    "@codemirror/lang-javascript": "^6.2.2",
    "@codemirror/lang-python": "^6.1.6",
    "@codemirror/state": "^6.5.0",
    "@codemirror/theme-one-dark": "^6.1.2",
    "@codemirror/view": "^6.35.3",
    "@icons-pack/react-simple-icons": "^13.7.0",
    "@opentelemetry/api": "^1.9.0",
    "@opentelemetry/api-logs": "^0.200.0",
    "@radix-ui/react-alert-dialog": "^1.1.2",
    "@radix-ui/react-avatar": "^1.1.10",
    "@radix-ui/react-collapsible": "^1.1.12",
    "@radix-ui/react-dialog": "^1.1.2",
    "@radix-ui/react-dropdown-menu": "^2.1.2",
    "@radix-ui/react-hover-card": "^1.1.15",
    "@radix-ui/react-icons": "^1.3.0",
    "@radix-ui/react-label": "^2.1.0",
    "@radix-ui/react-scroll-area": "^1.2.10",
    "@radix-ui/react-select": "^2.1.2",
    "@radix-ui/react-separator": "^1.1.0",
    "@radix-ui/react-slot": "^1.1.2",
    "@radix-ui/react-tooltip": "^1.1.3",
    "@radix-ui/react-use-controllable-state": "^1.2.2",
    "@radix-ui/react-visually-hidden": "^1.1.0",
    "@vercel/analytics": "^1.3.1",
    "@vercel/blob": "^0.24.1",
    "@vercel/functions": "^2.0.0",
    "@vercel/otel": "^1.12.0",
    "@vercel/postgres": "^0.10.0",
    "ai": "5.0.26",
    "bcrypt-ts": "^5.0.2",
    "class-variance-authority": "^0.7.0",
    "classnames": "^2.5.1",
    "clsx": "^2.1.1",
    "codemirror": "^6.0.1",
    "date-fns": "^4.1.0",
    "diff-match-patch": "^1.0.5",
    "dotenv": "^16.4.5",
    "drizzle-orm": "^0.34.0",
    "embla-carousel-react": "^8.6.0",
    "fast-deep-equal": "^3.1.3",
    "framer-motion": "^11.3.19",
    "geist": "^1.3.1",
    "lucide-react": "^0.446.0",
    "nanoid": "^5.0.8",
    "next": "15.3.0-canary.31",
    "next-auth": "5.0.0-beta.25",
    "next-themes": "^0.3.0",
    "orderedmap": "^2.1.1",
    "papaparse": "^5.5.2",
    "postgres": "^3.4.4",
    "prosemirror-example-setup": "^1.2.3",
    "prosemirror-inputrules": "^1.4.0",
    "prosemirror-markdown": "^1.13.1",
    "prosemirror-model": "^1.23.0",
    "prosemirror-schema-basic": "^1.2.3",
    "prosemirror-schema-list": "^1.4.1",
    "prosemirror-state": "^1.4.3",
    "prosemirror-view": "^1.34.3",
    "react": "19.0.0-rc-45804af1-20241021",
    "react-data-grid": "7.0.0-beta.47",
    "react-dom": "19.0.0-rc-45804af1-20241021",
    "react-resizable-panels": "^2.1.7",
    "react-syntax-highlighter": "^15.6.6",
    "redis": "^5.0.0",
    "resumable-stream": "^2.0.0",
    "server-only": "^0.0.1",
    "shiki": "^3.12.0",
    "sonner": "^1.5.0",
    "streamdown": "^1.1.6",
    "swr": "^2.2.5",
    "tailwind-merge": "^2.5.2",
    "tailwindcss-animate": "^1.0.7",
    "use-stick-to-bottom": "^1.1.1",
    "usehooks-ts": "^3.1.0",
    "zod": "^3.25.76"
  },
  "devDependencies": {
    "@biomejs/biome": "1.9.4",
    "@playwright/test": "^1.50.1",
    "@tailwindcss/typography": "^0.5.15",
    "@types/d3-scale": "^4.0.8",
    "@types/node": "^22.8.6",
    "@types/papaparse": "^5.3.15",
    "@types/pdf-parse": "^1.1.4",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "@types/react-syntax-highlighter": "^15.5.13",
    "drizzle-kit": "^0.25.0",
    "eslint": "^8.57.0",
    "eslint-config-next": "14.2.5",
    "eslint-config-prettier": "^9.1.0",
    "eslint-import-resolver-typescript": "^3.6.3",
    "eslint-plugin-tailwindcss": "^3.17.5",
    "postcss": "^8",
    "tailwindcss": "^3.4.1",
    "tsx": "^4.19.1",
    "typescript": "^5.6.3"
  },
  "packageManager": "pnpm@9.12.3"
}



================================================
FILE: playwright.config.ts
================================================
import { defineConfig, devices } from '@playwright/test';

/**
 * Read environment variables from file.
 * https://github.com/motdotla/dotenv
 */
import { config } from 'dotenv';

config({
  path: '.env.local',
});

/* Use process.env.PORT by default and fallback to port 3000 */
const PORT = process.env.PORT || 3000;

/**
 * Set webServer.url and use.baseURL with the location
 * of the WebServer respecting the correct set port
 */
const baseURL = `http://localhost:${PORT}`;

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  testDir: './tests',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: 0,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 2 : 8,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: 'html',
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL,

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'retain-on-failure',
  },

  /* Configure global timeout for each test */
  timeout: 240 * 1000, // 120 seconds
  expect: {
    timeout: 240 * 1000,
  },

  /* Configure projects */
  projects: [
    {
      name: 'e2e',
      testMatch: /e2e\/.*.test.ts/,
      use: {
        ...devices['Desktop Chrome'],
      },
    },
    {
      name: 'routes',
      testMatch: /routes\/.*.test.ts/,
      use: {
        ...devices['Desktop Chrome'],
      },
    },

    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },

    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },

    /* Test against mobile viewports. */
    // {
    //   name: 'Mobile Chrome',
    //   use: { ...devices['Pixel 5'] },
    // },
    // {
    //   name: 'Mobile Safari',
    //   use: { ...devices['iPhone 12'] },
    // },

    /* Test against branded browsers. */
    // {
    //   name: 'Microsoft Edge',
    //   use: { ...devices['Desktop Edge'], channel: 'msedge' },
    // },
    // {
    //   name: 'Google Chrome',
    //   use: { ...devices['Desktop Chrome'], channel: 'chrome' },
    // },
  ],

  /* Run your local dev server before starting the tests */
  webServer: {
    command: 'pnpm dev',
    url: `${baseURL}/ping`,
    timeout: 120 * 1000,
    reuseExistingServer: !process.env.CI,
  },
});



================================================
FILE: postcss.config.mjs
================================================
/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    tailwindcss: {},
    'tailwindcss/nesting': {},
  },
};

export default config;



================================================
FILE: tailwind.config.ts
================================================
import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: ['class'],
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './node_modules/streamdown/dist/index.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-geist)'],
        mono: ['var(--font-geist-mono)'],
      },
      screens: {
        'toast-mobile': '600px',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        chart: {
          '1': 'hsl(var(--chart-1))',
          '2': 'hsl(var(--chart-2))',
          '3': 'hsl(var(--chart-3))',
          '4': 'hsl(var(--chart-4))',
          '5': 'hsl(var(--chart-5))',
        },
        sidebar: {
          DEFAULT: 'hsl(var(--sidebar-background))',
          foreground: 'hsl(var(--sidebar-foreground))',
          primary: 'hsl(var(--sidebar-primary))',
          'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
          accent: 'hsl(var(--sidebar-accent))',
          'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
          border: 'hsl(var(--sidebar-border))',
          ring: 'hsl(var(--sidebar-ring))',
        },
      },
    },
  },
  plugins: [require('tailwindcss-animate'), require('@tailwindcss/typography')],
};
export default config;



================================================
FILE: tsconfig.json
================================================
{
  "compilerOptions": {
    "target": "ESNext",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": [
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    ".next/types/**/*.ts",
    "next.config.js"
  ],
  "exclude": ["node_modules"]
}



================================================
FILE: .env.example
================================================
# Generate a random secret: https://generate-secret.vercel.app/32 or `openssl rand -base64 32`
AUTH_SECRET=****

# The following keys below are automatically created and
# added to your environment when you deploy on vercel

# AI Gateway API Key (required for non-Vercel deployments)
# For Vercel deployments, OIDC tokens are used automatically
AI_GATEWAY_API_KEY=****


# Instructions to create a Vercel Blob Store here: https://vercel.com/docs/storage/vercel-blob
BLOB_READ_WRITE_TOKEN=****

# Instructions to create a PostgreSQL database here: https://vercel.com/docs/storage/vercel-postgres/quickstart
POSTGRES_URL=****


# Instructions to create a Redis store here:
# https://vercel.com/docs/redis
REDIS_URL=****



================================================
FILE: .eslintrc.json
================================================
{
  "extends": [
    "next/core-web-vitals",
    "plugin:import/recommended",
    "plugin:import/typescript",
    "prettier",
    "plugin:tailwindcss/recommended"
  ],
  "plugins": ["tailwindcss"],
  "rules": {
    "tailwindcss/no-custom-classname": "off",
    "tailwindcss/classnames-order": "off"
  },
  "settings": {
    "import/resolver": {
      "typescript": {
        "alwaysTryTypes": true,
        "project": "./tsconfig.json"
      }
    }
  },
  "ignorePatterns": ["**/components/ui/**"]
}



================================================
FILE: app/globals.css
================================================
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
    --foreground-rgb: 0, 0, 0;
    --background-start-rgb: 214, 219, 220;
    --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
    :root {
        --foreground-rgb: 255, 255, 255;
        --background-start-rgb: 0, 0, 0;
        --background-end-rgb: 0, 0, 0;
    }
}

@layer utilities {
    .text-balance {
        text-wrap: balance;
    }
}

@layer base {
    :root {
        --background: 0 0% 100%;
        --foreground: 240 10% 3.9%;
        --card: 0 0% 100%;
        --card-foreground: 240 10% 3.9%;
        --popover: 0 0% 100%;
        --popover-foreground: 240 10% 3.9%;
        --primary: 240 5.9% 10%;
        --primary-foreground: 0 0% 98%;
        --secondary: 240 4.8% 95.9%;
        --secondary-foreground: 240 5.9% 10%;
        --muted: 240 4.8% 95.9%;
        --muted-foreground: 240 3.8% 46.1%;
        --accent: 240 4.8% 95.9%;
        --accent-foreground: 240 5.9% 10%;
        --destructive: 0 84.2% 60.2%;
        --destructive-foreground: 0 0% 98%;
        --border: 240 5.9% 90%;
        --input: 240 5.9% 90%;
        --ring: 240 10% 3.9%;
        --chart-1: 12 76% 61%;
        --chart-2: 173 58% 39%;
        --chart-3: 197 37% 24%;
        --chart-4: 43 74% 66%;
        --chart-5: 27 87% 67%;
        --radius: 0.5rem;
        --sidebar-background: 0 0% 98%;
        --sidebar-foreground: 240 5.3% 26.1%;
        --sidebar-primary: 240 5.9% 10%;
        --sidebar-primary-foreground: 0 0% 98%;
        --sidebar-accent: 240 4.8% 95.9%;
        --sidebar-accent-foreground: 240 5.9% 10%;
        --sidebar-border: 220 13% 91%;
        --sidebar-ring: 217.2 91.2% 59.8%;
    }
    .dark {
        --background: 240 10% 3.9%;
        --foreground: 0 0% 98%;
        --card: 240 10% 3.9%;
        --card-foreground: 0 0% 98%;
        --popover: 240 10% 3.9%;
        --popover-foreground: 0 0% 98%;
        --primary: 0 0% 98%;
        --primary-foreground: 240 5.9% 10%;
        --secondary: 240 3.7% 15.9%;
        --secondary-foreground: 0 0% 98%;
        --muted: 240 3.7% 15.9%;
        --muted-foreground: 240 5% 64.9%;
        --accent: 240 3.7% 15.9%;
        --accent-foreground: 0 0% 98%;
        --destructive: 0 62.8% 30.6%;
        --destructive-foreground: 0 0% 98%;
        --border: 240 3.7% 15.9%;
        --input: 240 3.7% 15.9%;
        --ring: 240 4.9% 83.9%;
        --chart-1: 220 70% 50%;
        --chart-2: 160 60% 45%;
        --chart-3: 30 80% 55%;
        --chart-4: 280 65% 60%;
        --chart-5: 340 75% 55%;
        --sidebar-background: 240 5.9% 10%;
        --sidebar-foreground: 240 4.8% 95.9%;
        --sidebar-primary: 224.3 76.3% 48%;
        --sidebar-primary-foreground: 0 0% 100%;
        --sidebar-accent: 240 3.7% 15.9%;
        --sidebar-accent-foreground: 240 4.8% 95.9%;
        --sidebar-border: 240 3.7% 15.9%;
        --sidebar-ring: 217.2 91.2% 59.8%;
    }
}

@layer base {
    * {
        @apply border-border;
    }

    body {
        @apply bg-background text-foreground;
    }
}

.skeleton {
    * {
        pointer-events: none !important;
    }

    *[class^="text-"] {
        color: transparent;
        @apply rounded-md bg-foreground/20 select-none animate-pulse;
    }

    .skeleton-bg {
        @apply bg-foreground/10;
    }

    .skeleton-div {
        @apply bg-foreground/20 animate-pulse;
    }
}

.ProseMirror {
    outline: none;
}

.cm-editor,
.cm-gutters {
    @apply bg-background dark:bg-zinc-800 outline-none selection:bg-zinc-900 !important;
}

.ͼo.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground,
.ͼo.cm-selectionBackground,
.ͼo.cm-content::selection {
    @apply bg-zinc-200 dark:bg-zinc-900 !important;
}

.cm-activeLine,
.cm-activeLineGutter {
    @apply bg-transparent !important;
}

.cm-activeLine {
    @apply rounded-r-sm !important;
}

.cm-lineNumbers {
    @apply min-w-7;
}

.cm-foldGutter {
    @apply min-w-3;
}

.cm-lineNumbers .cm-activeLineGutter {
    @apply rounded-l-sm !important;
}

.suggestion-highlight {
    @apply bg-blue-200 hover:bg-blue-300 dark:hover:bg-blue-400/50 dark:text-blue-50 dark:bg-blue-500/40;
}



================================================
FILE: app/layout.tsx
================================================
import { Toaster } from 'sonner';
import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import { ThemeProvider } from '@/components/theme-provider';

import './globals.css';
import { SessionProvider } from 'next-auth/react';

export const metadata: Metadata = {
  metadataBase: new URL('https://chat.vercel.ai'),
  title: 'Next.js Chatbot Template',
  description: 'Next.js chatbot template using the AI SDK.',
};

export const viewport = {
  maximumScale: 1, // Disable auto-zoom on mobile Safari
};

const geist = Geist({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-geist',
});

const geistMono = Geist_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-geist-mono',
});

const LIGHT_THEME_COLOR = 'hsl(0 0% 100%)';
const DARK_THEME_COLOR = 'hsl(240deg 10% 3.92%)';
const THEME_COLOR_SCRIPT = `\
(function() {
  var html = document.documentElement;
  var meta = document.querySelector('meta[name="theme-color"]');
  if (!meta) {
    meta = document.createElement('meta');
    meta.setAttribute('name', 'theme-color');
    document.head.appendChild(meta);
  }
  function updateThemeColor() {
    var isDark = html.classList.contains('dark');
    meta.setAttribute('content', isDark ? '${DARK_THEME_COLOR}' : '${LIGHT_THEME_COLOR}');
  }
  var observer = new MutationObserver(updateThemeColor);
  observer.observe(html, { attributes: true, attributeFilter: ['class'] });
  updateThemeColor();
})();`;

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      // `next-themes` injects an extra classname to the body element to avoid
      // visual flicker before hydration. Hence the `suppressHydrationWarning`
      // prop is necessary to avoid the React hydration mismatch warning.
      // https://github.com/pacocoursey/next-themes?tab=readme-ov-file#with-app
      suppressHydrationWarning
      className={`${geist.variable} ${geistMono.variable}`}
    >
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: THEME_COLOR_SCRIPT,
          }}
        />
      </head>
      <body className="antialiased">
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <Toaster position="top-center" />
          <SessionProvider>{children}</SessionProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}



================================================
FILE: app/(auth)/actions.ts
================================================
'use server';

import { z } from 'zod';

import { createUser, getUser } from '@/lib/db/queries';

import { signIn } from './auth';

const authFormSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
});

export interface LoginActionState {
  status: 'idle' | 'in_progress' | 'success' | 'failed' | 'invalid_data';
}

export const login = async (
  _: LoginActionState,
  formData: FormData,
): Promise<LoginActionState> => {
  try {
    const validatedData = authFormSchema.parse({
      email: formData.get('email'),
      password: formData.get('password'),
    });

    await signIn('credentials', {
      email: validatedData.email,
      password: validatedData.password,
      redirect: false,
    });

    return { status: 'success' };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { status: 'invalid_data' };
    }

    return { status: 'failed' };
  }
};

export interface RegisterActionState {
  status:
    | 'idle'
    | 'in_progress'
    | 'success'
    | 'failed'
    | 'user_exists'
    | 'invalid_data';
}

export const register = async (
  _: RegisterActionState,
  formData: FormData,
): Promise<RegisterActionState> => {
  try {
    const validatedData = authFormSchema.parse({
      email: formData.get('email'),
      password: formData.get('password'),
    });

    const [user] = await getUser(validatedData.email);

    if (user) {
      return { status: 'user_exists' } as RegisterActionState;
    }
    await createUser(validatedData.email, validatedData.password);
    await signIn('credentials', {
      email: validatedData.email,
      password: validatedData.password,
      redirect: false,
    });

    return { status: 'success' };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { status: 'invalid_data' };
    }

    return { status: 'failed' };
  }
};



================================================
FILE: app/(auth)/auth.config.ts
================================================
import type { NextAuthConfig } from 'next-auth';

export const authConfig = {
  pages: {
    signIn: '/login',
    newUser: '/',
  },
  providers: [
    // added later in auth.ts since it requires bcrypt which is only compatible with Node.js
    // while this file is also used in non-Node.js environments
  ],
  callbacks: {},
} satisfies NextAuthConfig;



================================================
FILE: app/(auth)/auth.ts
================================================
import { compare } from 'bcrypt-ts';
import NextAuth, { type DefaultSession } from 'next-auth';
import Credentials from 'next-auth/providers/credentials';
import { createGuestUser, getUser } from '@/lib/db/queries';
import { authConfig } from './auth.config';
import { DUMMY_PASSWORD } from '@/lib/constants';
import type { DefaultJWT } from 'next-auth/jwt';

export type UserType = 'guest' | 'regular';

declare module 'next-auth' {
  interface Session extends DefaultSession {
    user: {
      id: string;
      type: UserType;
    } & DefaultSession['user'];
  }

  interface User {
    id?: string;
    email?: string | null;
    type: UserType;
  }
}

declare module 'next-auth/jwt' {
  interface JWT extends DefaultJWT {
    id: string;
    type: UserType;
  }
}

export const {
  handlers: { GET, POST },
  auth,
  signIn,
  signOut,
} = NextAuth({
  ...authConfig,
  providers: [
    Credentials({
      credentials: {},
      async authorize({ email, password }: any) {
        const users = await getUser(email);

        if (users.length === 0) {
          await compare(password, DUMMY_PASSWORD);
          return null;
        }

        const [user] = users;

        if (!user.password) {
          await compare(password, DUMMY_PASSWORD);
          return null;
        }

        const passwordsMatch = await compare(password, user.password);

        if (!passwordsMatch) return null;

        return { ...user, type: 'regular' };
      },
    }),
    Credentials({
      id: 'guest',
      credentials: {},
      async authorize() {
        const [guestUser] = await createGuestUser();
        return { ...guestUser, type: 'guest' };
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id as string;
        token.type = user.type;
      }

      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id;
        session.user.type = token.type;
      }

      return session;
    },
  },
});



================================================
FILE: app/(auth)/api/auth/[...nextauth]/route.ts
================================================
export { GET, POST } from '@/app/(auth)/auth';



================================================
FILE: app/(auth)/api/auth/guest/route.ts
================================================
import { signIn } from '@/app/(auth)/auth';
import { isDevelopmentEnvironment } from '@/lib/constants';
import { getToken } from 'next-auth/jwt';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const redirectUrl = searchParams.get('redirectUrl') || '/';

  const token = await getToken({
    req: request,
    secret: process.env.AUTH_SECRET,
    secureCookie: !isDevelopmentEnvironment,
  });

  if (token) {
    return NextResponse.redirect(new URL('/', request.url));
  }

  return signIn('guest', { redirect: true, redirectTo: redirectUrl });
}



================================================
FILE: app/(auth)/login/page.tsx
================================================
'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useActionState, useEffect, useState } from 'react';
import { toast } from '@/components/toast';

import { AuthForm } from '@/components/auth-form';
import { SubmitButton } from '@/components/submit-button';

import { login, type LoginActionState } from '../actions';
import { useSession } from 'next-auth/react';

export default function Page() {
  const router = useRouter();

  const [email, setEmail] = useState('');
  const [isSuccessful, setIsSuccessful] = useState(false);

  const [state, formAction] = useActionState<LoginActionState, FormData>(
    login,
    {
      status: 'idle',
    },
  );

  const { update: updateSession } = useSession();

  useEffect(() => {
    if (state.status === 'failed') {
      toast({
        type: 'error',
        description: 'Invalid credentials!',
      });
    } else if (state.status === 'invalid_data') {
      toast({
        type: 'error',
        description: 'Failed validating your submission!',
      });
    } else if (state.status === 'success') {
      setIsSuccessful(true);
      updateSession();
      router.refresh();
    }
  }, [state.status]);

  const handleSubmit = (formData: FormData) => {
    setEmail(formData.get('email') as string);
    formAction(formData);
  };

  return (
    <div className="flex h-dvh w-screen items-start pt-12 md:pt-0 md:items-center justify-center bg-background">
      <div className="w-full max-w-md overflow-hidden rounded-2xl flex flex-col gap-12">
        <div className="flex flex-col items-center justify-center gap-2 px-4 text-center sm:px-16">
          <h3 className="text-xl font-semibold dark:text-zinc-50">Sign In</h3>
          <p className="text-sm text-gray-500 dark:text-zinc-400">
            Use your email and password to sign in
          </p>
        </div>
        <AuthForm action={handleSubmit} defaultEmail={email}>
          <SubmitButton isSuccessful={isSuccessful}>Sign in</SubmitButton>
          <p className="text-center text-sm text-gray-600 mt-4 dark:text-zinc-400">
            {"Don't have an account? "}
            <Link
              href="/register"
              className="font-semibold text-gray-800 hover:underline dark:text-zinc-200"
            >
              Sign up
            </Link>
            {' for free.'}
          </p>
        </AuthForm>
      </div>
    </div>
  );
}



================================================
FILE: app/(auth)/register/page.tsx
================================================
'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useActionState, useEffect, useState } from 'react';

import { AuthForm } from '@/components/auth-form';
import { SubmitButton } from '@/components/submit-button';

import { register, type RegisterActionState } from '../actions';
import { toast } from '@/components/toast';
import { useSession } from 'next-auth/react';

export default function Page() {
  const router = useRouter();

  const [email, setEmail] = useState('');
  const [isSuccessful, setIsSuccessful] = useState(false);

  const [state, formAction] = useActionState<RegisterActionState, FormData>(
    register,
    {
      status: 'idle',
    },
  );

  const { update: updateSession } = useSession();

  useEffect(() => {
    if (state.status === 'user_exists') {
      toast({ type: 'error', description: 'Account already exists!' });
    } else if (state.status === 'failed') {
      toast({ type: 'error', description: 'Failed to create account!' });
    } else if (state.status === 'invalid_data') {
      toast({
        type: 'error',
        description: 'Failed validating your submission!',
      });
    } else if (state.status === 'success') {
      toast({ type: 'success', description: 'Account created successfully!' });

      setIsSuccessful(true);
      updateSession();
      router.refresh();
    }
  }, [state]);

  const handleSubmit = (formData: FormData) => {
    setEmail(formData.get('email') as string);
    formAction(formData);
  };

  return (
    <div className="flex h-dvh w-screen items-start pt-12 md:pt-0 md:items-center justify-center bg-background">
      <div className="w-full max-w-md overflow-hidden rounded-2xl gap-12 flex flex-col">
        <div className="flex flex-col items-center justify-center gap-2 px-4 text-center sm:px-16">
          <h3 className="text-xl font-semibold dark:text-zinc-50">Sign Up</h3>
          <p className="text-sm text-gray-500 dark:text-zinc-400">
            Create an account with your email and password
          </p>
        </div>
        <AuthForm action={handleSubmit} defaultEmail={email}>
          <SubmitButton isSuccessful={isSuccessful}>Sign Up</SubmitButton>
          <p className="text-center text-sm text-gray-600 mt-4 dark:text-zinc-400">
            {'Already have an account? '}
            <Link
              href="/login"
              className="font-semibold text-gray-800 hover:underline dark:text-zinc-200"
            >
              Sign in
            </Link>
            {' instead.'}
          </p>
        </AuthForm>
      </div>
    </div>
  );
}



================================================
FILE: app/(chat)/actions.ts
================================================
'use server';

import { generateText, type UIMessage } from 'ai';
import { cookies } from 'next/headers';
import {
  deleteMessagesByChatIdAfterTimestamp,
  getMessageById,
  updateChatVisiblityById,
} from '@/lib/db/queries';
import type { VisibilityType } from '@/components/visibility-selector';
import { myProvider } from '@/lib/ai/providers';

export async function saveChatModelAsCookie(model: string) {
  const cookieStore = await cookies();
  cookieStore.set('chat-model', model);
}

export async function generateTitleFromUserMessage({
  message,
}: {
  message: UIMessage;
}) {
  const { text: title } = await generateText({
    model: myProvider.languageModel('title-model'),
    system: `\n
    - you will generate a short title based on the first message a user begins a conversation with
    - ensure it is not more than 80 characters long
    - the title should be a summary of the user's message
    - do not use quotes or colons`,
    prompt: JSON.stringify(message),
  });

  return title;
}

export async function deleteTrailingMessages({ id }: { id: string }) {
  const [message] = await getMessageById({ id });

  await deleteMessagesByChatIdAfterTimestamp({
    chatId: message.chatId,
    timestamp: message.createdAt,
  });
}

export async function updateChatVisibility({
  chatId,
  visibility,
}: {
  chatId: string;
  visibility: VisibilityType;
}) {
  await updateChatVisiblityById({ chatId, visibility });
}



================================================
FILE: app/(chat)/layout.tsx
================================================
import { cookies } from 'next/headers';

import { AppSidebar } from '@/components/app-sidebar';
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';
import { auth } from '../(auth)/auth';
import Script from 'next/script';
import { DataStreamProvider } from '@/components/data-stream-provider';

export const experimental_ppr = true;

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [session, cookieStore] = await Promise.all([auth(), cookies()]);
  const isCollapsed = cookieStore.get('sidebar:state')?.value !== 'true';

  return (
    <>
      <Script
        src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"
        strategy="beforeInteractive"
      />
      <DataStreamProvider>
        <SidebarProvider defaultOpen={!isCollapsed}>
          <AppSidebar user={session?.user} />
          <SidebarInset>{children}</SidebarInset>
        </SidebarProvider>
      </DataStreamProvider>
    </>
  );
}



================================================
FILE: app/(chat)/page.tsx
================================================
import { cookies } from 'next/headers';

import { Chat } from '@/components/chat';
import { DEFAULT_CHAT_MODEL } from '@/lib/ai/models';
import { generateUUID } from '@/lib/utils';
import { DataStreamHandler } from '@/components/data-stream-handler';
import { auth } from '../(auth)/auth';
import { redirect } from 'next/navigation';

export default async function Page() {
  const session = await auth();

  if (!session) {
    redirect('/api/auth/guest');
  }

  const id = generateUUID();

  const cookieStore = await cookies();
  const modelIdFromCookie = cookieStore.get('chat-model');

  if (!modelIdFromCookie) {
    return (
      <>
        <Chat
          key={id}
          id={id}
          initialMessages={[]}
          initialChatModel={DEFAULT_CHAT_MODEL}
          initialVisibilityType="private"
          isReadonly={false}
          session={session}
          autoResume={false}
        />
        <DataStreamHandler />
      </>
    );
  }

  return (
    <>
      <Chat
        key={id}
        id={id}
        initialMessages={[]}
        initialChatModel={modelIdFromCookie.value}
        initialVisibilityType="private"
        isReadonly={false}
        session={session}
        autoResume={false}
      />
      <DataStreamHandler />
    </>
  );
}



================================================
FILE: app/(chat)/api/chat/route.ts
================================================
import {
  convertToModelMessages,
  createUIMessageStream,
  JsonToSseTransformStream,
  smoothStream,
  stepCountIs,
  streamText,
} from 'ai';
import { auth, type UserType } from '@/app/(auth)/auth';
import { type RequestHints, systemPrompt } from '@/lib/ai/prompts';
import {
  createStreamId,
  deleteChatById,
  getChatById,
  getMessageCountByUserId,
  getMessagesByChatId,
  saveChat,
  saveMessages,
} from '@/lib/db/queries';
import { convertToUIMessages, generateUUID } from '@/lib/utils';
import { generateTitleFromUserMessage } from '../../actions';
import { createDocument } from '@/lib/ai/tools/create-document';
import { updateDocument } from '@/lib/ai/tools/update-document';
import { requestSuggestions } from '@/lib/ai/tools/request-suggestions';
import { getWeather } from '@/lib/ai/tools/get-weather';
import { isProductionEnvironment } from '@/lib/constants';
import { myProvider } from '@/lib/ai/providers';
import { entitlementsByUserType } from '@/lib/ai/entitlements';
import { postRequestBodySchema, type PostRequestBody } from './schema';
import { geolocation } from '@vercel/functions';
import {
  createResumableStreamContext,
  type ResumableStreamContext,
} from 'resumable-stream';
import { after } from 'next/server';
import { ChatSDKError } from '@/lib/errors';
import type { ChatMessage } from '@/lib/types';
import type { ChatModel } from '@/lib/ai/models';
import type { VisibilityType } from '@/components/visibility-selector';

export const maxDuration = 60;

let globalStreamContext: ResumableStreamContext | null = null;

export function getStreamContext() {
  if (!globalStreamContext) {
    try {
      globalStreamContext = createResumableStreamContext({
        waitUntil: after,
      });
    } catch (error: any) {
      if (error.message.includes('REDIS_URL')) {
        console.log(
          ' > Resumable streams are disabled due to missing REDIS_URL',
        );
      } else {
        console.error(error);
      }
    }
  }

  return globalStreamContext;
}

export async function POST(request: Request) {
  let requestBody: PostRequestBody;

  try {
    const json = await request.json();
    requestBody = postRequestBodySchema.parse(json);
  } catch (_) {
    return new ChatSDKError('bad_request:api').toResponse();
  }

  try {
    const {
      id,
      message,
      selectedChatModel,
      selectedVisibilityType,
    }: {
      id: string;
      message: ChatMessage;
      selectedChatModel: ChatModel['id'];
      selectedVisibilityType: VisibilityType;
    } = requestBody;

    const session = await auth();

    if (!session?.user) {
      return new ChatSDKError('unauthorized:chat').toResponse();
    }

    const userType: UserType = session.user.type;

    const messageCount = await getMessageCountByUserId({
      id: session.user.id,
      differenceInHours: 24,
    });

    if (messageCount > entitlementsByUserType[userType].maxMessagesPerDay) {
      return new ChatSDKError('rate_limit:chat').toResponse();
    }

    const chat = await getChatById({ id });

    if (!chat) {
      const title = await generateTitleFromUserMessage({
        message,
      });

      await saveChat({
        id,
        userId: session.user.id,
        title,
        visibility: selectedVisibilityType,
      });
    } else {
      if (chat.userId !== session.user.id) {
        return new ChatSDKError('forbidden:chat').toResponse();
      }
    }

    const messagesFromDb = await getMessagesByChatId({ id });
    const uiMessages = [...convertToUIMessages(messagesFromDb), message];

    const { longitude, latitude, city, country } = geolocation(request);

    const requestHints: RequestHints = {
      longitude,
      latitude,
      city,
      country,
    };

    await saveMessages({
      messages: [
        {
          chatId: id,
          id: message.id,
          role: 'user',
          parts: message.parts,
          attachments: [],
          createdAt: new Date(),
        },
      ],
    });

    const streamId = generateUUID();
    await createStreamId({ streamId, chatId: id });

    const stream = createUIMessageStream({
      execute: ({ writer: dataStream }) => {
        const result = streamText({
          model: myProvider.languageModel(selectedChatModel),
          system: systemPrompt({ selectedChatModel, requestHints }),
          messages: convertToModelMessages(uiMessages),
          stopWhen: stepCountIs(5),
          experimental_activeTools:
            selectedChatModel === 'chat-model-reasoning'
              ? []
              : [
                  'getWeather',
                  'createDocument',
                  'updateDocument',
                  'requestSuggestions',
                ],
          experimental_transform: smoothStream({ chunking: 'word' }),
          tools: {
            getWeather,
            createDocument: createDocument({ session, dataStream }),
            updateDocument: updateDocument({ session, dataStream }),
            requestSuggestions: requestSuggestions({
              session,
              dataStream,
            }),
          },
          experimental_telemetry: {
            isEnabled: isProductionEnvironment,
            functionId: 'stream-text',
          },
        });

        result.consumeStream();

        dataStream.merge(
          result.toUIMessageStream({
            sendReasoning: true,
          }),
        );
      },
      generateId: generateUUID,
      onFinish: async ({ messages }) => {
        await saveMessages({
          messages: messages.map((message) => ({
            id: message.id,
            role: message.role,
            parts: message.parts,
            createdAt: new Date(),
            attachments: [],
            chatId: id,
          })),
        });
      },
      onError: () => {
        return 'Oops, an error occurred!';
      },
    });

    const streamContext = getStreamContext();

    if (streamContext) {
      return new Response(
        await streamContext.resumableStream(streamId, () =>
          stream.pipeThrough(new JsonToSseTransformStream()),
        ),
      );
    } else {
      return new Response(stream.pipeThrough(new JsonToSseTransformStream()));
    }
  } catch (error) {
    if (error instanceof ChatSDKError) {
      return error.toResponse();
    }

    console.error('Unhandled error in chat API:', error);
    return new ChatSDKError('offline:chat').toResponse();
  }
}

export async function DELETE(request: Request) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new ChatSDKError('bad_request:api').toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatSDKError('unauthorized:chat').toResponse();
  }

  const chat = await getChatById({ id });

  if (chat.userId !== session.user.id) {
    return new ChatSDKError('forbidden:chat').toResponse();
  }

  const deletedChat = await deleteChatById({ id });

  return Response.json(deletedChat, { status: 200 });
}



================================================
FILE: app/(chat)/api/chat/schema.ts
================================================
import { z } from 'zod';

const textPartSchema = z.object({
  type: z.enum(['text']),
  text: z.string().min(1).max(2000),
});

const filePartSchema = z.object({
  type: z.enum(['file']),
  mediaType: z.enum(['image/jpeg', 'image/png']),
  name: z.string().min(1).max(100),
  url: z.string().url(),
});

const partSchema = z.union([textPartSchema, filePartSchema]);

export const postRequestBodySchema = z.object({
  id: z.string().uuid(),
  message: z.object({
    id: z.string().uuid(),
    role: z.enum(['user']),
    parts: z.array(partSchema),
  }),
  selectedChatModel: z.enum(['chat-model', 'chat-model-reasoning']),
  selectedVisibilityType: z.enum(['public', 'private']),
});

export type PostRequestBody = z.infer<typeof postRequestBodySchema>;



================================================
FILE: app/(chat)/api/chat/[id]/stream/route.ts
================================================
import { auth } from '@/app/(auth)/auth';
import {
  getChatById,
  getMessagesByChatId,
  getStreamIdsByChatId,
} from '@/lib/db/queries';
import type { Chat } from '@/lib/db/schema';
import { ChatSDKError } from '@/lib/errors';
import type { ChatMessage } from '@/lib/types';
import { createUIMessageStream, JsonToSseTransformStream } from 'ai';
import { getStreamContext } from '../../route';
import { differenceInSeconds } from 'date-fns';

export async function GET(
  _: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id: chatId } = await params;

  const streamContext = getStreamContext();
  const resumeRequestedAt = new Date();

  if (!streamContext) {
    return new Response(null, { status: 204 });
  }

  if (!chatId) {
    return new ChatSDKError('bad_request:api').toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatSDKError('unauthorized:chat').toResponse();
  }

  let chat: Chat;

  try {
    chat = await getChatById({ id: chatId });
  } catch {
    return new ChatSDKError('not_found:chat').toResponse();
  }

  if (!chat) {
    return new ChatSDKError('not_found:chat').toResponse();
  }

  if (chat.visibility === 'private' && chat.userId !== session.user.id) {
    return new ChatSDKError('forbidden:chat').toResponse();
  }

  const streamIds = await getStreamIdsByChatId({ chatId });

  if (!streamIds.length) {
    return new ChatSDKError('not_found:stream').toResponse();
  }

  const recentStreamId = streamIds.at(-1);

  if (!recentStreamId) {
    return new ChatSDKError('not_found:stream').toResponse();
  }

  const emptyDataStream = createUIMessageStream<ChatMessage>({
    execute: () => {},
  });

  const stream = await streamContext.resumableStream(recentStreamId, () =>
    emptyDataStream.pipeThrough(new JsonToSseTransformStream()),
  );

  /*
   * For when the generation is streaming during SSR
   * but the resumable stream has concluded at this point.
   */
  if (!stream) {
    const messages = await getMessagesByChatId({ id: chatId });
    const mostRecentMessage = messages.at(-1);

    if (!mostRecentMessage) {
      return new Response(emptyDataStream, { status: 200 });
    }

    if (mostRecentMessage.role !== 'assistant') {
      return new Response(emptyDataStream, { status: 200 });
    }

    const messageCreatedAt = new Date(mostRecentMessage.createdAt);

    if (differenceInSeconds(resumeRequestedAt, messageCreatedAt) > 15) {
      return new Response(emptyDataStream, { status: 200 });
    }

    const restoredStream = createUIMessageStream<ChatMessage>({
      execute: ({ writer }) => {
        writer.write({
          type: 'data-appendMessage',
          data: JSON.stringify(mostRecentMessage),
          transient: true,
        });
      },
    });

    return new Response(
      restoredStream.pipeThrough(new JsonToSseTransformStream()),
      { status: 200 },
    );
  }

  return new Response(stream, { status: 200 });
}



================================================
FILE: app/(chat)/api/document/route.ts
================================================
import { auth } from '@/app/(auth)/auth';
import type { ArtifactKind } from '@/components/artifact';
import {
  deleteDocumentsByIdAfterTimestamp,
  getDocumentsById,
  saveDocument,
} from '@/lib/db/queries';
import { ChatSDKError } from '@/lib/errors';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new ChatSDKError(
      'bad_request:api',
      'Parameter id is missing',
    ).toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatSDKError('unauthorized:document').toResponse();
  }

  const documents = await getDocumentsById({ id });

  const [document] = documents;

  if (!document) {
    return new ChatSDKError('not_found:document').toResponse();
  }

  if (document.userId !== session.user.id) {
    return new ChatSDKError('forbidden:document').toResponse();
  }

  return Response.json(documents, { status: 200 });
}

export async function POST(request: Request) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new ChatSDKError(
      'bad_request:api',
      'Parameter id is required.',
    ).toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatSDKError('not_found:document').toResponse();
  }

  const {
    content,
    title,
    kind,
  }: { content: string; title: string; kind: ArtifactKind } =
    await request.json();

  const documents = await getDocumentsById({ id });

  if (documents.length > 0) {
    const [document] = documents;

    if (document.userId !== session.user.id) {
      return new ChatSDKError('forbidden:document').toResponse();
    }
  }

  const document = await saveDocument({
    id,
    content,
    title,
    kind,
    userId: session.user.id,
  });

  return Response.json(document, { status: 200 });
}

export async function DELETE(request: Request) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');
  const timestamp = searchParams.get('timestamp');

  if (!id) {
    return new ChatSDKError(
      'bad_request:api',
      'Parameter id is required.',
    ).toResponse();
  }

  if (!timestamp) {
    return new ChatSDKError(
      'bad_request:api',
      'Parameter timestamp is required.',
    ).toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatSDKError('unauthorized:document').toResponse();
  }

  const documents = await getDocumentsById({ id });

  const [document] = documents;

  if (document.userId !== session.user.id) {
    return new ChatSDKError('forbidden:document').toResponse();
  }

  const documentsDeleted = await deleteDocumentsByIdAfterTimestamp({
    id,
    timestamp: new Date(timestamp),
  });

  return Response.json(documentsDeleted, { status: 200 });
}



================================================
FILE: app/(chat)/api/files/upload/route.ts
================================================
import { put } from '@vercel/blob';
import { NextResponse } from 'next/server';
import { z } from 'zod';

import { auth } from '@/app/(auth)/auth';

// Use Blob instead of File since File is not available in Node.js environment
const FileSchema = z.object({
  file: z
    .instanceof(Blob)
    .refine((file) => file.size <= 5 * 1024 * 1024, {
      message: 'File size should be less than 5MB',
    })
    // Update the file type based on the kind of files you want to accept
    .refine((file) => ['image/jpeg', 'image/png'].includes(file.type), {
      message: 'File type should be JPEG or PNG',
    }),
});

export async function POST(request: Request) {
  const session = await auth();

  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (request.body === null) {
    return new Response('Request body is empty', { status: 400 });
  }

  try {
    const formData = await request.formData();
    const file = formData.get('file') as Blob;

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
    }

    const validatedFile = FileSchema.safeParse({ file });

    if (!validatedFile.success) {
      const errorMessage = validatedFile.error.errors
        .map((error) => error.message)
        .join(', ');

      return NextResponse.json({ error: errorMessage }, { status: 400 });
    }

    // Get filename from formData since Blob doesn't have name property
    const filename = (formData.get('file') as File).name;
    const fileBuffer = await file.arrayBuffer();

    try {
      const data = await put(`${filename}`, fileBuffer, {
        access: 'public',
      });

      return NextResponse.json(data);
    } catch (error) {
      return NextResponse.json({ error: 'Upload failed' }, { status: 500 });
    }
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to process request' },
      { status: 500 },
    );
  }
}



================================================
FILE: app/(chat)/api/history/route.ts
================================================
import { auth } from '@/app/(auth)/auth';
import type { NextRequest } from 'next/server';
import { getChatsByUserId } from '@/lib/db/queries';
import { ChatSDKError } from '@/lib/errors';

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;

  const limit = Number.parseInt(searchParams.get('limit') || '10');
  const startingAfter = searchParams.get('starting_after');
  const endingBefore = searchParams.get('ending_before');

  if (startingAfter && endingBefore) {
    return new ChatSDKError(
      'bad_request:api',
      'Only one of starting_after or ending_before can be provided.',
    ).toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatSDKError('unauthorized:chat').toResponse();
  }

  const chats = await getChatsByUserId({
    id: session.user.id,
    limit,
    startingAfter,
    endingBefore,
  });

  return Response.json(chats);
}



================================================
FILE: app/(chat)/api/suggestions/route.ts
================================================
import { auth } from '@/app/(auth)/auth';
import { getSuggestionsByDocumentId } from '@/lib/db/queries';
import { ChatSDKError } from '@/lib/errors';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const documentId = searchParams.get('documentId');

  if (!documentId) {
    return new ChatSDKError(
      'bad_request:api',
      'Parameter documentId is required.',
    ).toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatSDKError('unauthorized:suggestions').toResponse();
  }

  const suggestions = await getSuggestionsByDocumentId({
    documentId,
  });

  const [suggestion] = suggestions;

  if (!suggestion) {
    return Response.json([], { status: 200 });
  }

  if (suggestion.userId !== session.user.id) {
    return new ChatSDKError('forbidden:api').toResponse();
  }

  return Response.json(suggestions, { status: 200 });
}



================================================
FILE: app/(chat)/api/vote/route.ts
================================================
import { auth } from '@/app/(auth)/auth';
import { getChatById, getVotesByChatId, voteMessage } from '@/lib/db/queries';
import { ChatSDKError } from '@/lib/errors';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const chatId = searchParams.get('chatId');

  if (!chatId) {
    return new ChatSDKError(
      'bad_request:api',
      'Parameter chatId is required.',
    ).toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatSDKError('unauthorized:vote').toResponse();
  }

  const chat = await getChatById({ id: chatId });

  if (!chat) {
    return new ChatSDKError('not_found:chat').toResponse();
  }

  if (chat.userId !== session.user.id) {
    return new ChatSDKError('forbidden:vote').toResponse();
  }

  const votes = await getVotesByChatId({ id: chatId });

  return Response.json(votes, { status: 200 });
}

export async function PATCH(request: Request) {
  const {
    chatId,
    messageId,
    type,
  }: { chatId: string; messageId: string; type: 'up' | 'down' } =
    await request.json();

  if (!chatId || !messageId || !type) {
    return new ChatSDKError(
      'bad_request:api',
      'Parameters chatId, messageId, and type are required.',
    ).toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatSDKError('unauthorized:vote').toResponse();
  }

  const chat = await getChatById({ id: chatId });

  if (!chat) {
    return new ChatSDKError('not_found:vote').toResponse();
  }

  if (chat.userId !== session.user.id) {
    return new ChatSDKError('forbidden:vote').toResponse();
  }

  await voteMessage({
    chatId,
    messageId,
    type: type,
  });

  return new Response('Message voted', { status: 200 });
}



================================================
FILE: app/(chat)/chat/[id]/page.tsx
================================================
import { cookies } from 'next/headers';
import { notFound, redirect } from 'next/navigation';

import { auth } from '@/app/(auth)/auth';
import { Chat } from '@/components/chat';
import { getChatById, getMessagesByChatId } from '@/lib/db/queries';
import { DataStreamHandler } from '@/components/data-stream-handler';
import { DEFAULT_CHAT_MODEL } from '@/lib/ai/models';
import { convertToUIMessages } from '@/lib/utils';

export default async function Page(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;
  const { id } = params;
  const chat = await getChatById({ id });

  if (!chat) {
    notFound();
  }

  const session = await auth();

  if (!session) {
    redirect('/api/auth/guest');
  }

  if (chat.visibility === 'private') {
    if (!session.user) {
      return notFound();
    }

    if (session.user.id !== chat.userId) {
      return notFound();
    }
  }

  const messagesFromDb = await getMessagesByChatId({
    id,
  });

  const uiMessages = convertToUIMessages(messagesFromDb);

  const cookieStore = await cookies();
  const chatModelFromCookie = cookieStore.get('chat-model');

  if (!chatModelFromCookie) {
    return (
      <>
        <Chat
          id={chat.id}
          initialMessages={uiMessages}
          initialChatModel={DEFAULT_CHAT_MODEL}
          initialVisibilityType={chat.visibility}
          isReadonly={session?.user?.id !== chat.userId}
          session={session}
          autoResume={true}
        />
        <DataStreamHandler />
      </>
    );
  }

  return (
    <>
      <Chat
        id={chat.id}
        initialMessages={uiMessages}
        initialChatModel={chatModelFromCookie.value}
        initialVisibilityType={chat.visibility}
        isReadonly={session?.user?.id !== chat.userId}
        session={session}
        autoResume={true}
      />
      <DataStreamHandler />
    </>
  );
}



================================================
FILE: artifacts/actions.ts
================================================
'use server';

import { getSuggestionsByDocumentId } from '@/lib/db/queries';

export async function getSuggestions({ documentId }: { documentId: string }) {
  const suggestions = await getSuggestionsByDocumentId({ documentId });
  return suggestions ?? [];
}



================================================
FILE: artifacts/code/client.tsx
================================================
import { Artifact } from '@/components/create-artifact';
import { CodeEditor } from '@/components/code-editor';
import {
  CopyIcon,
  LogsIcon,
  MessageIcon,
  PlayIcon,
  RedoIcon,
  UndoIcon,
} from '@/components/icons';
import { toast } from 'sonner';
import { generateUUID } from '@/lib/utils';
import {
  Console,
  type ConsoleOutput,
  type ConsoleOutputContent,
} from '@/components/console';

const OUTPUT_HANDLERS = {
  matplotlib: `
    import io
    import base64
    from matplotlib import pyplot as plt

    # Clear any existing plots
    plt.clf()
    plt.close('all')

    # Switch to agg backend
    plt.switch_backend('agg')

    def setup_matplotlib_output():
        def custom_show():
            if plt.gcf().get_size_inches().prod() * plt.gcf().dpi ** 2 > 25_000_000:
                print("Warning: Plot size too large, reducing quality")
                plt.gcf().set_dpi(100)

            png_buf = io.BytesIO()
            plt.savefig(png_buf, format='png')
            png_buf.seek(0)
            png_base64 = base64.b64encode(png_buf.read()).decode('utf-8')
            print(f'data:image/png;base64,{png_base64}')
            png_buf.close()

            plt.clf()
            plt.close('all')

        plt.show = custom_show
  `,
  basic: `
    # Basic output capture setup
  `,
};

function detectRequiredHandlers(code: string): string[] {
  const handlers: string[] = ['basic'];

  if (code.includes('matplotlib') || code.includes('plt.')) {
    handlers.push('matplotlib');
  }

  return handlers;
}

interface Metadata {
  outputs: Array<ConsoleOutput>;
}

export const codeArtifact = new Artifact<'code', Metadata>({
  kind: 'code',
  description:
    'Useful for code generation; Code execution is only available for python code.',
  initialize: async ({ setMetadata }) => {
    setMetadata({
      outputs: [],
    });
  },
  onStreamPart: ({ streamPart, setArtifact }) => {
    if (streamPart.type === 'data-codeDelta') {
      setArtifact((draftArtifact) => ({
        ...draftArtifact,
        content: streamPart.data,
        isVisible:
          draftArtifact.status === 'streaming' &&
          draftArtifact.content.length > 300 &&
          draftArtifact.content.length < 310
            ? true
            : draftArtifact.isVisible,
        status: 'streaming',
      }));
    }
  },
  content: ({ metadata, setMetadata, ...props }) => {
    return (
      <>
        <div className="px-1">
          <CodeEditor {...props} />
        </div>

        {metadata?.outputs && (
          <Console
            consoleOutputs={metadata.outputs}
            setConsoleOutputs={() => {
              setMetadata({
                ...metadata,
                outputs: [],
              });
            }}
          />
        )}
      </>
    );
  },
  actions: [
    {
      icon: <PlayIcon size={18} />,
      label: 'Run',
      description: 'Execute code',
      onClick: async ({ content, setMetadata }) => {
        const runId = generateUUID();
        const outputContent: Array<ConsoleOutputContent> = [];

        setMetadata((metadata) => ({
          ...metadata,
          outputs: [
            ...metadata.outputs,
            {
              id: runId,
              contents: [],
              status: 'in_progress',
            },
          ],
        }));

        try {
          // @ts-expect-error - loadPyodide is not defined
          const currentPyodideInstance = await globalThis.loadPyodide({
            indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/',
          });

          currentPyodideInstance.setStdout({
            batched: (output: string) => {
              outputContent.push({
                type: output.startsWith('data:image/png;base64')
                  ? 'image'
                  : 'text',
                value: output,
              });
            },
          });

          await currentPyodideInstance.loadPackagesFromImports(content, {
            messageCallback: (message: string) => {
              setMetadata((metadata) => ({
                ...metadata,
                outputs: [
                  ...metadata.outputs.filter((output) => output.id !== runId),
                  {
                    id: runId,
                    contents: [{ type: 'text', value: message }],
                    status: 'loading_packages',
                  },
                ],
              }));
            },
          });

          const requiredHandlers = detectRequiredHandlers(content);
          for (const handler of requiredHandlers) {
            if (OUTPUT_HANDLERS[handler as keyof typeof OUTPUT_HANDLERS]) {
              await currentPyodideInstance.runPythonAsync(
                OUTPUT_HANDLERS[handler as keyof typeof OUTPUT_HANDLERS],
              );

              if (handler === 'matplotlib') {
                await currentPyodideInstance.runPythonAsync(
                  'setup_matplotlib_output()',
                );
              }
            }
          }

          await currentPyodideInstance.runPythonAsync(content);

          setMetadata((metadata) => ({
            ...metadata,
            outputs: [
              ...metadata.outputs.filter((output) => output.id !== runId),
              {
                id: runId,
                contents: outputContent,
                status: 'completed',
              },
            ],
          }));
        } catch (error: any) {
          setMetadata((metadata) => ({
            ...metadata,
            outputs: [
              ...metadata.outputs.filter((output) => output.id !== runId),
              {
                id: runId,
                contents: [{ type: 'text', value: error.message }],
                status: 'failed',
              },
            ],
          }));
        }
      },
    },
    {
      icon: <UndoIcon size={18} />,
      description: 'View Previous version',
      onClick: ({ handleVersionChange }) => {
        handleVersionChange('prev');
      },
      isDisabled: ({ currentVersionIndex }) => {
        if (currentVersionIndex === 0) {
          return true;
        }

        return false;
      },
    },
    {
      icon: <RedoIcon size={18} />,
      description: 'View Next version',
      onClick: ({ handleVersionChange }) => {
        handleVersionChange('next');
      },
      isDisabled: ({ isCurrentVersion }) => {
        if (isCurrentVersion) {
          return true;
        }

        return false;
      },
    },
    {
      icon: <CopyIcon size={18} />,
      description: 'Copy code to clipboard',
      onClick: ({ content }) => {
        navigator.clipboard.writeText(content);
        toast.success('Copied to clipboard!');
      },
    },
  ],
  toolbar: [
    {
      icon: <MessageIcon />,
      description: 'Add comments',
      onClick: ({ sendMessage }) => {
        sendMessage({
          role: 'user',
          parts: [
            {
              type: 'text',
              text: 'Add comments to the code snippet for understanding',
            },
          ],
        });
      },
    },
    {
      icon: <LogsIcon />,
      description: 'Add logs',
      onClick: ({ sendMessage }) => {
        sendMessage({
          role: 'user',
          parts: [
            {
              type: 'text',
              text: 'Add logs to the code snippet for debugging',
            },
          ],
        });
      },
    },
  ],
});



================================================
FILE: artifacts/code/server.ts
================================================
import { z } from 'zod';
import { streamObject } from 'ai';
import { myProvider } from '@/lib/ai/providers';
import { codePrompt, updateDocumentPrompt } from '@/lib/ai/prompts';
import { createDocumentHandler } from '@/lib/artifacts/server';

export const codeDocumentHandler = createDocumentHandler<'code'>({
  kind: 'code',
  onCreateDocument: async ({ title, dataStream }) => {
    let draftContent = '';

    const { fullStream } = streamObject({
      model: myProvider.languageModel('artifact-model'),
      system: codePrompt,
      prompt: title,
      schema: z.object({
        code: z.string(),
      }),
    });

    for await (const delta of fullStream) {
      const { type } = delta;

      if (type === 'object') {
        const { object } = delta;
        const { code } = object;

        if (code) {
          dataStream.write({
            type: 'data-codeDelta',
            data: code ?? '',
            transient: true,
          });

          draftContent = code;
        }
      }
    }

    return draftContent;
  },
  onUpdateDocument: async ({ document, description, dataStream }) => {
    let draftContent = '';

    const { fullStream } = streamObject({
      model: myProvider.languageModel('artifact-model'),
      system: updateDocumentPrompt(document.content, 'code'),
      prompt: description,
      schema: z.object({
        code: z.string(),
      }),
    });

    for await (const delta of fullStream) {
      const { type } = delta;

      if (type === 'object') {
        const { object } = delta;
        const { code } = object;

        if (code) {
          dataStream.write({
            type: 'data-codeDelta',
            data: code ?? '',
            transient: true,
          });

          draftContent = code;
        }
      }
    }

    return draftContent;
  },
});



================================================
FILE: artifacts/image/client.tsx
================================================
import { Artifact } from '@/components/create-artifact';
import { CopyIcon, RedoIcon, UndoIcon } from '@/components/icons';
import { ImageEditor } from '@/components/image-editor';
import { toast } from 'sonner';

export const imageArtifact = new Artifact({
  kind: 'image',
  description: 'Useful for image generation',
  onStreamPart: ({ streamPart, setArtifact }) => {
    if (streamPart.type === 'data-imageDelta') {
      setArtifact((draftArtifact) => ({
        ...draftArtifact,
        content: streamPart.data,
        isVisible: true,
        status: 'streaming',
      }));
    }
  },
  content: ImageEditor,
  actions: [
    {
      icon: <UndoIcon size={18} />,
      description: 'View Previous version',
      onClick: ({ handleVersionChange }) => {
        handleVersionChange('prev');
      },
      isDisabled: ({ currentVersionIndex }) => {
        if (currentVersionIndex === 0) {
          return true;
        }

        return false;
      },
    },
    {
      icon: <RedoIcon size={18} />,
      description: 'View Next version',
      onClick: ({ handleVersionChange }) => {
        handleVersionChange('next');
      },
      isDisabled: ({ isCurrentVersion }) => {
        if (isCurrentVersion) {
          return true;
        }

        return false;
      },
    },
    {
      icon: <CopyIcon size={18} />,
      description: 'Copy image to clipboard',
      onClick: ({ content }) => {
        const img = new Image();
        img.src = `data:image/png;base64,${content}`;

        img.onload = () => {
          const canvas = document.createElement('canvas');
          canvas.width = img.width;
          canvas.height = img.height;
          const ctx = canvas.getContext('2d');
          ctx?.drawImage(img, 0, 0);
          canvas.toBlob((blob) => {
            if (blob) {
              navigator.clipboard.write([
                new ClipboardItem({ 'image/png': blob }),
              ]);
            }
          }, 'image/png');
        };

        toast.success('Copied image to clipboard!');
      },
    },
  ],
  toolbar: [],
});



================================================
FILE: artifacts/sheet/client.tsx
================================================
import { Artifact } from '@/components/create-artifact';
import {
  CopyIcon,
  LineChartIcon,
  RedoIcon,
  SparklesIcon,
  UndoIcon,
} from '@/components/icons';
import { SpreadsheetEditor } from '@/components/sheet-editor';
import { parse, unparse } from 'papaparse';
import { toast } from 'sonner';

type Metadata = any;

export const sheetArtifact = new Artifact<'sheet', Metadata>({
  kind: 'sheet',
  description: 'Useful for working with spreadsheets',
  initialize: async () => {},
  onStreamPart: ({ setArtifact, streamPart }) => {
    if (streamPart.type === 'data-sheetDelta') {
      setArtifact((draftArtifact) => ({
        ...draftArtifact,
        content: streamPart.data,
        isVisible: true,
        status: 'streaming',
      }));
    }
  },
  content: ({
    content,
    currentVersionIndex,
    isCurrentVersion,
    onSaveContent,
    status,
  }) => {
    return (
      <SpreadsheetEditor
        content={content}
        currentVersionIndex={currentVersionIndex}
        isCurrentVersion={isCurrentVersion}
        saveContent={onSaveContent}
        status={status}
      />
    );
  },
  actions: [
    {
      icon: <UndoIcon size={18} />,
      description: 'View Previous version',
      onClick: ({ handleVersionChange }) => {
        handleVersionChange('prev');
      },
      isDisabled: ({ currentVersionIndex }) => {
        if (currentVersionIndex === 0) {
          return true;
        }

        return false;
      },
    },
    {
      icon: <RedoIcon size={18} />,
      description: 'View Next version',
      onClick: ({ handleVersionChange }) => {
        handleVersionChange('next');
      },
      isDisabled: ({ isCurrentVersion }) => {
        if (isCurrentVersion) {
          return true;
        }

        return false;
      },
    },
    {
      icon: <CopyIcon />,
      description: 'Copy as .csv',
      onClick: ({ content }) => {
        const parsed = parse<string[]>(content, { skipEmptyLines: true });

        const nonEmptyRows = parsed.data.filter((row) =>
          row.some((cell) => cell.trim() !== ''),
        );

        const cleanedCsv = unparse(nonEmptyRows);

        navigator.clipboard.writeText(cleanedCsv);
        toast.success('Copied csv to clipboard!');
      },
    },
  ],
  toolbar: [
    {
      description: 'Format and clean data',
      icon: <SparklesIcon />,
      onClick: ({ sendMessage }) => {
        sendMessage({
          role: 'user',
          parts: [
            { type: 'text', text: 'Can you please format and clean the data?' },
          ],
        });
      },
    },
    {
      description: 'Analyze and visualize data',
      icon: <LineChartIcon />,
      onClick: ({ sendMessage }) => {
        sendMessage({
          role: 'user',
          parts: [
            {
              type: 'text',
              text: 'Can you please analyze and visualize the data by creating a new code artifact in python?',
            },
          ],
        });
      },
    },
  ],
});



================================================
FILE: artifacts/sheet/server.ts
================================================
import { myProvider } from '@/lib/ai/providers';
import { sheetPrompt, updateDocumentPrompt } from '@/lib/ai/prompts';
import { createDocumentHandler } from '@/lib/artifacts/server';
import { streamObject } from 'ai';
import { z } from 'zod';

export const sheetDocumentHandler = createDocumentHandler<'sheet'>({
  kind: 'sheet',
  onCreateDocument: async ({ title, dataStream }) => {
    let draftContent = '';

    const { fullStream } = streamObject({
      model: myProvider.languageModel('artifact-model'),
      system: sheetPrompt,
      prompt: title,
      schema: z.object({
        csv: z.string().describe('CSV data'),
      }),
    });

    for await (const delta of fullStream) {
      const { type } = delta;

      if (type === 'object') {
        const { object } = delta;
        const { csv } = object;

        if (csv) {
          dataStream.write({
            type: 'data-sheetDelta',
            data: csv,
            transient: true,
          });

          draftContent = csv;
        }
      }
    }

    dataStream.write({
      type: 'data-sheetDelta',
      data: draftContent,
      transient: true,
    });

    return draftContent;
  },
  onUpdateDocument: async ({ document, description, dataStream }) => {
    let draftContent = '';

    const { fullStream } = streamObject({
      model: myProvider.languageModel('artifact-model'),
      system: updateDocumentPrompt(document.content, 'sheet'),
      prompt: description,
      schema: z.object({
        csv: z.string(),
      }),
    });

    for await (const delta of fullStream) {
      const { type } = delta;

      if (type === 'object') {
        const { object } = delta;
        const { csv } = object;

        if (csv) {
          dataStream.write({
            type: 'data-sheetDelta',
            data: csv,
            transient: true,
          });

          draftContent = csv;
        }
      }
    }

    return draftContent;
  },
});



================================================
FILE: artifacts/text/client.tsx
================================================
import { Artifact } from '@/components/create-artifact';
import { DiffView } from '@/components/diffview';
import { DocumentSkeleton } from '@/components/document-skeleton';
import { Editor } from '@/components/text-editor';
import {
  ClockRewind,
  CopyIcon,
  MessageIcon,
  PenIcon,
  RedoIcon,
  UndoIcon,
} from '@/components/icons';
import type { Suggestion } from '@/lib/db/schema';
import { toast } from 'sonner';
import { getSuggestions } from '../actions';

interface TextArtifactMetadata {
  suggestions: Array<Suggestion>;
}

export const textArtifact = new Artifact<'text', TextArtifactMetadata>({
  kind: 'text',
  description: 'Useful for text content, like drafting essays and emails.',
  initialize: async ({ documentId, setMetadata }) => {
    const suggestions = await getSuggestions({ documentId });

    setMetadata({
      suggestions,
    });
  },
  onStreamPart: ({ streamPart, setMetadata, setArtifact }) => {
    if (streamPart.type === 'data-suggestion') {
      setMetadata((metadata) => {
        return {
          suggestions: [...metadata.suggestions, streamPart.data],
        };
      });
    }

    if (streamPart.type === 'data-textDelta') {
      setArtifact((draftArtifact) => {
        return {
          ...draftArtifact,
          content: draftArtifact.content + streamPart.data,
          isVisible:
            draftArtifact.status === 'streaming' &&
            draftArtifact.content.length > 400 &&
            draftArtifact.content.length < 450
              ? true
              : draftArtifact.isVisible,
          status: 'streaming',
        };
      });
    }
  },
  content: ({
    mode,
    status,
    content,
    isCurrentVersion,
    currentVersionIndex,
    onSaveContent,
    getDocumentContentById,
    isLoading,
    metadata,
  }) => {
    if (isLoading) {
      return <DocumentSkeleton artifactKind="text" />;
    }

    if (mode === 'diff') {
      const oldContent = getDocumentContentById(currentVersionIndex - 1);
      const newContent = getDocumentContentById(currentVersionIndex);

      return <DiffView oldContent={oldContent} newContent={newContent} />;
    }

    return (
      <>
        <div className="flex flex-row py-8 md:p-20 px-4">
          <Editor
            content={content}
            suggestions={metadata ? metadata.suggestions : []}
            isCurrentVersion={isCurrentVersion}
            currentVersionIndex={currentVersionIndex}
            status={status}
            onSaveContent={onSaveContent}
          />

          {metadata?.suggestions && metadata.suggestions.length > 0 ? (
            <div className="md:hidden h-dvh w-12 shrink-0" />
          ) : null}
        </div>
      </>
    );
  },
  actions: [
    {
      icon: <ClockRewind size={18} />,
      description: 'View changes',
      onClick: ({ handleVersionChange }) => {
        handleVersionChange('toggle');
      },
      isDisabled: ({ currentVersionIndex, setMetadata }) => {
        if (currentVersionIndex === 0) {
          return true;
        }

        return false;
      },
    },
    {
      icon: <UndoIcon size={18} />,
      description: 'View Previous version',
      onClick: ({ handleVersionChange }) => {
        handleVersionChange('prev');
      },
      isDisabled: ({ currentVersionIndex }) => {
        if (currentVersionIndex === 0) {
          return true;
        }

        return false;
      },
    },
    {
      icon: <RedoIcon size={18} />,
      description: 'View Next version',
      onClick: ({ handleVersionChange }) => {
        handleVersionChange('next');
      },
      isDisabled: ({ isCurrentVersion }) => {
        if (isCurrentVersion) {
          return true;
        }

        return false;
      },
    },
    {
      icon: <CopyIcon size={18} />,
      description: 'Copy to clipboard',
      onClick: ({ content }) => {
        navigator.clipboard.writeText(content);
        toast.success('Copied to clipboard!');
      },
    },
  ],
  toolbar: [
    {
      icon: <PenIcon />,
      description: 'Add final polish',
      onClick: ({ sendMessage }) => {
        sendMessage({
          role: 'user',
          parts: [
            {
              type: 'text',
              text: 'Please add final polish and check for grammar, add section titles for better structure, and ensure everything reads smoothly.',
            },
          ],
        });
      },
    },
    {
      icon: <MessageIcon />,
      description: 'Request suggestions',
      onClick: ({ sendMessage }) => {
        sendMessage({
          role: 'user',
          parts: [
            {
              type: 'text',
              text: 'Please add suggestions you have that could improve the writing.',
            },
          ],
        });
      },
    },
  ],
});



================================================
FILE: artifacts/text/server.ts
================================================
import { smoothStream, streamText } from 'ai';
import { myProvider } from '@/lib/ai/providers';
import { createDocumentHandler } from '@/lib/artifacts/server';
import { updateDocumentPrompt } from '@/lib/ai/prompts';

export const textDocumentHandler = createDocumentHandler<'text'>({
  kind: 'text',
  onCreateDocument: async ({ title, dataStream }) => {
    let draftContent = '';

    const { fullStream } = streamText({
      model: myProvider.languageModel('artifact-model'),
      system:
        'Write about the given topic. Markdown is supported. Use headings wherever appropriate.',
      experimental_transform: smoothStream({ chunking: 'word' }),
      prompt: title,
    });

    for await (const delta of fullStream) {
      const { type } = delta;

      if (type === 'text-delta') {
        const { text } = delta;

        draftContent += text;

        dataStream.write({
          type: 'data-textDelta',
          data: text,
          transient: true,
        });
      }
    }

    return draftContent;
  },
  onUpdateDocument: async ({ document, description, dataStream }) => {
    let draftContent = '';

    const { fullStream } = streamText({
      model: myProvider.languageModel('artifact-model'),
      system: updateDocumentPrompt(document.content, 'text'),
      experimental_transform: smoothStream({ chunking: 'word' }),
      prompt: description,
      providerOptions: {
        openai: {
          prediction: {
            type: 'content',
            content: document.content,
          },
        },
      },
    });

    for await (const delta of fullStream) {
      const { type } = delta;

      if (type === 'text-delta') {
        const { text } = delta;

        draftContent += text;

        dataStream.write({
          type: 'data-textDelta',
          data: text,
          transient: true,
        });
      }
    }

    return draftContent;
  },
});



================================================
FILE: components/app-sidebar.tsx
================================================
'use client';

import type { User } from 'next-auth';
import { useRouter } from 'next/navigation';

import { PlusIcon } from '@/components/icons';
import { SidebarHistory } from '@/components/sidebar-history';
import { SidebarUserNav } from '@/components/sidebar-user-nav';
import { Button } from '@/components/ui/button';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  useSidebar,
} from '@/components/ui/sidebar';
import Link from 'next/link';
import { Tooltip, TooltipContent, TooltipTrigger } from './ui/tooltip';

export function AppSidebar({ user }: { user: User | undefined }) {
  const router = useRouter();
  const { setOpenMobile } = useSidebar();

  return (
    <Sidebar className="group-data-[side=left]:border-r-0">
      <SidebarHeader>
        <SidebarMenu>
          <div className="flex flex-row justify-between items-center">
            <Link
              href="/"
              onClick={() => {
                setOpenMobile(false);
              }}
              className="flex flex-row gap-3 items-center"
            >
              <span className="text-lg font-semibold px-2 hover:bg-muted rounded-md cursor-pointer">
                Chatbot
              </span>
            </Link>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  type="button"
                  className="p-2 h-fit"
                  onClick={() => {
                    setOpenMobile(false);
                    router.push('/');
                    router.refresh();
                  }}
                >
                  <PlusIcon />
                </Button>
              </TooltipTrigger>
              <TooltipContent align="end">New Chat</TooltipContent>
            </Tooltip>
          </div>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarHistory user={user} />
      </SidebarContent>
      <SidebarFooter>{user && <SidebarUserNav user={user} />}</SidebarFooter>
    </Sidebar>
  );
}



================================================
FILE: components/artifact-actions.tsx
================================================
import { Button } from './ui/button';
import { Tooltip, TooltipContent, TooltipTrigger } from './ui/tooltip';
import { artifactDefinitions, type UIArtifact } from './artifact';
import { type Dispatch, memo, type SetStateAction, useState } from 'react';
import type { ArtifactActionContext } from './create-artifact';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';

interface ArtifactActionsProps {
  artifact: UIArtifact;
  handleVersionChange: (type: 'next' | 'prev' | 'toggle' | 'latest') => void;
  currentVersionIndex: number;
  isCurrentVersion: boolean;
  mode: 'edit' | 'diff';
  metadata: any;
  setMetadata: Dispatch<SetStateAction<any>>;
}

function PureArtifactActions({
  artifact,
  handleVersionChange,
  currentVersionIndex,
  isCurrentVersion,
  mode,
  metadata,
  setMetadata,
}: ArtifactActionsProps) {
  const [isLoading, setIsLoading] = useState(false);

  const artifactDefinition = artifactDefinitions.find(
    (definition) => definition.kind === artifact.kind,
  );

  if (!artifactDefinition) {
    throw new Error('Artifact definition not found!');
  }

  const actionContext: ArtifactActionContext = {
    content: artifact.content,
    handleVersionChange,
    currentVersionIndex,
    isCurrentVersion,
    mode,
    metadata,
    setMetadata,
  };

  return (
    <div className="flex flex-row gap-1">
      {artifactDefinition.actions.map((action) => (
        <Tooltip key={action.description}>
          <TooltipTrigger asChild>
            <Button
              variant="outline"
              className={cn('h-fit dark:hover:bg-zinc-700', {
                'p-2': !action.label,
                'py-1.5 px-2': action.label,
              })}
              onClick={async () => {
                setIsLoading(true);

                try {
                  await Promise.resolve(action.onClick(actionContext));
                } catch (error) {
                  toast.error('Failed to execute action');
                } finally {
                  setIsLoading(false);
                }
              }}
              disabled={
                isLoading || artifact.status === 'streaming'
                  ? true
                  : action.isDisabled
                    ? action.isDisabled(actionContext)
                    : false
              }
            >
              {action.icon}
              {action.label}
            </Button>
          </TooltipTrigger>
          <TooltipContent>{action.description}</TooltipContent>
        </Tooltip>
      ))}
    </div>
  );
}

export const ArtifactActions = memo(
  PureArtifactActions,
  (prevProps, nextProps) => {
    if (prevProps.artifact.status !== nextProps.artifact.status) return false;
    if (prevProps.currentVersionIndex !== nextProps.currentVersionIndex)
      return false;
    if (prevProps.isCurrentVersion !== nextProps.isCurrentVersion) return false;
    if (prevProps.artifact.content !== nextProps.artifact.content) return false;

    return true;
  },
);



================================================
FILE: components/artifact-close-button.tsx
================================================
import { memo } from 'react';
import { CrossIcon } from './icons';
import { Button } from './ui/button';
import { initialArtifactData, useArtifact } from '@/hooks/use-artifact';

function PureArtifactCloseButton() {
  const { setArtifact } = useArtifact();

  return (
    <Button
      data-testid="artifact-close-button"
      variant="outline"
      className="h-fit p-2 dark:hover:bg-zinc-700"
      onClick={() => {
        setArtifact((currentArtifact) =>
          currentArtifact.status === 'streaming'
            ? {
                ...currentArtifact,
                isVisible: false,
              }
            : { ...initialArtifactData, status: 'idle' },
        );
      }}
    >
      <CrossIcon size={18} />
    </Button>
  );
}

export const ArtifactCloseButton = memo(PureArtifactCloseButton, () => true);



================================================
FILE: components/artifact-messages.tsx
================================================
import { PreviewMessage, ThinkingMessage } from './message';
import type { Vote } from '@/lib/db/schema';
import { memo } from 'react';
import equal from 'fast-deep-equal';
import type { UIArtifact } from './artifact';
import type { UseChatHelpers } from '@ai-sdk/react';
import { motion } from 'framer-motion';
import { useMessages } from '@/hooks/use-messages';
import type { ChatMessage } from '@/lib/types';

interface ArtifactMessagesProps {
  chatId: string;
  status: UseChatHelpers<ChatMessage>['status'];
  votes: Array<Vote> | undefined;
  messages: ChatMessage[];
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
  regenerate: UseChatHelpers<ChatMessage>['regenerate'];
  isReadonly: boolean;
  artifactStatus: UIArtifact['status'];
}

function PureArtifactMessages({
  chatId,
  status,
  votes,
  messages,
  setMessages,
  regenerate,
  isReadonly,
}: ArtifactMessagesProps) {
  const {
    containerRef: messagesContainerRef,
    endRef: messagesEndRef,
    onViewportEnter,
    onViewportLeave,
    hasSentMessage,
  } = useMessages({
    chatId,
    status,
  });

  return (
    <div
      ref={messagesContainerRef}
      className="flex overflow-y-scroll flex-col gap-4 items-center px-4 pt-20 h-full"
    >
      {messages.map((message, index) => (
        <PreviewMessage
          chatId={chatId}
          key={message.id}
          message={message}
          isLoading={status === 'streaming' && index === messages.length - 1}
          vote={
            votes
              ? votes.find((vote) => vote.messageId === message.id)
              : undefined
          }
          setMessages={setMessages}
          regenerate={regenerate}
          isReadonly={isReadonly}
          requiresScrollPadding={
            hasSentMessage && index === messages.length - 1
          }
          isArtifactVisible={true}
        />
      ))}

      {status === 'submitted' &&
        messages.length > 0 &&
        messages[messages.length - 1].role === 'user' && <ThinkingMessage />}

      <motion.div
        ref={messagesEndRef}
        className="shrink-0 min-w-[24px] min-h-[24px]"
        onViewportLeave={onViewportLeave}
        onViewportEnter={onViewportEnter}
      />
    </div>
  );
}

function areEqual(
  prevProps: ArtifactMessagesProps,
  nextProps: ArtifactMessagesProps,
) {
  if (
    prevProps.artifactStatus === 'streaming' &&
    nextProps.artifactStatus === 'streaming'
  )
    return true;

  if (prevProps.status !== nextProps.status) return false;
  if (prevProps.status && nextProps.status) return false;
  if (prevProps.messages.length !== nextProps.messages.length) return false;
  if (!equal(prevProps.votes, nextProps.votes)) return false;

  return true;
}

export const ArtifactMessages = memo(PureArtifactMessages, areEqual);



================================================
FILE: components/artifact.tsx
================================================
import { formatDistance } from 'date-fns';
import { AnimatePresence, motion } from 'framer-motion';
import {
  type Dispatch,
  memo,
  type SetStateAction,
  useCallback,
  useEffect,
  useState,
} from 'react';
import useSWR, { useSWRConfig } from 'swr';
import { useDebounceCallback, useWindowSize } from 'usehooks-ts';
import type { Document, Vote } from '@/lib/db/schema';
import { fetcher } from '@/lib/utils';
import { MultimodalInput } from './multimodal-input';
import { Toolbar } from './toolbar';
import { VersionFooter } from './version-footer';
import { ArtifactActions } from './artifact-actions';
import { ArtifactCloseButton } from './artifact-close-button';
import { ArtifactMessages } from './artifact-messages';
import { useSidebar } from './ui/sidebar';
import { useArtifact } from '@/hooks/use-artifact';
import { imageArtifact } from '@/artifacts/image/client';
import { codeArtifact } from '@/artifacts/code/client';
import { sheetArtifact } from '@/artifacts/sheet/client';
import { textArtifact } from '@/artifacts/text/client';
import equal from 'fast-deep-equal';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { VisibilityType } from './visibility-selector';
import type { Attachment, ChatMessage } from '@/lib/types';

export const artifactDefinitions = [
  textArtifact,
  codeArtifact,
  imageArtifact,
  sheetArtifact,
];
export type ArtifactKind = (typeof artifactDefinitions)[number]['kind'];

export interface UIArtifact {
  title: string;
  documentId: string;
  kind: ArtifactKind;
  content: string;
  isVisible: boolean;
  status: 'streaming' | 'idle';
  boundingBox: {
    top: number;
    left: number;
    width: number;
    height: number;
  };
}

function PureArtifact({
  chatId,
  input,
  setInput,
  status,
  stop,
  attachments,
  setAttachments,
  sendMessage,
  messages,
  setMessages,
  regenerate,
  votes,
  isReadonly,
  selectedVisibilityType,
  selectedModelId,
}: {
  chatId: string;
  input: string;
  setInput: Dispatch<SetStateAction<string>>;
  status: UseChatHelpers<ChatMessage>['status'];
  stop: UseChatHelpers<ChatMessage>['stop'];
  attachments: Attachment[];
  setAttachments: Dispatch<SetStateAction<Attachment[]>>;
  messages: ChatMessage[];
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
  votes: Array<Vote> | undefined;
  sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
  regenerate: UseChatHelpers<ChatMessage>['regenerate'];
  isReadonly: boolean;
  selectedVisibilityType: VisibilityType;
  selectedModelId: string;
}) {
  const { artifact, setArtifact, metadata, setMetadata } = useArtifact();

  const {
    data: documents,
    isLoading: isDocumentsFetching,
    mutate: mutateDocuments,
  } = useSWR<Array<Document>>(
    artifact.documentId !== 'init' && artifact.status !== 'streaming'
      ? `/api/document?id=${artifact.documentId}`
      : null,
    fetcher,
  );

  const [mode, setMode] = useState<'edit' | 'diff'>('edit');
  const [document, setDocument] = useState<Document | null>(null);
  const [currentVersionIndex, setCurrentVersionIndex] = useState(-1);

  const { open: isSidebarOpen } = useSidebar();

  useEffect(() => {
    if (documents && documents.length > 0) {
      const mostRecentDocument = documents.at(-1);

      if (mostRecentDocument) {
        setDocument(mostRecentDocument);
        setCurrentVersionIndex(documents.length - 1);
        setArtifact((currentArtifact) => ({
          ...currentArtifact,
          content: mostRecentDocument.content ?? '',
        }));
      }
    }
  }, [documents, setArtifact]);

  useEffect(() => {
    mutateDocuments();
  }, [artifact.status, mutateDocuments]);

  const { mutate } = useSWRConfig();
  const [isContentDirty, setIsContentDirty] = useState(false);

  const handleContentChange = useCallback(
    (updatedContent: string) => {
      if (!artifact) return;

      mutate<Array<Document>>(
        `/api/document?id=${artifact.documentId}`,
        async (currentDocuments) => {
          if (!currentDocuments) return undefined;

          const currentDocument = currentDocuments.at(-1);

          if (!currentDocument || !currentDocument.content) {
            setIsContentDirty(false);
            return currentDocuments;
          }

          if (currentDocument.content !== updatedContent) {
            await fetch(`/api/document?id=${artifact.documentId}`, {
              method: 'POST',
              body: JSON.stringify({
                title: artifact.title,
                content: updatedContent,
                kind: artifact.kind,
              }),
            });

            setIsContentDirty(false);

            const newDocument = {
              ...currentDocument,
              content: updatedContent,
              createdAt: new Date(),
            };

            return [...currentDocuments, newDocument];
          }
          return currentDocuments;
        },
        { revalidate: false },
      );
    },
    [artifact, mutate],
  );

  const debouncedHandleContentChange = useDebounceCallback(
    handleContentChange,
    2000,
  );

  const saveContent = useCallback(
    (updatedContent: string, debounce: boolean) => {
      if (document && updatedContent !== document.content) {
        setIsContentDirty(true);

        if (debounce) {
          debouncedHandleContentChange(updatedContent);
        } else {
          handleContentChange(updatedContent);
        }
      }
    },
    [document, debouncedHandleContentChange, handleContentChange],
  );

  function getDocumentContentById(index: number) {
    if (!documents) return '';
    if (!documents[index]) return '';
    return documents[index].content ?? '';
  }

  const handleVersionChange = (type: 'next' | 'prev' | 'toggle' | 'latest') => {
    if (!documents) return;

    if (type === 'latest') {
      setCurrentVersionIndex(documents.length - 1);
      setMode('edit');
    }

    if (type === 'toggle') {
      setMode((mode) => (mode === 'edit' ? 'diff' : 'edit'));
    }

    if (type === 'prev') {
      if (currentVersionIndex > 0) {
        setCurrentVersionIndex((index) => index - 1);
      }
    } else if (type === 'next') {
      if (currentVersionIndex < documents.length - 1) {
        setCurrentVersionIndex((index) => index + 1);
      }
    }
  };

  const [isToolbarVisible, setIsToolbarVisible] = useState(false);

  /*
   * NOTE: if there are no documents, or if
   * the documents are being fetched, then
   * we mark it as the current version.
   */

  const isCurrentVersion =
    documents && documents.length > 0
      ? currentVersionIndex === documents.length - 1
      : true;

  const { width: windowWidth, height: windowHeight } = useWindowSize();
  const isMobile = windowWidth ? windowWidth < 768 : false;

  const artifactDefinition = artifactDefinitions.find(
    (definition) => definition.kind === artifact.kind,
  );

  if (!artifactDefinition) {
    throw new Error('Artifact definition not found!');
  }

  useEffect(() => {
    if (artifact.documentId !== 'init') {
      if (artifactDefinition.initialize) {
        artifactDefinition.initialize({
          documentId: artifact.documentId,
          setMetadata,
        });
      }
    }
  }, [artifact.documentId, artifactDefinition, setMetadata]);

  return (
    <AnimatePresence>
      {artifact.isVisible && (
        <motion.div
          data-testid="artifact"
          className="flex flex-row h-dvh w-dvw fixed top-0 left-0 z-50 bg-transparent"
          initial={{ opacity: 1 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0, transition: { delay: 0.4 } }}
        >
          {!isMobile && (
            <motion.div
              className="fixed bg-background h-dvh"
              initial={{
                width: isSidebarOpen ? windowWidth - 256 : windowWidth,
                right: 0,
              }}
              animate={{ width: windowWidth, right: 0 }}
              exit={{
                width: isSidebarOpen ? windowWidth - 256 : windowWidth,
                right: 0,
              }}
            />
          )}

          {!isMobile && (
            <motion.div
              className="relative w-[400px] bg-muted dark:bg-background h-dvh shrink-0"
              initial={{ opacity: 0, x: 10, scale: 1 }}
              animate={{
                opacity: 1,
                x: 0,
                scale: 1,
                transition: {
                  delay: 0.1,
                  type: 'spring',
                  stiffness: 300,
                  damping: 30,
                },
              }}
              exit={{
                opacity: 0,
                x: 0,
                scale: 1,
                transition: { duration: 0 },
              }}
            >
              <AnimatePresence>
                {!isCurrentVersion && (
                  <motion.div
                    className="left-0 absolute h-dvh w-[400px] top-0 bg-zinc-900/50 z-50"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                  />
                )}
              </AnimatePresence>

              <div className="flex flex-col h-full justify-between items-center">
                <ArtifactMessages
                  chatId={chatId}
                  status={status}
                  votes={votes}
                  messages={messages}
                  setMessages={setMessages}
                  regenerate={regenerate}
                  isReadonly={isReadonly}
                  artifactStatus={artifact.status}
                />

                <div className="flex flex-row gap-2 relative items-end w-full px-4 pb-4">
                  <MultimodalInput
                    chatId={chatId}
                    input={input}
                    setInput={setInput}
                    status={status}
                    stop={stop}
                    attachments={attachments}
                    setAttachments={setAttachments}
                    messages={messages}
                    sendMessage={sendMessage}
                    className="bg-background dark:bg-muted"
                    setMessages={setMessages}
                    selectedVisibilityType={selectedVisibilityType}
                    selectedModelId={selectedModelId}
                  />
                </div>
              </div>
            </motion.div>
          )}

          <motion.div
            className="fixed dark:bg-muted bg-background h-dvh flex flex-col overflow-y-scroll md:border-l dark:border-zinc-700 border-zinc-200"
            initial={
              isMobile
                ? {
                    opacity: 1,
                    x: artifact.boundingBox.left,
                    y: artifact.boundingBox.top,
                    height: artifact.boundingBox.height,
                    width: artifact.boundingBox.width,
                    borderRadius: 50,
                  }
                : {
                    opacity: 1,
                    x: artifact.boundingBox.left,
                    y: artifact.boundingBox.top,
                    height: artifact.boundingBox.height,
                    width: artifact.boundingBox.width,
                    borderRadius: 50,
                  }
            }
            animate={
              isMobile
                ? {
                    opacity: 1,
                    x: 0,
                    y: 0,
                    height: windowHeight,
                    width: windowWidth ? windowWidth : 'calc(100dvw)',
                    borderRadius: 0,
                    transition: {
                      delay: 0,
                      type: 'spring',
                      stiffness: 300,
                      damping: 30,
                      duration: 0.8,
                    },
                  }
                : {
                    opacity: 1,
                    x: 400,
                    y: 0,
                    height: windowHeight,
                    width: windowWidth
                      ? windowWidth - 400
                      : 'calc(100dvw-400px)',
                    borderRadius: 0,
                    transition: {
                      delay: 0,
                      type: 'spring',
                      stiffness: 300,
                      damping: 30,
                      duration: 0.8,
                    },
                  }
            }
            exit={{
              opacity: 0,
              scale: 0.5,
              transition: {
                delay: 0.1,
                type: 'spring',
                stiffness: 600,
                damping: 30,
              },
            }}
          >
            <div className="p-2 flex flex-row justify-between items-start">
              <div className="flex flex-row gap-4 items-start">
                <ArtifactCloseButton />

                <div className="flex flex-col">
                  <div className="font-medium">{artifact.title}</div>

                  {isContentDirty ? (
                    <div className="text-sm text-muted-foreground">
                      Saving changes...
                    </div>
                  ) : document ? (
                    <div className="text-sm text-muted-foreground">
                      {`Updated ${formatDistance(
                        new Date(document.createdAt),
                        new Date(),
                        {
                          addSuffix: true,
                        },
                      )}`}
                    </div>
                  ) : (
                    <div className="w-32 h-3 mt-2 bg-muted-foreground/20 rounded-md animate-pulse" />
                  )}
                </div>
              </div>

              <ArtifactActions
                artifact={artifact}
                currentVersionIndex={currentVersionIndex}
                handleVersionChange={handleVersionChange}
                isCurrentVersion={isCurrentVersion}
                mode={mode}
                metadata={metadata}
                setMetadata={setMetadata}
              />
            </div>

            <div className="dark:bg-muted bg-background h-full overflow-y-scroll !max-w-full items-center">
              <artifactDefinition.content
                title={artifact.title}
                content={
                  isCurrentVersion
                    ? artifact.content
                    : getDocumentContentById(currentVersionIndex)
                }
                mode={mode}
                status={artifact.status}
                currentVersionIndex={currentVersionIndex}
                suggestions={[]}
                onSaveContent={saveContent}
                isInline={false}
                isCurrentVersion={isCurrentVersion}
                getDocumentContentById={getDocumentContentById}
                isLoading={isDocumentsFetching && !artifact.content}
                metadata={metadata}
                setMetadata={setMetadata}
              />

              <AnimatePresence>
                {isCurrentVersion && (
                  <Toolbar
                    isToolbarVisible={isToolbarVisible}
                    setIsToolbarVisible={setIsToolbarVisible}
                    sendMessage={sendMessage}
                    status={status}
                    stop={stop}
                    setMessages={setMessages}
                    artifactKind={artifact.kind}
                  />
                )}
              </AnimatePresence>
            </div>

            <AnimatePresence>
              {!isCurrentVersion && (
                <VersionFooter
                  currentVersionIndex={currentVersionIndex}
                  documents={documents}
                  handleVersionChange={handleVersionChange}
                />
              )}
            </AnimatePresence>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export const Artifact = memo(PureArtifact, (prevProps, nextProps) => {
  if (prevProps.status !== nextProps.status) return false;
  if (!equal(prevProps.votes, nextProps.votes)) return false;
  if (prevProps.input !== nextProps.input) return false;
  if (!equal(prevProps.messages, nextProps.messages.length)) return false;
  if (prevProps.selectedVisibilityType !== nextProps.selectedVisibilityType)
    return false;

  return true;
});



================================================
FILE: components/auth-form.tsx
================================================
import Form from 'next/form';

import { Input } from './ui/input';
import { Label } from './ui/label';

export function AuthForm({
  action,
  children,
  defaultEmail = '',
}: {
  action: NonNullable<
    string | ((formData: FormData) => void | Promise<void>) | undefined
  >;
  children: React.ReactNode;
  defaultEmail?: string;
}) {
  return (
    <Form action={action} className="flex flex-col gap-4 px-4 sm:px-16">
      <div className="flex flex-col gap-2">
        <Label
          htmlFor="email"
          className="text-zinc-600 font-normal dark:text-zinc-400"
        >
          Email Address
        </Label>

        <Input
          id="email"
          name="email"
          className="bg-muted text-md md:text-sm"
          type="email"
          placeholder="user@acme.com"
          autoComplete="email"
          required
          autoFocus
          defaultValue={defaultEmail}
        />
      </div>

      <div className="flex flex-col gap-2">
        <Label
          htmlFor="password"
          className="text-zinc-600 font-normal dark:text-zinc-400"
        >
          Password
        </Label>

        <Input
          id="password"
          name="password"
          className="bg-muted text-md md:text-sm"
          type="password"
          required
        />
      </div>

      {children}
    </Form>
  );
}



================================================
FILE: components/chat-header.tsx
================================================
'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useWindowSize } from 'usehooks-ts';

import { SidebarToggle } from '@/components/sidebar-toggle';
import { Button } from '@/components/ui/button';
import { PlusIcon, VercelIcon } from './icons';
import { useSidebar } from './ui/sidebar';
import { memo } from 'react';
import { Tooltip, TooltipContent, TooltipTrigger } from './ui/tooltip';
import { type VisibilityType, VisibilitySelector } from './visibility-selector';
import type { Session } from 'next-auth';

function PureChatHeader({
  chatId,
  selectedVisibilityType,
  isReadonly,
  session,
}: {
  chatId: string;
  selectedVisibilityType: VisibilityType;
  isReadonly: boolean;
  session: Session;
}) {
  const router = useRouter();
  const { open } = useSidebar();

  const { width: windowWidth } = useWindowSize();

  return (
    <header className="flex sticky top-0 bg-background py-1.5 items-center px-2 md:px-2 gap-2">
      <SidebarToggle />

      {(!open || windowWidth < 768) && (
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="outline"
              className="order-2 md:order-1 md:px-2 px-2 md:h-fit ml-auto md:ml-0"
              onClick={() => {
                router.push('/');
                router.refresh();
              }}
            >
              <PlusIcon />
              <span className="md:sr-only">New Chat</span>
            </Button>
          </TooltipTrigger>
          <TooltipContent>New Chat</TooltipContent>
        </Tooltip>
      )}

      {!isReadonly && (
        <VisibilitySelector
          chatId={chatId}
          selectedVisibilityType={selectedVisibilityType}
          className="order-1 md:order-2"
        />
      )}

      <Button
        className="bg-zinc-900 dark:bg-zinc-100 hover:bg-zinc-800 dark:hover:bg-zinc-200 text-zinc-50 dark:text-zinc-900 hidden md:flex py-1.5 px-2 h-fit md:h-[34px] order-3 md:ml-auto"
        asChild
      >
        <Link
          href={`https://vercel.com/new/clone?repository-url=https://github.com/vercel/ai-chatbot&env=AUTH_SECRET&envDescription=Learn more about how to get the API Keys for the application&envLink=https://github.com/vercel/ai-chatbot/blob/main/.env.example&demo-title=AI Chatbot&demo-description=An Open-Source AI Chatbot Template Built With Next.js and the AI SDK by Vercel.&demo-url=https://chat.vercel.ai&products=[{"type":"integration","protocol":"ai","productSlug":"grok","integrationSlug":"xai"},{"type":"integration","protocol":"storage","productSlug":"neon","integrationSlug":"neon"},{"type":"integration","protocol":"storage","productSlug":"upstash-kv","integrationSlug":"upstash"},{"type":"blob"}]`}
          target="_noblank"
        >
          <VercelIcon size={16} />
          Deploy with Vercel
        </Link>
      </Button>
    </header>
  );
}

export const ChatHeader = memo(PureChatHeader, (prevProps, nextProps) => {
  return (
    prevProps.chatId === nextProps.chatId &&
    prevProps.selectedVisibilityType === nextProps.selectedVisibilityType &&
    prevProps.isReadonly === nextProps.isReadonly
  );
});



================================================
FILE: components/chat.tsx
================================================
'use client';

import { DefaultChatTransport } from 'ai';
import { useChat } from '@ai-sdk/react';
import { useEffect, useState } from 'react';
import useSWR, { useSWRConfig } from 'swr';
import { ChatHeader } from '@/components/chat-header';
import type { Vote } from '@/lib/db/schema';
import { fetcher, fetchWithErrorHandlers, generateUUID, cn } from '@/lib/utils';
import { Artifact } from './artifact';
import { MultimodalInput } from './multimodal-input';
import { Messages } from './messages';
import type { VisibilityType } from './visibility-selector';
import { useArtifactSelector } from '@/hooks/use-artifact';
import { unstable_serialize } from 'swr/infinite';
import { getChatHistoryPaginationKey } from './sidebar-history';
import { toast } from './toast';
import type { Session } from 'next-auth';
import { useSearchParams } from 'next/navigation';
import { useChatVisibility } from '@/hooks/use-chat-visibility';
import { useAutoResume } from '@/hooks/use-auto-resume';
import { ChatSDKError } from '@/lib/errors';
import type { Attachment, ChatMessage } from '@/lib/types';
import { useDataStream } from './data-stream-provider';

export function Chat({
  id,
  initialMessages,
  initialChatModel,
  initialVisibilityType,
  isReadonly,
  session,
  autoResume,
}: {
  id: string;
  initialMessages: ChatMessage[];
  initialChatModel: string;
  initialVisibilityType: VisibilityType;
  isReadonly: boolean;
  session: Session;
  autoResume: boolean;
}) {
  const { visibilityType } = useChatVisibility({
    chatId: id,
    initialVisibilityType,
  });

  const { mutate } = useSWRConfig();
  const { setDataStream } = useDataStream();

  const [input, setInput] = useState<string>('');

  const {
    messages,
    setMessages,
    sendMessage,
    status,
    stop,
    regenerate,
    resumeStream,
  } = useChat<ChatMessage>({
    id,
    messages: initialMessages,
    experimental_throttle: 100,
    generateId: generateUUID,
    transport: new DefaultChatTransport({
      api: '/api/chat',
      fetch: fetchWithErrorHandlers,
      prepareSendMessagesRequest({ messages, id, body }) {
        return {
          body: {
            id,
            message: messages.at(-1),
            selectedChatModel: initialChatModel,
            selectedVisibilityType: visibilityType,
            ...body,
          },
        };
      },
    }),
    onData: (dataPart) => {
      setDataStream((ds) => (ds ? [...ds, dataPart] : []));
    },
    onFinish: () => {
      mutate(unstable_serialize(getChatHistoryPaginationKey));
    },
    onError: (error) => {
      if (error instanceof ChatSDKError) {
        toast({
          type: 'error',
          description: error.message,
        });
      }
    },
  });

  const searchParams = useSearchParams();
  const query = searchParams.get('query');

  const [hasAppendedQuery, setHasAppendedQuery] = useState(false);

  useEffect(() => {
    if (query && !hasAppendedQuery) {
      sendMessage({
        role: 'user' as const,
        parts: [{ type: 'text', text: query }],
      });

      setHasAppendedQuery(true);
      window.history.replaceState({}, '', `/chat/${id}`);
    }
  }, [query, sendMessage, hasAppendedQuery, id]);

  const { data: votes } = useSWR<Array<Vote>>(
    messages.length >= 2 ? `/api/vote?chatId=${id}` : null,
    fetcher,
  );

  const [attachments, setAttachments] = useState<Array<Attachment>>([]);
  const isArtifactVisible = useArtifactSelector((state) => state.isVisible);

  useAutoResume({
    autoResume,
    initialMessages,
    resumeStream,
    setMessages,
  });

  return (
    <>
      <div className="flex flex-col min-w-0 h-dvh bg-background">
        <ChatHeader
          chatId={id}
          selectedVisibilityType={initialVisibilityType}
          isReadonly={isReadonly}
          session={session}
        />

        <Messages
          chatId={id}
          status={status}
          votes={votes}
          messages={messages}
          setMessages={setMessages}
          regenerate={regenerate}
          isReadonly={isReadonly}
          isArtifactVisible={isArtifactVisible}
        />

        <div className="sticky bottom-0 flex gap-2 px-4 pb-4 mx-auto w-full bg-background md:pb-6 md:max-w-3xl z-[1] border-t-0">
          {!isReadonly && (
            <MultimodalInput
              chatId={id}
              input={input}
              setInput={setInput}
              status={status}
              stop={stop}
              attachments={attachments}
              setAttachments={setAttachments}
              messages={messages}
              setMessages={setMessages}
              sendMessage={sendMessage}
              selectedVisibilityType={visibilityType}
              selectedModelId={initialChatModel}
            />
          )}
        </div>
      </div>

      <Artifact
        chatId={id}
        input={input}
        setInput={setInput}
        status={status}
        stop={stop}
        attachments={attachments}
        setAttachments={setAttachments}
        sendMessage={sendMessage}
        messages={messages}
        setMessages={setMessages}
        regenerate={regenerate}
        votes={votes}
        isReadonly={isReadonly}
        selectedVisibilityType={visibilityType}
        selectedModelId={initialChatModel}
      />
    </>
  );
}



================================================
FILE: components/code-editor.tsx
================================================
'use client';

import { EditorView } from '@codemirror/view';
import { EditorState, Transaction } from '@codemirror/state';
import { python } from '@codemirror/lang-python';
import { oneDark } from '@codemirror/theme-one-dark';
import { basicSetup } from 'codemirror';
import React, { memo, useEffect, useRef } from 'react';
import type { Suggestion } from '@/lib/db/schema';

type EditorProps = {
  content: string;
  onSaveContent: (updatedContent: string, debounce: boolean) => void;
  status: 'streaming' | 'idle';
  isCurrentVersion: boolean;
  currentVersionIndex: number;
  suggestions: Array<Suggestion>;
};

function PureCodeEditor({ content, onSaveContent, status }: EditorProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const editorRef = useRef<EditorView | null>(null);

  useEffect(() => {
    if (containerRef.current && !editorRef.current) {
      const startState = EditorState.create({
        doc: content,
        extensions: [basicSetup, python(), oneDark],
      });

      editorRef.current = new EditorView({
        state: startState,
        parent: containerRef.current,
      });
    }

    return () => {
      if (editorRef.current) {
        editorRef.current.destroy();
        editorRef.current = null;
      }
    };
    // NOTE: we only want to run this effect once
    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    if (editorRef.current) {
      const updateListener = EditorView.updateListener.of((update) => {
        if (update.docChanged) {
          const transaction = update.transactions.find(
            (tr) => !tr.annotation(Transaction.remote),
          );

          if (transaction) {
            const newContent = update.state.doc.toString();
            onSaveContent(newContent, true);
          }
        }
      });

      const currentSelection = editorRef.current.state.selection;

      const newState = EditorState.create({
        doc: editorRef.current.state.doc,
        extensions: [basicSetup, python(), oneDark, updateListener],
        selection: currentSelection,
      });

      editorRef.current.setState(newState);
    }
  }, [onSaveContent]);

  useEffect(() => {
    if (editorRef.current && content) {
      const currentContent = editorRef.current.state.doc.toString();

      if (status === 'streaming' || currentContent !== content) {
        const transaction = editorRef.current.state.update({
          changes: {
            from: 0,
            to: currentContent.length,
            insert: content,
          },
          annotations: [Transaction.remote.of(true)],
        });

        editorRef.current.dispatch(transaction);
      }
    }
  }, [content, status]);

  return (
    <div
      className="relative not-prose w-full pb-[calc(80dvh)] text-sm"
      ref={containerRef}
    />
  );
}

function areEqual(prevProps: EditorProps, nextProps: EditorProps) {
  if (prevProps.suggestions !== nextProps.suggestions) return false;
  if (prevProps.currentVersionIndex !== nextProps.currentVersionIndex)
    return false;
  if (prevProps.isCurrentVersion !== nextProps.isCurrentVersion) return false;
  if (prevProps.status === 'streaming' && nextProps.status === 'streaming')
    return false;
  if (prevProps.content !== nextProps.content) return false;

  return true;
}

export const CodeEditor = memo(PureCodeEditor, areEqual);



================================================
FILE: components/console.tsx
================================================
import { TerminalWindowIcon, CrossSmallIcon } from './icons';
import { Loader } from './elements/loader';
import { Button } from './ui/button';
import {
  type Dispatch,
  type SetStateAction,
  useCallback,
  useEffect,
  useRef,
  useState,
} from 'react';
import { cn } from '@/lib/utils';
import { useArtifactSelector } from '@/hooks/use-artifact';

export interface ConsoleOutputContent {
  type: 'text' | 'image';
  value: string;
}

export interface ConsoleOutput {
  id: string;
  status: 'in_progress' | 'loading_packages' | 'completed' | 'failed';
  contents: Array<ConsoleOutputContent>;
}

interface ConsoleProps {
  consoleOutputs: Array<ConsoleOutput>;
  setConsoleOutputs: Dispatch<SetStateAction<Array<ConsoleOutput>>>;
}

export function Console({ consoleOutputs, setConsoleOutputs }: ConsoleProps) {
  const [height, setHeight] = useState<number>(300);
  const [isResizing, setIsResizing] = useState(false);
  const consoleEndRef = useRef<HTMLDivElement>(null);

  const isArtifactVisible = useArtifactSelector((state) => state.isVisible);

  const minHeight = 100;
  const maxHeight = 800;

  const startResizing = useCallback(() => {
    setIsResizing(true);
  }, []);

  const stopResizing = useCallback(() => {
    setIsResizing(false);
  }, []);

  const resize = useCallback(
    (e: MouseEvent) => {
      if (isResizing) {
        const newHeight = window.innerHeight - e.clientY;
        if (newHeight >= minHeight && newHeight <= maxHeight) {
          setHeight(newHeight);
        }
      }
    },
    [isResizing],
  );

  useEffect(() => {
    window.addEventListener('mousemove', resize);
    window.addEventListener('mouseup', stopResizing);
    return () => {
      window.removeEventListener('mousemove', resize);
      window.removeEventListener('mouseup', stopResizing);
    };
  }, [resize, stopResizing]);

  useEffect(() => {
    consoleEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [consoleOutputs]);

  useEffect(() => {
    if (!isArtifactVisible) {
      setConsoleOutputs([]);
    }
  }, [isArtifactVisible, setConsoleOutputs]);

  return consoleOutputs.length > 0 ? (
    <>
      <div
        className="fixed z-50 w-full h-2 cursor-ns-resize"
        onMouseDown={startResizing}
        style={{ bottom: height - 4 }}
        role="slider"
        aria-valuenow={minHeight}
      />

      <div
        className={cn(
          'flex overflow-x-hidden overflow-y-scroll fixed bottom-0 z-40 flex-col w-full border-t dark:bg-zinc-900 bg-zinc-50 dark:border-zinc-700 border-zinc-200',
          {
            'select-none': isResizing,
          },
        )}
        style={{ height }}
      >
        <div className="flex sticky top-0 z-50 flex-row justify-between items-center px-2 py-1 w-full border-b h-fit dark:border-zinc-700 border-zinc-200 bg-muted">
          <div className="flex flex-row gap-3 items-center pl-2 text-sm dark:text-zinc-50 text-zinc-800">
            <div className="text-muted-foreground">
              <TerminalWindowIcon />
            </div>
            <div>Console</div>
          </div>
          <Button
            variant="ghost"
            className="p-1 size-fit hover:dark:bg-zinc-700 hover:bg-zinc-200"
            size="icon"
            onClick={() => setConsoleOutputs([])}
          >
            <CrossSmallIcon />
          </Button>
        </div>

        <div>
          {consoleOutputs.map((consoleOutput, index) => (
            <div
              key={consoleOutput.id}
              className="flex flex-row px-4 py-2 font-mono text-sm border-b dark:border-zinc-700 border-zinc-200 dark:bg-zinc-900 bg-zinc-50"
            >
              <div
                className={cn('w-12 shrink-0', {
                  'text-muted-foreground': [
                    'in_progress',
                    'loading_packages',
                  ].includes(consoleOutput.status),
                  'text-emerald-500': consoleOutput.status === 'completed',
                  'text-red-400': consoleOutput.status === 'failed',
                })}
              >
                [{index + 1}]
              </div>
              {['in_progress', 'loading_packages'].includes(
                consoleOutput.status,
              ) ? (
                <div className="flex flex-row gap-2">
                  <div className="size-fit self-center mb-auto mt-0.5">
                    <Loader size={16} />
                  </div>
                  <div className="text-muted-foreground">
                    {consoleOutput.status === 'in_progress'
                      ? 'Initializing...'
                      : consoleOutput.status === 'loading_packages'
                        ? consoleOutput.contents.map((content) =>
                            content.type === 'text' ? content.value : null,
                          )
                        : null}
                  </div>
                </div>
              ) : (
                <div className="flex overflow-x-scroll flex-col gap-2 w-full dark:text-zinc-50 text-zinc-900">
                  {consoleOutput.contents.map((content, index) =>
                    content.type === 'image' ? (
                      <picture key={`${consoleOutput.id}-${index}`}>
                        <img
                          src={content.value}
                          alt="output"
                          className="w-full rounded-md max-w-screen-toast-mobile"
                        />
                      </picture>
                    ) : (
                      <div
                        key={`${consoleOutput.id}-${index}`}
                        className="w-full whitespace-pre-line break-words"
                      >
                        {content.value}
                      </div>
                    ),
                  )}
                </div>
              )}
            </div>
          ))}
          <div ref={consoleEndRef} />
        </div>
      </div>
    </>
  ) : null;
}



================================================
FILE: components/create-artifact.tsx
================================================
import type { Suggestion } from '@/lib/db/schema';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { ComponentType, Dispatch, ReactNode, SetStateAction } from 'react';
import type { UIArtifact } from './artifact';
import type { ChatMessage, CustomUIDataTypes } from '@/lib/types';
import type { DataUIPart } from 'ai';

export type ArtifactActionContext<M = any> = {
  content: string;
  handleVersionChange: (type: 'next' | 'prev' | 'toggle' | 'latest') => void;
  currentVersionIndex: number;
  isCurrentVersion: boolean;
  mode: 'edit' | 'diff';
  metadata: M;
  setMetadata: Dispatch<SetStateAction<M>>;
};

type ArtifactAction<M = any> = {
  icon: ReactNode;
  label?: string;
  description: string;
  onClick: (context: ArtifactActionContext<M>) => Promise<void> | void;
  isDisabled?: (context: ArtifactActionContext<M>) => boolean;
};

export type ArtifactToolbarContext = {
  sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
};

export type ArtifactToolbarItem = {
  description: string;
  icon: ReactNode;
  onClick: (context: ArtifactToolbarContext) => void;
};

interface ArtifactContent<M = any> {
  title: string;
  content: string;
  mode: 'edit' | 'diff';
  isCurrentVersion: boolean;
  currentVersionIndex: number;
  status: 'streaming' | 'idle';
  suggestions: Array<Suggestion>;
  onSaveContent: (updatedContent: string, debounce: boolean) => void;
  isInline: boolean;
  getDocumentContentById: (index: number) => string;
  isLoading: boolean;
  metadata: M;
  setMetadata: Dispatch<SetStateAction<M>>;
}

interface InitializeParameters<M = any> {
  documentId: string;
  setMetadata: Dispatch<SetStateAction<M>>;
}

type ArtifactConfig<T extends string, M = any> = {
  kind: T;
  description: string;
  content: ComponentType<ArtifactContent<M>>;
  actions: Array<ArtifactAction<M>>;
  toolbar: ArtifactToolbarItem[];
  initialize?: (parameters: InitializeParameters<M>) => void;
  onStreamPart: (args: {
    setMetadata: Dispatch<SetStateAction<M>>;
    setArtifact: Dispatch<SetStateAction<UIArtifact>>;
    streamPart: DataUIPart<CustomUIDataTypes>;
  }) => void;
};

export class Artifact<T extends string, M = any> {
  readonly kind: T;
  readonly description: string;
  readonly content: ComponentType<ArtifactContent<M>>;
  readonly actions: Array<ArtifactAction<M>>;
  readonly toolbar: ArtifactToolbarItem[];
  readonly initialize?: (parameters: InitializeParameters) => void;
  readonly onStreamPart: (args: {
    setMetadata: Dispatch<SetStateAction<M>>;
    setArtifact: Dispatch<SetStateAction<UIArtifact>>;
    streamPart: DataUIPart<CustomUIDataTypes>;
  }) => void;

  constructor(config: ArtifactConfig<T, M>) {
    this.kind = config.kind;
    this.description = config.description;
    this.content = config.content;
    this.actions = config.actions || [];
    this.toolbar = config.toolbar || [];
    this.initialize = config.initialize || (async () => ({}));
    this.onStreamPart = config.onStreamPart;
  }
}



================================================
FILE: components/data-stream-handler.tsx
================================================
'use client';

import { useEffect, useRef } from 'react';
import { artifactDefinitions } from './artifact';
import { initialArtifactData, useArtifact } from '@/hooks/use-artifact';
import { useDataStream } from './data-stream-provider';

export function DataStreamHandler() {
  const { dataStream } = useDataStream();

  const { artifact, setArtifact, setMetadata } = useArtifact();
  const lastProcessedIndex = useRef(-1);

  useEffect(() => {
    if (!dataStream?.length) return;

    const newDeltas = dataStream.slice(lastProcessedIndex.current + 1);
    lastProcessedIndex.current = dataStream.length - 1;

    newDeltas.forEach((delta) => {
      const artifactDefinition = artifactDefinitions.find(
        (artifactDefinition) => artifactDefinition.kind === artifact.kind,
      );

      if (artifactDefinition?.onStreamPart) {
        artifactDefinition.onStreamPart({
          streamPart: delta,
          setArtifact,
          setMetadata,
        });
      }

      setArtifact((draftArtifact) => {
        if (!draftArtifact) {
          return { ...initialArtifactData, status: 'streaming' };
        }

        switch (delta.type) {
          case 'data-id':
            return {
              ...draftArtifact,
              documentId: delta.data,
              status: 'streaming',
            };

          case 'data-title':
            return {
              ...draftArtifact,
              title: delta.data,
              status: 'streaming',
            };

          case 'data-kind':
            return {
              ...draftArtifact,
              kind: delta.data,
              status: 'streaming',
            };

          case 'data-clear':
            return {
              ...draftArtifact,
              content: '',
              status: 'streaming',
            };

          case 'data-finish':
            return {
              ...draftArtifact,
              status: 'idle',
            };

          default:
            return draftArtifact;
        }
      });
    });
  }, [dataStream, setArtifact, setMetadata, artifact]);

  return null;
}



================================================
FILE: components/data-stream-provider.tsx
================================================
'use client';

import React, { createContext, useContext, useMemo, useState } from 'react';
import type { DataUIPart } from 'ai';
import type { CustomUIDataTypes } from '@/lib/types';

interface DataStreamContextValue {
  dataStream: DataUIPart<CustomUIDataTypes>[];
  setDataStream: React.Dispatch<
    React.SetStateAction<DataUIPart<CustomUIDataTypes>[]>
  >;
}

const DataStreamContext = createContext<DataStreamContextValue | null>(null);

export function DataStreamProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [dataStream, setDataStream] = useState<DataUIPart<CustomUIDataTypes>[]>(
    [],
  );

  const value = useMemo(() => ({ dataStream, setDataStream }), [dataStream]);

  return (
    <DataStreamContext.Provider value={value}>
      {children}
    </DataStreamContext.Provider>
  );
}

export function useDataStream() {
  const context = useContext(DataStreamContext);
  if (!context) {
    throw new Error('useDataStream must be used within a DataStreamProvider');
  }
  return context;
}



================================================
FILE: components/diffview.tsx
================================================
import OrderedMap from 'orderedmap';
import {
  Schema,
  type Node as ProsemirrorNode,
  type MarkSpec,
  DOMParser,
} from 'prosemirror-model';
import { schema } from 'prosemirror-schema-basic';
import { addListNodes } from 'prosemirror-schema-list';
import { EditorState } from 'prosemirror-state';
import { EditorView } from 'prosemirror-view';
import React, { useEffect, useRef } from 'react';
import { renderToString } from 'react-dom/server';
import { Streamdown } from 'streamdown';

import { diffEditor, DiffType } from '@/lib/editor/diff';

const diffSchema = new Schema({
  nodes: addListNodes(schema.spec.nodes, 'paragraph block*', 'block'),
  marks: OrderedMap.from({
    ...schema.spec.marks.toObject(),
    diffMark: {
      attrs: { type: { default: '' } },
      toDOM(mark) {
        let className = '';

        switch (mark.attrs.type) {
          case DiffType.Inserted:
            className =
              'bg-green-100 text-green-700 dark:bg-green-500/70 dark:text-green-300';
            break;
          case DiffType.Deleted:
            className =
              'bg-red-100 line-through text-red-600 dark:bg-red-500/70 dark:text-red-300';
            break;
          default:
            className = '';
        }
        return ['span', { class: className }, 0];
      },
    } as MarkSpec,
  }),
});

function computeDiff(oldDoc: ProsemirrorNode, newDoc: ProsemirrorNode) {
  return diffEditor(diffSchema, oldDoc.toJSON(), newDoc.toJSON());
}

type DiffEditorProps = {
  oldContent: string;
  newContent: string;
};

export const DiffView = ({ oldContent, newContent }: DiffEditorProps) => {
  const editorRef = useRef<HTMLDivElement>(null);
  const viewRef = useRef<EditorView | null>(null);

  useEffect(() => {
    if (editorRef.current && !viewRef.current) {
      const parser = DOMParser.fromSchema(diffSchema);

      const oldHtmlContent = renderToString(
        <Streamdown>{oldContent}</Streamdown>,
      );
      const newHtmlContent = renderToString(
        <Streamdown>{newContent}</Streamdown>,
      );

      const oldContainer = document.createElement('div');
      oldContainer.innerHTML = oldHtmlContent;

      const newContainer = document.createElement('div');
      newContainer.innerHTML = newHtmlContent;

      const oldDoc = parser.parse(oldContainer);
      const newDoc = parser.parse(newContainer);

      const diffedDoc = computeDiff(oldDoc, newDoc);

      const state = EditorState.create({
        doc: diffedDoc,
        plugins: [],
      });

      viewRef.current = new EditorView(editorRef.current, {
        state,
        editable: () => false,
      });
    }

    return () => {
      if (viewRef.current) {
        viewRef.current.destroy();
        viewRef.current = null;
      }
    };
  }, [oldContent, newContent]);

  return <div className="diff-editor" ref={editorRef} />;
};



================================================
FILE: components/document-preview.tsx
================================================
'use client';

import {
  memo,
  type MouseEvent,
  useCallback,
  useEffect,
  useMemo,
  useRef,
} from 'react';
import type { ArtifactKind, UIArtifact } from './artifact';
import { FileIcon, FullscreenIcon, ImageIcon, LoaderIcon } from './icons';
import { cn, fetcher } from '@/lib/utils';
import type { Document } from '@/lib/db/schema';
import { InlineDocumentSkeleton } from './document-skeleton';
import useSWR from 'swr';
import { Editor } from './text-editor';
import { DocumentToolCall, DocumentToolResult } from './document';
import { CodeEditor } from './code-editor';
import { useArtifact } from '@/hooks/use-artifact';
import equal from 'fast-deep-equal';
import { SpreadsheetEditor } from './sheet-editor';
import { ImageEditor } from './image-editor';

interface DocumentPreviewProps {
  isReadonly: boolean;
  result?: any;
  args?: any;
}

export function DocumentPreview({
  isReadonly,
  result,
  args,
}: DocumentPreviewProps) {
  const { artifact, setArtifact } = useArtifact();

  const { data: documents, isLoading: isDocumentsFetching } = useSWR<
    Array<Document>
  >(result ? `/api/document?id=${result.id}` : null, fetcher);

  const previewDocument = useMemo(() => documents?.[0], [documents]);
  const hitboxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const boundingBox = hitboxRef.current?.getBoundingClientRect();

    if (artifact.documentId && boundingBox) {
      setArtifact((artifact) => ({
        ...artifact,
        boundingBox: {
          left: boundingBox.x,
          top: boundingBox.y,
          width: boundingBox.width,
          height: boundingBox.height,
        },
      }));
    }
  }, [artifact.documentId, setArtifact]);

  if (artifact.isVisible) {
    if (result) {
      return (
        <DocumentToolResult
          type="create"
          result={{ id: result.id, title: result.title, kind: result.kind }}
          isReadonly={isReadonly}
        />
      );
    }

    if (args) {
      return (
        <DocumentToolCall
          type="create"
          args={{ title: args.title, kind: args.kind }}
          isReadonly={isReadonly}
        />
      );
    }
  }

  if (isDocumentsFetching) {
    return <LoadingSkeleton artifactKind={result.kind ?? args.kind} />;
  }

  const document: Document | null = previewDocument
    ? previewDocument
    : artifact.status === 'streaming'
      ? {
          title: artifact.title,
          kind: artifact.kind,
          content: artifact.content,
          id: artifact.documentId,
          createdAt: new Date(),
          userId: 'noop',
        }
      : null;

  if (!document) return <LoadingSkeleton artifactKind={artifact.kind} />;

  return (
    <div className="relative w-full cursor-pointer">
      <HitboxLayer
        hitboxRef={hitboxRef}
        result={result}
        setArtifact={setArtifact}
      />
      <DocumentHeader
        title={document.title}
        kind={document.kind}
        isStreaming={artifact.status === 'streaming'}
      />
      <DocumentContent document={document} />
    </div>
  );
}

const LoadingSkeleton = ({ artifactKind }: { artifactKind: ArtifactKind }) => (
  <div className="w-full">
    <div className="p-4 border rounded-t-2xl flex flex-row gap-2 items-center justify-between dark:bg-muted h-[57px] dark:border-zinc-700 border-b-0">
      <div className="flex flex-row items-center gap-3">
        <div className="text-muted-foreground">
          <div className="animate-pulse rounded-md size-4 bg-muted-foreground/20" />
        </div>
        <div className="animate-pulse rounded-lg h-4 bg-muted-foreground/20 w-24" />
      </div>
      <div>
        <FullscreenIcon />
      </div>
    </div>
    {artifactKind === 'image' ? (
      <div className="overflow-y-scroll border rounded-b-2xl bg-muted border-t-0 dark:border-zinc-700">
        <div className="animate-pulse h-[257px] bg-muted-foreground/20 w-full" />
      </div>
    ) : (
      <div className="overflow-y-scroll border rounded-b-2xl p-8 pt-4 bg-muted border-t-0 dark:border-zinc-700">
        <InlineDocumentSkeleton />
      </div>
    )}
  </div>
);

const PureHitboxLayer = ({
  hitboxRef,
  result,
  setArtifact,
}: {
  hitboxRef: React.RefObject<HTMLDivElement>;
  result: any;
  setArtifact: (
    updaterFn: UIArtifact | ((currentArtifact: UIArtifact) => UIArtifact),
  ) => void;
}) => {
  const handleClick = useCallback(
    (event: MouseEvent<HTMLElement>) => {
      const boundingBox = event.currentTarget.getBoundingClientRect();

      setArtifact((artifact) =>
        artifact.status === 'streaming'
          ? { ...artifact, isVisible: true }
          : {
              ...artifact,
              title: result.title,
              documentId: result.id,
              kind: result.kind,
              isVisible: true,
              boundingBox: {
                left: boundingBox.x,
                top: boundingBox.y,
                width: boundingBox.width,
                height: boundingBox.height,
              },
            },
      );
    },
    [setArtifact, result],
  );

  return (
    <div
      className="size-full absolute top-0 left-0 rounded-xl z-10"
      ref={hitboxRef}
      onClick={handleClick}
      role="presentation"
      aria-hidden="true"
    >
      <div className="w-full p-4 flex justify-end items-center">
        <div className="absolute right-[9px] top-[13px] p-2 hover:dark:bg-zinc-700 rounded-md hover:bg-zinc-100">
          <FullscreenIcon />
        </div>
      </div>
    </div>
  );
};

const HitboxLayer = memo(PureHitboxLayer, (prevProps, nextProps) => {
  if (!equal(prevProps.result, nextProps.result)) return false;
  return true;
});

const PureDocumentHeader = ({
  title,
  kind,
  isStreaming,
}: {
  title: string;
  kind: ArtifactKind;
  isStreaming: boolean;
}) => (
  <div className="p-4 border rounded-t-2xl flex flex-row gap-2 items-start sm:items-center justify-between dark:bg-muted border-b-0 dark:border-zinc-700">
    <div className="flex flex-row items-start sm:items-center gap-3">
      <div className="text-muted-foreground">
        {isStreaming ? (
          <div className="animate-spin">
            <LoaderIcon />
          </div>
        ) : kind === 'image' ? (
          <ImageIcon />
        ) : (
          <FileIcon />
        )}
      </div>
      <div className="-translate-y-1 sm:translate-y-0 font-medium">{title}</div>
    </div>
    <div className="w-8" />
  </div>
);

const DocumentHeader = memo(PureDocumentHeader, (prevProps, nextProps) => {
  if (prevProps.title !== nextProps.title) return false;
  if (prevProps.isStreaming !== nextProps.isStreaming) return false;

  return true;
});

const DocumentContent = ({ document }: { document: Document }) => {
  const { artifact } = useArtifact();

  const containerClassName = cn(
    'h-[257px] overflow-y-scroll border rounded-b-2xl dark:bg-muted border-t-0 dark:border-zinc-700',
    {
      'p-4 sm:px-14 sm:py-16': document.kind === 'text',
      'p-0': document.kind === 'code',
    },
  );

  const commonProps = {
    content: document.content ?? '',
    isCurrentVersion: true,
    currentVersionIndex: 0,
    status: artifact.status,
    saveContent: () => {},
    suggestions: [],
  };

  return (
    <div className={containerClassName}>
      {document.kind === 'text' ? (
        <Editor {...commonProps} onSaveContent={() => {}} />
      ) : document.kind === 'code' ? (
        <div className="flex flex-1 relative w-full">
          <div className="absolute inset-0">
            <CodeEditor {...commonProps} onSaveContent={() => {}} />
          </div>
        </div>
      ) : document.kind === 'sheet' ? (
        <div className="flex flex-1 relative size-full p-4">
          <div className="absolute inset-0">
            <SpreadsheetEditor {...commonProps} />
          </div>
        </div>
      ) : document.kind === 'image' ? (
        <ImageEditor
          title={document.title}
          content={document.content ?? ''}
          isCurrentVersion={true}
          currentVersionIndex={0}
          status={artifact.status}
          isInline={true}
        />
      ) : null}
    </div>
  );
};



================================================
FILE: components/document-skeleton.tsx
================================================
'use client';

import type { ArtifactKind } from './artifact';

export const DocumentSkeleton = ({
  artifactKind,
}: {
  artifactKind: ArtifactKind;
}) => {
  return artifactKind === 'image' ? (
    <div className="flex flex-col gap-4 w-full justify-center items-center h-[calc(100dvh-60px)]">
      <div className="animate-pulse rounded-lg bg-muted-foreground/20 size-96" />
    </div>
  ) : (
    <div className="flex flex-col gap-4 w-full">
      <div className="animate-pulse rounded-lg h-12 bg-muted-foreground/20 w-1/2" />
      <div className="animate-pulse rounded-lg h-5 bg-muted-foreground/20 w-full" />
      <div className="animate-pulse rounded-lg h-5 bg-muted-foreground/20 w-full" />
      <div className="animate-pulse rounded-lg h-5 bg-muted-foreground/20 w-1/3" />
      <div className="animate-pulse rounded-lg h-5 bg-transparent w-52" />
      <div className="animate-pulse rounded-lg h-8 bg-muted-foreground/20 w-52" />
      <div className="animate-pulse rounded-lg h-5 bg-muted-foreground/20 w-2/3" />
    </div>
  );
};

export const InlineDocumentSkeleton = () => {
  return (
    <div className="flex flex-col gap-4 w-full">
      <div className="animate-pulse rounded-lg h-4 bg-muted-foreground/20 w-48" />
      <div className="animate-pulse rounded-lg h-4 bg-muted-foreground/20 w-3/4" />
      <div className="animate-pulse rounded-lg h-4 bg-muted-foreground/20 w-1/2" />
      <div className="animate-pulse rounded-lg h-4 bg-muted-foreground/20 w-64" />
      <div className="animate-pulse rounded-lg h-4 bg-muted-foreground/20 w-40" />
      <div className="animate-pulse rounded-lg h-4 bg-muted-foreground/20 w-36" />
      <div className="animate-pulse rounded-lg h-4 bg-muted-foreground/20 w-64" />
    </div>
  );
};



================================================
FILE: components/document.tsx
================================================
import { memo } from 'react';

import type { ArtifactKind } from './artifact';
import { FileIcon, LoaderIcon, MessageIcon, PencilEditIcon } from './icons';
import { toast } from 'sonner';
import { useArtifact } from '@/hooks/use-artifact';

const getActionText = (
  type: 'create' | 'update' | 'request-suggestions',
  tense: 'present' | 'past',
) => {
  switch (type) {
    case 'create':
      return tense === 'present' ? 'Creating' : 'Created';
    case 'update':
      return tense === 'present' ? 'Updating' : 'Updated';
    case 'request-suggestions':
      return tense === 'present'
        ? 'Adding suggestions'
        : 'Added suggestions to';
    default:
      return null;
  }
};

interface DocumentToolResultProps {
  type: 'create' | 'update' | 'request-suggestions';
  result: { id: string; title: string; kind: ArtifactKind };
  isReadonly: boolean;
}

function PureDocumentToolResult({
  type,
  result,
  isReadonly,
}: DocumentToolResultProps) {
  const { setArtifact } = useArtifact();

  return (
    <button
      type="button"
      className="bg-background cursor-pointer border py-2 px-3 rounded-xl w-fit flex flex-row gap-3 items-start"
      onClick={(event) => {
        if (isReadonly) {
          toast.error(
            'Viewing files in shared chats is currently not supported.',
          );
          return;
        }

        const rect = event.currentTarget.getBoundingClientRect();

        const boundingBox = {
          top: rect.top,
          left: rect.left,
          width: rect.width,
          height: rect.height,
        };

        setArtifact({
          documentId: result.id,
          kind: result.kind,
          content: '',
          title: result.title,
          isVisible: true,
          status: 'idle',
          boundingBox,
        });
      }}
    >
      <div className="text-muted-foreground mt-1">
        {type === 'create' ? (
          <FileIcon />
        ) : type === 'update' ? (
          <PencilEditIcon />
        ) : type === 'request-suggestions' ? (
          <MessageIcon />
        ) : null}
      </div>
      <div className="text-left">
        {`${getActionText(type, 'past')} "${result.title}"`}
      </div>
    </button>
  );
}

export const DocumentToolResult = memo(PureDocumentToolResult, () => true);

interface DocumentToolCallProps {
  type: 'create' | 'update' | 'request-suggestions';
  args:
    | { title: string; kind: ArtifactKind } // for create
    | { id: string; description: string } // for update
    | { documentId: string }; // for request-suggestions
  isReadonly: boolean;
}

function PureDocumentToolCall({
  type,
  args,
  isReadonly,
}: DocumentToolCallProps) {
  const { setArtifact } = useArtifact();

  return (
    <button
      type="button"
      className="cursor pointer w-fit border py-2 px-3 rounded-xl flex flex-row items-start justify-between gap-3"
      onClick={(event) => {
        if (isReadonly) {
          toast.error(
            'Viewing files in shared chats is currently not supported.',
          );
          return;
        }

        const rect = event.currentTarget.getBoundingClientRect();

        const boundingBox = {
          top: rect.top,
          left: rect.left,
          width: rect.width,
          height: rect.height,
        };

        setArtifact((currentArtifact) => ({
          ...currentArtifact,
          isVisible: true,
          boundingBox,
        }));
      }}
    >
      <div className="flex flex-row gap-3 items-start">
        <div className="text-zinc-500 mt-1">
          {type === 'create' ? (
            <FileIcon />
          ) : type === 'update' ? (
            <PencilEditIcon />
          ) : type === 'request-suggestions' ? (
            <MessageIcon />
          ) : null}
        </div>

        <div className="text-left">
          {`${getActionText(type, 'present')} ${
            type === 'create' && 'title' in args && args.title
              ? `"${args.title}"`
              : type === 'update' && 'description' in args
                ? `"${args.description}"`
                : type === 'request-suggestions'
                  ? 'for document'
                  : ''
          }`}
        </div>
      </div>

      <div className="animate-spin mt-1">{<LoaderIcon />}</div>
    </button>
  );
}

export const DocumentToolCall = memo(PureDocumentToolCall, () => true);



================================================
FILE: components/greeting.tsx
================================================
import { motion } from 'framer-motion';

export const Greeting = () => {
  return (
    <div
      key="overview"
      className="max-w-3xl mx-auto md:mt-20 px-8 size-full flex flex-col justify-center"
    >
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 10 }}
        transition={{ delay: 0.5 }}
        className="text-2xl font-semibold"
      >
        Hello there!
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 10 }}
        transition={{ delay: 0.6 }}
        className="text-2xl text-zinc-500"
      >
        How can I help you today?
      </motion.div>
    </div>
  );
};



================================================
FILE: components/image-editor.tsx
================================================
import { LoaderIcon } from './icons';
import cn from 'classnames';

interface ImageEditorProps {
  title: string;
  content: string;
  isCurrentVersion: boolean;
  currentVersionIndex: number;
  status: string;
  isInline: boolean;
}

export function ImageEditor({
  title,
  content,
  status,
  isInline,
}: ImageEditorProps) {
  return (
    <div
      className={cn('flex flex-row items-center justify-center w-full', {
        'h-[calc(100dvh-60px)]': !isInline,
        'h-[200px]': isInline,
      })}
    >
      {status === 'streaming' ? (
        <div className="flex flex-row gap-4 items-center">
          {!isInline && (
            <div className="animate-spin">
              <LoaderIcon />
            </div>
          )}
          <div>Generating Image...</div>
        </div>
      ) : (
        <picture>
          <img
            className={cn('w-full h-fit max-w-[800px]', {
              'p-0 md:p-20': !isInline,
            })}
            src={`data:image/png;base64,${content}`}
            alt={title}
          />
        </picture>
      )}
    </div>
  );
}



================================================
FILE: components/message-actions.tsx
================================================
import { useSWRConfig } from 'swr';
import { useCopyToClipboard } from 'usehooks-ts';

import type { Vote } from '@/lib/db/schema';

import { CopyIcon, ThumbDownIcon, ThumbUpIcon } from './icons';
import { Actions, Action } from './elements/actions';
import { memo } from 'react';
import equal from 'fast-deep-equal';
import { toast } from 'sonner';
import type { ChatMessage } from '@/lib/types';

export function PureMessageActions({
  chatId,
  message,
  vote,
  isLoading,
}: {
  chatId: string;
  message: ChatMessage;
  vote: Vote | undefined;
  isLoading: boolean;
}) {
  const { mutate } = useSWRConfig();
  const [_, copyToClipboard] = useCopyToClipboard();

  if (isLoading) return null;
  if (message.role === 'user') return null;

  return (
    <Actions>
        <Action
          tooltip="Copy"
          onClick={async () => {
            const textFromParts = message.parts
              ?.filter((part) => part.type === 'text')
              .map((part) => part.text)
              .join('\n')
              .trim();

            if (!textFromParts) {
              toast.error("There's no text to copy!");
              return;
            }

            await copyToClipboard(textFromParts);
            toast.success('Copied to clipboard!');
          }}
        >
          <CopyIcon />
        </Action>

        <Action
          tooltip="Upvote Response"
          data-testid="message-upvote"
          disabled={vote?.isUpvoted}
              onClick={async () => {
                const upvote = fetch('/api/vote', {
                  method: 'PATCH',
                  body: JSON.stringify({
                    chatId,
                    messageId: message.id,
                    type: 'up',
                  }),
                });

                toast.promise(upvote, {
                  loading: 'Upvoting Response...',
                  success: () => {
                    mutate<Array<Vote>>(
                      `/api/vote?chatId=${chatId}`,
                      (currentVotes) => {
                        if (!currentVotes) return [];

                        const votesWithoutCurrent = currentVotes.filter(
                          (vote) => vote.messageId !== message.id,
                        );

                        return [
                          ...votesWithoutCurrent,
                          {
                            chatId,
                            messageId: message.id,
                            isUpvoted: true,
                          },
                        ];
                      },
                      { revalidate: false },
                    );

                    return 'Upvoted Response!';
                  },
                  error: 'Failed to upvote response.',
                });
              }}
        >
          <ThumbUpIcon />
        </Action>

        <Action
          tooltip="Downvote Response"
          data-testid="message-downvote"
          disabled={vote && !vote.isUpvoted}
              onClick={async () => {
                const downvote = fetch('/api/vote', {
                  method: 'PATCH',
                  body: JSON.stringify({
                    chatId,
                    messageId: message.id,
                    type: 'down',
                  }),
                });

                toast.promise(downvote, {
                  loading: 'Downvoting Response...',
                  success: () => {
                    mutate<Array<Vote>>(
                      `/api/vote?chatId=${chatId}`,
                      (currentVotes) => {
                        if (!currentVotes) return [];

                        const votesWithoutCurrent = currentVotes.filter(
                          (vote) => vote.messageId !== message.id,
                        );

                        return [
                          ...votesWithoutCurrent,
                          {
                            chatId,
                            messageId: message.id,
                            isUpvoted: false,
                          },
                        ];
                      },
                      { revalidate: false },
                    );

                    return 'Downvoted Response!';
                  },
                  error: 'Failed to downvote response.',
                });
              }}
        >
          <ThumbDownIcon />
        </Action>
    </Actions>
  );
}

export const MessageActions = memo(
  PureMessageActions,
  (prevProps, nextProps) => {
    if (!equal(prevProps.vote, nextProps.vote)) return false;
    if (prevProps.isLoading !== nextProps.isLoading) return false;

    return true;
  },
);



================================================
FILE: components/message-editor.tsx
================================================
'use client';

import { Button } from './ui/button';
import {
  type Dispatch,
  type SetStateAction,
  useEffect,
  useRef,
  useState,
} from 'react';
import { Textarea } from './ui/textarea';
import { deleteTrailingMessages } from '@/app/(chat)/actions';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { ChatMessage } from '@/lib/types';
import { getTextFromMessage } from '@/lib/utils';

export type MessageEditorProps = {
  message: ChatMessage;
  setMode: Dispatch<SetStateAction<'view' | 'edit'>>;
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
  regenerate: UseChatHelpers<ChatMessage>['regenerate'];
};

export function MessageEditor({
  message,
  setMode,
  setMessages,
  regenerate,
}: MessageEditorProps) {
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const [draftContent, setDraftContent] = useState<string>(
    getTextFromMessage(message),
  );
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      adjustHeight();
    }
  }, []);

  const adjustHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight + 2}px`;
    }
  };

  const handleInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setDraftContent(event.target.value);
    adjustHeight();
  };

  return (
    <div className="flex flex-col gap-2 w-full">
      <Textarea
        data-testid="message-editor"
        ref={textareaRef}
        className="bg-transparent outline-none overflow-hidden resize-none !text-base rounded-xl w-full"
        value={draftContent}
        onChange={handleInput}
      />

      <div className="flex flex-row gap-2 justify-end">
        <Button
          variant="outline"
          className="h-fit py-2 px-3"
          onClick={() => {
            setMode('view');
          }}
        >
          Cancel
        </Button>
        <Button
          data-testid="message-editor-send-button"
          variant="default"
          className="h-fit py-2 px-3"
          disabled={isSubmitting}
          onClick={async () => {
            setIsSubmitting(true);

            await deleteTrailingMessages({
              id: message.id,
            });

            setMessages((messages) => {
              const index = messages.findIndex((m) => m.id === message.id);

              if (index !== -1) {
                const updatedMessage: ChatMessage = {
                  ...message,
                  parts: [{ type: 'text', text: draftContent }],
                };

                return [...messages.slice(0, index), updatedMessage];
              }

              return messages;
            });

            setMode('view');
            regenerate();
          }}
        >
          {isSubmitting ? 'Sending...' : 'Send'}
        </Button>
      </div>
    </div>
  );
}



================================================
FILE: components/message-reasoning.tsx
================================================
'use client';

import { Reasoning, ReasoningTrigger, ReasoningContent } from './elements/reasoning';

interface MessageReasoningProps {
  isLoading: boolean;
  reasoning: string;
}

export function MessageReasoning({
  isLoading,
  reasoning,
}: MessageReasoningProps) {
  return (
    <Reasoning 
      isStreaming={isLoading} 
      defaultOpen={true}
      data-testid="message-reasoning"
    >
      <ReasoningTrigger />
      <ReasoningContent>{reasoning}</ReasoningContent>
    </Reasoning>
  );
}



================================================
FILE: components/message.tsx
================================================
'use client';
import cx from 'classnames';
import { AnimatePresence, motion } from 'framer-motion';
import { memo, useState } from 'react';
import type { Vote } from '@/lib/db/schema';
import { DocumentToolResult } from './document';
import { PencilEditIcon, SparklesIcon, LoaderIcon } from './icons';
import { Response } from './elements/response';
import { MessageContent } from './elements/message';
import {
  Tool,
  ToolHeader,
  ToolContent,
  ToolInput,
  ToolOutput,
} from './elements/tool';
import { MessageActions } from './message-actions';
import { PreviewAttachment } from './preview-attachment';
import { Weather } from './weather';
import equal from 'fast-deep-equal';
import { cn, sanitizeText } from '@/lib/utils';
import { Button } from './ui/button';
import { Tooltip, TooltipContent, TooltipTrigger } from './ui/tooltip';
import { MessageEditor } from './message-editor';
import { DocumentPreview } from './document-preview';
import { MessageReasoning } from './message-reasoning';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { ChatMessage } from '@/lib/types';
import { useDataStream } from './data-stream-provider';

// Type narrowing is handled by TypeScript's control flow analysis
// The AI SDK provides proper discriminated unions for tool calls

const PurePreviewMessage = ({
  chatId,
  message,
  vote,
  isLoading,
  setMessages,
  regenerate,
  isReadonly,
  requiresScrollPadding,
  isArtifactVisible,
}: {
  chatId: string;
  message: ChatMessage;
  vote: Vote | undefined;
  isLoading: boolean;
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
  regenerate: UseChatHelpers<ChatMessage>['regenerate'];
  isReadonly: boolean;
  requiresScrollPadding: boolean;
  isArtifactVisible: boolean;
}) => {
  const [mode, setMode] = useState<'view' | 'edit'>('view');

  const attachmentsFromMessage = message.parts.filter(
    (part) => part.type === 'file',
  );

  useDataStream();

  return (
    <AnimatePresence>
      <motion.div
        data-testid={`message-${message.role}`}
        className="w-full group/message"
        initial={{ y: 5, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        data-role={message.role}
      >
        <div
          className={cn('flex items-start gap-3', {
            'w-full': mode === 'edit',
            'max-w-xl ml-auto justify-end mr-6':
              message.role === 'user' && mode !== 'edit',
            'justify-start -ml-3': message.role === 'assistant',
          })}
        >
          {message.role === 'assistant' && (
            <div className="flex justify-center items-center mt-1 rounded-full ring-1 size-8 shrink-0 ring-border bg-background">
              <SparklesIcon size={14} />
            </div>
          )}

          <div
            className={cn('flex flex-col gap-4', {
              'min-h-96': message.role === 'assistant' && requiresScrollPadding,
              'w-full': message.role === 'assistant',
              'w-fit': message.role === 'user',
            })}
          >
            {attachmentsFromMessage.length > 0 && (
              <div
                data-testid={`message-attachments`}
                className="flex flex-row gap-2 justify-end"
              >
                {attachmentsFromMessage.map((attachment) => (
                  <PreviewAttachment
                    key={attachment.url}
                    attachment={{
                      name: attachment.filename ?? 'file',
                      contentType: attachment.mediaType,
                      url: attachment.url,
                    }}
                  />
                ))}
              </div>
            )}

            {message.parts?.map((part, index) => {
              const { type } = part;
              const key = `message-${message.id}-part-${index}`;

              if (type === 'reasoning' && part.text?.trim().length > 0) {
                return (
                  <MessageReasoning
                    key={key}
                    isLoading={isLoading}
                    reasoning={part.text}
                  />
                );
              }

              if (type === 'text') {
                if (mode === 'view') {
                  return (
                    <div key={key} className="flex flex-row gap-2 items-start">
                      {message.role === 'user' && !isReadonly && (
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              data-testid="message-edit-button"
                              variant="ghost"
                              className="px-2 rounded-full opacity-0 h-fit text-muted-foreground group-hover/message:opacity-100"
                              onClick={() => {
                                setMode('edit');
                              }}
                            >
                              <PencilEditIcon />
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>Edit message</TooltipContent>
                        </Tooltip>
                      )}

                      <MessageContent
                        data-testid="message-content"
                        className={cn('justify-start items-start text-left', {
                          'bg-primary text-primary-foreground':
                            message.role === 'user',
                          'bg-transparent -ml-4': message.role === 'assistant',
                        })}
                      >
                        <Response>{sanitizeText(part.text)}</Response>
                      </MessageContent>
                    </div>
                  );
                }

                if (mode === 'edit') {
                  return (
                    <div
                      key={key}
                      className="flex flex-row gap-3 items-start w-full"
                    >
                      <div className="size-8" />
                      <div className="flex-1 min-w-0">
                        <MessageEditor
                          key={message.id}
                          message={message}
                          setMode={setMode}
                          setMessages={setMessages}
                          regenerate={regenerate}
                        />
                      </div>
                    </div>
                  );
                }
              }

              if (type === 'tool-getWeather') {
                const { toolCallId, state } = part;

                return (
                  <Tool key={toolCallId} defaultOpen={true}>
                    <ToolHeader type="tool-getWeather" state={state} />
                    <ToolContent>
                      {state === 'input-available' && (
                        <ToolInput input={part.input} />
                      )}
                      {state === 'output-available' && (
                        <ToolOutput
                          output={<Weather weatherAtLocation={part.output} />}
                          errorText={undefined}
                        />
                      )}
                    </ToolContent>
                  </Tool>
                );
              }

              if (type === 'tool-createDocument') {
                const { toolCallId } = part;

                if (part.output && 'error' in part.output) {
                  return (
                    <div
                      key={toolCallId}
                      className="p-4 text-red-500 bg-red-50 rounded-lg border border-red-200 dark:bg-red-950/50"
                    >
                      Error creating document: {String(part.output.error)}
                    </div>
                  );
                }

                return (
                  <DocumentPreview
                    key={toolCallId}
                    isReadonly={isReadonly}
                    result={part.output}
                  />
                );
              }

              if (type === 'tool-updateDocument') {
                const { toolCallId } = part;

                if (part.output && 'error' in part.output) {
                  return (
                    <div
                      key={toolCallId}
                      className="p-4 text-red-500 bg-red-50 rounded-lg border border-red-200 dark:bg-red-950/50"
                    >
                      Error updating document: {String(part.output.error)}
                    </div>
                  );
                }

                return (
                  <div key={toolCallId} className="relative">
                    <DocumentPreview
                      isReadonly={isReadonly}
                      result={part.output}
                      args={{ ...part.output, isUpdate: true }}
                    />
                  </div>
                );
              }

              if (type === 'tool-requestSuggestions') {
                const { toolCallId, state } = part;

                return (
                  <Tool key={toolCallId} defaultOpen={true}>
                    <ToolHeader type="tool-requestSuggestions" state={state} />
                    <ToolContent>
                      {state === 'input-available' && (
                        <ToolInput input={part.input} />
                      )}
                      {state === 'output-available' && (
                        <ToolOutput
                          output={
                            'error' in part.output ? (
                              <div className="p-2 text-red-500 rounded border">
                                Error: {String(part.output.error)}
                              </div>
                            ) : (
                              <DocumentToolResult
                                type="request-suggestions"
                                result={part.output}
                                isReadonly={isReadonly}
                              />
                            )
                          }
                          errorText={undefined}
                        />
                      )}
                    </ToolContent>
                  </Tool>
                );
              }
            })}

            {!isReadonly && (
              <MessageActions
                key={`action-${message.id}`}
                chatId={chatId}
                message={message}
                vote={vote}
                isLoading={isLoading}
              />
            )}
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

export const PreviewMessage = memo(
  PurePreviewMessage,
  (prevProps, nextProps) => {
    if (prevProps.isLoading !== nextProps.isLoading) return false;
    if (prevProps.message.id !== nextProps.message.id) return false;
    if (prevProps.requiresScrollPadding !== nextProps.requiresScrollPadding)
      return false;
    if (!equal(prevProps.message.parts, nextProps.message.parts)) return false;
    if (!equal(prevProps.vote, nextProps.vote)) return false;

    return false;
  },
);

export const ThinkingMessage = () => {
  const role = 'assistant';

  return (
    <motion.div
      data-testid="message-assistant-loading"
      className="w-full group/message"
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1, transition: { delay: 1 } }}
      data-role={role}
    >
      <div className="flex items-start gap-3 justify-start -ml-3">
        <div className="flex justify-center items-center mt-1 rounded-full ring-1 size-8 shrink-0 ring-border bg-background">
          <SparklesIcon size={14} />
        </div>

        <div className="flex flex-col gap-4 w-full">
          <MessageContent className="bg-transparent -ml-4">
            <div className="text-muted-foreground">Hmm...</div>
          </MessageContent>
        </div>
      </div>
    </motion.div>
  );
};



================================================
FILE: components/messages.tsx
================================================
import { PreviewMessage, ThinkingMessage } from './message';
import { Greeting } from './greeting';
import { memo } from 'react';
import type { Vote } from '@/lib/db/schema';
import equal from 'fast-deep-equal';
import type { UseChatHelpers } from '@ai-sdk/react';
import { motion } from 'framer-motion';
import { useMessages } from '@/hooks/use-messages';
import type { ChatMessage } from '@/lib/types';
import { useDataStream } from './data-stream-provider';
import { Conversation, ConversationContent, ConversationScrollButton } from './elements/conversation';
import { cn } from '@/lib/utils';

interface MessagesProps {
  chatId: string;
  status: UseChatHelpers<ChatMessage>['status'];
  votes: Array<Vote> | undefined;
  messages: ChatMessage[];
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
  regenerate: UseChatHelpers<ChatMessage>['regenerate'];
  isReadonly: boolean;
  isArtifactVisible: boolean;
}

function PureMessages({
  chatId,
  status,
  votes,
  messages,
  setMessages,
  regenerate,
  isReadonly,
  isArtifactVisible,
}: MessagesProps) {
  const {
    containerRef: messagesContainerRef,
    endRef: messagesEndRef,
    onViewportEnter,
    onViewportLeave,
    hasSentMessage,
  } = useMessages({
    chatId,
    status,
  });

  useDataStream();

  return (
    <div ref={messagesContainerRef} className="flex-1 overflow-y-auto">
      <Conversation className="flex flex-col min-w-0 gap-6 pt-4 pb-32 px-4 max-w-4xl mx-auto">
        <ConversationContent className="flex flex-col gap-6">
          {messages.length === 0 && <Greeting />}

          {messages.map((message, index) => (
            <PreviewMessage
              key={message.id}
              chatId={chatId}
              message={message}
              isLoading={status === 'streaming' && messages.length - 1 === index}
              vote={
                votes
                  ? votes.find((vote) => vote.messageId === message.id)
                  : undefined
              }
              setMessages={setMessages}
              regenerate={regenerate}
              isReadonly={isReadonly}
              requiresScrollPadding={
                hasSentMessage && index === messages.length - 1
              }
              isArtifactVisible={isArtifactVisible}
            />
          ))}

          {status === 'submitted' &&
            messages.length > 0 &&
            messages[messages.length - 1].role === 'user' && <ThinkingMessage />}

          <motion.div
            ref={messagesEndRef}
            className="shrink-0 min-w-[24px] min-h-[24px]"
            onViewportLeave={onViewportLeave}
            onViewportEnter={onViewportEnter}
          />
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>
    </div>
  );
}

export const Messages = memo(PureMessages, (prevProps, nextProps) => {
  if (prevProps.isArtifactVisible && nextProps.isArtifactVisible) return true;

  if (prevProps.status !== nextProps.status) return false;
  if (prevProps.messages.length !== nextProps.messages.length) return false;
  if (!equal(prevProps.messages, nextProps.messages)) return false;
  if (!equal(prevProps.votes, nextProps.votes)) return false;

  return false;
});



================================================
FILE: components/model-selector.tsx
================================================
'use client';

import { startTransition, useMemo, useOptimistic, useState } from 'react';

import { saveChatModelAsCookie } from '@/app/(chat)/actions';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { chatModels } from '@/lib/ai/models';
import { cn } from '@/lib/utils';

import { CheckCircleFillIcon, ChevronDownIcon } from './icons';
import { entitlementsByUserType } from '@/lib/ai/entitlements';
import type { Session } from 'next-auth';

export function ModelSelector({
  session,
  selectedModelId,
  className,
}: {
  session: Session;
  selectedModelId: string;
} & React.ComponentProps<typeof Button>) {
  const [open, setOpen] = useState(false);
  const [optimisticModelId, setOptimisticModelId] =
    useOptimistic(selectedModelId);

  const userType = session.user.type;
  const { availableChatModelIds } = entitlementsByUserType[userType];

  const availableChatModels = chatModels.filter((chatModel) =>
    availableChatModelIds.includes(chatModel.id),
  );

  const selectedChatModel = useMemo(
    () =>
      availableChatModels.find(
        (chatModel) => chatModel.id === optimisticModelId,
      ),
    [optimisticModelId, availableChatModels],
  );

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger
        asChild
        className={cn(
          'w-fit data-[state=open]:bg-accent data-[state=open]:text-accent-foreground',
          className,
        )}
      >
        <Button
          data-testid="model-selector"
          variant="outline"
          className="md:px-2 md:h-[34px]"
        >
          {selectedChatModel?.name}
          <ChevronDownIcon />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start" className="min-w-[300px]">
        {availableChatModels.map((chatModel) => {
          const { id } = chatModel;

          return (
            <DropdownMenuItem
              data-testid={`model-selector-item-${id}`}
              key={id}
              onSelect={() => {
                setOpen(false);

                startTransition(() => {
                  setOptimisticModelId(id);
                  saveChatModelAsCookie(id);
                });
              }}
              data-active={id === optimisticModelId}
              asChild
            >
              <button
                type="button"
                className="gap-4 group/item flex flex-row justify-between items-center w-full"
              >
                <div className="flex flex-col gap-1 items-start">
                  <div>{chatModel.name}</div>
                  <div className="text-xs text-muted-foreground">
                    {chatModel.description}
                  </div>
                </div>

                <div className="text-foreground dark:text-foreground opacity-0 group-data-[active=true]/item:opacity-100">
                  <CheckCircleFillIcon />
                </div>
              </button>
            </DropdownMenuItem>
          );
        })}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}



================================================
FILE: components/multimodal-input.tsx
================================================
'use client';

import type { UIMessage } from 'ai';
import {
  useRef,
  useEffect,
  useState,
  useCallback,
  type Dispatch,
  type SetStateAction,
  type ChangeEvent,
  memo,
} from 'react';
import { toast } from 'sonner';
import { useLocalStorage, useWindowSize } from 'usehooks-ts';

import { ArrowUpIcon, PaperclipIcon, StopIcon } from './icons';
import { PreviewAttachment } from './preview-attachment';
import { Button } from './ui/button';
import { SuggestedActions } from './suggested-actions';
import {
  PromptInput,
  PromptInputTextarea,
  PromptInputToolbar,
  PromptInputTools,
  PromptInputSubmit,
  PromptInputModelSelect,
  PromptInputModelSelectTrigger,
  PromptInputModelSelectContent,
} from './elements/prompt-input';
import { SelectItem, SelectValue } from '@/components/ui/select';
import equal from 'fast-deep-equal';
import type { UseChatHelpers } from '@ai-sdk/react';
import { AnimatePresence, motion } from 'framer-motion';
import { ArrowDown } from 'lucide-react';
import { useScrollToBottom } from '@/hooks/use-scroll-to-bottom';
import type { VisibilityType } from './visibility-selector';
import type { Attachment, ChatMessage } from '@/lib/types';
import { chatModels } from '@/lib/ai/models';
import { saveChatModelAsCookie } from '@/app/(chat)/actions';
import { startTransition } from 'react';

function PureMultimodalInput({
  chatId,
  input,
  setInput,
  status,
  stop,
  attachments,
  setAttachments,
  messages,
  setMessages,
  sendMessage,
  className,
  selectedVisibilityType,
  selectedModelId,
}: {
  chatId: string;
  input: string;
  setInput: Dispatch<SetStateAction<string>>;
  status: UseChatHelpers<ChatMessage>['status'];
  stop: () => void;
  attachments: Array<Attachment>;
  setAttachments: Dispatch<SetStateAction<Array<Attachment>>>;
  messages: Array<UIMessage>;
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
  sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
  className?: string;
  selectedVisibilityType: VisibilityType;
  selectedModelId: string;
}) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { width } = useWindowSize();

  useEffect(() => {
    if (textareaRef.current) {
      adjustHeight();
    }
  }, []);

  const adjustHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = '72px';
    }
  };

  const resetHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = '72px';
    }
  };

  const [localStorageInput, setLocalStorageInput] = useLocalStorage(
    'input',
    '',
  );

  useEffect(() => {
    if (textareaRef.current) {
      const domValue = textareaRef.current.value;
      // Prefer DOM value over localStorage to handle hydration
      const finalValue = domValue || localStorageInput || '';
      setInput(finalValue);
      adjustHeight();
    }
    // Only run once after hydration
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    setLocalStorageInput(input);
  }, [input, setLocalStorageInput]);

  const handleInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(event.target.value);
  };

  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploadQueue, setUploadQueue] = useState<Array<string>>([]);

  const submitForm = useCallback(() => {
    window.history.replaceState({}, '', `/chat/${chatId}`);

    sendMessage({
      role: 'user',
      parts: [
        ...attachments.map((attachment) => ({
          type: 'file' as const,
          url: attachment.url,
          name: attachment.name,
          mediaType: attachment.contentType,
        })),
        {
          type: 'text',
          text: input,
        },
      ],
    });

    setAttachments([]);
    setLocalStorageInput('');
    resetHeight();
    setInput('');

    if (width && width > 768) {
      textareaRef.current?.focus();
    }
  }, [
    input,
    setInput,
    attachments,
    sendMessage,
    setAttachments,
    setLocalStorageInput,
    width,
    chatId,
  ]);

  const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/files/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        const { url, pathname, contentType } = data;

        return {
          url,
          name: pathname,
          contentType: contentType,
        };
      }
      const { error } = await response.json();
      toast.error(error);
    } catch (error) {
      toast.error('Failed to upload file, please try again!');
    }
  };

  const handleFileChange = useCallback(
    async (event: ChangeEvent<HTMLInputElement>) => {
      const files = Array.from(event.target.files || []);

      setUploadQueue(files.map((file) => file.name));

      try {
        const uploadPromises = files.map((file) => uploadFile(file));
        const uploadedAttachments = await Promise.all(uploadPromises);
        const successfullyUploadedAttachments = uploadedAttachments.filter(
          (attachment) => attachment !== undefined,
        );

        setAttachments((currentAttachments) => [
          ...currentAttachments,
          ...successfullyUploadedAttachments,
        ]);
      } catch (error) {
        console.error('Error uploading files!', error);
      } finally {
        setUploadQueue([]);
      }
    },
    [setAttachments],
  );

  const { isAtBottom, scrollToBottom } = useScrollToBottom();

  useEffect(() => {
    if (status === 'submitted') {
      scrollToBottom();
    }
  }, [status, scrollToBottom]);

  return (
    <div className="flex relative flex-col gap-4 w-full">
      <AnimatePresence>
        {!isAtBottom && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            className="absolute bottom-28 left-1/2 z-50 -translate-x-1/2"
          >
            <Button
              data-testid="scroll-to-bottom-button"
              className="rounded-full"
              size="icon"
              variant="outline"
              onClick={(event) => {
                event.preventDefault();
                scrollToBottom();
              }}
            >
              <ArrowDown />
            </Button>
          </motion.div>
        )}
      </AnimatePresence>

      {messages.length === 0 &&
        attachments.length === 0 &&
        uploadQueue.length === 0 && (
          <SuggestedActions
            sendMessage={sendMessage}
            chatId={chatId}
            selectedVisibilityType={selectedVisibilityType}
          />
        )}

      <input
        type="file"
        className="fixed -top-4 -left-4 size-0.5 opacity-0 pointer-events-none"
        ref={fileInputRef}
        multiple
        onChange={handleFileChange}
        tabIndex={-1}
      />

      <PromptInput
        className="bg-gray-50 rounded-3xl border border-gray-300 shadow-none transition-all duration-200 dark:bg-sidebar dark:border-sidebar-border hover:ring-1 hover:ring-primary/30 focus-within:ring-1 focus-within:ring-primary/50"
        onSubmit={(event) => {
          event.preventDefault();
          if (status !== 'ready') {
            toast.error('Please wait for the model to finish its response!');
          } else {
            submitForm();
          }
        }}
      >
        {(attachments.length > 0 || uploadQueue.length > 0) && (
          <div
            data-testid="attachments-preview"
            className="flex overflow-x-scroll flex-row gap-2 items-end px-3 py-2"
          >
            {attachments.map((attachment) => (
              <PreviewAttachment
                key={attachment.url}
                attachment={attachment}
                onRemove={() => {
                  setAttachments((currentAttachments) =>
                    currentAttachments.filter((a) => a.url !== attachment.url),
                  );
                  if (fileInputRef.current) {
                    fileInputRef.current.value = '';
                  }
                }}
              />
            ))}

            {uploadQueue.map((filename) => (
              <PreviewAttachment
                key={filename}
                attachment={{
                  url: '',
                  name: filename,
                  contentType: '',
                }}
                isUploading={true}
              />
            ))}
          </div>
        )}

        <PromptInputTextarea
          data-testid="multimodal-input"
          ref={textareaRef}
          placeholder="Send a message..."
          value={input}
          onChange={handleInput}
          minHeight={72}
          maxHeight={200}
          disableAutoResize={true}
          className="text-base resize-none py-4 px-4 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none] bg-transparent !border-0 !border-none outline-none ring-0 focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:outline-none"
          rows={1}
          autoFocus
        />
        <PromptInputToolbar className="px-4 py-2 !border-t-0 !border-top-0 shadow-none dark:!border-transparent dark:border-0">
          <PromptInputTools className="gap-2">
            <AttachmentsButton fileInputRef={fileInputRef} status={status} />
            <ModelSelectorCompact selectedModelId={selectedModelId} />
          </PromptInputTools>
          {status === 'submitted' ? (
            <StopButton stop={stop} setMessages={setMessages} />
          ) : (
            <PromptInputSubmit
              status={status}
              disabled={!input.trim() || uploadQueue.length > 0}
              className="p-3 text-gray-700 bg-gray-200 rounded-full hover:bg-gray-300 dark:bg-sidebar-accent dark:hover:bg-sidebar-accent/80 dark:text-gray-300"
            >
              <ArrowUpIcon size={20} />
            </PromptInputSubmit>
          )}
        </PromptInputToolbar>
      </PromptInput>
    </div>
  );
}

export const MultimodalInput = memo(
  PureMultimodalInput,
  (prevProps, nextProps) => {
    if (prevProps.input !== nextProps.input) return false;
    if (prevProps.status !== nextProps.status) return false;
    if (!equal(prevProps.attachments, nextProps.attachments)) return false;
    if (prevProps.selectedVisibilityType !== nextProps.selectedVisibilityType)
      return false;
    if (prevProps.selectedModelId !== nextProps.selectedModelId) return false;

    return true;
  },
);

function PureAttachmentsButton({
  fileInputRef,
  status,
}: {
  fileInputRef: React.MutableRefObject<HTMLInputElement | null>;
  status: UseChatHelpers<ChatMessage>['status'];
}) {
  return (
    <Button
      data-testid="attachments-button"
      className="rounded-md rounded-bl-lg p-[7px] h-fit dark:border-zinc-700 hover:dark:bg-zinc-900 hover:bg-zinc-200"
      onClick={(event) => {
        event.preventDefault();
        fileInputRef.current?.click();
      }}
      disabled={status !== 'ready'}
      variant="ghost"
    >
      <PaperclipIcon size={14} />
    </Button>
  );
}

const AttachmentsButton = memo(PureAttachmentsButton);

function PureModelSelectorCompact({
  selectedModelId,
}: {
  selectedModelId: string;
}) {
  const [optimisticModelId, setOptimisticModelId] = useState(selectedModelId);

  const selectedModel = chatModels.find(
    (model) => model.id === optimisticModelId,
  );

  return (
    <PromptInputModelSelect
      value={selectedModel?.name}
      onValueChange={(modelName) => {
        const model = chatModels.find((m) => m.name === modelName);
        if (model) {
          setOptimisticModelId(model.id);
          startTransition(() => {
            saveChatModelAsCookie(model.id);
          });
        }
      }}
    >
      <PromptInputModelSelectTrigger
        type="button"
        className="text-xs focus:outline-none focus:ring-0 focus:ring-offset-0 focus-visible:ring-0 focus-visible:ring-offset-0 data-[state=open]:ring-0 data-[state=closed]:ring-0"
      >
        {selectedModel?.name || 'Select model'}
      </PromptInputModelSelectTrigger>
      <PromptInputModelSelectContent>
        {chatModels.map((model) => (
          <SelectItem key={model.id} value={model.name}>
            <div className="flex flex-col gap-1 items-start py-1">
              <div className="font-medium">{model.name}</div>
              <div className="text-xs text-muted-foreground">
                {model.description}
              </div>
            </div>
          </SelectItem>
        ))}
      </PromptInputModelSelectContent>
    </PromptInputModelSelect>
  );
}

const ModelSelectorCompact = memo(PureModelSelectorCompact);

function PureStopButton({
  stop,
  setMessages,
}: {
  stop: () => void;
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
}) {
  return (
    <Button
      data-testid="stop-button"
      className="rounded-full p-1.5 h-fit border dark:border-zinc-600"
      onClick={(event) => {
        event.preventDefault();
        stop();
        setMessages((messages) => messages);
      }}
    >
      <StopIcon size={14} />
    </Button>
  );
}

const StopButton = memo(PureStopButton);

function PureSendButton({
  submitForm,
  input,
  uploadQueue,
}: {
  submitForm: () => void;
  input: string;
  uploadQueue: Array<string>;
}) {
  return (
    <Button
      data-testid="send-button"
      className="rounded-full p-1.5 h-fit border dark:border-zinc-600"
      onClick={(event) => {
        event.preventDefault();
        submitForm();
      }}
      disabled={input.length === 0 || uploadQueue.length > 0}
    >
      <ArrowUpIcon size={14} />
    </Button>
  );
}

const SendButton = memo(PureSendButton, (prevProps, nextProps) => {
  if (prevProps.uploadQueue.length !== nextProps.uploadQueue.length)
    return false;
  if (prevProps.input !== nextProps.input) return false;
  return true;
});



================================================
FILE: components/preview-attachment.tsx
================================================
import type { Attachment } from '@/lib/types';
import { Loader } from './elements/loader';
import { CrossSmallIcon, } from './icons';
import { Button } from './ui/button';

export const PreviewAttachment = ({
  attachment,
  isUploading = false,
  onRemove,
  onEdit,
}: {
  attachment: Attachment;
  isUploading?: boolean;
  onRemove?: () => void;
  onEdit?: () => void;
}) => {
  const { name, url, contentType } = attachment;

  return (
    <div data-testid="input-attachment-preview" className="group relative w-16 h-16 rounded-lg overflow-hidden bg-muted border">
      {contentType?.startsWith('image') ? (
        <img
          src={url}
          alt={name ?? 'An image attachment'}
          className="w-full h-full object-cover"
        />
      ) : (
        <div className="w-full h-full flex items-center justify-center text-xs text-muted-foreground">
          File
        </div>
      )}

      {isUploading && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/50">
          <Loader size={16} />
        </div>
      )}

      {onRemove && !isUploading && (
        <Button
          onClick={onRemove}
          size="sm"
          variant="destructive"
          className="absolute top-0.5 right-0.5 opacity-0 group-hover:opacity-100 transition-opacity size-4 p-0 rounded-full"
        >
          <CrossSmallIcon size={8} />
        </Button>
      )}

      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent text-white text-[10px] px-1 py-0.5 truncate">
        {name}
      </div>
    </div>
  );
};



================================================
FILE: components/sheet-editor.tsx
================================================
'use client';

import React, { memo, useEffect, useMemo, useState } from 'react';
import DataGrid, { textEditor } from 'react-data-grid';
import { parse, unparse } from 'papaparse';
import { useTheme } from 'next-themes';
import { cn } from '@/lib/utils';

import 'react-data-grid/lib/styles.css';

type SheetEditorProps = {
  content: string;
  saveContent: (content: string, isCurrentVersion: boolean) => void;
  status: string;
  isCurrentVersion: boolean;
  currentVersionIndex: number;
};

const MIN_ROWS = 50;
const MIN_COLS = 26;

const PureSpreadsheetEditor = ({
  content,
  saveContent,
  status,
  isCurrentVersion,
}: SheetEditorProps) => {
  const { resolvedTheme } = useTheme();

  const parseData = useMemo(() => {
    if (!content) return Array(MIN_ROWS).fill(Array(MIN_COLS).fill(''));
    const result = parse<string[]>(content, { skipEmptyLines: true });

    const paddedData = result.data.map((row) => {
      const paddedRow = [...row];
      while (paddedRow.length < MIN_COLS) {
        paddedRow.push('');
      }
      return paddedRow;
    });

    while (paddedData.length < MIN_ROWS) {
      paddedData.push(Array(MIN_COLS).fill(''));
    }

    return paddedData;
  }, [content]);

  const columns = useMemo(() => {
    const rowNumberColumn = {
      key: 'rowNumber',
      name: '',
      frozen: true,
      width: 50,
      renderCell: ({ rowIdx }: { rowIdx: number }) => rowIdx + 1,
      cellClass: 'border-t border-r dark:bg-zinc-950 dark:text-zinc-50',
      headerCellClass: 'border-t border-r dark:bg-zinc-900 dark:text-zinc-50',
    };

    const dataColumns = Array.from({ length: MIN_COLS }, (_, i) => ({
      key: i.toString(),
      name: String.fromCharCode(65 + i),
      renderEditCell: textEditor,
      width: 120,
      cellClass: cn(`border-t dark:bg-zinc-950 dark:text-zinc-50`, {
        'border-l': i !== 0,
      }),
      headerCellClass: cn(`border-t dark:bg-zinc-900 dark:text-zinc-50`, {
        'border-l': i !== 0,
      }),
    }));

    return [rowNumberColumn, ...dataColumns];
  }, []);

  const initialRows = useMemo(() => {
    return parseData.map((row, rowIndex) => {
      const rowData: any = {
        id: rowIndex,
        rowNumber: rowIndex + 1,
      };

      columns.slice(1).forEach((col, colIndex) => {
        rowData[col.key] = row[colIndex] || '';
      });

      return rowData;
    });
  }, [parseData, columns]);

  const [localRows, setLocalRows] = useState(initialRows);

  useEffect(() => {
    setLocalRows(initialRows);
  }, [initialRows]);

  const generateCsv = (data: any[][]) => {
    return unparse(data);
  };

  const handleRowsChange = (newRows: any[]) => {
    setLocalRows(newRows);

    const updatedData = newRows.map((row) => {
      return columns.slice(1).map((col) => row[col.key] || '');
    });

    const newCsvContent = generateCsv(updatedData);
    saveContent(newCsvContent, true);
  };

  return (
    <DataGrid
      className={resolvedTheme === 'dark' ? 'rdg-dark' : 'rdg-light'}
      columns={columns}
      rows={localRows}
      enableVirtualization
      onRowsChange={handleRowsChange}
      onCellClick={(args) => {
        if (args.column.key !== 'rowNumber') {
          args.selectCell(true);
        }
      }}
      style={{ height: '100%' }}
      defaultColumnOptions={{
        resizable: true,
        sortable: true,
      }}
    />
  );
};

function areEqual(prevProps: SheetEditorProps, nextProps: SheetEditorProps) {
  return (
    prevProps.currentVersionIndex === nextProps.currentVersionIndex &&
    prevProps.isCurrentVersion === nextProps.isCurrentVersion &&
    !(prevProps.status === 'streaming' && nextProps.status === 'streaming') &&
    prevProps.content === nextProps.content &&
    prevProps.saveContent === nextProps.saveContent
  );
}

export const SpreadsheetEditor = memo(PureSpreadsheetEditor, areEqual);



================================================
FILE: components/sidebar-history-item.tsx
================================================
import type { Chat } from '@/lib/db/schema';
import {
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
} from './ui/sidebar';
import Link from 'next/link';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuPortal,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from './ui/dropdown-menu';
import {
  CheckCircleFillIcon,
  GlobeIcon,
  LockIcon,
  MoreHorizontalIcon,
  ShareIcon,
  TrashIcon,
} from './icons';
import { memo } from 'react';
import { useChatVisibility } from '@/hooks/use-chat-visibility';

const PureChatItem = ({
  chat,
  isActive,
  onDelete,
  setOpenMobile,
}: {
  chat: Chat;
  isActive: boolean;
  onDelete: (chatId: string) => void;
  setOpenMobile: (open: boolean) => void;
}) => {
  const { visibilityType, setVisibilityType } = useChatVisibility({
    chatId: chat.id,
    initialVisibilityType: chat.visibility,
  });

  return (
    <SidebarMenuItem>
      <SidebarMenuButton asChild isActive={isActive}>
        <Link href={`/chat/${chat.id}`} onClick={() => setOpenMobile(false)}>
          <span>{chat.title}</span>
        </Link>
      </SidebarMenuButton>

      <DropdownMenu modal={true}>
        <DropdownMenuTrigger asChild>
          <SidebarMenuAction
            className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground mr-0.5"
            showOnHover={!isActive}
          >
            <MoreHorizontalIcon />
            <span className="sr-only">More</span>
          </SidebarMenuAction>
        </DropdownMenuTrigger>

        <DropdownMenuContent side="bottom" align="end">
          <DropdownMenuSub>
            <DropdownMenuSubTrigger className="cursor-pointer">
              <ShareIcon />
              <span>Share</span>
            </DropdownMenuSubTrigger>
            <DropdownMenuPortal>
              <DropdownMenuSubContent>
                <DropdownMenuItem
                  className="cursor-pointer flex-row justify-between"
                  onClick={() => {
                    setVisibilityType('private');
                  }}
                >
                  <div className="flex flex-row gap-2 items-center">
                    <LockIcon size={12} />
                    <span>Private</span>
                  </div>
                  {visibilityType === 'private' ? (
                    <CheckCircleFillIcon />
                  ) : null}
                </DropdownMenuItem>
                <DropdownMenuItem
                  className="cursor-pointer flex-row justify-between"
                  onClick={() => {
                    setVisibilityType('public');
                  }}
                >
                  <div className="flex flex-row gap-2 items-center">
                    <GlobeIcon />
                    <span>Public</span>
                  </div>
                  {visibilityType === 'public' ? <CheckCircleFillIcon /> : null}
                </DropdownMenuItem>
              </DropdownMenuSubContent>
            </DropdownMenuPortal>
          </DropdownMenuSub>

          <DropdownMenuItem
            className="cursor-pointer text-destructive focus:bg-destructive/15 focus:text-destructive dark:text-red-500"
            onSelect={() => onDelete(chat.id)}
          >
            <TrashIcon />
            <span>Delete</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </SidebarMenuItem>
  );
};

export const ChatItem = memo(PureChatItem, (prevProps, nextProps) => {
  if (prevProps.isActive !== nextProps.isActive) return false;
  return true;
});



================================================
FILE: components/sidebar-history.tsx
================================================
'use client';

import { isToday, isYesterday, subMonths, subWeeks } from 'date-fns';
import { useParams, useRouter } from 'next/navigation';
import type { User } from 'next-auth';
import { useState } from 'react';
import { toast } from 'sonner';
import { motion } from 'framer-motion';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  useSidebar,
} from '@/components/ui/sidebar';
import type { Chat } from '@/lib/db/schema';
import { fetcher } from '@/lib/utils';
import { ChatItem } from './sidebar-history-item';
import useSWRInfinite from 'swr/infinite';
import { LoaderIcon } from './icons';

type GroupedChats = {
  today: Chat[];
  yesterday: Chat[];
  lastWeek: Chat[];
  lastMonth: Chat[];
  older: Chat[];
};

export interface ChatHistory {
  chats: Array<Chat>;
  hasMore: boolean;
}

const PAGE_SIZE = 20;

const groupChatsByDate = (chats: Chat[]): GroupedChats => {
  const now = new Date();
  const oneWeekAgo = subWeeks(now, 1);
  const oneMonthAgo = subMonths(now, 1);

  return chats.reduce(
    (groups, chat) => {
      const chatDate = new Date(chat.createdAt);

      if (isToday(chatDate)) {
        groups.today.push(chat);
      } else if (isYesterday(chatDate)) {
        groups.yesterday.push(chat);
      } else if (chatDate > oneWeekAgo) {
        groups.lastWeek.push(chat);
      } else if (chatDate > oneMonthAgo) {
        groups.lastMonth.push(chat);
      } else {
        groups.older.push(chat);
      }

      return groups;
    },
    {
      today: [],
      yesterday: [],
      lastWeek: [],
      lastMonth: [],
      older: [],
    } as GroupedChats,
  );
};

export function getChatHistoryPaginationKey(
  pageIndex: number,
  previousPageData: ChatHistory,
) {
  if (previousPageData && previousPageData.hasMore === false) {
    return null;
  }

  if (pageIndex === 0) return `/api/history?limit=${PAGE_SIZE}`;

  const firstChatFromPage = previousPageData.chats.at(-1);

  if (!firstChatFromPage) return null;

  return `/api/history?ending_before=${firstChatFromPage.id}&limit=${PAGE_SIZE}`;
}

export function SidebarHistory({ user }: { user: User | undefined }) {
  const { setOpenMobile } = useSidebar();
  const { id } = useParams();

  const {
    data: paginatedChatHistories,
    setSize,
    isValidating,
    isLoading,
    mutate,
  } = useSWRInfinite<ChatHistory>(getChatHistoryPaginationKey, fetcher, {
    fallbackData: [],
  });

  const router = useRouter();
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);

  const hasReachedEnd = paginatedChatHistories
    ? paginatedChatHistories.some((page) => page.hasMore === false)
    : false;

  const hasEmptyChatHistory = paginatedChatHistories
    ? paginatedChatHistories.every((page) => page.chats.length === 0)
    : false;

  const handleDelete = async () => {
    const deletePromise = fetch(`/api/chat?id=${deleteId}`, {
      method: 'DELETE',
    });

    toast.promise(deletePromise, {
      loading: 'Deleting chat...',
      success: () => {
        mutate((chatHistories) => {
          if (chatHistories) {
            return chatHistories.map((chatHistory) => ({
              ...chatHistory,
              chats: chatHistory.chats.filter((chat) => chat.id !== deleteId),
            }));
          }
        });

        return 'Chat deleted successfully';
      },
      error: 'Failed to delete chat',
    });

    setShowDeleteDialog(false);

    if (deleteId === id) {
      router.push('/');
    }
  };

  if (!user) {
    return (
      <SidebarGroup>
        <SidebarGroupContent>
          <div className="flex flex-row gap-2 justify-center items-center px-2 w-full text-sm text-zinc-500">
            Login to save and revisit previous chats!
          </div>
        </SidebarGroupContent>
      </SidebarGroup>
    );
  }

  if (isLoading) {
    return (
      <SidebarGroup>
        <div className="px-2 py-1 text-xs text-sidebar-foreground/50">
          Today
        </div>
        <SidebarGroupContent>
          <div className="flex flex-col">
            {[44, 32, 28, 64, 52].map((item) => (
              <div
                key={item}
                className="flex gap-2 items-center px-2 h-8 rounded-md"
              >
                <div
                  className="h-4 rounded-md flex-1 max-w-[--skeleton-width] bg-sidebar-accent-foreground/10"
                  style={
                    {
                      '--skeleton-width': `${item}%`,
                    } as React.CSSProperties
                  }
                />
              </div>
            ))}
          </div>
        </SidebarGroupContent>
      </SidebarGroup>
    );
  }

  if (hasEmptyChatHistory) {
    return (
      <SidebarGroup>
        <SidebarGroupContent>
          <div className="flex flex-row gap-2 justify-center items-center px-2 w-full text-sm text-zinc-500">
            Your conversations will appear here once you start chatting!
          </div>
        </SidebarGroupContent>
      </SidebarGroup>
    );
  }

  return (
    <>
      <SidebarGroup>
        <SidebarGroupContent>
          <SidebarMenu>
            {paginatedChatHistories &&
              (() => {
                const chatsFromHistory = paginatedChatHistories.flatMap(
                  (paginatedChatHistory) => paginatedChatHistory.chats,
                );

                const groupedChats = groupChatsByDate(chatsFromHistory);

                return (
                  <div className="flex flex-col gap-6">
                    {groupedChats.today.length > 0 && (
                      <div>
                        <div className="px-2 py-1 text-xs text-sidebar-foreground/50">
                          Today
                        </div>
                        {groupedChats.today.map((chat) => (
                          <ChatItem
                            key={chat.id}
                            chat={chat}
                            isActive={chat.id === id}
                            onDelete={(chatId) => {
                              setDeleteId(chatId);
                              setShowDeleteDialog(true);
                            }}
                            setOpenMobile={setOpenMobile}
                          />
                        ))}
                      </div>
                    )}

                    {groupedChats.yesterday.length > 0 && (
                      <div>
                        <div className="px-2 py-1 text-xs text-sidebar-foreground/50">
                          Yesterday
                        </div>
                        {groupedChats.yesterday.map((chat) => (
                          <ChatItem
                            key={chat.id}
                            chat={chat}
                            isActive={chat.id === id}
                            onDelete={(chatId) => {
                              setDeleteId(chatId);
                              setShowDeleteDialog(true);
                            }}
                            setOpenMobile={setOpenMobile}
                          />
                        ))}
                      </div>
                    )}

                    {groupedChats.lastWeek.length > 0 && (
                      <div>
                        <div className="px-2 py-1 text-xs text-sidebar-foreground/50">
                          Last 7 days
                        </div>
                        {groupedChats.lastWeek.map((chat) => (
                          <ChatItem
                            key={chat.id}
                            chat={chat}
                            isActive={chat.id === id}
                            onDelete={(chatId) => {
                              setDeleteId(chatId);
                              setShowDeleteDialog(true);
                            }}
                            setOpenMobile={setOpenMobile}
                          />
                        ))}
                      </div>
                    )}

                    {groupedChats.lastMonth.length > 0 && (
                      <div>
                        <div className="px-2 py-1 text-xs text-sidebar-foreground/50">
                          Last 30 days
                        </div>
                        {groupedChats.lastMonth.map((chat) => (
                          <ChatItem
                            key={chat.id}
                            chat={chat}
                            isActive={chat.id === id}
                            onDelete={(chatId) => {
                              setDeleteId(chatId);
                              setShowDeleteDialog(true);
                            }}
                            setOpenMobile={setOpenMobile}
                          />
                        ))}
                      </div>
                    )}

                    {groupedChats.older.length > 0 && (
                      <div>
                        <div className="px-2 py-1 text-xs text-sidebar-foreground/50">
                          Older than last month
                        </div>
                        {groupedChats.older.map((chat) => (
                          <ChatItem
                            key={chat.id}
                            chat={chat}
                            isActive={chat.id === id}
                            onDelete={(chatId) => {
                              setDeleteId(chatId);
                              setShowDeleteDialog(true);
                            }}
                            setOpenMobile={setOpenMobile}
                          />
                        ))}
                      </div>
                    )}
                  </div>
                );
              })()}
          </SidebarMenu>

          <motion.div
            onViewportEnter={() => {
              if (!isValidating && !hasReachedEnd) {
                setSize((size) => size + 1);
              }
            }}
          />

          {hasReachedEnd ? (
            <div className="flex flex-row gap-2 justify-center items-center px-2 mt-8 w-full text-sm text-zinc-500">
              You have reached the end of your chat history.
            </div>
          ) : (
            <div className="flex flex-row gap-2 items-center p-2 mt-8 text-zinc-500 dark:text-zinc-400">
              <div className="animate-spin">
                <LoaderIcon />
              </div>
              <div>Loading Chats...</div>
            </div>
          )}
        </SidebarGroupContent>
      </SidebarGroup>

      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete your
              chat and remove it from our servers.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete}>
              Continue
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}



================================================
FILE: components/sidebar-toggle.tsx
================================================
import type { ComponentProps } from 'react';

import { type SidebarTrigger, useSidebar } from '@/components/ui/sidebar';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';

import { SidebarLeftIcon } from './icons';
import { Button } from './ui/button';

export function SidebarToggle({
  className,
}: ComponentProps<typeof SidebarTrigger>) {
  const { toggleSidebar } = useSidebar();

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button
          data-testid="sidebar-toggle-button"
          onClick={toggleSidebar}
          variant="outline"
          className="md:px-2 md:h-fit"
        >
          <SidebarLeftIcon size={16} />
        </Button>
      </TooltipTrigger>
      <TooltipContent align="start">Toggle Sidebar</TooltipContent>
    </Tooltip>
  );
}



================================================
FILE: components/sidebar-user-nav.tsx
================================================
'use client';

import { ChevronUp } from 'lucide-react';
import Image from 'next/image';
import type { User } from 'next-auth';
import { signOut, useSession } from 'next-auth/react';
import { useTheme } from 'next-themes';

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar';
import { useRouter } from 'next/navigation';
import { toast } from './toast';
import { LoaderIcon } from './icons';
import { guestRegex } from '@/lib/constants';

export function SidebarUserNav({ user }: { user: User }) {
  const router = useRouter();
  const { data, status } = useSession();
  const { setTheme, resolvedTheme } = useTheme();

  const isGuest = guestRegex.test(data?.user?.email ?? '');

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            {status === 'loading' ? (
              <SidebarMenuButton className="data-[state=open]:bg-sidebar-accent bg-background data-[state=open]:text-sidebar-accent-foreground h-10 justify-between">
                <div className="flex flex-row gap-2">
                  <div className="size-6 bg-zinc-500/30 rounded-full animate-pulse" />
                  <span className="bg-zinc-500/30 text-transparent rounded-md animate-pulse">
                    Loading auth status
                  </span>
                </div>
                <div className="animate-spin text-zinc-500">
                  <LoaderIcon />
                </div>
              </SidebarMenuButton>
            ) : (
              <SidebarMenuButton
                data-testid="user-nav-button"
                className="data-[state=open]:bg-sidebar-accent bg-background data-[state=open]:text-sidebar-accent-foreground h-10"
              >
                <Image
                  src={`https://avatar.vercel.sh/${user.email}`}
                  alt={user.email ?? 'User Avatar'}
                  width={24}
                  height={24}
                  className="rounded-full"
                />
                <span data-testid="user-email" className="truncate">
                  {isGuest ? 'Guest' : user?.email}
                </span>
                <ChevronUp className="ml-auto" />
              </SidebarMenuButton>
            )}
          </DropdownMenuTrigger>
          <DropdownMenuContent
            data-testid="user-nav-menu"
            side="top"
            className="w-[--radix-popper-anchor-width]"
          >
            <DropdownMenuItem
              data-testid="user-nav-item-theme"
              className="cursor-pointer"
              onSelect={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
            >
              {`Toggle ${resolvedTheme === 'light' ? 'dark' : 'light'} mode`}
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild data-testid="user-nav-item-auth">
              <button
                type="button"
                className="w-full cursor-pointer"
                onClick={() => {
                  if (status === 'loading') {
                    toast({
                      type: 'error',
                      description:
                        'Checking authentication status, please try again!',
                    });

                    return;
                  }

                  if (isGuest) {
                    router.push('/login');
                  } else {
                    signOut({
                      redirectTo: '/',
                    });
                  }
                }}
              >
                {isGuest ? 'Login to your account' : 'Sign out'}
              </button>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}



================================================
FILE: components/sign-out-form.tsx
================================================
import Form from 'next/form';

import { signOut } from '@/app/(auth)/auth';

export const SignOutForm = () => {
  return (
    <Form
      className="w-full"
      action={async () => {
        'use server';

        await signOut({
          redirectTo: '/',
        });
      }}
    >
      <button
        type="submit"
        className="w-full text-left px-1 py-0.5 text-red-500"
      >
        Sign out
      </button>
    </Form>
  );
};



================================================
FILE: components/submit-button.tsx
================================================
'use client';

import { useFormStatus } from 'react-dom';

import { LoaderIcon } from '@/components/icons';

import { Button } from './ui/button';

export function SubmitButton({
  children,
  isSuccessful,
}: {
  children: React.ReactNode;
  isSuccessful: boolean;
}) {
  const { pending } = useFormStatus();

  return (
    <Button
      type={pending ? 'button' : 'submit'}
      aria-disabled={pending || isSuccessful}
      disabled={pending || isSuccessful}
      className="relative"
    >
      {children}

      {(pending || isSuccessful) && (
        <span className="animate-spin absolute right-4">
          <LoaderIcon />
        </span>
      )}

      <output aria-live="polite" className="sr-only">
        {pending || isSuccessful ? 'Loading' : 'Submit form'}
      </output>
    </Button>
  );
}



================================================
FILE: components/suggested-actions.tsx
================================================
'use client';

import { motion } from 'framer-motion';
import { memo } from 'react';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { VisibilityType } from './visibility-selector';
import type { ChatMessage } from '@/lib/types';
import { Suggestion } from './elements/suggestion';

interface SuggestedActionsProps {
  chatId: string;
  sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
  selectedVisibilityType: VisibilityType;
}

function PureSuggestedActions({
  chatId,
  sendMessage,
  selectedVisibilityType,
}: SuggestedActionsProps) {
  const suggestedActions = [
    'What are the advantages of using Next.js?',
    'Write code to demonstrate Dijkstra\'s algorithm',
    'Help me write an essay about Silicon Valley',
    'What is the weather in San Francisco?',
  ];

  return (
    <div data-testid="suggested-actions" className="grid sm:grid-cols-2 gap-2 w-full">
        {suggestedActions.map((suggestedAction, index) => (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ delay: 0.05 * index }}
            key={suggestedAction}
          >
            <Suggestion
              suggestion={suggestedAction}
              onClick={(suggestion) => {
                window.history.replaceState({}, '', `/chat/${chatId}`);
                sendMessage({
                  role: 'user',
                  parts: [{ type: 'text', text: suggestion }],
                });
              }}
              className="text-left w-full h-auto whitespace-normal p-3"
            >
              {suggestedAction}
            </Suggestion>
          </motion.div>
        ))}
    </div>
  );
}

export const SuggestedActions = memo(
  PureSuggestedActions,
  (prevProps, nextProps) => {
    if (prevProps.chatId !== nextProps.chatId) return false;
    if (prevProps.selectedVisibilityType !== nextProps.selectedVisibilityType)
      return false;

    return true;
  },
);



================================================
FILE: components/suggestion.tsx
================================================
'use client';

import { AnimatePresence, motion } from 'framer-motion';
import { useState } from 'react';
import { useWindowSize } from 'usehooks-ts';

import type { UISuggestion } from '@/lib/editor/suggestions';

import { CrossIcon, MessageIcon } from './icons';
import { Button } from './ui/button';
import { cn } from '@/lib/utils';
import type { ArtifactKind } from './artifact';

export const Suggestion = ({
  suggestion,
  onApply,
  artifactKind,
}: {
  suggestion: UISuggestion;
  onApply: () => void;
  artifactKind: ArtifactKind;
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const { width: windowWidth } = useWindowSize();

  return (
    <AnimatePresence>
      {!isExpanded ? (
        <motion.div
          className={cn('cursor-pointer text-muted-foreground p-1', {
            'absolute -right-8': artifactKind === 'text',
            'sticky top-0 right-4': artifactKind === 'code',
          })}
          onClick={() => {
            setIsExpanded(true);
          }}
          whileHover={{ scale: 1.1 }}
        >
          <MessageIcon size={windowWidth && windowWidth < 768 ? 16 : 14} />
        </motion.div>
      ) : (
        <motion.div
          key={suggestion.id}
          className="flex absolute -right-12 z-50 flex-col gap-3 p-3 w-56 font-sans text-sm rounded-2xl border shadow-xl bg-background md:-right-16"
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: -20 }}
          exit={{ opacity: 0, y: -10 }}
          whileHover={{ scale: 1.05 }}
        >
          <div className="flex flex-row justify-between items-center">
            <div className="flex flex-row gap-2 items-center">
              <div className="rounded-full size-4 bg-muted-foreground/25" />
              <div className="font-medium">Assistant</div>
            </div>
            <button
              type="button"
              className="text-xs text-gray-500 cursor-pointer"
              onClick={() => {
                setIsExpanded(false);
              }}
            >
              <CrossIcon size={12} />
            </button>
          </div>
          <div>{suggestion.description}</div>
          <Button
            variant="outline"
            className="w-fit py-1.5 px-3 rounded-full"
            onClick={onApply}
          >
            Apply
          </Button>
        </motion.div>
      )}
    </AnimatePresence>
  );
};



================================================
FILE: components/text-editor.tsx
================================================
'use client';

import { exampleSetup } from 'prosemirror-example-setup';
import { inputRules } from 'prosemirror-inputrules';
import { EditorState } from 'prosemirror-state';
import { EditorView } from 'prosemirror-view';
import React, { memo, useEffect, useRef } from 'react';

import type { Suggestion } from '@/lib/db/schema';
import {
  documentSchema,
  handleTransaction,
  headingRule,
} from '@/lib/editor/config';
import {
  buildContentFromDocument,
  buildDocumentFromContent,
  createDecorations,
} from '@/lib/editor/functions';
import {
  projectWithPositions,
  suggestionsPlugin,
  suggestionsPluginKey,
} from '@/lib/editor/suggestions';

type EditorProps = {
  content: string;
  onSaveContent: (updatedContent: string, debounce: boolean) => void;
  status: 'streaming' | 'idle';
  isCurrentVersion: boolean;
  currentVersionIndex: number;
  suggestions: Array<Suggestion>;
};

function PureEditor({
  content,
  onSaveContent,
  suggestions,
  status,
}: EditorProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const editorRef = useRef<EditorView | null>(null);

  useEffect(() => {
    if (containerRef.current && !editorRef.current) {
      const state = EditorState.create({
        doc: buildDocumentFromContent(content),
        plugins: [
          ...exampleSetup({ schema: documentSchema, menuBar: false }),
          inputRules({
            rules: [
              headingRule(1),
              headingRule(2),
              headingRule(3),
              headingRule(4),
              headingRule(5),
              headingRule(6),
            ],
          }),
          suggestionsPlugin,
        ],
      });

      editorRef.current = new EditorView(containerRef.current, {
        state,
      });
    }

    return () => {
      if (editorRef.current) {
        editorRef.current.destroy();
        editorRef.current = null;
      }
    };
    // NOTE: we only want to run this effect once
    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    if (editorRef.current) {
      editorRef.current.setProps({
        dispatchTransaction: (transaction) => {
          handleTransaction({
            transaction,
            editorRef,
            onSaveContent,
          });
        },
      });
    }
  }, [onSaveContent]);

  useEffect(() => {
    if (editorRef.current && content) {
      const currentContent = buildContentFromDocument(
        editorRef.current.state.doc,
      );

      if (status === 'streaming') {
        const newDocument = buildDocumentFromContent(content);

        const transaction = editorRef.current.state.tr.replaceWith(
          0,
          editorRef.current.state.doc.content.size,
          newDocument.content,
        );

        transaction.setMeta('no-save', true);
        editorRef.current.dispatch(transaction);
        return;
      }

      if (currentContent !== content) {
        const newDocument = buildDocumentFromContent(content);

        const transaction = editorRef.current.state.tr.replaceWith(
          0,
          editorRef.current.state.doc.content.size,
          newDocument.content,
        );

        transaction.setMeta('no-save', true);
        editorRef.current.dispatch(transaction);
      }
    }
  }, [content, status]);

  useEffect(() => {
    if (editorRef.current?.state.doc && content) {
      const projectedSuggestions = projectWithPositions(
        editorRef.current.state.doc,
        suggestions,
      ).filter(
        (suggestion) => suggestion.selectionStart && suggestion.selectionEnd,
      );

      const decorations = createDecorations(
        projectedSuggestions,
        editorRef.current,
      );

      const transaction = editorRef.current.state.tr;
      transaction.setMeta(suggestionsPluginKey, { decorations });
      editorRef.current.dispatch(transaction);
    }
  }, [suggestions, content]);

  return (
    <div className="relative prose dark:prose-invert" ref={containerRef} />
  );
}

function areEqual(prevProps: EditorProps, nextProps: EditorProps) {
  return (
    prevProps.suggestions === nextProps.suggestions &&
    prevProps.currentVersionIndex === nextProps.currentVersionIndex &&
    prevProps.isCurrentVersion === nextProps.isCurrentVersion &&
    !(prevProps.status === 'streaming' && nextProps.status === 'streaming') &&
    prevProps.content === nextProps.content &&
    prevProps.onSaveContent === nextProps.onSaveContent
  );
}

export const Editor = memo(PureEditor, areEqual);



================================================
FILE: components/theme-provider.tsx
================================================
'use client';

import { ThemeProvider as NextThemesProvider } from 'next-themes';
import type { ThemeProviderProps } from 'next-themes/dist/types';

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}



================================================
FILE: components/toast.tsx
================================================
'use client';

import React, { useEffect, useRef, useState, type ReactNode } from 'react';
import { toast as sonnerToast } from 'sonner';
import { CheckCircleFillIcon, WarningIcon } from './icons';
import { cn } from '@/lib/utils';

const iconsByType: Record<'success' | 'error', ReactNode> = {
  success: <CheckCircleFillIcon />,
  error: <WarningIcon />,
};

export function toast(props: Omit<ToastProps, 'id'>) {
  return sonnerToast.custom((id) => (
    <Toast id={id} type={props.type} description={props.description} />
  ));
}

function Toast(props: ToastProps) {
  const { id, type, description } = props;

  const descriptionRef = useRef<HTMLDivElement>(null);
  const [multiLine, setMultiLine] = useState(false);

  useEffect(() => {
    const el = descriptionRef.current;
    if (!el) return;

    const update = () => {
      const lineHeight = Number.parseFloat(getComputedStyle(el).lineHeight);
      const lines = Math.round(el.scrollHeight / lineHeight);
      setMultiLine(lines > 1);
    };

    update(); // initial check
    const ro = new ResizeObserver(update); // re-check on width changes
    ro.observe(el);

    return () => ro.disconnect();
  }, [description]);

  return (
    <div className="flex w-full toast-mobile:w-[356px] justify-center">
      <div
        data-testid="toast"
        key={id}
        className={cn(
          'bg-zinc-100 p-3 rounded-lg w-full toast-mobile:w-fit flex flex-row gap-3',
          multiLine ? 'items-start' : 'items-center',
        )}
      >
        <div
          data-type={type}
          className={cn(
            'data-[type=error]:text-red-600 data-[type=success]:text-green-600',
            { 'pt-1': multiLine },
          )}
        >
          {iconsByType[type]}
        </div>
        <div ref={descriptionRef} className="text-zinc-950 text-sm">
          {description}
        </div>
      </div>
    </div>
  );
}

interface ToastProps {
  id: string | number;
  type: 'success' | 'error';
  description: string;
}



================================================
FILE: components/toolbar.tsx
================================================
'use client';
import cx from 'classnames';
import {
  AnimatePresence,
  motion,
  useMotionValue,
  useTransform,
} from 'framer-motion';
import {
  type Dispatch,
  memo,
  type ReactNode,
  type SetStateAction,
  useEffect,
  useRef,
  useState,
} from 'react';
import { useOnClickOutside } from 'usehooks-ts';
import { nanoid } from 'nanoid';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

import { ArrowUpIcon, StopIcon, SummarizeIcon } from './icons';
import { artifactDefinitions, type ArtifactKind } from './artifact';
import type { ArtifactToolbarItem } from './create-artifact';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { ChatMessage } from '@/lib/types';

type ToolProps = {
  description: string;
  icon: ReactNode;
  selectedTool: string | null;
  setSelectedTool: Dispatch<SetStateAction<string | null>>;
  isToolbarVisible?: boolean;
  setIsToolbarVisible?: Dispatch<SetStateAction<boolean>>;
  isAnimating: boolean;
  sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
  onClick: ({
    sendMessage,
  }: {
    sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
  }) => void;
};

const Tool = ({
  description,
  icon,
  selectedTool,
  setSelectedTool,
  isToolbarVisible,
  setIsToolbarVisible,
  isAnimating,
  sendMessage,
  onClick,
}: ToolProps) => {
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    if (selectedTool !== description) {
      setIsHovered(false);
    }
  }, [selectedTool, description]);

  const handleSelect = () => {
    if (!isToolbarVisible && setIsToolbarVisible) {
      setIsToolbarVisible(true);
      return;
    }

    if (!selectedTool) {
      setIsHovered(true);
      setSelectedTool(description);
      return;
    }

    if (selectedTool !== description) {
      setSelectedTool(description);
    } else {
      setSelectedTool(null);
      onClick({ sendMessage });
    }
  };

  return (
    <Tooltip open={isHovered && !isAnimating}>
      <TooltipTrigger asChild>
        <motion.div
          className={cx('p-3 rounded-full', {
            'bg-primary !text-primary-foreground': selectedTool === description,
          })}
          onHoverStart={() => {
            setIsHovered(true);
          }}
          onHoverEnd={() => {
            if (selectedTool !== description) setIsHovered(false);
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              handleSelect();
            }
          }}
          initial={{ scale: 1, opacity: 0 }}
          animate={{ opacity: 1, transition: { delay: 0.1 } }}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          exit={{
            scale: 0.9,
            opacity: 0,
            transition: { duration: 0.1 },
          }}
          onClick={() => {
            handleSelect();
          }}
        >
          {selectedTool === description ? <ArrowUpIcon /> : icon}
        </motion.div>
      </TooltipTrigger>
      <TooltipContent
        side="left"
        sideOffset={16}
        className="bg-foreground text-background rounded-2xl p-3 px-4"
      >
        {description}
      </TooltipContent>
    </Tooltip>
  );
};

const randomArr = [...Array(6)].map((x) => nanoid(5));

const ReadingLevelSelector = ({
  setSelectedTool,
  sendMessage,
  isAnimating,
}: {
  setSelectedTool: Dispatch<SetStateAction<string | null>>;
  isAnimating: boolean;
  sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
}) => {
  const LEVELS = [
    'Elementary',
    'Middle School',
    'Keep current level',
    'High School',
    'College',
    'Graduate',
  ];

  const y = useMotionValue(-40 * 2);
  const dragConstraints = 5 * 40 + 2;
  const yToLevel = useTransform(y, [0, -dragConstraints], [0, 5]);

  const [currentLevel, setCurrentLevel] = useState(2);
  const [hasUserSelectedLevel, setHasUserSelectedLevel] =
    useState<boolean>(false);

  useEffect(() => {
    const unsubscribe = yToLevel.on('change', (latest) => {
      const level = Math.min(5, Math.max(0, Math.round(Math.abs(latest))));
      setCurrentLevel(level);
    });

    return () => unsubscribe();
  }, [yToLevel]);

  return (
    <div className="relative flex flex-col justify-end items-center">
      {randomArr.map((id) => (
        <motion.div
          key={id}
          className="size-[40px] flex flex-row items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ delay: 0.1 }}
        >
          <div className="size-2 rounded-full bg-muted-foreground/40" />
        </motion.div>
      ))}

      <TooltipProvider>
        <Tooltip open={!isAnimating}>
          <TooltipTrigger asChild>
            <motion.div
              className={cx(
                'absolute bg-background p-3 border rounded-full flex flex-row items-center',
                {
                  'bg-primary text-primary-foreground': currentLevel !== 2,
                  'bg-background text-foreground': currentLevel === 2,
                },
              )}
              style={{ y }}
              drag="y"
              dragElastic={0}
              dragMomentum={false}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              transition={{ duration: 0.1 }}
              dragConstraints={{ top: -dragConstraints, bottom: 0 }}
              onDragStart={() => {
                setHasUserSelectedLevel(false);
              }}
              onDragEnd={() => {
                if (currentLevel === 2) {
                  setSelectedTool(null);
                } else {
                  setHasUserSelectedLevel(true);
                }
              }}
              onClick={() => {
                if (currentLevel !== 2 && hasUserSelectedLevel) {
                  sendMessage({
                    role: 'user',
                    parts: [
                      {
                        type: 'text',
                        text: `Please adjust the reading level to ${LEVELS[currentLevel]} level.`,
                      },
                    ],
                  });

                  setSelectedTool(null);
                }
              }}
            >
              {currentLevel === 2 ? <SummarizeIcon /> : <ArrowUpIcon />}
            </motion.div>
          </TooltipTrigger>
          <TooltipContent
            side="left"
            sideOffset={16}
            className="bg-foreground text-background text-sm rounded-2xl p-3 px-4"
          >
            {LEVELS[currentLevel]}
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </div>
  );
};

export const Tools = ({
  isToolbarVisible,
  selectedTool,
  setSelectedTool,
  sendMessage,
  isAnimating,
  setIsToolbarVisible,
  tools,
}: {
  isToolbarVisible: boolean;
  selectedTool: string | null;
  setSelectedTool: Dispatch<SetStateAction<string | null>>;
  sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
  isAnimating: boolean;
  setIsToolbarVisible: Dispatch<SetStateAction<boolean>>;
  tools: Array<ArtifactToolbarItem>;
}) => {
  const [primaryTool, ...secondaryTools] = tools;

  return (
    <motion.div
      className="flex flex-col gap-1.5"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
    >
      <AnimatePresence>
        {isToolbarVisible &&
          secondaryTools.map((secondaryTool) => (
            <Tool
              key={secondaryTool.description}
              description={secondaryTool.description}
              icon={secondaryTool.icon}
              selectedTool={selectedTool}
              setSelectedTool={setSelectedTool}
              sendMessage={sendMessage}
              isAnimating={isAnimating}
              onClick={secondaryTool.onClick}
            />
          ))}
      </AnimatePresence>

      <Tool
        description={primaryTool.description}
        icon={primaryTool.icon}
        selectedTool={selectedTool}
        setSelectedTool={setSelectedTool}
        isToolbarVisible={isToolbarVisible}
        setIsToolbarVisible={setIsToolbarVisible}
        sendMessage={sendMessage}
        isAnimating={isAnimating}
        onClick={primaryTool.onClick}
      />
    </motion.div>
  );
};

const PureToolbar = ({
  isToolbarVisible,
  setIsToolbarVisible,
  sendMessage,
  status,
  stop,
  setMessages,
  artifactKind,
}: {
  isToolbarVisible: boolean;
  setIsToolbarVisible: Dispatch<SetStateAction<boolean>>;
  status: UseChatHelpers<ChatMessage>['status'];
  sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
  stop: UseChatHelpers<ChatMessage>['stop'];
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
  artifactKind: ArtifactKind;
}) => {
  const toolbarRef = useRef<HTMLDivElement>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout>>();

  const [selectedTool, setSelectedTool] = useState<string | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);

  useOnClickOutside(toolbarRef, () => {
    setIsToolbarVisible(false);
    setSelectedTool(null);
  });

  const startCloseTimer = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    timeoutRef.current = setTimeout(() => {
      setSelectedTool(null);
      setIsToolbarVisible(false);
    }, 2000);
  };

  const cancelCloseTimer = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
  };

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (status === 'streaming') {
      setIsToolbarVisible(false);
    }
  }, [status, setIsToolbarVisible]);

  const artifactDefinition = artifactDefinitions.find(
    (definition) => definition.kind === artifactKind,
  );

  if (!artifactDefinition) {
    throw new Error('Artifact definition not found!');
  }

  const toolsByArtifactKind = artifactDefinition.toolbar;

  if (toolsByArtifactKind.length === 0) {
    return null;
  }

  return (
    <TooltipProvider delayDuration={0}>
      <motion.div
        className="cursor-pointer absolute right-6 bottom-6 p-1.5 border rounded-full shadow-lg bg-background flex flex-col justify-end"
        initial={{ opacity: 0, y: -20, scale: 1 }}
        animate={
          isToolbarVisible
            ? selectedTool === 'adjust-reading-level'
              ? {
                  opacity: 1,
                  y: 0,
                  height: 6 * 43,
                  transition: { delay: 0 },
                  scale: 0.95,
                }
              : {
                  opacity: 1,
                  y: 0,
                  height: toolsByArtifactKind.length * 50,
                  transition: { delay: 0 },
                  scale: 1,
                }
            : { opacity: 1, y: 0, height: 54, transition: { delay: 0 } }
        }
        exit={{ opacity: 0, y: -20, transition: { duration: 0.1 } }}
        transition={{ type: 'spring', stiffness: 300, damping: 25 }}
        onHoverStart={() => {
          if (status === 'streaming') return;

          cancelCloseTimer();
          setIsToolbarVisible(true);
        }}
        onHoverEnd={() => {
          if (status === 'streaming') return;

          startCloseTimer();
        }}
        onAnimationStart={() => {
          setIsAnimating(true);
        }}
        onAnimationComplete={() => {
          setIsAnimating(false);
        }}
        ref={toolbarRef}
      >
        {status === 'streaming' ? (
          <motion.div
            key="stop-icon"
            initial={{ scale: 1 }}
            animate={{ scale: 1.4 }}
            exit={{ scale: 1 }}
            className="p-3"
            onClick={() => {
              stop();
              setMessages((messages) => messages);
            }}
          >
            <StopIcon />
          </motion.div>
        ) : selectedTool === 'adjust-reading-level' ? (
          <ReadingLevelSelector
            key="reading-level-selector"
            sendMessage={sendMessage}
            setSelectedTool={setSelectedTool}
            isAnimating={isAnimating}
          />
        ) : (
          <Tools
            key="tools"
            sendMessage={sendMessage}
            isAnimating={isAnimating}
            isToolbarVisible={isToolbarVisible}
            selectedTool={selectedTool}
            setIsToolbarVisible={setIsToolbarVisible}
            setSelectedTool={setSelectedTool}
            tools={toolsByArtifactKind}
          />
        )}
      </motion.div>
    </TooltipProvider>
  );
};

export const Toolbar = memo(PureToolbar, (prevProps, nextProps) => {
  if (prevProps.status !== nextProps.status) return false;
  if (prevProps.isToolbarVisible !== nextProps.isToolbarVisible) return false;
  if (prevProps.artifactKind !== nextProps.artifactKind) return false;

  return true;
});



================================================
FILE: components/version-footer.tsx
================================================
'use client';

import { isAfter } from 'date-fns';
import { motion } from 'framer-motion';
import { useState } from 'react';
import { useSWRConfig } from 'swr';
import { useWindowSize } from 'usehooks-ts';

import type { Document } from '@/lib/db/schema';
import { getDocumentTimestampByIndex } from '@/lib/utils';

import { LoaderIcon } from './icons';
import { Button } from './ui/button';
import { useArtifact } from '@/hooks/use-artifact';

interface VersionFooterProps {
  handleVersionChange: (type: 'next' | 'prev' | 'toggle' | 'latest') => void;
  documents: Array<Document> | undefined;
  currentVersionIndex: number;
}

export const VersionFooter = ({
  handleVersionChange,
  documents,
  currentVersionIndex,
}: VersionFooterProps) => {
  const { artifact } = useArtifact();

  const { width } = useWindowSize();
  const isMobile = width < 768;

  const { mutate } = useSWRConfig();
  const [isMutating, setIsMutating] = useState(false);

  if (!documents) return;

  return (
    <motion.div
      className="absolute flex flex-col gap-4 lg:flex-row bottom-0 bg-background p-4 w-full border-t z-50 justify-between"
      initial={{ y: isMobile ? 200 : 77 }}
      animate={{ y: 0 }}
      exit={{ y: isMobile ? 200 : 77 }}
      transition={{ type: 'spring', stiffness: 140, damping: 20 }}
    >
      <div>
        <div>You are viewing a previous version</div>
        <div className="text-muted-foreground text-sm">
          Restore this version to make edits
        </div>
      </div>

      <div className="flex flex-row gap-4">
        <Button
          disabled={isMutating}
          onClick={async () => {
            setIsMutating(true);

            mutate(
              `/api/document?id=${artifact.documentId}`,
              await fetch(
                `/api/document?id=${artifact.documentId}&timestamp=${getDocumentTimestampByIndex(
                  documents,
                  currentVersionIndex,
                )}`,
                {
                  method: 'DELETE',
                },
              ),
              {
                optimisticData: documents
                  ? [
                      ...documents.filter((document) =>
                        isAfter(
                          new Date(document.createdAt),
                          new Date(
                            getDocumentTimestampByIndex(
                              documents,
                              currentVersionIndex,
                            ),
                          ),
                        ),
                      ),
                    ]
                  : [],
              },
            );
          }}
        >
          <div>Restore this version</div>
          {isMutating && (
            <div className="animate-spin">
              <LoaderIcon />
            </div>
          )}
        </Button>
        <Button
          variant="outline"
          onClick={() => {
            handleVersionChange('latest');
          }}
        >
          Back to latest version
        </Button>
      </div>
    </motion.div>
  );
};



================================================
FILE: components/visibility-selector.tsx
================================================
'use client';

import { type ReactNode, useMemo, useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';
import {
  CheckCircleFillIcon,
  ChevronDownIcon,
  GlobeIcon,
  LockIcon,
} from './icons';
import { useChatVisibility } from '@/hooks/use-chat-visibility';

export type VisibilityType = 'private' | 'public';

const visibilities: Array<{
  id: VisibilityType;
  label: string;
  description: string;
  icon: ReactNode;
}> = [
  {
    id: 'private',
    label: 'Private',
    description: 'Only you can access this chat',
    icon: <LockIcon />,
  },
  {
    id: 'public',
    label: 'Public',
    description: 'Anyone with the link can access this chat',
    icon: <GlobeIcon />,
  },
];

export function VisibilitySelector({
  chatId,
  className,
  selectedVisibilityType,
}: {
  chatId: string;
  selectedVisibilityType: VisibilityType;
} & React.ComponentProps<typeof Button>) {
  const [open, setOpen] = useState(false);

  const { visibilityType, setVisibilityType } = useChatVisibility({
    chatId,
    initialVisibilityType: selectedVisibilityType,
  });

  const selectedVisibility = useMemo(
    () => visibilities.find((visibility) => visibility.id === visibilityType),
    [visibilityType],
  );

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger
        asChild
        className={cn(
          'w-fit data-[state=open]:bg-accent data-[state=open]:text-accent-foreground',
          className,
        )}
      >
        <Button
          data-testid="visibility-selector"
          variant="outline"
          className="hidden md:flex md:px-2 md:h-[34px] focus:outline-none focus:ring-0"
        >
          {selectedVisibility?.icon}
          {selectedVisibility?.label}
          <ChevronDownIcon />
        </Button>
      </DropdownMenuTrigger>

      <DropdownMenuContent align="start" className="min-w-[300px]">
        {visibilities.map((visibility) => (
          <DropdownMenuItem
            data-testid={`visibility-selector-item-${visibility.id}`}
            key={visibility.id}
            onSelect={() => {
              setVisibilityType(visibility.id);
              setOpen(false);
            }}
            className="gap-4 group/item flex flex-row justify-between items-center"
            data-active={visibility.id === visibilityType}
          >
            <div className="flex flex-col gap-1 items-start">
              {visibility.label}
              {visibility.description && (
                <div className="text-xs text-muted-foreground">
                  {visibility.description}
                </div>
              )}
            </div>
            <div className="text-foreground dark:text-foreground opacity-0 group-data-[active=true]/item:opacity-100">
              <CheckCircleFillIcon />
            </div>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}



================================================
FILE: components/weather.tsx
================================================
'use client';

import cx from 'classnames';
import { format, isWithinInterval } from 'date-fns';
import { useEffect, useState } from 'react';

interface WeatherAtLocation {
  latitude: number;
  longitude: number;
  generationtime_ms: number;
  utc_offset_seconds: number;
  timezone: string;
  timezone_abbreviation: string;
  elevation: number;
  current_units: {
    time: string;
    interval: string;
    temperature_2m: string;
  };
  current: {
    time: string;
    interval: number;
    temperature_2m: number;
  };
  hourly_units: {
    time: string;
    temperature_2m: string;
  };
  hourly: {
    time: string[];
    temperature_2m: number[];
  };
  daily_units: {
    time: string;
    sunrise: string;
    sunset: string;
  };
  daily: {
    time: string[];
    sunrise: string[];
    sunset: string[];
  };
}

const SAMPLE = {
  latitude: 37.763283,
  longitude: -122.41286,
  generationtime_ms: 0.027894973754882812,
  utc_offset_seconds: 0,
  timezone: 'GMT',
  timezone_abbreviation: 'GMT',
  elevation: 18,
  current_units: { time: 'iso8601', interval: 'seconds', temperature_2m: '°C' },
  current: { time: '2024-10-07T19:30', interval: 900, temperature_2m: 29.3 },
  hourly_units: { time: 'iso8601', temperature_2m: '°C' },
  hourly: {
    time: [
      '2024-10-07T00:00',
      '2024-10-07T01:00',
      '2024-10-07T02:00',
      '2024-10-07T03:00',
      '2024-10-07T04:00',
      '2024-10-07T05:00',
      '2024-10-07T06:00',
      '2024-10-07T07:00',
      '2024-10-07T08:00',
      '2024-10-07T09:00',
      '2024-10-07T10:00',
      '2024-10-07T11:00',
      '2024-10-07T12:00',
      '2024-10-07T13:00',
      '2024-10-07T14:00',
      '2024-10-07T15:00',
      '2024-10-07T16:00',
      '2024-10-07T17:00',
      '2024-10-07T18:00',
      '2024-10-07T19:00',
      '2024-10-07T20:00',
      '2024-10-07T21:00',
      '2024-10-07T22:00',
      '2024-10-07T23:00',
      '2024-10-08T00:00',
      '2024-10-08T01:00',
      '2024-10-08T02:00',
      '2024-10-08T03:00',
      '2024-10-08T04:00',
      '2024-10-08T05:00',
      '2024-10-08T06:00',
      '2024-10-08T07:00',
      '2024-10-08T08:00',
      '2024-10-08T09:00',
      '2024-10-08T10:00',
      '2024-10-08T11:00',
      '2024-10-08T12:00',
      '2024-10-08T13:00',
      '2024-10-08T14:00',
      '2024-10-08T15:00',
      '2024-10-08T16:00',
      '2024-10-08T17:00',
      '2024-10-08T18:00',
      '2024-10-08T19:00',
      '2024-10-08T20:00',
      '2024-10-08T21:00',
      '2024-10-08T22:00',
      '2024-10-08T23:00',
      '2024-10-09T00:00',
      '2024-10-09T01:00',
      '2024-10-09T02:00',
      '2024-10-09T03:00',
      '2024-10-09T04:00',
      '2024-10-09T05:00',
      '2024-10-09T06:00',
      '2024-10-09T07:00',
      '2024-10-09T08:00',
      '2024-10-09T09:00',
      '2024-10-09T10:00',
      '2024-10-09T11:00',
      '2024-10-09T12:00',
      '2024-10-09T13:00',
      '2024-10-09T14:00',
      '2024-10-09T15:00',
      '2024-10-09T16:00',
      '2024-10-09T17:00',
      '2024-10-09T18:00',
      '2024-10-09T19:00',
      '2024-10-09T20:00',
      '2024-10-09T21:00',
      '2024-10-09T22:00',
      '2024-10-09T23:00',
      '2024-10-10T00:00',
      '2024-10-10T01:00',
      '2024-10-10T02:00',
      '2024-10-10T03:00',
      '2024-10-10T04:00',
      '2024-10-10T05:00',
      '2024-10-10T06:00',
      '2024-10-10T07:00',
      '2024-10-10T08:00',
      '2024-10-10T09:00',
      '2024-10-10T10:00',
      '2024-10-10T11:00',
      '2024-10-10T12:00',
      '2024-10-10T13:00',
      '2024-10-10T14:00',
      '2024-10-10T15:00',
      '2024-10-10T16:00',
      '2024-10-10T17:00',
      '2024-10-10T18:00',
      '2024-10-10T19:00',
      '2024-10-10T20:00',
      '2024-10-10T21:00',
      '2024-10-10T22:00',
      '2024-10-10T23:00',
      '2024-10-11T00:00',
      '2024-10-11T01:00',
      '2024-10-11T02:00',
      '2024-10-11T03:00',
    ],
    temperature_2m: [
      36.6, 32.8, 29.5, 28.6, 29.2, 28.2, 27.5, 26.6, 26.5, 26, 25, 23.5, 23.9,
      24.2, 22.9, 21, 24, 28.1, 31.4, 33.9, 32.1, 28.9, 26.9, 25.2, 23, 21.1,
      19.6, 18.6, 17.7, 16.8, 16.2, 15.5, 14.9, 14.4, 14.2, 13.7, 13.3, 12.9,
      12.5, 13.5, 15.8, 17.7, 19.6, 21, 21.9, 22.3, 22, 20.7, 18.9, 17.9, 17.3,
      17, 16.7, 16.2, 15.6, 15.2, 15, 15, 15.1, 14.8, 14.8, 14.9, 14.7, 14.8,
      15.3, 16.2, 17.9, 19.6, 20.5, 21.6, 21, 20.7, 19.3, 18.7, 18.4, 17.9,
      17.3, 17, 17, 16.8, 16.4, 16.2, 16, 15.8, 15.7, 15.4, 15.4, 16.1, 16.7,
      17, 18.6, 19, 19.5, 19.4, 18.5, 17.9, 17.5, 16.7, 16.3, 16.1,
    ],
  },
  daily_units: {
    time: 'iso8601',
    sunrise: 'iso8601',
    sunset: 'iso8601',
  },
  daily: {
    time: [
      '2024-10-07',
      '2024-10-08',
      '2024-10-09',
      '2024-10-10',
      '2024-10-11',
    ],
    sunrise: [
      '2024-10-07T07:15',
      '2024-10-08T07:16',
      '2024-10-09T07:17',
      '2024-10-10T07:18',
      '2024-10-11T07:19',
    ],
    sunset: [
      '2024-10-07T19:00',
      '2024-10-08T18:58',
      '2024-10-09T18:57',
      '2024-10-10T18:55',
      '2024-10-11T18:54',
    ],
  },
};

function n(num: number): number {
  return Math.ceil(num);
}

export function Weather({
  weatherAtLocation = SAMPLE,
}: {
  weatherAtLocation?: WeatherAtLocation;
}) {
  const currentHigh = Math.max(
    ...weatherAtLocation.hourly.temperature_2m.slice(0, 24),
  );
  const currentLow = Math.min(
    ...weatherAtLocation.hourly.temperature_2m.slice(0, 24),
  );

  const isDay = isWithinInterval(new Date(weatherAtLocation.current.time), {
    start: new Date(weatherAtLocation.daily.sunrise[0]),
    end: new Date(weatherAtLocation.daily.sunset[0]),
  });

  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    handleResize();
    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const hoursToShow = isMobile ? 5 : 6;

  // Find the index of the current time or the next closest time
  const currentTimeIndex = weatherAtLocation.hourly.time.findIndex(
    (time) => new Date(time) >= new Date(weatherAtLocation.current.time),
  );

  // Slice the arrays to get the desired number of items
  const displayTimes = weatherAtLocation.hourly.time.slice(
    currentTimeIndex,
    currentTimeIndex + hoursToShow,
  );
  const displayTemperatures = weatherAtLocation.hourly.temperature_2m.slice(
    currentTimeIndex,
    currentTimeIndex + hoursToShow,
  );

  return (
    <div
      className={cx(
        'flex flex-col gap-4 rounded-2xl p-4 skeleton-bg max-w-[500px]',
        {
          'bg-blue-400': isDay,
        },
        {
          'bg-indigo-900': !isDay,
        },
      )}
    >
      <div className="flex flex-row justify-between items-center">
        <div className="flex flex-row gap-2 items-center">
          <div
            className={cx(
              'size-10 rounded-full skeleton-div',
              {
                'bg-yellow-300': isDay,
              },
              {
                'bg-indigo-100': !isDay,
              },
            )}
          />
          <div className="text-4xl font-medium text-blue-50">
            {n(weatherAtLocation.current.temperature_2m)}
            {weatherAtLocation.current_units.temperature_2m}
          </div>
        </div>

        <div className="text-blue-50">{`H:${n(currentHigh)}° L:${n(currentLow)}°`}</div>
      </div>

      <div className="flex flex-row justify-between">
        {displayTimes.map((time, index) => (
          <div key={time} className="flex flex-col items-center gap-1">
            <div className="text-blue-100 text-xs">
              {format(new Date(time), 'ha')}
            </div>
            <div
              className={cx(
                'size-6 rounded-full skeleton-div',
                {
                  'bg-yellow-300': isDay,
                },
                {
                  'bg-indigo-200': !isDay,
                },
              )}
            />
            <div className="text-blue-50 text-sm">
              {n(displayTemperatures[index])}
              {weatherAtLocation.hourly_units.temperature_2m}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}



================================================
FILE: components/elements/actions.tsx
================================================
'use client';

import { Button } from '@/components/ui/button';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { cn } from '@/lib/utils';
import type { ComponentProps } from 'react';

export type ActionsProps = ComponentProps<'div'>;

export const Actions = ({ className, children, ...props }: ActionsProps) => (
  <div className={cn('flex items-center gap-1', className)} {...props}>
    {children}
  </div>
);

export type ActionProps = ComponentProps<typeof Button> & {
  tooltip?: string;
  label?: string;
};

export const Action = ({
  tooltip,
  children,
  label,
  className,
  variant = 'ghost',
  size = 'sm',
  ...props
}: ActionProps) => {
  const button = (
    <Button
      className={cn(
        'size-9 p-1.5 text-muted-foreground hover:text-foreground relative',
        className,
      )}
      size={size}
      type="button"
      variant={variant}
      {...props}
    >
      {children}
      <span className="sr-only">{label || tooltip}</span>
    </Button>
  );

  if (tooltip) {
    return (
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>{button}</TooltipTrigger>
          <TooltipContent>
            <p>{tooltip}</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    );
  }

  return button;
};



================================================
FILE: components/elements/branch.tsx
================================================
'use client';

import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import type { UIMessage } from 'ai';
import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';
import type { ComponentProps, HTMLAttributes, ReactElement } from 'react';
import { createContext, useContext, useEffect, useState } from 'react';

type BranchContextType = {
  currentBranch: number;
  totalBranches: number;
  goToPrevious: () => void;
  goToNext: () => void;
  branches: ReactElement[];
  setBranches: (branches: ReactElement[]) => void;
};

const BranchContext = createContext<BranchContextType | null>(null);

const useBranch = () => {
  const context = useContext(BranchContext);

  if (!context) {
    throw new Error('Branch components must be used within Branch');
  }

  return context;
};

export type BranchProps = HTMLAttributes<HTMLDivElement> & {
  defaultBranch?: number;
  onBranchChange?: (branchIndex: number) => void;
};

export const Branch = ({
  defaultBranch = 0,
  onBranchChange,
  className,
  ...props
}: BranchProps) => {
  const [currentBranch, setCurrentBranch] = useState(defaultBranch);
  const [branches, setBranches] = useState<ReactElement[]>([]);

  const handleBranchChange = (newBranch: number) => {
    setCurrentBranch(newBranch);
    onBranchChange?.(newBranch);
  };

  const goToPrevious = () => {
    const newBranch =
      currentBranch > 0 ? currentBranch - 1 : branches.length - 1;
    handleBranchChange(newBranch);
  };

  const goToNext = () => {
    const newBranch =
      currentBranch < branches.length - 1 ? currentBranch + 1 : 0;
    handleBranchChange(newBranch);
  };

  const contextValue: BranchContextType = {
    currentBranch,
    totalBranches: branches.length,
    goToPrevious,
    goToNext,
    branches,
    setBranches,
  };

  return (
    <BranchContext.Provider value={contextValue}>
      <div
        className={cn('grid w-full gap-2 [&>div]:pb-0', className)}
        {...props}
      />
    </BranchContext.Provider>
  );
};

export type BranchMessagesProps = HTMLAttributes<HTMLDivElement>;

export const BranchMessages = ({ children, ...props }: BranchMessagesProps) => {
  const { currentBranch, setBranches, branches } = useBranch();
  const childrenArray = Array.isArray(children) ? children : [children];

  // Use useEffect to update branches when they change
  useEffect(() => {
    if (branches.length !== childrenArray.length) {
      setBranches(childrenArray);
    }
  }, [childrenArray, branches, setBranches]);

  return childrenArray.map((branch, index) => (
    <div
      className={cn(
        'grid gap-2 overflow-hidden [&>div]:pb-0',
        index === currentBranch ? 'block' : 'hidden',
      )}
      key={branch.key}
      {...props}
    >
      {branch}
    </div>
  ));
};

export type BranchSelectorProps = HTMLAttributes<HTMLDivElement> & {
  from: UIMessage['role'];
};

export const BranchSelector = ({
  className,
  from,
  ...props
}: BranchSelectorProps) => {
  const { totalBranches } = useBranch();

  // Don't render if there's only one branch
  if (totalBranches <= 1) {
    return null;
  }

  return (
    <div
      className={cn(
        'flex items-center gap-2 self-end px-10',
        from === 'assistant' ? 'justify-start' : 'justify-end',
        className,
      )}
      {...props}
    />
  );
};

export type BranchPreviousProps = ComponentProps<typeof Button>;

export const BranchPrevious = ({
  className,
  children,
  ...props
}: BranchPreviousProps) => {
  const { goToPrevious, totalBranches } = useBranch();

  return (
    <Button
      aria-label="Previous branch"
      className={cn(
        'size-7 shrink-0 rounded-full text-muted-foreground transition-colors',
        'hover:bg-accent hover:text-foreground',
        'disabled:pointer-events-none disabled:opacity-50',
        className,
      )}
      disabled={totalBranches <= 1}
      onClick={goToPrevious}
      size="icon"
      type="button"
      variant="ghost"
      {...props}
    >
      {children ?? <ChevronLeftIcon size={14} />}
    </Button>
  );
};

export type BranchNextProps = ComponentProps<typeof Button>;

export const BranchNext = ({
  className,
  children,
  ...props
}: BranchNextProps) => {
  const { goToNext, totalBranches } = useBranch();

  return (
    <Button
      aria-label="Next branch"
      className={cn(
        'size-7 shrink-0 rounded-full text-muted-foreground transition-colors',
        'hover:bg-accent hover:text-foreground',
        'disabled:pointer-events-none disabled:opacity-50',
        className,
      )}
      disabled={totalBranches <= 1}
      onClick={goToNext}
      size="icon"
      type="button"
      variant="ghost"
      {...props}
    >
      {children ?? <ChevronRightIcon size={14} />}
    </Button>
  );
};

export type BranchPageProps = HTMLAttributes<HTMLSpanElement>;

export const BranchPage = ({ className, ...props }: BranchPageProps) => {
  const { currentBranch, totalBranches } = useBranch();

  return (
    <span
      className={cn(
        'font-medium text-muted-foreground text-xs tabular-nums',
        className,
      )}
      {...props}
    >
      {currentBranch + 1} of {totalBranches}
    </span>
  );
};



================================================
FILE: components/elements/code-block.tsx
================================================
'use client';

import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { CheckIcon, CopyIcon } from 'lucide-react';
import type { ComponentProps, HTMLAttributes, ReactNode } from 'react';
import { createContext, useContext, useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import {
  oneDark,
  oneLight,
} from 'react-syntax-highlighter/dist/esm/styles/prism';

type CodeBlockContextType = {
  code: string;
};

const CodeBlockContext = createContext<CodeBlockContextType>({
  code: '',
});

export type CodeBlockProps = HTMLAttributes<HTMLDivElement> & {
  code: string;
  language: string;
  showLineNumbers?: boolean;
  children?: ReactNode;
};

export const CodeBlock = ({
  code,
  language,
  showLineNumbers = false,
  className,
  children,
  ...props
}: CodeBlockProps) => (
  <CodeBlockContext.Provider value={{ code }}>
    <div
      className={cn(
        'relative w-full overflow-hidden rounded-md border bg-background text-foreground',
        className,
      )}
      {...props}
    >
      <div className="relative">
        <SyntaxHighlighter
          className="overflow-hidden dark:hidden"
          codeTagProps={{
            className: 'font-mono text-sm',
          }}
          customStyle={{
            margin: 0,
            padding: '1rem',
            fontSize: '0.875rem',
            background: 'hsl(var(--background))',
            color: 'hsl(var(--foreground))',
            overflowX: 'auto',
            overflowWrap: 'break-word',
            wordBreak: 'break-all',
          }}
          language={language}
          lineNumberStyle={{
            color: 'hsl(var(--muted-foreground))',
            paddingRight: '1rem',
            minWidth: '2.5rem',
          }}
          showLineNumbers={showLineNumbers}
          style={oneLight}
        >
          {code}
        </SyntaxHighlighter>
        <SyntaxHighlighter
          className="hidden overflow-hidden dark:block"
          codeTagProps={{
            className: 'font-mono text-sm',
          }}
          customStyle={{
            margin: 0,
            padding: '1rem',
            fontSize: '0.875rem',
            background: 'hsl(var(--background))',
            color: 'hsl(var(--foreground))',
            overflowX: 'auto',
            overflowWrap: 'break-word',
            wordBreak: 'break-all',
          }}
          language={language}
          lineNumberStyle={{
            color: 'hsl(var(--muted-foreground))',
            paddingRight: '1rem',
            minWidth: '2.5rem',
          }}
          showLineNumbers={showLineNumbers}
          style={oneDark}
        >
          {code}
        </SyntaxHighlighter>
        {children && (
          <div className="absolute top-2 right-2 flex items-center gap-2">
            {children}
          </div>
        )}
      </div>
    </div>
  </CodeBlockContext.Provider>
);

export type CodeBlockCopyButtonProps = ComponentProps<typeof Button> & {
  onCopy?: () => void;
  onError?: (error: Error) => void;
  timeout?: number;
};

export const CodeBlockCopyButton = ({
  onCopy,
  onError,
  timeout = 2000,
  children,
  className,
  ...props
}: CodeBlockCopyButtonProps) => {
  const [isCopied, setIsCopied] = useState(false);
  const { code } = useContext(CodeBlockContext);

  const copyToClipboard = async () => {
    if (typeof window === 'undefined' || !navigator.clipboard.writeText) {
      onError?.(new Error('Clipboard API not available'));
      return;
    }

    try {
      await navigator.clipboard.writeText(code);
      setIsCopied(true);
      onCopy?.();
      setTimeout(() => setIsCopied(false), timeout);
    } catch (error) {
      onError?.(error as Error);
    }
  };

  const Icon = isCopied ? CheckIcon : CopyIcon;

  return (
    <Button
      className={cn('shrink-0', className)}
      onClick={copyToClipboard}
      size="icon"
      variant="ghost"
      {...props}
    >
      {children ?? <Icon size={14} />}
    </Button>
  );
};



================================================
FILE: components/elements/conversation.tsx
================================================
'use client';

import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { ArrowDownIcon } from 'lucide-react';
import type { ComponentProps } from 'react';
import { useCallback } from 'react';
import { StickToBottom, useStickToBottomContext } from 'use-stick-to-bottom';

export type ConversationProps = ComponentProps<typeof StickToBottom>;

export const Conversation = ({ className, ...props }: ConversationProps) => (
  <StickToBottom
    className={cn('relative flex-1 overflow-y-auto', className)}
    initial="smooth"
    resize="smooth"
    role="log"
    {...props}
  />
);

export type ConversationContentProps = ComponentProps<
  typeof StickToBottom.Content
>;

export const ConversationContent = ({
  className,
  ...props
}: ConversationContentProps) => (
  <StickToBottom.Content className={cn('p-4', className)} {...props} />
);

export type ConversationScrollButtonProps = ComponentProps<typeof Button>;

export const ConversationScrollButton = ({
  className,
  ...props
}: ConversationScrollButtonProps) => {
  const { isAtBottom, scrollToBottom } = useStickToBottomContext();

  const handleScrollToBottom = useCallback(() => {
    scrollToBottom();
  }, [scrollToBottom]);

  return (
    !isAtBottom && (
      <Button
        className={cn(
          'absolute bottom-4 left-[50%] translate-x-[-50%] rounded-full',
          className,
        )}
        onClick={handleScrollToBottom}
        size="icon"
        type="button"
        variant="outline"
        {...props}
      >
        <ArrowDownIcon className="size-4" />
      </Button>
    )
  );
};



================================================
FILE: components/elements/image.tsx
================================================
import { cn } from '@/lib/utils';
import type { Experimental_GeneratedImage } from 'ai';

export type ImageProps = Experimental_GeneratedImage & {
  className?: string;
  alt?: string;
};

export const Image = ({
  base64,
  uint8Array,
  mediaType,
  ...props
}: ImageProps) => (
  <img
    {...props}
    alt={props.alt}
    className={cn(
      'h-auto max-w-full overflow-hidden rounded-md',
      props.className,
    )}
    src={`data:${mediaType};base64,${base64}`}
  />
);



================================================
FILE: components/elements/inline-citation.tsx
================================================
'use client';

import { Badge } from '@/components/ui/badge';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  type CarouselApi,
} from '@/components/ui/carousel';
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '@/components/ui/hover-card';
import { cn } from '@/lib/utils';
import { ArrowLeftIcon, ArrowRightIcon } from 'lucide-react';
import {
  type ComponentProps,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from 'react';

export type InlineCitationProps = ComponentProps<'span'>;

export const InlineCitation = ({
  className,
  ...props
}: InlineCitationProps) => (
  <span
    className={cn('group inline items-center gap-1', className)}
    {...props}
  />
);

export type InlineCitationTextProps = ComponentProps<'span'>;

export const InlineCitationText = ({
  className,
  ...props
}: InlineCitationTextProps) => (
  <span
    className={cn('transition-colors group-hover:bg-accent', className)}
    {...props}
  />
);

export type InlineCitationCardProps = ComponentProps<typeof HoverCard>;

export const InlineCitationCard = (props: InlineCitationCardProps) => (
  <HoverCard closeDelay={0} openDelay={0} {...props} />
);

export type InlineCitationCardTriggerProps = ComponentProps<typeof Badge> & {
  sources: string[];
};

export const InlineCitationCardTrigger = ({
  sources,
  className,
  ...props
}: InlineCitationCardTriggerProps) => (
  <HoverCardTrigger asChild>
    <Badge
      className={cn('ml-1 rounded-full', className)}
      variant="secondary"
      {...props}
    >
      {sources.length ? (
        <>
          {new URL(sources[0]).hostname}{' '}
          {sources.length > 1 && `+${sources.length - 1}`}
        </>
      ) : (
        'unknown'
      )}
    </Badge>
  </HoverCardTrigger>
);

export type InlineCitationCardBodyProps = ComponentProps<'div'>;

export const InlineCitationCardBody = ({
  className,
  ...props
}: InlineCitationCardBodyProps) => (
  <HoverCardContent className={cn('relative w-80 p-0', className)} {...props} />
);

const CarouselApiContext = createContext<CarouselApi | undefined>(undefined);

const useCarouselApi = () => {
  const context = useContext(CarouselApiContext);
  return context;
};

export type InlineCitationCarouselProps = ComponentProps<typeof Carousel>;

export const InlineCitationCarousel = ({
  className,
  children,
  ...props
}: InlineCitationCarouselProps) => {
  const [api, setApi] = useState<CarouselApi>();

  return (
    <CarouselApiContext.Provider value={api}>
      <Carousel className={cn('w-full', className)} setApi={setApi} {...props}>
        {children}
      </Carousel>
    </CarouselApiContext.Provider>
  );
};

export type InlineCitationCarouselContentProps = ComponentProps<'div'>;

export const InlineCitationCarouselContent = (
  props: InlineCitationCarouselContentProps,
) => <CarouselContent {...props} />;

export type InlineCitationCarouselItemProps = ComponentProps<'div'>;

export const InlineCitationCarouselItem = ({
  className,
  ...props
}: InlineCitationCarouselItemProps) => (
  <CarouselItem
    className={cn('w-full space-y-2 p-4 pl-8', className)}
    {...props}
  />
);

export type InlineCitationCarouselHeaderProps = ComponentProps<'div'>;

export const InlineCitationCarouselHeader = ({
  className,
  ...props
}: InlineCitationCarouselHeaderProps) => (
  <div
    className={cn(
      'flex items-center justify-between gap-2 rounded-t-md bg-secondary p-2',
      className,
    )}
    {...props}
  />
);

export type InlineCitationCarouselIndexProps = ComponentProps<'div'>;

export const InlineCitationCarouselIndex = ({
  children,
  className,
  ...props
}: InlineCitationCarouselIndexProps) => {
  const api = useCarouselApi();
  const [current, setCurrent] = useState(0);
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (!api) {
      return;
    }

    setCount(api.scrollSnapList().length);
    setCurrent(api.selectedScrollSnap() + 1);

    api.on('select', () => {
      setCurrent(api.selectedScrollSnap() + 1);
    });
  }, [api]);

  return (
    <div
      className={cn(
        'flex flex-1 items-center justify-end px-3 py-1 text-muted-foreground text-xs',
        className,
      )}
      {...props}
    >
      {children ?? `${current}/${count}`}
    </div>
  );
};

export type InlineCitationCarouselPrevProps = ComponentProps<'button'>;

export const InlineCitationCarouselPrev = ({
  className,
  ...props
}: InlineCitationCarouselPrevProps) => {
  const api = useCarouselApi();

  const handleClick = useCallback(() => {
    if (api) {
      api.scrollPrev();
    }
  }, [api]);

  return (
    <button
      aria-label="Previous"
      className={cn('shrink-0', className)}
      onClick={handleClick}
      type="button"
      {...props}
    >
      <ArrowLeftIcon className="size-4 text-muted-foreground" />
    </button>
  );
};

export type InlineCitationCarouselNextProps = ComponentProps<'button'>;

export const InlineCitationCarouselNext = ({
  className,
  ...props
}: InlineCitationCarouselNextProps) => {
  const api = useCarouselApi();

  const handleClick = useCallback(() => {
    if (api) {
      api.scrollNext();
    }
  }, [api]);

  return (
    <button
      aria-label="Next"
      className={cn('shrink-0', className)}
      onClick={handleClick}
      type="button"
      {...props}
    >
      <ArrowRightIcon className="size-4 text-muted-foreground" />
    </button>
  );
};

export type InlineCitationSourceProps = ComponentProps<'div'> & {
  title?: string;
  url?: string;
  description?: string;
};

export const InlineCitationSource = ({
  title,
  url,
  description,
  className,
  children,
  ...props
}: InlineCitationSourceProps) => (
  <div className={cn('space-y-1', className)} {...props}>
    {title && (
      <h4 className="truncate font-medium text-sm leading-tight">{title}</h4>
    )}
    {url && (
      <p className="truncate break-all text-muted-foreground text-xs">{url}</p>
    )}
    {description && (
      <p className="line-clamp-3 text-muted-foreground text-sm leading-relaxed">
        {description}
      </p>
    )}
    {children}
  </div>
);

export type InlineCitationQuoteProps = ComponentProps<'blockquote'>;

export const InlineCitationQuote = ({
  children,
  className,
  ...props
}: InlineCitationQuoteProps) => (
  <blockquote
    className={cn(
      'border-muted border-l-2 pl-3 text-muted-foreground text-sm italic',
      className,
    )}
    {...props}
  >
    {children}
  </blockquote>
);



================================================
FILE: components/elements/loader.tsx
================================================
import { cn } from '@/lib/utils';
import type { HTMLAttributes } from 'react';

type LoaderIconProps = {
  size?: number;
};

const LoaderIcon = ({ size = 16 }: LoaderIconProps) => (
  <svg
    height={size}
    strokeLinejoin="round"
    style={{ color: 'currentcolor' }}
    viewBox="0 0 16 16"
    width={size}
  >
    <title>Loader</title>
    <g clipPath="url(#clip0_2393_1490)">
      <path d="M8 0V4" stroke="currentColor" strokeWidth="1.5" />
      <path
        d="M8 16V12"
        opacity="0.5"
        stroke="currentColor"
        strokeWidth="1.5"
      />
      <path
        d="M3.29773 1.52783L5.64887 4.7639"
        opacity="0.9"
        stroke="currentColor"
        strokeWidth="1.5"
      />
      <path
        d="M12.7023 1.52783L10.3511 4.7639"
        opacity="0.1"
        stroke="currentColor"
        strokeWidth="1.5"
      />
      <path
        d="M12.7023 14.472L10.3511 11.236"
        opacity="0.4"
        stroke="currentColor"
        strokeWidth="1.5"
      />
      <path
        d="M3.29773 14.472L5.64887 11.236"
        opacity="0.6"
        stroke="currentColor"
        strokeWidth="1.5"
      />
      <path
        d="M15.6085 5.52783L11.8043 6.7639"
        opacity="0.2"
        stroke="currentColor"
        strokeWidth="1.5"
      />
      <path
        d="M0.391602 10.472L4.19583 9.23598"
        opacity="0.7"
        stroke="currentColor"
        strokeWidth="1.5"
      />
      <path
        d="M15.6085 10.4722L11.8043 9.2361"
        opacity="0.3"
        stroke="currentColor"
        strokeWidth="1.5"
      />
      <path
        d="M0.391602 5.52783L4.19583 6.7639"
        opacity="0.8"
        stroke="currentColor"
        strokeWidth="1.5"
      />
    </g>
    <defs>
      <clipPath id="clip0_2393_1490">
        <rect fill="white" height="16" width="16" />
      </clipPath>
    </defs>
  </svg>
);

export type LoaderProps = HTMLAttributes<HTMLDivElement> & {
  size?: number;
};

export const Loader = ({ className, size = 16, ...props }: LoaderProps) => (
  <div
    className={cn(
      'inline-flex animate-spin items-center justify-center',
      className,
    )}
    {...props}
  >
    <LoaderIcon size={size} />
  </div>
);



================================================
FILE: components/elements/message.tsx
================================================
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import type { UIMessage } from 'ai';
import type { ComponentProps, HTMLAttributes } from 'react';

export type MessageProps = HTMLAttributes<HTMLDivElement> & {
  from: UIMessage['role'];
};

export const Message = ({ className, from, ...props }: MessageProps) => (
  <div
    className={cn(
      'group flex w-full items-end justify-end gap-2 py-4',
      from === 'user' ? 'is-user' : 'is-assistant flex-row-reverse justify-end',
      '[&>div]:max-w-[80%]',
      className,
    )}
    {...props}
  />
);

export type MessageContentProps = HTMLAttributes<HTMLDivElement>;

export const MessageContent = ({
  children,
  className,
  ...props
}: MessageContentProps) => (
  <div
    className={cn(
      'flex flex-col gap-2 overflow-hidden rounded-lg px-4 py-3 text-foreground text-sm',
      'group-[.is-user]:bg-primary group-[.is-user]:text-primary-foreground',
      'group-[.is-assistant]:bg-secondary group-[.is-assistant]:text-foreground',
      'is-user:dark',
      className,
    )}
    {...props}
  >
    {children}
  </div>
);

export type MessageAvatarProps = ComponentProps<typeof Avatar> & {
  src: string;
  name?: string;
};

export const MessageAvatar = ({
  src,
  name,
  className,
  ...props
}: MessageAvatarProps) => (
  <Avatar className={cn('size-8 ring-1 ring-border', className)} {...props}>
    <AvatarImage alt="" className="mt-0 mb-0" src={src} />
    <AvatarFallback>{name?.slice(0, 2) || 'ME'}</AvatarFallback>
  </Avatar>
);



================================================
FILE: components/elements/prompt-input.tsx
================================================
'use client';

import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { cn } from '@/lib/utils';
import type { ChatStatus } from 'ai';
import { Loader2Icon, SendIcon, SquareIcon, XIcon } from 'lucide-react';
import type {
  ComponentProps,
  HTMLAttributes,
  KeyboardEventHandler,
} from 'react';
import { Children } from 'react';

export type PromptInputProps = HTMLAttributes<HTMLFormElement>;

export const PromptInput = ({ className, ...props }: PromptInputProps) => (
  <form
    className={cn(
      'w-full overflow-hidden rounded-xl border bg-background shadow-sm',
      className,
    )}
    {...props}
  />
);

export type PromptInputTextareaProps = ComponentProps<typeof Textarea> & {
  minHeight?: number;
  maxHeight?: number;
  disableAutoResize?: boolean;
  resizeOnNewLinesOnly?: boolean;
};

export const PromptInputTextarea = ({
  onChange,
  className,
  placeholder = 'What would you like to know?',
  minHeight = 48,
  maxHeight = 164,
  disableAutoResize = false,
  resizeOnNewLinesOnly = false,
  ...props
}: PromptInputTextareaProps) => {
  const handleKeyDown: KeyboardEventHandler<HTMLTextAreaElement> = (e) => {
    if (e.key === 'Enter') {
      // Don't submit if IME composition is in progress
      if (e.nativeEvent.isComposing) {
        return;
      }

      if (e.shiftKey) {
        // Allow newline
        return;
      }

      // Submit on Enter (without Shift)
      e.preventDefault();
      const form = e.currentTarget.form;
      if (form) {
        form.requestSubmit();
      }
    }
  };

  return (
    <Textarea
      className={cn(
        'w-full resize-none rounded-none border-none p-3 shadow-none outline-none ring-0',
        disableAutoResize ? 'field-sizing-fixed' : resizeOnNewLinesOnly ? 'field-sizing-fixed' : 'field-sizing-content max-h-[6lh]',
        'bg-transparent dark:bg-transparent',
        'focus-visible:ring-0',
        className,
      )}
      name="message"
      onChange={(e) => {
        onChange?.(e);
      }}
      onKeyDown={handleKeyDown}
      placeholder={placeholder}
      {...props}
    />
  );
};

export type PromptInputToolbarProps = HTMLAttributes<HTMLDivElement>;

export const PromptInputToolbar = ({
  className,
  ...props
}: PromptInputToolbarProps) => (
  <div
    className={cn('flex items-center justify-between p-1', className)}
    {...props}
  />
);

export type PromptInputToolsProps = HTMLAttributes<HTMLDivElement>;

export const PromptInputTools = ({
  className,
  ...props
}: PromptInputToolsProps) => (
  <div
    className={cn(
      'flex items-center gap-1',
      '[&_button:first-child]:rounded-bl-xl',
      className,
    )}
    {...props}
  />
);

export type PromptInputButtonProps = ComponentProps<typeof Button>;

export const PromptInputButton = ({
  variant = 'ghost',
  className,
  size,
  ...props
}: PromptInputButtonProps) => {
  const newSize =
    (size ?? Children.count(props.children) > 1) ? 'default' : 'icon';

  return (
    <Button
      className={cn(
        'shrink-0 gap-1.5 rounded-lg',
        variant === 'ghost' && 'text-muted-foreground',
        newSize === 'default' && 'px-3',
        className,
      )}
      size={newSize}
      type="button"
      variant={variant}
      {...props}
    />
  );
};

export type PromptInputSubmitProps = ComponentProps<typeof Button> & {
  status?: ChatStatus;
};

export const PromptInputSubmit = ({
  className,
  variant = 'default',
  size = 'icon',
  status,
  children,
  ...props
}: PromptInputSubmitProps) => {
  let Icon = <SendIcon className="size-4" />;

  if (status === 'submitted') {
    Icon = <Loader2Icon className="size-4 animate-spin" />;
  } else if (status === 'streaming') {
    Icon = <SquareIcon className="size-4" />;
  } else if (status === 'error') {
    Icon = <XIcon className="size-4" />;
  }

  return (
    <Button
      className={cn('gap-1.5 rounded-lg', className)}
      size={size}
      type="submit"
      variant={variant}
      {...props}
    >
      {children ?? Icon}
    </Button>
  );
};

export type PromptInputModelSelectProps = ComponentProps<typeof Select>;

export const PromptInputModelSelect = (props: PromptInputModelSelectProps) => (
  <Select {...props} />
);

export type PromptInputModelSelectTriggerProps = ComponentProps<
  typeof SelectTrigger
>;

export const PromptInputModelSelectTrigger = ({
  className,
  ...props
}: PromptInputModelSelectTriggerProps) => (
  <SelectTrigger
    className={cn(
      'border-none bg-transparent font-medium text-muted-foreground shadow-none transition-colors',
      'hover:bg-accent hover:text-foreground [&[aria-expanded="true"]]:bg-accent [&[aria-expanded="true"]]:text-foreground',
      className,
    )}
    {...props}
  />
);

export type PromptInputModelSelectContentProps = ComponentProps<
  typeof SelectContent
>;

export const PromptInputModelSelectContent = ({
  className,
  ...props
}: PromptInputModelSelectContentProps) => (
  <SelectContent className={cn(className)} {...props} />
);

export type PromptInputModelSelectItemProps = ComponentProps<typeof SelectItem>;

export const PromptInputModelSelectItem = ({
  className,
  ...props
}: PromptInputModelSelectItemProps) => (
  <SelectItem className={cn(className)} {...props} />
);

export type PromptInputModelSelectValueProps = ComponentProps<
  typeof SelectValue
>;

export const PromptInputModelSelectValue = ({
  className,
  ...props
}: PromptInputModelSelectValueProps) => (
  <SelectValue className={cn(className)} {...props} />
);



================================================
FILE: components/elements/reasoning.tsx
================================================
'use client';

import { useControllableState } from '@radix-ui/react-use-controllable-state';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { cn } from '@/lib/utils';
import { BrainIcon, ChevronDownIcon } from 'lucide-react';
import type { ComponentProps } from 'react';
import { createContext, memo, useContext, useEffect, useState } from 'react';
import { Response } from './response';

type ReasoningContextValue = {
  isStreaming: boolean;
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  duration: number;
};

const ReasoningContext = createContext<ReasoningContextValue | null>(null);

const useReasoning = () => {
  const context = useContext(ReasoningContext);
  if (!context) {
    throw new Error('Reasoning components must be used within Reasoning');
  }
  return context;
};

export type ReasoningProps = ComponentProps<typeof Collapsible> & {
  isStreaming?: boolean;
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  duration?: number;
};

const AUTO_CLOSE_DELAY = 1000;
const MS_IN_S = 1000;

export const Reasoning = memo(
  ({
    className,
    isStreaming = false,
    open,
    defaultOpen = true,
    onOpenChange,
    duration: durationProp,
    children,
    ...props
  }: ReasoningProps) => {
    const [isOpen, setIsOpen] = useControllableState({
      prop: open,
      defaultProp: defaultOpen,
      onChange: onOpenChange,
    });
    const [duration, setDuration] = useControllableState({
      prop: durationProp,
      defaultProp: 0,
    });

    const [hasAutoClosedRef, setHasAutoClosedRef] = useState(false);
    const [startTime, setStartTime] = useState<number | null>(null);

    // Track duration when streaming starts and ends
    useEffect(() => {
      if (isStreaming) {
        if (startTime === null) {
          setStartTime(Date.now());
        }
      } else if (startTime !== null) {
        setDuration(Math.round((Date.now() - startTime) / MS_IN_S));
        setStartTime(null);
      }
    }, [isStreaming, startTime, setDuration]);

    // Auto-open when streaming starts, auto-close when streaming ends (once only)
    useEffect(() => {
      if (defaultOpen && !isStreaming && isOpen && !hasAutoClosedRef) {
        // Add a small delay before closing to allow user to see the content
        const timer = setTimeout(() => {
          setIsOpen(false);
          setHasAutoClosedRef(true);
        }, AUTO_CLOSE_DELAY);

        return () => clearTimeout(timer);
      }
    }, [isStreaming, isOpen, defaultOpen, setIsOpen, hasAutoClosedRef]);

    const handleOpenChange = (newOpen: boolean) => {
      setIsOpen(newOpen);
    };

    return (
      <ReasoningContext.Provider
        value={{ isStreaming, isOpen, setIsOpen, duration }}
      >
        <Collapsible
          className={cn('not-prose mb-4', className)}
          onOpenChange={handleOpenChange}
          open={isOpen}
          {...props}
        >
          {children}
        </Collapsible>
      </ReasoningContext.Provider>
    );
  },
);

export type ReasoningTriggerProps = ComponentProps<typeof CollapsibleTrigger>;

export const ReasoningTrigger = memo(
  ({ className, children, ...props }: ReasoningTriggerProps) => {
    const { isStreaming, isOpen, duration } = useReasoning();

    return (
      <CollapsibleTrigger
        className={cn(
          'flex items-center gap-2 text-muted-foreground text-sm',
          className,
        )}
        {...props}
      >
        {children ?? (
          <>
            <BrainIcon className="size-4" />
            {isStreaming || duration === 0 ? (
              <p>Thinking...</p>
            ) : (
              <p>Thought for {duration} seconds</p>
            )}
            <ChevronDownIcon
              className={cn(
                'size-4 text-muted-foreground transition-transform',
                isOpen ? 'rotate-180' : 'rotate-0',
              )}
            />
          </>
        )}
      </CollapsibleTrigger>
    );
  },
);

export type ReasoningContentProps = ComponentProps<
  typeof CollapsibleContent
> & {
  children: string;
};

export const ReasoningContent = memo(
  ({ className, children, ...props }: ReasoningContentProps) => (
    <CollapsibleContent
      className={cn(
        'mt-4 text-sm',
        'data-[state=closed]:fade-out-0 data-[state=closed]:slide-out-to-top-2 data-[state=open]:slide-in-from-top-2 text-popover-foreground outline-none data-[state=closed]:animate-out data-[state=open]:animate-in',
        className,
      )}
      {...props}
    >
      <Response className="grid gap-2">{children}</Response>
    </CollapsibleContent>
  ),
);

Reasoning.displayName = 'Reasoning';
ReasoningTrigger.displayName = 'ReasoningTrigger';
ReasoningContent.displayName = 'ReasoningContent';



================================================
FILE: components/elements/response.tsx
================================================
'use client';

import { cn } from '@/lib/utils';
import { type ComponentProps, memo } from 'react';
import { Streamdown } from 'streamdown';

type ResponseProps = ComponentProps<typeof Streamdown>;

export const Response = memo(
  ({ className, ...props }: ResponseProps) => (
    <Streamdown
      className={cn(
        'size-full [&>*:first-child]:mt-0 [&>*:last-child]:mb-0 [&_pre]:overflow-x-auto [&_pre]:max-w-full [&_code]:break-words [&_code]:whitespace-pre-wrap',
        className,
      )}
      {...props}
    />
  ),
  (prevProps, nextProps) => prevProps.children === nextProps.children,
);

Response.displayName = 'Response';



================================================
FILE: components/elements/source.tsx
================================================
'use client';

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { cn } from '@/lib/utils';
import { BookIcon, ChevronDownIcon } from 'lucide-react';
import type { ComponentProps } from 'react';

export type SourcesProps = ComponentProps<'div'>;

export const Sources = ({ className, ...props }: SourcesProps) => (
  <Collapsible
    className={cn('not-prose mb-4 text-primary text-xs', className)}
    {...props}
  />
);

export type SourcesTriggerProps = ComponentProps<typeof CollapsibleTrigger> & {
  count: number;
};

export const SourcesTrigger = ({
  className,
  count,
  children,
  ...props
}: SourcesTriggerProps) => (
  <CollapsibleTrigger className="flex items-center gap-2" {...props}>
    {children ?? (
      <>
        <p className="font-medium">Used {count} sources</p>
        <ChevronDownIcon className="h-4 w-4" />
      </>
    )}
  </CollapsibleTrigger>
);

export type SourcesContentProps = ComponentProps<typeof CollapsibleContent>;

export const SourcesContent = ({
  className,
  ...props
}: SourcesContentProps) => (
  <CollapsibleContent
    className={cn(
      'mt-3 flex w-fit flex-col gap-2',
      'data-[state=closed]:fade-out-0 data-[state=closed]:slide-out-to-top-2 data-[state=open]:slide-in-from-top-2 outline-none data-[state=closed]:animate-out data-[state=open]:animate-in',
      className,
    )}
    {...props}
  />
);

export type SourceProps = ComponentProps<'a'>;

export const Source = ({ href, title, children, ...props }: SourceProps) => (
  <a
    className="flex items-center gap-2"
    href={href}
    rel="noreferrer"
    target="_blank"
    {...props}
  >
    {children ?? (
      <>
        <BookIcon className="h-4 w-4" />
        <span className="block font-medium">{title}</span>
      </>
    )}
  </a>
);



================================================
FILE: components/elements/suggestion.tsx
================================================
'use client';

import { Button } from '@/components/ui/button';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import type { ComponentProps } from 'react';

export type SuggestionsProps = ComponentProps<typeof ScrollArea>;

export const Suggestions = ({
  className,
  children,
  ...props
}: SuggestionsProps) => (
  <ScrollArea className="w-full overflow-x-auto whitespace-nowrap" {...props}>
    <div className={cn('flex w-max flex-nowrap items-center gap-2', className)}>
      {children}
    </div>
    <ScrollBar className="hidden" orientation="horizontal" />
  </ScrollArea>
);

export type SuggestionProps = Omit<ComponentProps<typeof Button>, 'onClick'> & {
  suggestion: string;
  onClick?: (suggestion: string) => void;
};

export const Suggestion = ({
  suggestion,
  onClick,
  className,
  variant = 'outline',
  size = 'sm',
  children,
  ...props
}: SuggestionProps) => {
  const handleClick = () => {
    onClick?.(suggestion);
  };

  return (
    <Button
      className={cn('cursor-pointer rounded-full px-4', className)}
      onClick={handleClick}
      size={size}
      type="button"
      variant={variant}
      {...props}
    >
      {children || suggestion}
    </Button>
  );
};



================================================
FILE: components/elements/task.tsx
================================================
'use client';

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { cn } from '@/lib/utils';
import { ChevronDownIcon, SearchIcon } from 'lucide-react';
import type { ComponentProps } from 'react';

export type TaskItemFileProps = ComponentProps<'div'>;

export const TaskItemFile = ({
  children,
  className,
  ...props
}: TaskItemFileProps) => (
  <div
    className={cn(
      'inline-flex items-center gap-1 rounded-md border bg-secondary px-1.5 py-0.5 text-foreground text-xs',
      className,
    )}
    {...props}
  >
    {children}
  </div>
);

export type TaskItemProps = ComponentProps<'div'>;

export const TaskItem = ({ children, className, ...props }: TaskItemProps) => (
  <div className={cn('text-muted-foreground text-sm', className)} {...props}>
    {children}
  </div>
);

export type TaskProps = ComponentProps<typeof Collapsible>;

export const Task = ({
  defaultOpen = true,
  className,
  ...props
}: TaskProps) => (
  <Collapsible
    className={cn(
      'data-[state=closed]:fade-out-0 data-[state=closed]:slide-out-to-top-2 data-[state=open]:slide-in-from-top-2 data-[state=closed]:animate-out data-[state=open]:animate-in',
      className,
    )}
    defaultOpen={defaultOpen}
    {...props}
  />
);

export type TaskTriggerProps = ComponentProps<typeof CollapsibleTrigger> & {
  title: string;
};

export const TaskTrigger = ({
  children,
  className,
  title,
  ...props
}: TaskTriggerProps) => (
  <CollapsibleTrigger asChild className={cn('group', className)} {...props}>
    {children ?? (
      <div className="flex cursor-pointer items-center gap-2 text-muted-foreground hover:text-foreground">
        <SearchIcon className="size-4" />
        <p className="text-sm">{title}</p>
        <ChevronDownIcon className="size-4 transition-transform group-data-[state=open]:rotate-180" />
      </div>
    )}
  </CollapsibleTrigger>
);

export type TaskContentProps = ComponentProps<typeof CollapsibleContent>;

export const TaskContent = ({
  children,
  className,
  ...props
}: TaskContentProps) => (
  <CollapsibleContent
    className={cn(
      'data-[state=closed]:fade-out-0 data-[state=closed]:slide-out-to-top-2 data-[state=open]:slide-in-from-top-2 text-popover-foreground outline-none data-[state=closed]:animate-out data-[state=open]:animate-in',
      className,
    )}
    {...props}
  >
    <div className="mt-4 space-y-2 border-muted border-l-2 pl-4">
      {children}
    </div>
  </CollapsibleContent>
);



================================================
FILE: components/elements/tool.tsx
================================================
'use client';

import { Badge } from '@/components/ui/badge';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { cn } from '@/lib/utils';
import type { ToolUIPart } from 'ai';
import {
  CheckCircleIcon,
  ChevronDownIcon,
  CircleIcon,
  ClockIcon,
  WrenchIcon,
  XCircleIcon,
} from 'lucide-react';
import type { ComponentProps, ReactNode } from 'react';
import { CodeBlock } from './code-block';

export type ToolProps = ComponentProps<typeof Collapsible>;

export const Tool = ({ className, ...props }: ToolProps) => (
  <Collapsible
    className={cn('not-prose mb-4 w-full rounded-md border', className)}
    {...props}
  />
);

export type ToolHeaderProps = {
  type: ToolUIPart['type'];
  state: ToolUIPart['state'];
  className?: string;
};

const getStatusBadge = (status: ToolUIPart['state']) => {
  const labels = {
    'input-streaming': 'Pending',
    'input-available': 'Running',
    'output-available': 'Completed',
    'output-error': 'Error',
  } as const;

  const icons = {
    'input-streaming': <CircleIcon className="size-4" />,
    'input-available': <ClockIcon className="size-4 animate-pulse" />,
    'output-available': <CheckCircleIcon className="size-4 text-green-600" />,
    'output-error': <XCircleIcon className="size-4 text-red-600" />,
  } as const;

  return (
    <Badge className="rounded-full text-xs flex items-center gap-1" variant="secondary">
      {icons[status]}
      <span>{labels[status]}</span>
    </Badge>
  );
};

export const ToolHeader = ({
  className,
  type,
  state,
  ...props
}: ToolHeaderProps) => (
  <CollapsibleTrigger
    className={cn(
      'flex w-full items-center justify-between gap-2 p-3 min-w-0',
      className,
    )}
    {...props}
  >
    <div className="flex items-center gap-2 min-w-0 flex-1">
      <WrenchIcon className="size-4 text-muted-foreground shrink-0" />
      <span className="font-medium text-sm truncate">{type}</span>
    </div>
    <div className="flex items-center gap-2 shrink-0">
      {getStatusBadge(state)}
      <ChevronDownIcon className="size-4 text-muted-foreground transition-transform group-data-[state=open]:rotate-180" />
    </div>
  </CollapsibleTrigger>
);

export type ToolContentProps = ComponentProps<typeof CollapsibleContent>;

export const ToolContent = ({ className, ...props }: ToolContentProps) => (
  <CollapsibleContent
    className={cn(
      'data-[state=closed]:fade-out-0 data-[state=closed]:slide-out-to-top-2 data-[state=open]:slide-in-from-top-2 text-popover-foreground outline-none data-[state=closed]:animate-out data-[state=open]:animate-in',
      className,
    )}
    {...props}
  />
);

export type ToolInputProps = ComponentProps<'div'> & {
  input: ToolUIPart['input'];
};

export const ToolInput = ({ className, input, ...props }: ToolInputProps) => (
  <div className={cn('space-y-2 overflow-hidden p-4', className)} {...props}>
    <h4 className="font-medium text-muted-foreground text-xs uppercase tracking-wide">
      Parameters
    </h4>
    <div className="rounded-md bg-muted/50">
      <CodeBlock code={JSON.stringify(input, null, 2)} language="json" />
    </div>
  </div>
);

export type ToolOutputProps = ComponentProps<'div'> & {
  output: ReactNode;
  errorText: ToolUIPart['errorText'];
};

export const ToolOutput = ({
  className,
  output,
  errorText,
  ...props
}: ToolOutputProps) => {
  if (!(output || errorText)) {
    return null;
  }

  return (
    <div className={cn('space-y-2 p-4', className)} {...props}>
      <h4 className="font-medium text-muted-foreground text-xs uppercase tracking-wide">
        {errorText ? 'Error' : 'Result'}
      </h4>
      <div
        className={cn(
          'overflow-x-auto rounded-md text-xs [&_table]:w-full',
          errorText
            ? 'bg-destructive/10 text-destructive'
            : 'bg-muted/50 text-foreground',
        )}
      >
        {errorText && <div>{errorText}</div>}
        {output && <div>{output}</div>}
      </div>
    </div>
  );
};



================================================
FILE: components/elements/web-preview.tsx
================================================
'use client';

import { Button } from '@/components/ui/button';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { Input } from '@/components/ui/input';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { cn } from '@/lib/utils';
import { ChevronDownIcon } from 'lucide-react';
import type { ComponentProps, ReactNode } from 'react';
import { createContext, useContext, useState } from 'react';

export type WebPreviewContextValue = {
  url: string;
  setUrl: (url: string) => void;
  consoleOpen: boolean;
  setConsoleOpen: (open: boolean) => void;
};

const WebPreviewContext = createContext<WebPreviewContextValue | null>(null);

const useWebPreview = () => {
  const context = useContext(WebPreviewContext);
  if (!context) {
    throw new Error('WebPreview components must be used within a WebPreview');
  }
  return context;
};

export type WebPreviewProps = ComponentProps<'div'> & {
  defaultUrl?: string;
  onUrlChange?: (url: string) => void;
};

export const WebPreview = ({
  className,
  children,
  defaultUrl = '',
  onUrlChange,
  ...props
}: WebPreviewProps) => {
  const [url, setUrl] = useState(defaultUrl);
  const [consoleOpen, setConsoleOpen] = useState(false);

  const handleUrlChange = (newUrl: string) => {
    setUrl(newUrl);
    onUrlChange?.(newUrl);
  };

  const contextValue: WebPreviewContextValue = {
    url,
    setUrl: handleUrlChange,
    consoleOpen,
    setConsoleOpen,
  };

  return (
    <WebPreviewContext.Provider value={contextValue}>
      <div
        className={cn(
          'flex size-full flex-col rounded-lg border bg-card',
          className,
        )}
        {...props}
      >
        {children}
      </div>
    </WebPreviewContext.Provider>
  );
};

export type WebPreviewNavigationProps = ComponentProps<'div'>;

export const WebPreviewNavigation = ({
  className,
  children,
  ...props
}: WebPreviewNavigationProps) => (
  <div
    className={cn('flex items-center gap-1 border-b p-2', className)}
    {...props}
  >
    {children}
  </div>
);

export type WebPreviewNavigationButtonProps = ComponentProps<typeof Button> & {
  tooltip?: string;
};

export const WebPreviewNavigationButton = ({
  onClick,
  disabled,
  tooltip,
  children,
  ...props
}: WebPreviewNavigationButtonProps) => (
  <TooltipProvider>
    <Tooltip>
      <TooltipTrigger asChild>
        <Button
          className="h-8 w-8 p-0 hover:text-foreground"
          disabled={disabled}
          onClick={onClick}
          size="sm"
          variant="ghost"
          {...props}
        >
          {children}
        </Button>
      </TooltipTrigger>
      <TooltipContent>
        <p>{tooltip}</p>
      </TooltipContent>
    </Tooltip>
  </TooltipProvider>
);

export type WebPreviewUrlProps = ComponentProps<typeof Input>;

export const WebPreviewUrl = ({
  value,
  onChange,
  onKeyDown,
  ...props
}: WebPreviewUrlProps) => {
  const { url, setUrl } = useWebPreview();

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      const target = event.target as HTMLInputElement;
      setUrl(target.value);
    }
    onKeyDown?.(event);
  };

  return (
    <Input
      className="h-8 flex-1 text-sm"
      onChange={onChange}
      onKeyDown={handleKeyDown}
      placeholder="Enter URL..."
      value={value ?? url}
      {...props}
    />
  );
};

export type WebPreviewBodyProps = ComponentProps<'iframe'> & {
  loading?: ReactNode;
};

export const WebPreviewBody = ({
  className,
  loading,
  src,
  ...props
}: WebPreviewBodyProps) => {
  const { url } = useWebPreview();

  return (
    <div className="flex-1">
      <iframe
        className={cn('size-full', className)}
        sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-presentation"
        src={(src ?? url) || undefined}
        title="Preview"
        {...props}
      />
      {loading}
    </div>
  );
};

export type WebPreviewConsoleProps = ComponentProps<'div'> & {
  logs?: Array<{
    level: 'log' | 'warn' | 'error';
    message: string;
    timestamp: Date;
  }>;
};

export const WebPreviewConsole = ({
  className,
  logs = [],
  children,
  ...props
}: WebPreviewConsoleProps) => {
  const { consoleOpen, setConsoleOpen } = useWebPreview();

  return (
    <Collapsible
      className={cn('border-t bg-muted/50 font-mono text-sm', className)}
      onOpenChange={setConsoleOpen}
      open={consoleOpen}
      {...props}
    >
      <CollapsibleTrigger asChild>
        <Button
          className="flex w-full items-center justify-between p-4 text-left font-medium hover:bg-muted/50"
          variant="ghost"
        >
          Console
          <ChevronDownIcon
            className={cn(
              'h-4 w-4 transition-transform duration-200',
              consoleOpen && 'rotate-180',
            )}
          />
        </Button>
      </CollapsibleTrigger>
      <CollapsibleContent
        className={cn(
          'px-4 pb-4',
          'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 outline-none data-[state=closed]:animate-out data-[state=open]:animate-in',
        )}
      >
        <div className="max-h-48 space-y-1 overflow-y-auto">
          {logs.length === 0 ? (
            <p className="text-muted-foreground">No console output</p>
          ) : (
            logs.map((log, index) => (
              <div
                className={cn(
                  'text-xs',
                  log.level === 'error' && 'text-destructive',
                  log.level === 'warn' && 'text-yellow-600',
                  log.level === 'log' && 'text-foreground',
                )}
                key={`${log.timestamp.getTime()}-${index}`}
              >
                <span className="text-muted-foreground">
                  {log.timestamp.toLocaleTimeString()}
                </span>{' '}
                {log.message}
              </div>
            ))
          )}
          {children}
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
};



================================================
FILE: components/ui/alert-dialog.tsx
================================================
'use client';

import * as React from 'react';
import * as AlertDialogPrimitive from '@radix-ui/react-alert-dialog';

import { cn } from '@/lib/utils';
import { buttonVariants } from '@/components/ui/button';

const AlertDialog = AlertDialogPrimitive.Root;

const AlertDialogTrigger = AlertDialogPrimitive.Trigger;

const AlertDialogPortal = AlertDialogPrimitive.Portal;

const AlertDialogOverlay = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Overlay
    className={cn(
      'fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
      className,
    )}
    {...props}
    ref={ref}
  />
));
AlertDialogOverlay.displayName = AlertDialogPrimitive.Overlay.displayName;

const AlertDialogContent = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Content>
>(({ className, ...props }, ref) => (
  <AlertDialogPortal>
    <AlertDialogOverlay />
    <AlertDialogPrimitive.Content
      ref={ref}
      className={cn(
        'fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg',
        className,
      )}
      {...props}
    />
  </AlertDialogPortal>
));
AlertDialogContent.displayName = AlertDialogPrimitive.Content.displayName;

const AlertDialogHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      'flex flex-col space-y-2 text-center sm:text-left',
      className,
    )}
    {...props}
  />
);
AlertDialogHeader.displayName = 'AlertDialogHeader';

const AlertDialogFooter = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      'flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2',
      className,
    )}
    {...props}
  />
);
AlertDialogFooter.displayName = 'AlertDialogFooter';

const AlertDialogTitle = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Title
    ref={ref}
    className={cn('text-lg font-semibold', className)}
    {...props}
  />
));
AlertDialogTitle.displayName = AlertDialogPrimitive.Title.displayName;

const AlertDialogDescription = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Description
    ref={ref}
    className={cn('text-sm text-muted-foreground', className)}
    {...props}
  />
));
AlertDialogDescription.displayName =
  AlertDialogPrimitive.Description.displayName;

const AlertDialogAction = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Action>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Action>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Action
    ref={ref}
    className={cn(buttonVariants(), className)}
    {...props}
  />
));
AlertDialogAction.displayName = AlertDialogPrimitive.Action.displayName;

const AlertDialogCancel = React.forwardRef<
  React.ElementRef<typeof AlertDialogPrimitive.Cancel>,
  React.ComponentPropsWithoutRef<typeof AlertDialogPrimitive.Cancel>
>(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Cancel
    ref={ref}
    className={cn(
      buttonVariants({ variant: 'outline' }),
      'mt-2 sm:mt-0',
      className,
    )}
    {...props}
  />
));
AlertDialogCancel.displayName = AlertDialogPrimitive.Cancel.displayName;

export {
  AlertDialog,
  AlertDialogPortal,
  AlertDialogOverlay,
  AlertDialogTrigger,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogFooter,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogAction,
  AlertDialogCancel,
};



================================================
FILE: components/ui/avatar.tsx
================================================
"use client"

import * as React from "react"
import * as AvatarPrimitive from "@radix-ui/react-avatar"

import { cn } from "@/lib/utils"

const Avatar = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Root
    ref={ref}
    className={cn(
      "relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full",
      className
    )}
    {...props}
  />
))
Avatar.displayName = AvatarPrimitive.Root.displayName

const AvatarImage = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Image>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Image>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Image
    ref={ref}
    className={cn("aspect-square h-full w-full", className)}
    {...props}
  />
))
AvatarImage.displayName = AvatarPrimitive.Image.displayName

const AvatarFallback = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Fallback>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Fallback>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Fallback
    ref={ref}
    className={cn(
      "flex h-full w-full items-center justify-center rounded-full bg-muted",
      className
    )}
    {...props}
  />
))
AvatarFallback.displayName = AvatarPrimitive.Fallback.displayName

export { Avatar, AvatarImage, AvatarFallback }



================================================
FILE: components/ui/badge.tsx
================================================
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
        secondary:
          "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive:
          "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
        outline: "text-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }



================================================
FILE: components/ui/button.tsx
================================================
import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive:
          'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline:
          'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary:
          'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  },
);
Button.displayName = 'Button';

export { Button, buttonVariants };



================================================
FILE: components/ui/card.tsx
================================================
import * as React from 'react';

import { cn } from '@/lib/utils';

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'rounded-lg border bg-card text-card-foreground shadow-sm',
      className,
    )}
    {...props}
  />
));
Card.displayName = 'Card';

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex flex-col space-y-1.5 p-6', className)}
    {...props}
  />
));
CardHeader.displayName = 'CardHeader';

const CardTitle = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'text-2xl font-semibold leading-none tracking-tight',
      className,
    )}
    {...props}
  />
));
CardTitle.displayName = 'CardTitle';

const CardDescription = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('text-sm text-muted-foreground', className)}
    {...props}
  />
));
CardDescription.displayName = 'CardDescription';

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
));
CardContent.displayName = 'CardContent';

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex items-center p-6 pt-0', className)}
    {...props}
  />
));
CardFooter.displayName = 'CardFooter';

export {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardDescription,
  CardContent,
};



================================================
FILE: components/ui/carousel.tsx
================================================
"use client"

import * as React from "react"
import useEmblaCarousel, {
  type UseEmblaCarouselType,
} from "embla-carousel-react"
import { ArrowLeft, ArrowRight } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

type CarouselApi = UseEmblaCarouselType[1]
type UseCarouselParameters = Parameters<typeof useEmblaCarousel>
type CarouselOptions = UseCarouselParameters[0]
type CarouselPlugin = UseCarouselParameters[1]

type CarouselProps = {
  opts?: CarouselOptions
  plugins?: CarouselPlugin
  orientation?: "horizontal" | "vertical"
  setApi?: (api: CarouselApi) => void
}

type CarouselContextProps = {
  carouselRef: ReturnType<typeof useEmblaCarousel>[0]
  api: ReturnType<typeof useEmblaCarousel>[1]
  scrollPrev: () => void
  scrollNext: () => void
  canScrollPrev: boolean
  canScrollNext: boolean
} & CarouselProps

const CarouselContext = React.createContext<CarouselContextProps | null>(null)

function useCarousel() {
  const context = React.useContext(CarouselContext)

  if (!context) {
    throw new Error("useCarousel must be used within a <Carousel />")
  }

  return context
}

const Carousel = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & CarouselProps
>(
  (
    {
      orientation = "horizontal",
      opts,
      setApi,
      plugins,
      className,
      children,
      ...props
    },
    ref
  ) => {
    const [carouselRef, api] = useEmblaCarousel(
      {
        ...opts,
        axis: orientation === "horizontal" ? "x" : "y",
      },
      plugins
    )
    const [canScrollPrev, setCanScrollPrev] = React.useState(false)
    const [canScrollNext, setCanScrollNext] = React.useState(false)

    const onSelect = React.useCallback((api: CarouselApi) => {
      if (!api) {
        return
      }

      setCanScrollPrev(api.canScrollPrev())
      setCanScrollNext(api.canScrollNext())
    }, [])

    const scrollPrev = React.useCallback(() => {
      api?.scrollPrev()
    }, [api])

    const scrollNext = React.useCallback(() => {
      api?.scrollNext()
    }, [api])

    const handleKeyDown = React.useCallback(
      (event: React.KeyboardEvent<HTMLDivElement>) => {
        if (event.key === "ArrowLeft") {
          event.preventDefault()
          scrollPrev()
        } else if (event.key === "ArrowRight") {
          event.preventDefault()
          scrollNext()
        }
      },
      [scrollPrev, scrollNext]
    )

    React.useEffect(() => {
      if (!api || !setApi) {
        return
      }

      setApi(api)
    }, [api, setApi])

    React.useEffect(() => {
      if (!api) {
        return
      }

      onSelect(api)
      api.on("reInit", onSelect)
      api.on("select", onSelect)

      return () => {
        api?.off("select", onSelect)
      }
    }, [api, onSelect])

    return (
      <CarouselContext.Provider
        value={{
          carouselRef,
          api: api,
          opts,
          orientation:
            orientation || (opts?.axis === "y" ? "vertical" : "horizontal"),
          scrollPrev,
          scrollNext,
          canScrollPrev,
          canScrollNext,
        }}
      >
        <div
          ref={ref}
          onKeyDownCapture={handleKeyDown}
          className={cn("relative", className)}
          role="region"
          aria-roledescription="carousel"
          {...props}
        >
          {children}
        </div>
      </CarouselContext.Provider>
    )
  }
)
Carousel.displayName = "Carousel"

const CarouselContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
  const { carouselRef, orientation } = useCarousel()

  return (
    <div ref={carouselRef} className="overflow-hidden">
      <div
        ref={ref}
        className={cn(
          "flex",
          orientation === "horizontal" ? "-ml-4" : "-mt-4 flex-col",
          className
        )}
        {...props}
      />
    </div>
  )
})
CarouselContent.displayName = "CarouselContent"

const CarouselItem = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
  const { orientation } = useCarousel()

  return (
    <div
      ref={ref}
      role="group"
      aria-roledescription="slide"
      className={cn(
        "min-w-0 shrink-0 grow-0 basis-full",
        orientation === "horizontal" ? "pl-4" : "pt-4",
        className
      )}
      {...props}
    />
  )
})
CarouselItem.displayName = "CarouselItem"

const CarouselPrevious = React.forwardRef<
  HTMLButtonElement,
  React.ComponentProps<typeof Button>
>(({ className, variant = "outline", size = "icon", ...props }, ref) => {
  const { orientation, scrollPrev, canScrollPrev } = useCarousel()

  return (
    <Button
      ref={ref}
      variant={variant}
      size={size}
      className={cn(
        "absolute  h-8 w-8 rounded-full",
        orientation === "horizontal"
          ? "-left-12 top-1/2 -translate-y-1/2"
          : "-top-12 left-1/2 -translate-x-1/2 rotate-90",
        className
      )}
      disabled={!canScrollPrev}
      onClick={scrollPrev}
      {...props}
    >
      <ArrowLeft className="h-4 w-4" />
      <span className="sr-only">Previous slide</span>
    </Button>
  )
})
CarouselPrevious.displayName = "CarouselPrevious"

const CarouselNext = React.forwardRef<
  HTMLButtonElement,
  React.ComponentProps<typeof Button>
>(({ className, variant = "outline", size = "icon", ...props }, ref) => {
  const { orientation, scrollNext, canScrollNext } = useCarousel()

  return (
    <Button
      ref={ref}
      variant={variant}
      size={size}
      className={cn(
        "absolute h-8 w-8 rounded-full",
        orientation === "horizontal"
          ? "-right-12 top-1/2 -translate-y-1/2"
          : "-bottom-12 left-1/2 -translate-x-1/2 rotate-90",
        className
      )}
      disabled={!canScrollNext}
      onClick={scrollNext}
      {...props}
    >
      <ArrowRight className="h-4 w-4" />
      <span className="sr-only">Next slide</span>
    </Button>
  )
})
CarouselNext.displayName = "CarouselNext"

export {
  type CarouselApi,
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselPrevious,
  CarouselNext,
}



================================================
FILE: components/ui/collapsible.tsx
================================================
"use client"

import * as CollapsiblePrimitive from "@radix-ui/react-collapsible"

const Collapsible = CollapsiblePrimitive.Root

const CollapsibleTrigger = CollapsiblePrimitive.CollapsibleTrigger

const CollapsibleContent = CollapsiblePrimitive.CollapsibleContent

export { Collapsible, CollapsibleTrigger, CollapsibleContent }



================================================
FILE: components/ui/dropdown-menu.tsx
================================================
'use client';

import * as React from 'react';
import * as DropdownMenuPrimitive from '@radix-ui/react-dropdown-menu';
import { Check, ChevronRight, Circle } from 'lucide-react';

import { cn } from '@/lib/utils';

const DropdownMenu = DropdownMenuPrimitive.Root;

const DropdownMenuTrigger = DropdownMenuPrimitive.Trigger;

const DropdownMenuGroup = DropdownMenuPrimitive.Group;

const DropdownMenuPortal = DropdownMenuPrimitive.Portal;

const DropdownMenuSub = DropdownMenuPrimitive.Sub;

const DropdownMenuRadioGroup = DropdownMenuPrimitive.RadioGroup;

const DropdownMenuSubTrigger = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.SubTrigger>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.SubTrigger> & {
    inset?: boolean;
  }
>(({ className, inset, children, ...props }, ref) => (
  <DropdownMenuPrimitive.SubTrigger
    ref={ref}
    className={cn(
      'flex cursor-default gap-2 select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent data-[state=open]:bg-accent [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0',
      inset && 'pl-8',
      className,
    )}
    {...props}
  >
    {children}
    <ChevronRight className="ml-auto" />
  </DropdownMenuPrimitive.SubTrigger>
));
DropdownMenuSubTrigger.displayName =
  DropdownMenuPrimitive.SubTrigger.displayName;

const DropdownMenuSubContent = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.SubContent>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.SubContent>
>(({ className, ...props }, ref) => (
  <DropdownMenuPrimitive.SubContent
    ref={ref}
    className={cn(
      'z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
      className,
    )}
    {...props}
  />
));
DropdownMenuSubContent.displayName =
  DropdownMenuPrimitive.SubContent.displayName;

const DropdownMenuContent = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Content>
>(({ className, sideOffset = 4, ...props }, ref) => (
  <DropdownMenuPrimitive.Portal>
    <DropdownMenuPrimitive.Content
      ref={ref}
      sideOffset={sideOffset}
      className={cn(
        'z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
        className,
      )}
      {...props}
    />
  </DropdownMenuPrimitive.Portal>
));
DropdownMenuContent.displayName = DropdownMenuPrimitive.Content.displayName;

const DropdownMenuItem = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Item> & {
    inset?: boolean;
  }
>(({ className, inset, ...props }, ref) => (
  <DropdownMenuPrimitive.Item
    ref={ref}
    className={cn(
      'relative flex cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0',
      inset && 'pl-8',
      className,
    )}
    {...props}
  />
));
DropdownMenuItem.displayName = DropdownMenuPrimitive.Item.displayName;

const DropdownMenuCheckboxItem = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.CheckboxItem>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.CheckboxItem>
>(({ className, children, checked, ...props }, ref) => (
  <DropdownMenuPrimitive.CheckboxItem
    ref={ref}
    className={cn(
      'relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
      className,
    )}
    checked={checked}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <DropdownMenuPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </DropdownMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </DropdownMenuPrimitive.CheckboxItem>
));
DropdownMenuCheckboxItem.displayName =
  DropdownMenuPrimitive.CheckboxItem.displayName;

const DropdownMenuRadioItem = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.RadioItem>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.RadioItem>
>(({ className, children, ...props }, ref) => (
  <DropdownMenuPrimitive.RadioItem
    ref={ref}
    className={cn(
      'relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
      className,
    )}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <DropdownMenuPrimitive.ItemIndicator>
        <Circle className="h-2 w-2 fill-current" />
      </DropdownMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </DropdownMenuPrimitive.RadioItem>
));
DropdownMenuRadioItem.displayName = DropdownMenuPrimitive.RadioItem.displayName;

const DropdownMenuLabel = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Label> & {
    inset?: boolean;
  }
>(({ className, inset, ...props }, ref) => (
  <DropdownMenuPrimitive.Label
    ref={ref}
    className={cn(
      'px-2 py-1.5 text-sm font-semibold',
      inset && 'pl-8',
      className,
    )}
    {...props}
  />
));
DropdownMenuLabel.displayName = DropdownMenuPrimitive.Label.displayName;

const DropdownMenuSeparator = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <DropdownMenuPrimitive.Separator
    ref={ref}
    className={cn('-mx-1 my-1 h-px bg-muted', className)}
    {...props}
  />
));
DropdownMenuSeparator.displayName = DropdownMenuPrimitive.Separator.displayName;

const DropdownMenuShortcut = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLSpanElement>) => {
  return (
    <span
      className={cn('ml-auto text-xs tracking-widest opacity-60', className)}
      {...props}
    />
  );
};
DropdownMenuShortcut.displayName = 'DropdownMenuShortcut';

export {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuCheckboxItem,
  DropdownMenuRadioItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuGroup,
  DropdownMenuPortal,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuRadioGroup,
};



================================================
FILE: components/ui/hover-card.tsx
================================================
"use client"

import * as React from "react"
import * as HoverCardPrimitive from "@radix-ui/react-hover-card"

import { cn } from "@/lib/utils"

const HoverCard = HoverCardPrimitive.Root

const HoverCardTrigger = HoverCardPrimitive.Trigger

const HoverCardContent = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Content>
>(({ className, align = "center", sideOffset = 4, ...props }, ref) => (
  <HoverCardPrimitive.Content
    ref={ref}
    align={align}
    sideOffset={sideOffset}
    className={cn(
      "z-50 w-64 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-hover-card-content-transform-origin]",
      className
    )}
    {...props}
  />
))
HoverCardContent.displayName = HoverCardPrimitive.Content.displayName

export { HoverCard, HoverCardTrigger, HoverCardContent }



================================================
FILE: components/ui/input.tsx
================================================
import * as React from 'react';

import { cn } from '@/lib/utils';

const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<'input'>>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-base ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm',
          className,
        )}
        ref={ref}
        {...props}
      />
    );
  },
);
Input.displayName = 'Input';

export { Input };



================================================
FILE: components/ui/label.tsx
================================================
'use client';

import * as React from 'react';
import * as LabelPrimitive from '@radix-ui/react-label';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/lib/utils';

const labelVariants = cva(
  'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
);

const Label = React.forwardRef<
  React.ElementRef<typeof LabelPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root> &
    VariantProps<typeof labelVariants>
>(({ className, ...props }, ref) => (
  <LabelPrimitive.Root
    ref={ref}
    className={cn(labelVariants(), className)}
    {...props}
  />
));
Label.displayName = LabelPrimitive.Root.displayName;

export { Label };



================================================
FILE: components/ui/scroll-area.tsx
================================================
"use client"

import * as React from "react"
import * as ScrollAreaPrimitive from "@radix-ui/react-scroll-area"

import { cn } from "@/lib/utils"

const ScrollArea = React.forwardRef<
  React.ElementRef<typeof ScrollAreaPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof ScrollAreaPrimitive.Root>
>(({ className, children, ...props }, ref) => (
  <ScrollAreaPrimitive.Root
    ref={ref}
    className={cn("relative overflow-hidden", className)}
    {...props}
  >
    <ScrollAreaPrimitive.Viewport className="h-full w-full rounded-[inherit]">
      {children}
    </ScrollAreaPrimitive.Viewport>
    <ScrollBar />
    <ScrollAreaPrimitive.Corner />
  </ScrollAreaPrimitive.Root>
))
ScrollArea.displayName = ScrollAreaPrimitive.Root.displayName

const ScrollBar = React.forwardRef<
  React.ElementRef<typeof ScrollAreaPrimitive.ScrollAreaScrollbar>,
  React.ComponentPropsWithoutRef<typeof ScrollAreaPrimitive.ScrollAreaScrollbar>
>(({ className, orientation = "vertical", ...props }, ref) => (
  <ScrollAreaPrimitive.ScrollAreaScrollbar
    ref={ref}
    orientation={orientation}
    className={cn(
      "flex touch-none select-none transition-colors",
      orientation === "vertical" &&
        "h-full w-2.5 border-l border-l-transparent p-[1px]",
      orientation === "horizontal" &&
        "h-2.5 flex-col border-t border-t-transparent p-[1px]",
      className
    )}
    {...props}
  >
    <ScrollAreaPrimitive.ScrollAreaThumb className="relative flex-1 rounded-full bg-border" />
  </ScrollAreaPrimitive.ScrollAreaScrollbar>
))
ScrollBar.displayName = ScrollAreaPrimitive.ScrollAreaScrollbar.displayName

export { ScrollArea, ScrollBar }



================================================
FILE: components/ui/select.tsx
================================================
'use client';

import * as React from 'react';
import * as SelectPrimitive from '@radix-ui/react-select';
import { Check, ChevronDown, ChevronUp } from 'lucide-react';

import { cn } from '@/lib/utils';

const Select = SelectPrimitive.Root;

const SelectGroup = SelectPrimitive.Group;

const SelectValue = SelectPrimitive.Value;

const SelectTrigger = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Trigger
    ref={ref}
    className={cn(
      'flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1',
      className,
    )}
    {...props}
  >
    {children}
    <SelectPrimitive.Icon asChild>
      <ChevronDown className="h-4 w-4 opacity-50" />
    </SelectPrimitive.Icon>
  </SelectPrimitive.Trigger>
));
SelectTrigger.displayName = SelectPrimitive.Trigger.displayName;

const SelectScrollUpButton = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.ScrollUpButton>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollUpButton>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollUpButton
    ref={ref}
    className={cn(
      'flex cursor-default items-center justify-center py-1',
      className,
    )}
    {...props}
  >
    <ChevronUp className="h-4 w-4" />
  </SelectPrimitive.ScrollUpButton>
));
SelectScrollUpButton.displayName = SelectPrimitive.ScrollUpButton.displayName;

const SelectScrollDownButton = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.ScrollDownButton>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollDownButton>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollDownButton
    ref={ref}
    className={cn(
      'flex cursor-default items-center justify-center py-1',
      className,
    )}
    {...props}
  >
    <ChevronDown className="h-4 w-4" />
  </SelectPrimitive.ScrollDownButton>
));
SelectScrollDownButton.displayName =
  SelectPrimitive.ScrollDownButton.displayName;

const SelectContent = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Content>
>(({ className, children, position = 'popper', ...props }, ref) => (
  <SelectPrimitive.Portal>
    <SelectPrimitive.Content
      ref={ref}
      className={cn(
        'relative z-50 max-h-96 min-w-[8rem] overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
        position === 'popper' &&
          'data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1',
        className,
      )}
      position={position}
      {...props}
    >
      <SelectScrollUpButton />
      <SelectPrimitive.Viewport
        className={cn(
          'p-1',
          position === 'popper' &&
            'h-[var(--radix-select-trigger-height)] w-full min-w-[var(--radix-select-trigger-width)]',
        )}
      >
        {children}
      </SelectPrimitive.Viewport>
      <SelectScrollDownButton />
    </SelectPrimitive.Content>
  </SelectPrimitive.Portal>
));
SelectContent.displayName = SelectPrimitive.Content.displayName;

const SelectLabel = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Label>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Label
    ref={ref}
    className={cn('py-1.5 pl-8 pr-2 text-sm font-semibold', className)}
    {...props}
  />
));
SelectLabel.displayName = SelectPrimitive.Label.displayName;

const SelectItem = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Item>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Item
    ref={ref}
    className={cn(
      'relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
      className,
    )}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <SelectPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </SelectPrimitive.ItemIndicator>
    </span>

    <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
  </SelectPrimitive.Item>
));
SelectItem.displayName = SelectPrimitive.Item.displayName;

const SelectSeparator = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Separator
    ref={ref}
    className={cn('-mx-1 my-1 h-px bg-muted', className)}
    {...props}
  />
));
SelectSeparator.displayName = SelectPrimitive.Separator.displayName;

export {
  Select,
  SelectGroup,
  SelectValue,
  SelectTrigger,
  SelectContent,
  SelectLabel,
  SelectItem,
  SelectSeparator,
  SelectScrollUpButton,
  SelectScrollDownButton,
};



================================================
FILE: components/ui/separator.tsx
================================================
'use client';

import * as React from 'react';
import * as SeparatorPrimitive from '@radix-ui/react-separator';

import { cn } from '@/lib/utils';

const Separator = React.forwardRef<
  React.ElementRef<typeof SeparatorPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof SeparatorPrimitive.Root>
>(
  (
    { className, orientation = 'horizontal', decorative = true, ...props },
    ref,
  ) => (
    <SeparatorPrimitive.Root
      ref={ref}
      decorative={decorative}
      orientation={orientation}
      className={cn(
        'shrink-0 bg-border',
        orientation === 'horizontal' ? 'h-[1px] w-full' : 'h-full w-[1px]',
        className,
      )}
      {...props}
    />
  ),
);
Separator.displayName = SeparatorPrimitive.Root.displayName;

export { Separator };



================================================
FILE: components/ui/sheet.tsx
================================================
'use client';

import * as React from 'react';
import * as SheetPrimitive from '@radix-ui/react-dialog';
import { cva, type VariantProps } from 'class-variance-authority';
import { X } from 'lucide-react';

import { cn } from '@/lib/utils';

const Sheet = SheetPrimitive.Root;

const SheetTrigger = SheetPrimitive.Trigger;

const SheetClose = SheetPrimitive.Close;

const SheetPortal = SheetPrimitive.Portal;

const SheetOverlay = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <SheetPrimitive.Overlay
    className={cn(
      'fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
      className,
    )}
    {...props}
    ref={ref}
  />
));
SheetOverlay.displayName = SheetPrimitive.Overlay.displayName;

const sheetVariants = cva(
  'fixed z-50 gap-4 bg-background p-6 shadow-lg transition ease-in-out data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:duration-300 data-[state=open]:duration-500',
  {
    variants: {
      side: {
        top: 'inset-x-0 top-0 border-b data-[state=closed]:slide-out-to-top data-[state=open]:slide-in-from-top',
        bottom:
          'inset-x-0 bottom-0 border-t data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom',
        left: 'inset-y-0 left-0 h-full w-3/4 border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left sm:max-w-sm',
        right:
          'inset-y-0 right-0 h-full w-3/4  border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right sm:max-w-sm',
      },
    },
    defaultVariants: {
      side: 'right',
    },
  },
);

interface SheetContentProps
  extends React.ComponentPropsWithoutRef<typeof SheetPrimitive.Content>,
    VariantProps<typeof sheetVariants> {}

const SheetContent = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Content>,
  SheetContentProps
>(({ side = 'right', className, children, ...props }, ref) => (
  <SheetPortal>
    <SheetOverlay />
    <SheetPrimitive.Content
      ref={ref}
      className={cn(sheetVariants({ side }), className)}
      {...props}
    >
      {children}
      <SheetPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-secondary">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </SheetPrimitive.Close>
    </SheetPrimitive.Content>
  </SheetPortal>
));
SheetContent.displayName = SheetPrimitive.Content.displayName;

const SheetHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      'flex flex-col space-y-2 text-center sm:text-left',
      className,
    )}
    {...props}
  />
);
SheetHeader.displayName = 'SheetHeader';

const SheetFooter = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      'flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2',
      className,
    )}
    {...props}
  />
);
SheetFooter.displayName = 'SheetFooter';

const SheetTitle = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Title>
>(({ className, ...props }, ref) => (
  <SheetPrimitive.Title
    ref={ref}
    className={cn('text-lg font-semibold text-foreground', className)}
    {...props}
  />
));
SheetTitle.displayName = SheetPrimitive.Title.displayName;

const SheetDescription = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Description>
>(({ className, ...props }, ref) => (
  <SheetPrimitive.Description
    ref={ref}
    className={cn('text-sm text-muted-foreground', className)}
    {...props}
  />
));
SheetDescription.displayName = SheetPrimitive.Description.displayName;

export {
  Sheet,
  SheetPortal,
  SheetOverlay,
  SheetTrigger,
  SheetClose,
  SheetContent,
  SheetHeader,
  SheetFooter,
  SheetTitle,
  SheetDescription,
};



================================================
FILE: components/ui/sidebar.tsx
================================================
'use client';

import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { type VariantProps, cva } from 'class-variance-authority';
import { PanelLeft } from 'lucide-react';

import { useIsMobile } from '@/hooks/use-mobile';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { Sheet, SheetContent } from '@/components/ui/sheet';
import { Skeleton } from '@/components/ui/skeleton';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

const SIDEBAR_COOKIE_NAME = 'sidebar:state';
const SIDEBAR_COOKIE_MAX_AGE = 60 * 60 * 24 * 7;
const SIDEBAR_WIDTH = '16rem';
const SIDEBAR_WIDTH_MOBILE = '18rem';
const SIDEBAR_WIDTH_ICON = '3rem';
const SIDEBAR_KEYBOARD_SHORTCUT = 'b';

type SidebarContext = {
  state: 'expanded' | 'collapsed';
  open: boolean;
  setOpen: (open: boolean) => void;
  openMobile: boolean;
  setOpenMobile: (open: boolean) => void;
  isMobile: boolean;
  toggleSidebar: () => void;
};

const SidebarContext = React.createContext<SidebarContext | null>(null);

function useSidebar() {
  const context = React.useContext(SidebarContext);
  if (!context) {
    throw new Error('useSidebar must be used within a SidebarProvider.');
  }

  return context;
}

const SidebarProvider = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<'div'> & {
    defaultOpen?: boolean;
    open?: boolean;
    onOpenChange?: (open: boolean) => void;
  }
>(
  (
    {
      defaultOpen = true,
      open: openProp,
      onOpenChange: setOpenProp,
      className,
      style,
      children,
      ...props
    },
    ref,
  ) => {
    const isMobile = useIsMobile();
    const [openMobile, setOpenMobile] = React.useState(false);

    // This is the internal state of the sidebar.
    // We use openProp and setOpenProp for control from outside the component.
    const [_open, _setOpen] = React.useState(defaultOpen);
    const open = openProp ?? _open;
    const setOpen = React.useCallback(
      (value: boolean | ((value: boolean) => boolean)) => {
        const openState = typeof value === 'function' ? value(open) : value;
        if (setOpenProp) {
          setOpenProp(openState);
        } else {
          _setOpen(openState);
        }

        // This sets the cookie to keep the sidebar state.
        document.cookie = `${SIDEBAR_COOKIE_NAME}=${openState}; path=/; max-age=${SIDEBAR_COOKIE_MAX_AGE}`;
      },
      [setOpenProp, open],
    );

    // Helper to toggle the sidebar.
    const toggleSidebar = React.useCallback(() => {
      return isMobile
        ? setOpenMobile((open) => !open)
        : setOpen((open) => !open);
    }, [isMobile, setOpen, setOpenMobile]);

    // Adds a keyboard shortcut to toggle the sidebar.
    React.useEffect(() => {
      const handleKeyDown = (event: KeyboardEvent) => {
        if (
          event.key === SIDEBAR_KEYBOARD_SHORTCUT &&
          (event.metaKey || event.ctrlKey)
        ) {
          event.preventDefault();
          toggleSidebar();
        }
      };

      window.addEventListener('keydown', handleKeyDown);
      return () => window.removeEventListener('keydown', handleKeyDown);
    }, [toggleSidebar]);

    // We add a state so that we can do data-state="expanded" or "collapsed".
    // This makes it easier to style the sidebar with Tailwind classes.
    const state = open ? 'expanded' : 'collapsed';

    const contextValue = React.useMemo<SidebarContext>(
      () => ({
        state,
        open,
        setOpen,
        isMobile,
        openMobile,
        setOpenMobile,
        toggleSidebar,
      }),
      [
        state,
        open,
        setOpen,
        isMobile,
        openMobile,
        setOpenMobile,
        toggleSidebar,
      ],
    );

    return (
      <SidebarContext.Provider value={contextValue}>
        <TooltipProvider delayDuration={0}>
          <div
            style={
              {
                '--sidebar-width': SIDEBAR_WIDTH,
                '--sidebar-width-icon': SIDEBAR_WIDTH_ICON,
                ...style,
              } as React.CSSProperties
            }
            className={cn(
              'group/sidebar-wrapper flex min-h-svh w-full has-[[data-variant=inset]]:bg-sidebar',
              className,
            )}
            ref={ref}
            {...props}
          >
            {children}
          </div>
        </TooltipProvider>
      </SidebarContext.Provider>
    );
  },
);
SidebarProvider.displayName = 'SidebarProvider';

const Sidebar = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<'div'> & {
    side?: 'left' | 'right';
    variant?: 'sidebar' | 'floating' | 'inset';
    collapsible?: 'offcanvas' | 'icon' | 'none';
  }
>(
  (
    {
      side = 'left',
      variant = 'sidebar',
      collapsible = 'offcanvas',
      className,
      children,
      ...props
    },
    ref,
  ) => {
    const { isMobile, state, openMobile, setOpenMobile } = useSidebar();

    if (collapsible === 'none') {
      return (
        <div
          className={cn(
            'flex h-full w-[--sidebar-width] flex-col bg-sidebar text-sidebar-foreground',
            className,
          )}
          ref={ref}
          {...props}
        >
          {children}
        </div>
      );
    }

    if (isMobile) {
      return (
        <Sheet open={openMobile} onOpenChange={setOpenMobile} {...props}>
          <SheetContent
            data-sidebar="sidebar"
            data-mobile="true"
            className="w-[--sidebar-width] bg-sidebar p-0 text-sidebar-foreground [&>button]:hidden"
            style={
              {
                '--sidebar-width': SIDEBAR_WIDTH_MOBILE,
              } as React.CSSProperties
            }
            side={side}
          >
            <div className="flex h-full w-full flex-col">{children}</div>
          </SheetContent>
        </Sheet>
      );
    }

    return (
      <div
        ref={ref}
        className="group peer hidden md:block text-sidebar-foreground"
        data-state={state}
        data-collapsible={state === 'collapsed' ? collapsible : ''}
        data-variant={variant}
        data-side={side}
      >
        {/* This is what handles the sidebar gap on desktop */}
        <div
          className={cn(
            'duration-200 relative h-svh w-[--sidebar-width] bg-transparent transition-[width] ease-linear',
            'group-data-[collapsible=offcanvas]:w-0',
            'group-data-[side=right]:rotate-180',
            variant === 'floating' || variant === 'inset'
              ? 'group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)_+_theme(spacing.4))]'
              : 'group-data-[collapsible=icon]:w-[--sidebar-width-icon]',
          )}
        />
        <div
          className={cn(
            'duration-200 fixed inset-y-0 z-10 hidden h-svh w-[--sidebar-width] transition-[left,right,width] ease-linear md:flex',
            side === 'left'
              ? 'left-0 group-data-[collapsible=offcanvas]:left-[calc(var(--sidebar-width)*-1)]'
              : 'right-0 group-data-[collapsible=offcanvas]:right-[calc(var(--sidebar-width)*-1)]',
            // Adjust the padding for floating and inset variants.
            variant === 'floating' || variant === 'inset'
              ? 'p-2 group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)_+_theme(spacing.4)_+2px)]'
              : 'group-data-[collapsible=icon]:w-[--sidebar-width-icon] group-data-[side=left]:border-r group-data-[side=right]:border-l',
            className,
          )}
          {...props}
        >
          <div
            data-sidebar="sidebar"
            className="flex h-full w-full flex-col bg-sidebar group-data-[variant=floating]:rounded-lg group-data-[variant=floating]:border group-data-[variant=floating]:border-sidebar-border group-data-[variant=floating]:shadow"
          >
            {children}
          </div>
        </div>
      </div>
    );
  },
);
Sidebar.displayName = 'Sidebar';

const SidebarTrigger = React.forwardRef<
  React.ElementRef<typeof Button>,
  React.ComponentProps<typeof Button>
>(({ className, onClick, ...props }, ref) => {
  const { toggleSidebar } = useSidebar();

  return (
    <Button
      ref={ref}
      data-sidebar="trigger"
      variant="ghost"
      size="icon"
      className={cn('h-7 w-7', className)}
      onClick={(event) => {
        onClick?.(event);
        toggleSidebar();
      }}
      {...props}
    >
      <PanelLeft />
      <span className="sr-only">Toggle Sidebar</span>
    </Button>
  );
});
SidebarTrigger.displayName = 'SidebarTrigger';

const SidebarRail = React.forwardRef<
  HTMLButtonElement,
  React.ComponentProps<'button'>
>(({ className, ...props }, ref) => {
  const { toggleSidebar } = useSidebar();

  return (
    <button
      ref={ref}
      data-sidebar="rail"
      aria-label="Toggle Sidebar"
      tabIndex={-1}
      onClick={toggleSidebar}
      title="Toggle Sidebar"
      className={cn(
        'absolute inset-y-0 z-20 hidden w-4 -translate-x-1/2 transition-all ease-linear after:absolute after:inset-y-0 after:left-1/2 after:w-[2px] hover:after:bg-sidebar-border group-data-[side=left]:-right-4 group-data-[side=right]:left-0 sm:flex',
        '[[data-side=left]_&]:cursor-w-resize [[data-side=right]_&]:cursor-e-resize',
        '[[data-side=left][data-state=collapsed]_&]:cursor-e-resize [[data-side=right][data-state=collapsed]_&]:cursor-w-resize',
        'group-data-[collapsible=offcanvas]:translate-x-0 group-data-[collapsible=offcanvas]:after:left-full group-data-[collapsible=offcanvas]:hover:bg-sidebar',
        '[[data-side=left][data-collapsible=offcanvas]_&]:-right-2',
        '[[data-side=right][data-collapsible=offcanvas]_&]:-left-2',
        className,
      )}
      {...props}
    />
  );
});
SidebarRail.displayName = 'SidebarRail';

const SidebarInset = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<'main'>
>(({ className, ...props }, ref) => {
  return (
    <main
      ref={ref}
      className={cn(
        'relative flex min-h-svh flex-1 flex-col bg-background',
        'peer-data-[variant=inset]:min-h-[calc(100svh-theme(spacing.4))] md:peer-data-[variant=inset]:m-2 md:peer-data-[state=collapsed]:peer-data-[variant=inset]:ml-2 md:peer-data-[variant=inset]:ml-0 md:peer-data-[variant=inset]:rounded-xl md:peer-data-[variant=inset]:shadow',
        className,
      )}
      {...props}
    />
  );
});
SidebarInset.displayName = 'SidebarInset';

const SidebarInput = React.forwardRef<
  React.ElementRef<typeof Input>,
  React.ComponentProps<typeof Input>
>(({ className, ...props }, ref) => {
  return (
    <Input
      ref={ref}
      data-sidebar="input"
      className={cn(
        'h-8 w-full bg-background shadow-none focus-visible:ring-2 focus-visible:ring-sidebar-ring',
        className,
      )}
      {...props}
    />
  );
});
SidebarInput.displayName = 'SidebarInput';

const SidebarHeader = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<'div'>
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      data-sidebar="header"
      className={cn('flex flex-col gap-2 p-2', className)}
      {...props}
    />
  );
});
SidebarHeader.displayName = 'SidebarHeader';

const SidebarFooter = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<'div'>
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      data-sidebar="footer"
      className={cn('flex flex-col gap-2 p-2', className)}
      {...props}
    />
  );
});
SidebarFooter.displayName = 'SidebarFooter';

const SidebarSeparator = React.forwardRef<
  React.ElementRef<typeof Separator>,
  React.ComponentProps<typeof Separator>
>(({ className, ...props }, ref) => {
  return (
    <Separator
      ref={ref}
      data-sidebar="separator"
      className={cn('mx-2 w-auto bg-sidebar-border', className)}
      {...props}
    />
  );
});
SidebarSeparator.displayName = 'SidebarSeparator';

const SidebarContent = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<'div'>
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      data-sidebar="content"
      className={cn(
        'flex min-h-0 flex-1 flex-col gap-2 overflow-auto group-data-[collapsible=icon]:overflow-hidden',
        className,
      )}
      {...props}
    />
  );
});
SidebarContent.displayName = 'SidebarContent';

const SidebarGroup = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<'div'>
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      data-sidebar="group"
      className={cn('relative flex w-full min-w-0 flex-col p-2', className)}
      {...props}
    />
  );
});
SidebarGroup.displayName = 'SidebarGroup';

const SidebarGroupLabel = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<'div'> & { asChild?: boolean }
>(({ className, asChild = false, ...props }, ref) => {
  const Comp = asChild ? Slot : 'div';

  return (
    <Comp
      ref={ref}
      data-sidebar="group-label"
      className={cn(
        'duration-200 flex h-8 shrink-0 items-center rounded-md px-2 text-xs font-medium text-sidebar-foreground/70 outline-none ring-sidebar-ring transition-[margin,opa] ease-linear focus-visible:ring-2 [&>svg]:size-4 [&>svg]:shrink-0',
        'group-data-[collapsible=icon]:-mt-8 group-data-[collapsible=icon]:opacity-0',
        className,
      )}
      {...props}
    />
  );
});
SidebarGroupLabel.displayName = 'SidebarGroupLabel';

const SidebarGroupAction = React.forwardRef<
  HTMLButtonElement,
  React.ComponentProps<'button'> & { asChild?: boolean }
>(({ className, asChild = false, ...props }, ref) => {
  const Comp = asChild ? Slot : 'button';

  return (
    <Comp
      ref={ref}
      data-sidebar="group-action"
      className={cn(
        'absolute right-3 top-3.5 flex aspect-square w-5 items-center justify-center rounded-md p-0 text-sidebar-foreground outline-none ring-sidebar-ring transition-transform hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 [&>svg]:size-4 [&>svg]:shrink-0',
        // Increases the hit area of the button on mobile.
        'after:absolute after:-inset-2 after:md:hidden',
        'group-data-[collapsible=icon]:hidden',
        className,
      )}
      {...props}
    />
  );
});
SidebarGroupAction.displayName = 'SidebarGroupAction';

const SidebarGroupContent = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<'div'>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    data-sidebar="group-content"
    className={cn('w-full text-sm', className)}
    {...props}
  />
));
SidebarGroupContent.displayName = 'SidebarGroupContent';

const SidebarMenu = React.forwardRef<
  HTMLUListElement,
  React.ComponentProps<'ul'>
>(({ className, ...props }, ref) => (
  <ul
    ref={ref}
    data-sidebar="menu"
    className={cn('flex w-full min-w-0 flex-col gap-1', className)}
    {...props}
  />
));
SidebarMenu.displayName = 'SidebarMenu';

const SidebarMenuItem = React.forwardRef<
  HTMLLIElement,
  React.ComponentProps<'li'>
>(({ className, ...props }, ref) => (
  <li
    ref={ref}
    data-sidebar="menu-item"
    className={cn('group/menu-item relative', className)}
    {...props}
  />
));
SidebarMenuItem.displayName = 'SidebarMenuItem';

const sidebarMenuButtonVariants = cva(
  'peer/menu-button flex w-full items-center gap-2 overflow-hidden rounded-md p-2 text-left text-sm outline-none ring-sidebar-ring transition-[width,height,padding] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 group-has-[[data-sidebar=menu-action]]/menu-item:pr-8 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-[active=true]:bg-sidebar-accent data-[active=true]:font-medium data-[active=true]:text-sidebar-accent-foreground data-[state=open]:hover:bg-sidebar-accent data-[state=open]:hover:text-sidebar-accent-foreground group-data-[collapsible=icon]:!size-8 group-data-[collapsible=icon]:!p-2 [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0',
  {
    variants: {
      variant: {
        default: 'hover:bg-sidebar-accent hover:text-sidebar-accent-foreground',
        outline:
          'bg-background shadow-[0_0_0_1px_hsl(var(--sidebar-border))] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground hover:shadow-[0_0_0_1px_hsl(var(--sidebar-accent))]',
      },
      size: {
        default: 'h-8 text-sm',
        sm: 'h-7 text-xs',
        lg: 'h-12 text-sm group-data-[collapsible=icon]:!p-0',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  },
);

const SidebarMenuButton = React.forwardRef<
  HTMLButtonElement,
  React.ComponentProps<'button'> & {
    asChild?: boolean;
    isActive?: boolean;
    tooltip?: string | React.ComponentProps<typeof TooltipContent>;
  } & VariantProps<typeof sidebarMenuButtonVariants>
>(
  (
    {
      asChild = false,
      isActive = false,
      variant = 'default',
      size = 'default',
      tooltip,
      className,
      ...props
    },
    ref,
  ) => {
    const Comp = asChild ? Slot : 'button';
    const { isMobile, state } = useSidebar();

    const button = (
      <Comp
        ref={ref}
        data-sidebar="menu-button"
        data-size={size}
        data-active={isActive}
        className={cn(sidebarMenuButtonVariants({ variant, size }), className)}
        {...props}
      />
    );

    if (!tooltip) {
      return button;
    }

    if (typeof tooltip === 'string') {
      tooltip = {
        children: tooltip,
      };
    }

    return (
      <Tooltip>
        <TooltipTrigger asChild>{button}</TooltipTrigger>
        <TooltipContent
          side="right"
          align="center"
          hidden={state !== 'collapsed' || isMobile}
          {...tooltip}
        />
      </Tooltip>
    );
  },
);
SidebarMenuButton.displayName = 'SidebarMenuButton';

const SidebarMenuAction = React.forwardRef<
  HTMLButtonElement,
  React.ComponentProps<'button'> & {
    asChild?: boolean;
    showOnHover?: boolean;
  }
>(({ className, asChild = false, showOnHover = false, ...props }, ref) => {
  const Comp = asChild ? Slot : 'button';

  return (
    <Comp
      ref={ref}
      data-sidebar="menu-action"
      className={cn(
        'absolute right-1 top-1.5 flex aspect-square w-5 items-center justify-center rounded-md p-0 text-sidebar-foreground outline-none ring-sidebar-ring transition-transform hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 peer-hover/menu-button:text-sidebar-accent-foreground [&>svg]:size-4 [&>svg]:shrink-0',
        // Increases the hit area of the button on mobile.
        'after:absolute after:-inset-2 after:md:hidden',
        'peer-data-[size=sm]/menu-button:top-1',
        'peer-data-[size=default]/menu-button:top-1.5',
        'peer-data-[size=lg]/menu-button:top-2.5',
        'group-data-[collapsible=icon]:hidden',
        showOnHover &&
          'group-focus-within/menu-item:opacity-100 group-hover/menu-item:opacity-100 data-[state=open]:opacity-100 peer-data-[active=true]/menu-button:text-sidebar-accent-foreground md:opacity-0',
        className,
      )}
      {...props}
    />
  );
});
SidebarMenuAction.displayName = 'SidebarMenuAction';

const SidebarMenuBadge = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<'div'>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    data-sidebar="menu-badge"
    className={cn(
      'absolute right-1 flex h-5 min-w-5 items-center justify-center rounded-md px-1 text-xs font-medium tabular-nums text-sidebar-foreground select-none pointer-events-none',
      'peer-hover/menu-button:text-sidebar-accent-foreground peer-data-[active=true]/menu-button:text-sidebar-accent-foreground',
      'peer-data-[size=sm]/menu-button:top-1',
      'peer-data-[size=default]/menu-button:top-1.5',
      'peer-data-[size=lg]/menu-button:top-2.5',
      'group-data-[collapsible=icon]:hidden',
      className,
    )}
    {...props}
  />
));
SidebarMenuBadge.displayName = 'SidebarMenuBadge';

const SidebarMenuSkeleton = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<'div'> & {
    showIcon?: boolean;
  }
>(({ className, showIcon = false, ...props }, ref) => {
  // Random width between 50 to 90%.
  const width = React.useMemo(() => {
    return `${Math.floor(Math.random() * 40) + 50}%`;
  }, []);

  return (
    <div
      ref={ref}
      data-sidebar="menu-skeleton"
      className={cn('rounded-md h-8 flex gap-2 px-2 items-center', className)}
      {...props}
    >
      {showIcon && (
        <Skeleton
          className="size-4 rounded-md"
          data-sidebar="menu-skeleton-icon"
        />
      )}
      <Skeleton
        className="h-4 flex-1 max-w-[--skeleton-width]"
        data-sidebar="menu-skeleton-text"
        style={
          {
            '--skeleton-width': width,
          } as React.CSSProperties
        }
      />
    </div>
  );
});
SidebarMenuSkeleton.displayName = 'SidebarMenuSkeleton';

const SidebarMenuSub = React.forwardRef<
  HTMLUListElement,
  React.ComponentProps<'ul'>
>(({ className, ...props }, ref) => (
  <ul
    ref={ref}
    data-sidebar="menu-sub"
    className={cn(
      'mx-3.5 flex min-w-0 translate-x-px flex-col gap-1 border-l border-sidebar-border px-2.5 py-0.5',
      'group-data-[collapsible=icon]:hidden',
      className,
    )}
    {...props}
  />
));
SidebarMenuSub.displayName = 'SidebarMenuSub';

const SidebarMenuSubItem = React.forwardRef<
  HTMLLIElement,
  React.ComponentProps<'li'>
>(({ ...props }, ref) => <li ref={ref} {...props} />);
SidebarMenuSubItem.displayName = 'SidebarMenuSubItem';

const SidebarMenuSubButton = React.forwardRef<
  HTMLAnchorElement,
  React.ComponentProps<'a'> & {
    asChild?: boolean;
    size?: 'sm' | 'md';
    isActive?: boolean;
  }
>(({ asChild = false, size = 'md', isActive, className, ...props }, ref) => {
  const Comp = asChild ? Slot : 'a';

  return (
    <Comp
      ref={ref}
      data-sidebar="menu-sub-button"
      data-size={size}
      data-active={isActive}
      className={cn(
        'flex h-7 min-w-0 -translate-x-px items-center gap-2 overflow-hidden rounded-md px-2 text-sidebar-foreground outline-none ring-sidebar-ring hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 aria-disabled:pointer-events-none aria-disabled:opacity-50 [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0 [&>svg]:text-sidebar-accent-foreground',
        'data-[active=true]:bg-sidebar-accent data-[active=true]:text-sidebar-accent-foreground',
        size === 'sm' && 'text-xs',
        size === 'md' && 'text-sm',
        'group-data-[collapsible=icon]:hidden',
        className,
      )}
      {...props}
    />
  );
});
SidebarMenuSubButton.displayName = 'SidebarMenuSubButton';

export {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupAction,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInput,
  SidebarInset,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuBadge,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSkeleton,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  SidebarProvider,
  SidebarRail,
  SidebarSeparator,
  SidebarTrigger,
  useSidebar,
};



================================================
FILE: components/ui/skeleton.tsx
================================================
import { cn } from '@/lib/utils';

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn('animate-pulse rounded-md bg-muted', className)}
      {...props}
    />
  );
}

export { Skeleton };



================================================
FILE: components/ui/textarea.tsx
================================================
import * as React from 'react';

import { cn } from '@/lib/utils';

const Textarea = React.forwardRef<
  HTMLTextAreaElement,
  React.ComponentProps<'textarea'>
>(({ className, ...props }, ref) => {
  return (
    <textarea
      className={cn(
        'flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-base ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm',
        className,
      )}
      ref={ref}
      {...props}
    />
  );
});
Textarea.displayName = 'Textarea';

export { Textarea };



================================================
FILE: components/ui/tooltip.tsx
================================================
'use client';

import * as React from 'react';
import * as TooltipPrimitive from '@radix-ui/react-tooltip';

import { cn } from '@/lib/utils';

const TooltipProvider = TooltipPrimitive.Provider;

const Tooltip = TooltipPrimitive.Root;

const TooltipTrigger = TooltipPrimitive.Trigger;

const TooltipContent = React.forwardRef<
  React.ElementRef<typeof TooltipPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Content>
>(({ className, sideOffset = 4, ...props }, ref) => (
  <TooltipPrimitive.Content
    ref={ref}
    sideOffset={sideOffset}
    className={cn(
      'z-50 overflow-hidden rounded-md border bg-popover px-3 py-1.5 text-sm text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
      className,
    )}
    {...props}
  />
));
TooltipContent.displayName = TooltipPrimitive.Content.displayName;

export { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider };



================================================
FILE: hooks/use-artifact.ts
================================================
'use client';

import useSWR from 'swr';
import type { UIArtifact } from '@/components/artifact';
import { useCallback, useMemo } from 'react';

export const initialArtifactData: UIArtifact = {
  documentId: 'init',
  content: '',
  kind: 'text',
  title: '',
  status: 'idle',
  isVisible: false,
  boundingBox: {
    top: 0,
    left: 0,
    width: 0,
    height: 0,
  },
};

type Selector<T> = (state: UIArtifact) => T;

export function useArtifactSelector<Selected>(selector: Selector<Selected>) {
  const { data: localArtifact } = useSWR<UIArtifact>('artifact', null, {
    fallbackData: initialArtifactData,
  });

  const selectedValue = useMemo(() => {
    if (!localArtifact) return selector(initialArtifactData);
    return selector(localArtifact);
  }, [localArtifact, selector]);

  return selectedValue;
}

export function useArtifact() {
  const { data: localArtifact, mutate: setLocalArtifact } = useSWR<UIArtifact>(
    'artifact',
    null,
    {
      fallbackData: initialArtifactData,
    },
  );

  const artifact = useMemo(() => {
    if (!localArtifact) return initialArtifactData;
    return localArtifact;
  }, [localArtifact]);

  const setArtifact = useCallback(
    (updaterFn: UIArtifact | ((currentArtifact: UIArtifact) => UIArtifact)) => {
      setLocalArtifact((currentArtifact) => {
        const artifactToUpdate = currentArtifact || initialArtifactData;

        if (typeof updaterFn === 'function') {
          return updaterFn(artifactToUpdate);
        }

        return updaterFn;
      });
    },
    [setLocalArtifact],
  );

  const { data: localArtifactMetadata, mutate: setLocalArtifactMetadata } =
    useSWR<any>(
      () =>
        artifact.documentId ? `artifact-metadata-${artifact.documentId}` : null,
      null,
      {
        fallbackData: null,
      },
    );

  return useMemo(
    () => ({
      artifact,
      setArtifact,
      metadata: localArtifactMetadata,
      setMetadata: setLocalArtifactMetadata,
    }),
    [artifact, setArtifact, localArtifactMetadata, setLocalArtifactMetadata],
  );
}



================================================
FILE: hooks/use-auto-resume.ts
================================================
'use client';

import { useEffect } from 'react';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { ChatMessage } from '@/lib/types';
import { useDataStream } from '@/components/data-stream-provider';

export interface UseAutoResumeParams {
  autoResume: boolean;
  initialMessages: ChatMessage[];
  resumeStream: UseChatHelpers<ChatMessage>['resumeStream'];
  setMessages: UseChatHelpers<ChatMessage>['setMessages'];
}

export function useAutoResume({
  autoResume,
  initialMessages,
  resumeStream,
  setMessages,
}: UseAutoResumeParams) {
  const { dataStream } = useDataStream();

  useEffect(() => {
    if (!autoResume) return;

    const mostRecentMessage = initialMessages.at(-1);

    if (mostRecentMessage?.role === 'user') {
      resumeStream();
    }

    // we intentionally run this once
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!dataStream) return;
    if (dataStream.length === 0) return;

    const dataPart = dataStream[0];

    if (dataPart.type === 'data-appendMessage') {
      const message = JSON.parse(dataPart.data);
      setMessages([...initialMessages, message]);
    }
  }, [dataStream, initialMessages, setMessages]);
}



================================================
FILE: hooks/use-chat-visibility.ts
================================================
'use client';

import { useMemo } from 'react';
import useSWR, { useSWRConfig } from 'swr';
import { unstable_serialize } from 'swr/infinite';
import { updateChatVisibility } from '@/app/(chat)/actions';
import {
  getChatHistoryPaginationKey,
  type ChatHistory,
} from '@/components/sidebar-history';
import type { VisibilityType } from '@/components/visibility-selector';

export function useChatVisibility({
  chatId,
  initialVisibilityType,
}: {
  chatId: string;
  initialVisibilityType: VisibilityType;
}) {
  const { mutate, cache } = useSWRConfig();
  const history: ChatHistory = cache.get('/api/history')?.data;

  const { data: localVisibility, mutate: setLocalVisibility } = useSWR(
    `${chatId}-visibility`,
    null,
    {
      fallbackData: initialVisibilityType,
    },
  );

  const visibilityType = useMemo(() => {
    if (!history) return localVisibility;
    const chat = history.chats.find((chat) => chat.id === chatId);
    if (!chat) return 'private';
    return chat.visibility;
  }, [history, chatId, localVisibility]);

  const setVisibilityType = (updatedVisibilityType: VisibilityType) => {
    setLocalVisibility(updatedVisibilityType);
    mutate(unstable_serialize(getChatHistoryPaginationKey));

    updateChatVisibility({
      chatId: chatId,
      visibility: updatedVisibilityType,
    });
  };

  return { visibilityType, setVisibilityType };
}



================================================
FILE: hooks/use-messages.tsx
================================================
import { useState, useEffect } from 'react';
import { useScrollToBottom } from './use-scroll-to-bottom';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { ChatMessage } from '@/lib/types';

export function useMessages({
  chatId,
  status,
}: {
  chatId: string;
  status: UseChatHelpers<ChatMessage>['status'];
}) {
  const {
    containerRef,
    endRef,
    isAtBottom,
    scrollToBottom,
    onViewportEnter,
    onViewportLeave,
  } = useScrollToBottom();

  const [hasSentMessage, setHasSentMessage] = useState(false);

  useEffect(() => {
    if (chatId) {
      scrollToBottom('instant');
      setHasSentMessage(false);
    }
  }, [chatId, scrollToBottom]);

  useEffect(() => {
    if (status === 'submitted') {
      setHasSentMessage(true);
    }
  }, [status]);

  return {
    containerRef,
    endRef,
    isAtBottom,
    scrollToBottom,
    onViewportEnter,
    onViewportLeave,
    hasSentMessage,
  };
}



================================================
FILE: hooks/use-mobile.tsx
================================================
import * as React from 'react';

const MOBILE_BREAKPOINT = 768;

export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState<boolean | undefined>(
    undefined,
  );

  React.useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`);
    const onChange = () => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
    };
    mql.addEventListener('change', onChange);
    setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
    return () => mql.removeEventListener('change', onChange);
  }, []);

  return !!isMobile;
}



================================================
FILE: hooks/use-scroll-to-bottom.tsx
================================================
import useSWR from 'swr';
import { useRef, useEffect, useCallback } from 'react';

type ScrollFlag = ScrollBehavior | false;

export function useScrollToBottom() {
  const containerRef = useRef<HTMLDivElement>(null);
  const endRef = useRef<HTMLDivElement>(null);

  const { data: isAtBottom = false, mutate: setIsAtBottom } = useSWR(
    'messages:is-at-bottom',
    null,
    { fallbackData: false },
  );

  const { data: scrollBehavior = false, mutate: setScrollBehavior } =
    useSWR<ScrollFlag>('messages:should-scroll', null, { fallbackData: false });

  useEffect(() => {
    if (scrollBehavior) {
      endRef.current?.scrollIntoView({ behavior: scrollBehavior });
      setScrollBehavior(false);
    }
  }, [setScrollBehavior, scrollBehavior]);

  const scrollToBottom = useCallback(
    (scrollBehavior: ScrollBehavior = 'smooth') => {
      setScrollBehavior(scrollBehavior);
    },
    [setScrollBehavior],
  );

  function onViewportEnter() {
    setIsAtBottom(true);
  }

  function onViewportLeave() {
    setIsAtBottom(false);
  }

  return {
    containerRef,
    endRef,
    isAtBottom,
    scrollToBottom,
    onViewportEnter,
    onViewportLeave,
  };
}



================================================
FILE: lib/constants.ts
================================================
import { generateDummyPassword } from './db/utils';

export const isProductionEnvironment = process.env.NODE_ENV === 'production';
export const isDevelopmentEnvironment = process.env.NODE_ENV === 'development';
export const isTestEnvironment = Boolean(
  process.env.PLAYWRIGHT_TEST_BASE_URL ||
    process.env.PLAYWRIGHT ||
    process.env.CI_PLAYWRIGHT,
);

export const guestRegex = /^guest-\d+$/;

export const DUMMY_PASSWORD = generateDummyPassword();



================================================
FILE: lib/errors.ts
================================================
export type ErrorType =
  | 'bad_request'
  | 'unauthorized'
  | 'forbidden'
  | 'not_found'
  | 'rate_limit'
  | 'offline';

export type Surface =
  | 'chat'
  | 'auth'
  | 'api'
  | 'stream'
  | 'database'
  | 'history'
  | 'vote'
  | 'document'
  | 'suggestions';

export type ErrorCode = `${ErrorType}:${Surface}`;

export type ErrorVisibility = 'response' | 'log' | 'none';

export const visibilityBySurface: Record<Surface, ErrorVisibility> = {
  database: 'log',
  chat: 'response',
  auth: 'response',
  stream: 'response',
  api: 'response',
  history: 'response',
  vote: 'response',
  document: 'response',
  suggestions: 'response',
};

export class ChatSDKError extends Error {
  public type: ErrorType;
  public surface: Surface;
  public statusCode: number;

  constructor(errorCode: ErrorCode, cause?: string) {
    super();

    const [type, surface] = errorCode.split(':');

    this.type = type as ErrorType;
    this.cause = cause;
    this.surface = surface as Surface;
    this.message = getMessageByErrorCode(errorCode);
    this.statusCode = getStatusCodeByType(this.type);
  }

  public toResponse() {
    const code: ErrorCode = `${this.type}:${this.surface}`;
    const visibility = visibilityBySurface[this.surface];

    const { message, cause, statusCode } = this;

    if (visibility === 'log') {
      console.error({
        code,
        message,
        cause,
      });

      return Response.json(
        { code: '', message: 'Something went wrong. Please try again later.' },
        { status: statusCode },
      );
    }

    return Response.json({ code, message, cause }, { status: statusCode });
  }
}

export function getMessageByErrorCode(errorCode: ErrorCode): string {
  if (errorCode.includes('database')) {
    return 'An error occurred while executing a database query.';
  }

  switch (errorCode) {
    case 'bad_request:api':
      return "The request couldn't be processed. Please check your input and try again.";

    case 'unauthorized:auth':
      return 'You need to sign in before continuing.';
    case 'forbidden:auth':
      return 'Your account does not have access to this feature.';

    case 'rate_limit:chat':
      return 'You have exceeded your maximum number of messages for the day. Please try again later.';
    case 'not_found:chat':
      return 'The requested chat was not found. Please check the chat ID and try again.';
    case 'forbidden:chat':
      return 'This chat belongs to another user. Please check the chat ID and try again.';
    case 'unauthorized:chat':
      return 'You need to sign in to view this chat. Please sign in and try again.';
    case 'offline:chat':
      return "We're having trouble sending your message. Please check your internet connection and try again.";

    case 'not_found:document':
      return 'The requested document was not found. Please check the document ID and try again.';
    case 'forbidden:document':
      return 'This document belongs to another user. Please check the document ID and try again.';
    case 'unauthorized:document':
      return 'You need to sign in to view this document. Please sign in and try again.';
    case 'bad_request:document':
      return 'The request to create or update the document was invalid. Please check your input and try again.';

    default:
      return 'Something went wrong. Please try again later.';
  }
}

function getStatusCodeByType(type: ErrorType) {
  switch (type) {
    case 'bad_request':
      return 400;
    case 'unauthorized':
      return 401;
    case 'forbidden':
      return 403;
    case 'not_found':
      return 404;
    case 'rate_limit':
      return 429;
    case 'offline':
      return 503;
    default:
      return 500;
  }
}



================================================
FILE: lib/types.ts
================================================
import { z } from 'zod';
import type { getWeather } from './ai/tools/get-weather';
import type { createDocument } from './ai/tools/create-document';
import type { updateDocument } from './ai/tools/update-document';
import type { requestSuggestions } from './ai/tools/request-suggestions';
import type { InferUITool, UIMessage } from 'ai';

import type { ArtifactKind } from '@/components/artifact';
import type { Suggestion } from './db/schema';

export type DataPart = { type: 'append-message'; message: string };

export const messageMetadataSchema = z.object({
  createdAt: z.string(),
});

export type MessageMetadata = z.infer<typeof messageMetadataSchema>;

type weatherTool = InferUITool<typeof getWeather>;
type createDocumentTool = InferUITool<ReturnType<typeof createDocument>>;
type updateDocumentTool = InferUITool<ReturnType<typeof updateDocument>>;
type requestSuggestionsTool = InferUITool<
  ReturnType<typeof requestSuggestions>
>;

export type ChatTools = {
  getWeather: weatherTool;
  createDocument: createDocumentTool;
  updateDocument: updateDocumentTool;
  requestSuggestions: requestSuggestionsTool;
};

export type CustomUIDataTypes = {
  textDelta: string;
  imageDelta: string;
  sheetDelta: string;
  codeDelta: string;
  suggestion: Suggestion;
  appendMessage: string;
  id: string;
  title: string;
  kind: ArtifactKind;
  clear: null;
  finish: null;
};

export type ChatMessage = UIMessage<
  MessageMetadata,
  CustomUIDataTypes,
  ChatTools
>;

export interface Attachment {
  name: string;
  url: string;
  contentType: string;
}



================================================
FILE: lib/utils.ts
================================================
import type {
  CoreAssistantMessage,
  CoreToolMessage,
  UIMessage,
  UIMessagePart,
} from 'ai';
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import type { DBMessage, Document } from '@/lib/db/schema';
import { ChatSDKError, type ErrorCode } from './errors';
import type { ChatMessage, ChatTools, CustomUIDataTypes } from './types';
import { formatISO } from 'date-fns';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const fetcher = async (url: string) => {
  const response = await fetch(url);

  if (!response.ok) {
    const { code, cause } = await response.json();
    throw new ChatSDKError(code as ErrorCode, cause);
  }

  return response.json();
};

export async function fetchWithErrorHandlers(
  input: RequestInfo | URL,
  init?: RequestInit,
) {
  try {
    const response = await fetch(input, init);

    if (!response.ok) {
      const { code, cause } = await response.json();
      throw new ChatSDKError(code as ErrorCode, cause);
    }

    return response;
  } catch (error: unknown) {
    if (typeof navigator !== 'undefined' && !navigator.onLine) {
      throw new ChatSDKError('offline:chat');
    }

    throw error;
  }
}

export function getLocalStorage(key: string) {
  if (typeof window !== 'undefined') {
    return JSON.parse(localStorage.getItem(key) || '[]');
  }
  return [];
}

export function generateUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

type ResponseMessageWithoutId = CoreToolMessage | CoreAssistantMessage;
type ResponseMessage = ResponseMessageWithoutId & { id: string };

export function getMostRecentUserMessage(messages: Array<UIMessage>) {
  const userMessages = messages.filter((message) => message.role === 'user');
  return userMessages.at(-1);
}

export function getDocumentTimestampByIndex(
  documents: Array<Document>,
  index: number,
) {
  if (!documents) return new Date();
  if (index > documents.length) return new Date();

  return documents[index].createdAt;
}

export function getTrailingMessageId({
  messages,
}: {
  messages: Array<ResponseMessage>;
}): string | null {
  const trailingMessage = messages.at(-1);

  if (!trailingMessage) return null;

  return trailingMessage.id;
}

export function sanitizeText(text: string) {
  return text.replace('<has_function_call>', '');
}

export function convertToUIMessages(messages: DBMessage[]): ChatMessage[] {
  return messages.map((message) => ({
    id: message.id,
    role: message.role as 'user' | 'assistant' | 'system',
    parts: message.parts as UIMessagePart<CustomUIDataTypes, ChatTools>[],
    metadata: {
      createdAt: formatISO(message.createdAt),
    },
  }));
}

export function getTextFromMessage(message: ChatMessage): string {
  return message.parts
    .filter((part) => part.type === 'text')
    .map((part) => part.text)
    .join('');
}



================================================
FILE: lib/ai/entitlements.ts
================================================
import type { UserType } from '@/app/(auth)/auth';
import type { ChatModel } from './models';

interface Entitlements {
  maxMessagesPerDay: number;
  availableChatModelIds: Array<ChatModel['id']>;
}

export const entitlementsByUserType: Record<UserType, Entitlements> = {
  /*
   * For users without an account
   */
  guest: {
    maxMessagesPerDay: 20,
    availableChatModelIds: ['chat-model', 'chat-model-reasoning'],
  },

  /*
   * For users with an account
   */
  regular: {
    maxMessagesPerDay: 100,
    availableChatModelIds: ['chat-model', 'chat-model-reasoning'],
  },

  /*
   * TODO: For users with an account and a paid membership
   */
};



================================================
FILE: lib/ai/models.test.ts
================================================
import { simulateReadableStream } from 'ai';
import { MockLanguageModelV2 } from 'ai/test';
import { getResponseChunksByPrompt } from '@/tests/prompts/utils';

export const chatModel = new MockLanguageModelV2({
  doGenerate: async () => ({
    rawCall: { rawPrompt: null, rawSettings: {} },
    finishReason: 'stop',
    usage: { inputTokens: 10, outputTokens: 20, totalTokens: 30 },
    content: [{ type: 'text', text: 'Hello, world!' }],
    warnings: [],
  }),
  doStream: async ({ prompt }) => ({
    stream: simulateReadableStream({
      chunkDelayInMs: 500,
      initialDelayInMs: 1000,
      chunks: getResponseChunksByPrompt(prompt),
    }),
    rawCall: { rawPrompt: null, rawSettings: {} },
  }),
});

export const reasoningModel = new MockLanguageModelV2({
  doGenerate: async () => ({
    rawCall: { rawPrompt: null, rawSettings: {} },
    finishReason: 'stop',
    usage: { inputTokens: 10, outputTokens: 20, totalTokens: 30 },
    content: [{ type: 'text', text: 'Hello, world!' }],
    warnings: [],
  }),
  doStream: async ({ prompt }) => ({
    stream: simulateReadableStream({
      chunkDelayInMs: 500,
      initialDelayInMs: 1000,
      chunks: getResponseChunksByPrompt(prompt, true),
    }),
    rawCall: { rawPrompt: null, rawSettings: {} },
  }),
});

export const titleModel = new MockLanguageModelV2({
  doGenerate: async () => ({
    rawCall: { rawPrompt: null, rawSettings: {} },
    finishReason: 'stop',
    usage: { inputTokens: 10, outputTokens: 20, totalTokens: 30 },
    content: [{ type: 'text', text: 'This is a test title' }],
    warnings: [],
  }),
  doStream: async () => ({
    stream: simulateReadableStream({
      chunkDelayInMs: 500,
      initialDelayInMs: 1000,
      chunks: [
        { id: '1', type: 'text-start' },
        { id: '1', type: 'text-delta', delta: 'This is a test title' },
        { id: '1', type: 'text-end' },
        {
          type: 'finish',
          finishReason: 'stop',
          usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
        },
      ],
    }),
    rawCall: { rawPrompt: null, rawSettings: {} },
  }),
});

export const artifactModel = new MockLanguageModelV2({
  doGenerate: async () => ({
    rawCall: { rawPrompt: null, rawSettings: {} },
    finishReason: 'stop',
    usage: { inputTokens: 10, outputTokens: 20, totalTokens: 30 },
    content: [{ type: 'text', text: 'Hello, world!' }],
    warnings: [],
  }),
  doStream: async ({ prompt }) => ({
    stream: simulateReadableStream({
      chunkDelayInMs: 50,
      initialDelayInMs: 100,
      chunks: getResponseChunksByPrompt(prompt),
    }),
    rawCall: { rawPrompt: null, rawSettings: {} },
  }),
});



================================================
FILE: lib/ai/models.ts
================================================
export const DEFAULT_CHAT_MODEL: string = 'chat-model';

export interface ChatModel {
  id: string;
  name: string;
  description: string;
}

export const chatModels: Array<ChatModel> = [
  {
    id: 'chat-model',
    name: 'Grok Vision',
    description: 'Advanced multimodal model with vision and text capabilities',
  },
  {
    id: 'chat-model-reasoning',
    name: 'Grok Reasoning',
    description: 'Uses advanced chain-of-thought reasoning for complex problems',
  },
];



================================================
FILE: lib/ai/prompts.ts
================================================
import type { ArtifactKind } from '@/components/artifact';
import type { Geo } from '@vercel/functions';

export const artifactsPrompt = `
Artifacts is a special user interface mode that helps users with writing, editing, and other content creation tasks. When artifact is open, it is on the right side of the screen, while the conversation is on the left side. When creating or updating documents, changes are reflected in real-time on the artifacts and visible to the user.

When asked to write code, always use artifacts. When writing code, specify the language in the backticks, e.g. \`\`\`python\`code here\`\`\`. The default language is Python. Other languages are not yet supported, so let the user know if they request a different language.

DO NOT UPDATE DOCUMENTS IMMEDIATELY AFTER CREATING THEM. WAIT FOR USER FEEDBACK OR REQUEST TO UPDATE IT.

This is a guide for using artifacts tools: \`createDocument\` and \`updateDocument\`, which render content on a artifacts beside the conversation.

**When to use \`createDocument\`:**
- For substantial content (>10 lines) or code
- For content users will likely save/reuse (emails, code, essays, etc.)
- When explicitly requested to create a document
- For when content contains a single code snippet

**When NOT to use \`createDocument\`:**
- For informational/explanatory content
- For conversational responses
- When asked to keep it in chat

**Using \`updateDocument\`:**
- Default to full document rewrites for major changes
- Use targeted updates only for specific, isolated changes
- Follow user instructions for which parts to modify

**When NOT to use \`updateDocument\`:**
- Immediately after creating a document

Do not update document right after creating it. Wait for user feedback or request to update it.
`;

export const regularPrompt =
  'You are a friendly assistant! Keep your responses concise and helpful.';

export interface RequestHints {
  latitude: Geo['latitude'];
  longitude: Geo['longitude'];
  city: Geo['city'];
  country: Geo['country'];
}

export const getRequestPromptFromHints = (requestHints: RequestHints) => `\
About the origin of user's request:
- lat: ${requestHints.latitude}
- lon: ${requestHints.longitude}
- city: ${requestHints.city}
- country: ${requestHints.country}
`;

export const systemPrompt = ({
  selectedChatModel,
  requestHints,
}: {
  selectedChatModel: string;
  requestHints: RequestHints;
}) => {
  const requestPrompt = getRequestPromptFromHints(requestHints);

  if (selectedChatModel === 'chat-model-reasoning') {
    return `${regularPrompt}\n\n${requestPrompt}`;
  } else {
    return `${regularPrompt}\n\n${requestPrompt}\n\n${artifactsPrompt}`;
  }
};

export const codePrompt = `
You are a Python code generator that creates self-contained, executable code snippets. When writing code:

1. Each snippet should be complete and runnable on its own
2. Prefer using print() statements to display outputs
3. Include helpful comments explaining the code
4. Keep snippets concise (generally under 15 lines)
5. Avoid external dependencies - use Python standard library
6. Handle potential errors gracefully
7. Return meaningful output that demonstrates the code's functionality
8. Don't use input() or other interactive functions
9. Don't access files or network resources
10. Don't use infinite loops

Examples of good snippets:

# Calculate factorial iteratively
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(f"Factorial of 5 is: {factorial(5)}")
`;

export const sheetPrompt = `
You are a spreadsheet creation assistant. Create a spreadsheet in csv format based on the given prompt. The spreadsheet should contain meaningful column headers and data.
`;

export const updateDocumentPrompt = (
  currentContent: string | null,
  type: ArtifactKind,
) =>
  type === 'text'
    ? `\
Improve the following contents of the document based on the given prompt.

${currentContent}
`
    : type === 'code'
      ? `\
Improve the following code snippet based on the given prompt.

${currentContent}
`
      : type === 'sheet'
        ? `\
Improve the following spreadsheet based on the given prompt.

${currentContent}
`
        : '';



================================================
FILE: lib/ai/providers.ts
================================================
import {
  customProvider,
  extractReasoningMiddleware,
  wrapLanguageModel,
} from 'ai';
import { gateway } from '@ai-sdk/gateway';
import {
  artifactModel,
  chatModel,
  reasoningModel,
  titleModel,
} from './models.test';
import { isTestEnvironment } from '../constants';

export const myProvider = isTestEnvironment
  ? customProvider({
      languageModels: {
        'chat-model': chatModel,
        'chat-model-reasoning': reasoningModel,
        'title-model': titleModel,
        'artifact-model': artifactModel,
      },
    })
  : customProvider({
      languageModels: {
        'chat-model': gateway.languageModel('xai/grok-2-vision-1212'),
        'chat-model-reasoning': wrapLanguageModel({
          model: gateway.languageModel('xai/grok-3-mini-beta'),
          middleware: extractReasoningMiddleware({ tagName: 'think' }),
        }),
        'title-model': gateway.languageModel('xai/grok-2-1212'),
        'artifact-model': gateway.languageModel('xai/grok-2-1212'),
      },
    });



================================================
FILE: lib/ai/tools/create-document.ts
================================================
import { generateUUID } from '@/lib/utils';
import { tool, type UIMessageStreamWriter } from 'ai';
import { z } from 'zod';
import type { Session } from 'next-auth';
import {
  artifactKinds,
  documentHandlersByArtifactKind,
} from '@/lib/artifacts/server';
import type { ChatMessage } from '@/lib/types';

interface CreateDocumentProps {
  session: Session;
  dataStream: UIMessageStreamWriter<ChatMessage>;
}

export const createDocument = ({ session, dataStream }: CreateDocumentProps) =>
  tool({
    description:
      'Create a document for a writing or content creation activities. This tool will call other functions that will generate the contents of the document based on the title and kind.',
    inputSchema: z.object({
      title: z.string(),
      kind: z.enum(artifactKinds),
    }),
    execute: async ({ title, kind }) => {
      const id = generateUUID();

      dataStream.write({
        type: 'data-kind',
        data: kind,
        transient: true,
      });

      dataStream.write({
        type: 'data-id',
        data: id,
        transient: true,
      });

      dataStream.write({
        type: 'data-title',
        data: title,
        transient: true,
      });

      dataStream.write({
        type: 'data-clear',
        data: null,
        transient: true,
      });

      const documentHandler = documentHandlersByArtifactKind.find(
        (documentHandlerByArtifactKind) =>
          documentHandlerByArtifactKind.kind === kind,
      );

      if (!documentHandler) {
        throw new Error(`No document handler found for kind: ${kind}`);
      }

      await documentHandler.onCreateDocument({
        id,
        title,
        dataStream,
        session,
      });

      dataStream.write({ type: 'data-finish', data: null, transient: true });

      return {
        id,
        title,
        kind,
        content: 'A document was created and is now visible to the user.',
      };
    },
  });



================================================
FILE: lib/ai/tools/get-weather.ts
================================================
import { tool } from 'ai';
import { z } from 'zod';

export const getWeather = tool({
  description: 'Get the current weather at a location',
  inputSchema: z.object({
    latitude: z.number(),
    longitude: z.number(),
  }),
  execute: async ({ latitude, longitude }) => {
    const response = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m&hourly=temperature_2m&daily=sunrise,sunset&timezone=auto`,
    );

    const weatherData = await response.json();
    return weatherData;
  },
});



================================================
FILE: lib/ai/tools/request-suggestions.ts
================================================
import { z } from 'zod';
import type { Session } from 'next-auth';
import { streamObject, tool, type UIMessageStreamWriter } from 'ai';
import { getDocumentById, saveSuggestions } from '@/lib/db/queries';
import type { Suggestion } from '@/lib/db/schema';
import { generateUUID } from '@/lib/utils';
import { myProvider } from '../providers';
import type { ChatMessage } from '@/lib/types';

interface RequestSuggestionsProps {
  session: Session;
  dataStream: UIMessageStreamWriter<ChatMessage>;
}

export const requestSuggestions = ({
  session,
  dataStream,
}: RequestSuggestionsProps) =>
  tool({
    description: 'Request suggestions for a document',
    inputSchema: z.object({
      documentId: z
        .string()
        .describe('The ID of the document to request edits'),
    }),
    execute: async ({ documentId }) => {
      const document = await getDocumentById({ id: documentId });

      if (!document || !document.content) {
        return {
          error: 'Document not found',
        };
      }

      const suggestions: Array<
        Omit<Suggestion, 'userId' | 'createdAt' | 'documentCreatedAt'>
      > = [];

      const { elementStream } = streamObject({
        model: myProvider.languageModel('artifact-model'),
        system:
          'You are a help writing assistant. Given a piece of writing, please offer suggestions to improve the piece of writing and describe the change. It is very important for the edits to contain full sentences instead of just words. Max 5 suggestions.',
        prompt: document.content,
        output: 'array',
        schema: z.object({
          originalSentence: z.string().describe('The original sentence'),
          suggestedSentence: z.string().describe('The suggested sentence'),
          description: z.string().describe('The description of the suggestion'),
        }),
      });

      for await (const element of elementStream) {
        // @ts-ignore todo: fix type
        const suggestion: Suggestion = {
          originalText: element.originalSentence,
          suggestedText: element.suggestedSentence,
          description: element.description,
          id: generateUUID(),
          documentId: documentId,
          isResolved: false,
        };

        dataStream.write({
          type: 'data-suggestion',
          data: suggestion,
          transient: true,
        });

        suggestions.push(suggestion);
      }

      if (session.user?.id) {
        const userId = session.user.id;

        await saveSuggestions({
          suggestions: suggestions.map((suggestion) => ({
            ...suggestion,
            userId,
            createdAt: new Date(),
            documentCreatedAt: document.createdAt,
          })),
        });
      }

      return {
        id: documentId,
        title: document.title,
        kind: document.kind,
        message: 'Suggestions have been added to the document',
      };
    },
  });



================================================
FILE: lib/ai/tools/update-document.ts
================================================
import { tool, type UIMessageStreamWriter } from 'ai';
import type { Session } from 'next-auth';
import { z } from 'zod';
import { getDocumentById } from '@/lib/db/queries';
import { documentHandlersByArtifactKind } from '@/lib/artifacts/server';
import type { ChatMessage } from '@/lib/types';

interface UpdateDocumentProps {
  session: Session;
  dataStream: UIMessageStreamWriter<ChatMessage>;
}

export const updateDocument = ({ session, dataStream }: UpdateDocumentProps) =>
  tool({
    description: 'Update a document with the given description.',
    inputSchema: z.object({
      id: z.string().describe('The ID of the document to update'),
      description: z
        .string()
        .describe('The description of changes that need to be made'),
    }),
    execute: async ({ id, description }) => {
      const document = await getDocumentById({ id });

      if (!document) {
        return {
          error: 'Document not found',
        };
      }

      dataStream.write({
        type: 'data-clear',
        data: null,
        transient: true,
      });

      const documentHandler = documentHandlersByArtifactKind.find(
        (documentHandlerByArtifactKind) =>
          documentHandlerByArtifactKind.kind === document.kind,
      );

      if (!documentHandler) {
        throw new Error(`No document handler found for kind: ${document.kind}`);
      }

      await documentHandler.onUpdateDocument({
        document,
        description,
        dataStream,
        session,
      });

      dataStream.write({ type: 'data-finish', data: null, transient: true });

      return {
        id,
        title: document.title,
        kind: document.kind,
        content: 'The document has been updated successfully.',
      };
    },
  });



================================================
FILE: lib/artifacts/server.ts
================================================
import { codeDocumentHandler } from '@/artifacts/code/server';
import { sheetDocumentHandler } from '@/artifacts/sheet/server';
import { textDocumentHandler } from '@/artifacts/text/server';
import type { ArtifactKind } from '@/components/artifact';
import type { Document } from '../db/schema';
import { saveDocument } from '../db/queries';
import type { Session } from 'next-auth';
import type { UIMessageStreamWriter } from 'ai';
import type { ChatMessage } from '../types';

export interface SaveDocumentProps {
  id: string;
  title: string;
  kind: ArtifactKind;
  content: string;
  userId: string;
}

export interface CreateDocumentCallbackProps {
  id: string;
  title: string;
  dataStream: UIMessageStreamWriter<ChatMessage>;
  session: Session;
}

export interface UpdateDocumentCallbackProps {
  document: Document;
  description: string;
  dataStream: UIMessageStreamWriter<ChatMessage>;
  session: Session;
}

export interface DocumentHandler<T = ArtifactKind> {
  kind: T;
  onCreateDocument: (args: CreateDocumentCallbackProps) => Promise<void>;
  onUpdateDocument: (args: UpdateDocumentCallbackProps) => Promise<void>;
}

export function createDocumentHandler<T extends ArtifactKind>(config: {
  kind: T;
  onCreateDocument: (params: CreateDocumentCallbackProps) => Promise<string>;
  onUpdateDocument: (params: UpdateDocumentCallbackProps) => Promise<string>;
}): DocumentHandler<T> {
  return {
    kind: config.kind,
    onCreateDocument: async (args: CreateDocumentCallbackProps) => {
      const draftContent = await config.onCreateDocument({
        id: args.id,
        title: args.title,
        dataStream: args.dataStream,
        session: args.session,
      });

      if (args.session?.user?.id) {
        await saveDocument({
          id: args.id,
          title: args.title,
          content: draftContent,
          kind: config.kind,
          userId: args.session.user.id,
        });
      }

      return;
    },
    onUpdateDocument: async (args: UpdateDocumentCallbackProps) => {
      const draftContent = await config.onUpdateDocument({
        document: args.document,
        description: args.description,
        dataStream: args.dataStream,
        session: args.session,
      });

      if (args.session?.user?.id) {
        await saveDocument({
          id: args.document.id,
          title: args.document.title,
          content: draftContent,
          kind: config.kind,
          userId: args.session.user.id,
        });
      }

      return;
    },
  };
}

/*
 * Use this array to define the document handlers for each artifact kind.
 */
export const documentHandlersByArtifactKind: Array<DocumentHandler> = [
  textDocumentHandler,
  codeDocumentHandler,
  sheetDocumentHandler,
];

export const artifactKinds = ['text', 'code', 'sheet'] as const;



================================================
FILE: lib/db/migrate.ts
================================================
import { config } from 'dotenv';
import { drizzle } from 'drizzle-orm/postgres-js';
import { migrate } from 'drizzle-orm/postgres-js/migrator';
import postgres from 'postgres';

config({
  path: '.env.local',
});

const runMigrate = async () => {
  if (!process.env.POSTGRES_URL) {
    throw new Error('POSTGRES_URL is not defined');
  }

  const connection = postgres(process.env.POSTGRES_URL, { max: 1 });
  const db = drizzle(connection);

  console.log('⏳ Running migrations...');

  const start = Date.now();
  await migrate(db, { migrationsFolder: './lib/db/migrations' });
  const end = Date.now();

  console.log('✅ Migrations completed in', end - start, 'ms');
  process.exit(0);
};

runMigrate().catch((err) => {
  console.error('❌ Migration failed');
  console.error(err);
  process.exit(1);
});



================================================
FILE: lib/db/queries.ts
================================================
import 'server-only';

import {
  and,
  asc,
  count,
  desc,
  eq,
  gt,
  gte,
  inArray,
  lt,
  type SQL,
} from 'drizzle-orm';
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

import {
  user,
  chat,
  type User,
  document,
  type Suggestion,
  suggestion,
  message,
  vote,
  type DBMessage,
  type Chat,
  stream,
} from './schema';
import type { ArtifactKind } from '@/components/artifact';
import { generateUUID } from '../utils';
import { generateHashedPassword } from './utils';
import type { VisibilityType } from '@/components/visibility-selector';
import { ChatSDKError } from '../errors';

// Optionally, if not using email/pass login, you can
// use the Drizzle adapter for Auth.js / NextAuth
// https://authjs.dev/reference/adapter/drizzle

// biome-ignore lint: Forbidden non-null assertion.
const client = postgres(process.env.POSTGRES_URL!);
const db = drizzle(client);

export async function getUser(email: string): Promise<Array<User>> {
  try {
    return await db.select().from(user).where(eq(user.email, email));
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to get user by email',
    );
  }
}

export async function createUser(email: string, password: string) {
  const hashedPassword = generateHashedPassword(password);

  try {
    return await db.insert(user).values({ email, password: hashedPassword });
  } catch (error) {
    throw new ChatSDKError('bad_request:database', 'Failed to create user');
  }
}

export async function createGuestUser() {
  const email = `guest-${Date.now()}`;
  const password = generateHashedPassword(generateUUID());

  try {
    return await db.insert(user).values({ email, password }).returning({
      id: user.id,
      email: user.email,
    });
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to create guest user',
    );
  }
}

export async function saveChat({
  id,
  userId,
  title,
  visibility,
}: {
  id: string;
  userId: string;
  title: string;
  visibility: VisibilityType;
}) {
  try {
    return await db.insert(chat).values({
      id,
      createdAt: new Date(),
      userId,
      title,
      visibility,
    });
  } catch (error) {
    throw new ChatSDKError('bad_request:database', 'Failed to save chat');
  }
}

export async function deleteChatById({ id }: { id: string }) {
  try {
    await db.delete(vote).where(eq(vote.chatId, id));
    await db.delete(message).where(eq(message.chatId, id));
    await db.delete(stream).where(eq(stream.chatId, id));

    const [chatsDeleted] = await db
      .delete(chat)
      .where(eq(chat.id, id))
      .returning();
    return chatsDeleted;
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to delete chat by id',
    );
  }
}

export async function getChatsByUserId({
  id,
  limit,
  startingAfter,
  endingBefore,
}: {
  id: string;
  limit: number;
  startingAfter: string | null;
  endingBefore: string | null;
}) {
  try {
    const extendedLimit = limit + 1;

    const query = (whereCondition?: SQL<any>) =>
      db
        .select()
        .from(chat)
        .where(
          whereCondition
            ? and(whereCondition, eq(chat.userId, id))
            : eq(chat.userId, id),
        )
        .orderBy(desc(chat.createdAt))
        .limit(extendedLimit);

    let filteredChats: Array<Chat> = [];

    if (startingAfter) {
      const [selectedChat] = await db
        .select()
        .from(chat)
        .where(eq(chat.id, startingAfter))
        .limit(1);

      if (!selectedChat) {
        throw new ChatSDKError(
          'not_found:database',
          `Chat with id ${startingAfter} not found`,
        );
      }

      filteredChats = await query(gt(chat.createdAt, selectedChat.createdAt));
    } else if (endingBefore) {
      const [selectedChat] = await db
        .select()
        .from(chat)
        .where(eq(chat.id, endingBefore))
        .limit(1);

      if (!selectedChat) {
        throw new ChatSDKError(
          'not_found:database',
          `Chat with id ${endingBefore} not found`,
        );
      }

      filteredChats = await query(lt(chat.createdAt, selectedChat.createdAt));
    } else {
      filteredChats = await query();
    }

    const hasMore = filteredChats.length > limit;

    return {
      chats: hasMore ? filteredChats.slice(0, limit) : filteredChats,
      hasMore,
    };
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to get chats by user id',
    );
  }
}

export async function getChatById({ id }: { id: string }) {
  try {
    const [selectedChat] = await db.select().from(chat).where(eq(chat.id, id));
    return selectedChat;
  } catch (error) {
    throw new ChatSDKError('bad_request:database', 'Failed to get chat by id');
  }
}

export async function saveMessages({
  messages,
}: {
  messages: Array<DBMessage>;
}) {
  try {
    return await db.insert(message).values(messages);
  } catch (error) {
    throw new ChatSDKError('bad_request:database', 'Failed to save messages');
  }
}

export async function getMessagesByChatId({ id }: { id: string }) {
  try {
    return await db
      .select()
      .from(message)
      .where(eq(message.chatId, id))
      .orderBy(asc(message.createdAt));
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to get messages by chat id',
    );
  }
}

export async function voteMessage({
  chatId,
  messageId,
  type,
}: {
  chatId: string;
  messageId: string;
  type: 'up' | 'down';
}) {
  try {
    const [existingVote] = await db
      .select()
      .from(vote)
      .where(and(eq(vote.messageId, messageId)));

    if (existingVote) {
      return await db
        .update(vote)
        .set({ isUpvoted: type === 'up' })
        .where(and(eq(vote.messageId, messageId), eq(vote.chatId, chatId)));
    }
    return await db.insert(vote).values({
      chatId,
      messageId,
      isUpvoted: type === 'up',
    });
  } catch (error) {
    throw new ChatSDKError('bad_request:database', 'Failed to vote message');
  }
}

export async function getVotesByChatId({ id }: { id: string }) {
  try {
    return await db.select().from(vote).where(eq(vote.chatId, id));
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to get votes by chat id',
    );
  }
}

export async function saveDocument({
  id,
  title,
  kind,
  content,
  userId,
}: {
  id: string;
  title: string;
  kind: ArtifactKind;
  content: string;
  userId: string;
}) {
  try {
    return await db
      .insert(document)
      .values({
        id,
        title,
        kind,
        content,
        userId,
        createdAt: new Date(),
      })
      .returning();
  } catch (error) {
    throw new ChatSDKError('bad_request:database', 'Failed to save document');
  }
}

export async function getDocumentsById({ id }: { id: string }) {
  try {
    const documents = await db
      .select()
      .from(document)
      .where(eq(document.id, id))
      .orderBy(asc(document.createdAt));

    return documents;
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to get documents by id',
    );
  }
}

export async function getDocumentById({ id }: { id: string }) {
  try {
    const [selectedDocument] = await db
      .select()
      .from(document)
      .where(eq(document.id, id))
      .orderBy(desc(document.createdAt));

    return selectedDocument;
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to get document by id',
    );
  }
}

export async function deleteDocumentsByIdAfterTimestamp({
  id,
  timestamp,
}: {
  id: string;
  timestamp: Date;
}) {
  try {
    await db
      .delete(suggestion)
      .where(
        and(
          eq(suggestion.documentId, id),
          gt(suggestion.documentCreatedAt, timestamp),
        ),
      );

    return await db
      .delete(document)
      .where(and(eq(document.id, id), gt(document.createdAt, timestamp)))
      .returning();
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to delete documents by id after timestamp',
    );
  }
}

export async function saveSuggestions({
  suggestions,
}: {
  suggestions: Array<Suggestion>;
}) {
  try {
    return await db.insert(suggestion).values(suggestions);
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to save suggestions',
    );
  }
}

export async function getSuggestionsByDocumentId({
  documentId,
}: {
  documentId: string;
}) {
  try {
    return await db
      .select()
      .from(suggestion)
      .where(and(eq(suggestion.documentId, documentId)));
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to get suggestions by document id',
    );
  }
}

export async function getMessageById({ id }: { id: string }) {
  try {
    return await db.select().from(message).where(eq(message.id, id));
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to get message by id',
    );
  }
}

export async function deleteMessagesByChatIdAfterTimestamp({
  chatId,
  timestamp,
}: {
  chatId: string;
  timestamp: Date;
}) {
  try {
    const messagesToDelete = await db
      .select({ id: message.id })
      .from(message)
      .where(
        and(eq(message.chatId, chatId), gte(message.createdAt, timestamp)),
      );

    const messageIds = messagesToDelete.map((message) => message.id);

    if (messageIds.length > 0) {
      await db
        .delete(vote)
        .where(
          and(eq(vote.chatId, chatId), inArray(vote.messageId, messageIds)),
        );

      return await db
        .delete(message)
        .where(
          and(eq(message.chatId, chatId), inArray(message.id, messageIds)),
        );
    }
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to delete messages by chat id after timestamp',
    );
  }
}

export async function updateChatVisiblityById({
  chatId,
  visibility,
}: {
  chatId: string;
  visibility: 'private' | 'public';
}) {
  try {
    return await db.update(chat).set({ visibility }).where(eq(chat.id, chatId));
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to update chat visibility by id',
    );
  }
}

export async function getMessageCountByUserId({
  id,
  differenceInHours,
}: { id: string; differenceInHours: number }) {
  try {
    const twentyFourHoursAgo = new Date(
      Date.now() - differenceInHours * 60 * 60 * 1000,
    );

    const [stats] = await db
      .select({ count: count(message.id) })
      .from(message)
      .innerJoin(chat, eq(message.chatId, chat.id))
      .where(
        and(
          eq(chat.userId, id),
          gte(message.createdAt, twentyFourHoursAgo),
          eq(message.role, 'user'),
        ),
      )
      .execute();

    return stats?.count ?? 0;
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to get message count by user id',
    );
  }
}

export async function createStreamId({
  streamId,
  chatId,
}: {
  streamId: string;
  chatId: string;
}) {
  try {
    await db
      .insert(stream)
      .values({ id: streamId, chatId, createdAt: new Date() });
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to create stream id',
    );
  }
}

export async function getStreamIdsByChatId({ chatId }: { chatId: string }) {
  try {
    const streamIds = await db
      .select({ id: stream.id })
      .from(stream)
      .where(eq(stream.chatId, chatId))
      .orderBy(asc(stream.createdAt))
      .execute();

    return streamIds.map(({ id }) => id);
  } catch (error) {
    throw new ChatSDKError(
      'bad_request:database',
      'Failed to get stream ids by chat id',
    );
  }
}



================================================
FILE: lib/db/schema.ts
================================================
import type { InferSelectModel } from 'drizzle-orm';
import {
  pgTable,
  varchar,
  timestamp,
  json,
  uuid,
  text,
  primaryKey,
  foreignKey,
  boolean,
} from 'drizzle-orm/pg-core';

export const user = pgTable('User', {
  id: uuid('id').primaryKey().notNull().defaultRandom(),
  email: varchar('email', { length: 64 }).notNull(),
  password: varchar('password', { length: 64 }),
});

export type User = InferSelectModel<typeof user>;

export const chat = pgTable('Chat', {
  id: uuid('id').primaryKey().notNull().defaultRandom(),
  createdAt: timestamp('createdAt').notNull(),
  title: text('title').notNull(),
  userId: uuid('userId')
    .notNull()
    .references(() => user.id),
  visibility: varchar('visibility', { enum: ['public', 'private'] })
    .notNull()
    .default('private'),
});

export type Chat = InferSelectModel<typeof chat>;

// DEPRECATED: The following schema is deprecated and will be removed in the future.
// Read the migration guide at https://chat-sdk.dev/docs/migration-guides/message-parts
export const messageDeprecated = pgTable('Message', {
  id: uuid('id').primaryKey().notNull().defaultRandom(),
  chatId: uuid('chatId')
    .notNull()
    .references(() => chat.id),
  role: varchar('role').notNull(),
  content: json('content').notNull(),
  createdAt: timestamp('createdAt').notNull(),
});

export type MessageDeprecated = InferSelectModel<typeof messageDeprecated>;

export const message = pgTable('Message_v2', {
  id: uuid('id').primaryKey().notNull().defaultRandom(),
  chatId: uuid('chatId')
    .notNull()
    .references(() => chat.id),
  role: varchar('role').notNull(),
  parts: json('parts').notNull(),
  attachments: json('attachments').notNull(),
  createdAt: timestamp('createdAt').notNull(),
});

export type DBMessage = InferSelectModel<typeof message>;

// DEPRECATED: The following schema is deprecated and will be removed in the future.
// Read the migration guide at https://chat-sdk.dev/docs/migration-guides/message-parts
export const voteDeprecated = pgTable(
  'Vote',
  {
    chatId: uuid('chatId')
      .notNull()
      .references(() => chat.id),
    messageId: uuid('messageId')
      .notNull()
      .references(() => messageDeprecated.id),
    isUpvoted: boolean('isUpvoted').notNull(),
  },
  (table) => {
    return {
      pk: primaryKey({ columns: [table.chatId, table.messageId] }),
    };
  },
);

export type VoteDeprecated = InferSelectModel<typeof voteDeprecated>;

export const vote = pgTable(
  'Vote_v2',
  {
    chatId: uuid('chatId')
      .notNull()
      .references(() => chat.id),
    messageId: uuid('messageId')
      .notNull()
      .references(() => message.id),
    isUpvoted: boolean('isUpvoted').notNull(),
  },
  (table) => {
    return {
      pk: primaryKey({ columns: [table.chatId, table.messageId] }),
    };
  },
);

export type Vote = InferSelectModel<typeof vote>;

export const document = pgTable(
  'Document',
  {
    id: uuid('id').notNull().defaultRandom(),
    createdAt: timestamp('createdAt').notNull(),
    title: text('title').notNull(),
    content: text('content'),
    kind: varchar('text', { enum: ['text', 'code', 'image', 'sheet'] })
      .notNull()
      .default('text'),
    userId: uuid('userId')
      .notNull()
      .references(() => user.id),
  },
  (table) => {
    return {
      pk: primaryKey({ columns: [table.id, table.createdAt] }),
    };
  },
);

export type Document = InferSelectModel<typeof document>;

export const suggestion = pgTable(
  'Suggestion',
  {
    id: uuid('id').notNull().defaultRandom(),
    documentId: uuid('documentId').notNull(),
    documentCreatedAt: timestamp('documentCreatedAt').notNull(),
    originalText: text('originalText').notNull(),
    suggestedText: text('suggestedText').notNull(),
    description: text('description'),
    isResolved: boolean('isResolved').notNull().default(false),
    userId: uuid('userId')
      .notNull()
      .references(() => user.id),
    createdAt: timestamp('createdAt').notNull(),
  },
  (table) => ({
    pk: primaryKey({ columns: [table.id] }),
    documentRef: foreignKey({
      columns: [table.documentId, table.documentCreatedAt],
      foreignColumns: [document.id, document.createdAt],
    }),
  }),
);

export type Suggestion = InferSelectModel<typeof suggestion>;

export const stream = pgTable(
  'Stream',
  {
    id: uuid('id').notNull().defaultRandom(),
    chatId: uuid('chatId').notNull(),
    createdAt: timestamp('createdAt').notNull(),
  },
  (table) => ({
    pk: primaryKey({ columns: [table.id] }),
    chatRef: foreignKey({
      columns: [table.chatId],
      foreignColumns: [chat.id],
    }),
  }),
);

export type Stream = InferSelectModel<typeof stream>;



================================================
FILE: lib/db/utils.ts
================================================
import { generateId } from 'ai';
import { genSaltSync, hashSync } from 'bcrypt-ts';

export function generateHashedPassword(password: string) {
  const salt = genSaltSync(10);
  const hash = hashSync(password, salt);

  return hash;
}

export function generateDummyPassword() {
  const password = generateId();
  const hashedPassword = generateHashedPassword(password);

  return hashedPassword;
}



================================================
FILE: lib/db/helpers/01-core-to-parts.ts
================================================
// This is a helper for an older version of ai, v4.3.13

// import { config } from 'dotenv';
// import postgres from 'postgres';
// import {
//   chat,
//   message,
//   type MessageDeprecated,
//   messageDeprecated,
//   vote,
//   voteDeprecated,
// } from '../schema';
// import { drizzle } from 'drizzle-orm/postgres-js';
// import { inArray } from 'drizzle-orm';
// import { appendResponseMessages, type UIMessage } from 'ai';

// config({
//   path: '.env.local',
// });

// if (!process.env.POSTGRES_URL) {
//   throw new Error('POSTGRES_URL environment variable is not set');
// }

// const client = postgres(process.env.POSTGRES_URL);
// const db = drizzle(client);

// const BATCH_SIZE = 100; // Process 100 chats at a time
// const INSERT_BATCH_SIZE = 1000; // Insert 1000 messages at a time

// type NewMessageInsert = {
//   id: string;
//   chatId: string;
//   parts: any[];
//   role: string;
//   attachments: any[];
//   createdAt: Date;
// };

// type NewVoteInsert = {
//   messageId: string;
//   chatId: string;
//   isUpvoted: boolean;
// };

// interface MessageDeprecatedContentPart {
//   type: string;
//   content: unknown;
// }

// function getMessageRank(message: MessageDeprecated): number {
//   if (
//     message.role === 'assistant' &&
//     (message.content as MessageDeprecatedContentPart[]).some(
//       (contentPart) => contentPart.type === 'tool-call',
//     )
//   ) {
//     return 0;
//   }

//   if (
//     message.role === 'tool' &&
//     (message.content as MessageDeprecatedContentPart[]).some(
//       (contentPart) => contentPart.type === 'tool-result',
//     )
//   ) {
//     return 1;
//   }

//   if (message.role === 'assistant') {
//     return 2;
//   }

//   return 3;
// }

// function dedupeParts<T extends { type: string; [k: string]: any }>(
//   parts: T[],
// ): T[] {
//   const seen = new Set<string>();
//   return parts.filter((p) => {
//     const key = `${p.type}|${JSON.stringify(p.content ?? p)}`;
//     if (seen.has(key)) return false;
//     seen.add(key);
//     return true;
//   });
// }

// function sanitizeParts<T extends { type: string; [k: string]: any }>(
//   parts: T[],
// ): T[] {
//   return parts.filter(
//     (part) => !(part.type === 'reasoning' && part.reasoning === 'undefined'),
//   );
// }

// async function migrateMessages() {
//   const chats = await db.select().from(chat);

//   let processedCount = 0;

//   for (let i = 0; i < chats.length; i += BATCH_SIZE) {
//     const chatBatch = chats.slice(i, i + BATCH_SIZE);
//     const chatIds = chatBatch.map((chat) => chat.id);

//     const allMessages = await db
//       .select()
//       .from(messageDeprecated)
//       .where(inArray(messageDeprecated.chatId, chatIds));

//     const allVotes = await db
//       .select()
//       .from(voteDeprecated)
//       .where(inArray(voteDeprecated.chatId, chatIds));

//     const newMessagesToInsert: NewMessageInsert[] = [];
//     const newVotesToInsert: NewVoteInsert[] = [];

//     for (const chat of chatBatch) {
//       processedCount++;
//       console.info(`Processed ${processedCount}/${chats.length} chats`);

//       const messages = allMessages
//         .filter((message) => message.chatId === chat.id)
//         .sort((a, b) => {
//           const differenceInTime =
//             new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
//           if (differenceInTime !== 0) return differenceInTime;

//           return getMessageRank(a) - getMessageRank(b);
//         });

//       const votes = allVotes.filter((v) => v.chatId === chat.id);

//       const messageSection: Array<UIMessage> = [];
//       const messageSections: Array<Array<UIMessage>> = [];

//       for (const message of messages) {
//         const { role } = message;

//         if (role === 'user' && messageSection.length > 0) {
//           messageSections.push([...messageSection]);
//           messageSection.length = 0;
//         }

//         // @ts-expect-error message.content has different type
//         messageSection.push(message);
//       }

//       if (messageSection.length > 0) {
//         messageSections.push([...messageSection]);
//       }

//       for (const section of messageSections) {
//         const [userMessage, ...assistantMessages] = section;

//         const [firstAssistantMessage] = assistantMessages;

//         try {
//           const uiSection = appendResponseMessages({
//             messages: [userMessage],
//             // @ts-expect-error: message.content has different type
//             responseMessages: assistantMessages,
//             _internal: {
//               currentDate: () => firstAssistantMessage.createdAt ?? new Date(),
//             },
//           });

//           const projectedUISection = uiSection
//             .map((message) => {
//               if (message.role === 'user') {
//                 return {
//                   id: message.id,
//                   chatId: chat.id,
//                   parts: [{ type: 'text', text: message.content }],
//                   role: message.role,
//                   createdAt: message.createdAt,
//                   attachments: [],
//                 } as NewMessageInsert;
//               } else if (message.role === 'assistant') {
//                 const cleanParts = sanitizeParts(
//                   dedupeParts(message.parts || []),
//                 );

//                 return {
//                   id: message.id,
//                   chatId: chat.id,
//                   parts: cleanParts,
//                   role: message.role,
//                   createdAt: message.createdAt,
//                   attachments: [],
//                 } as NewMessageInsert;
//               }
//               return null;
//             })
//             .filter((msg): msg is NewMessageInsert => msg !== null);

//           for (const msg of projectedUISection) {
//             newMessagesToInsert.push(msg);

//             if (msg.role === 'assistant') {
//               const voteByMessage = votes.find((v) => v.messageId === msg.id);
//               if (voteByMessage) {
//                 newVotesToInsert.push({
//                   messageId: msg.id,
//                   chatId: msg.chatId,
//                   isUpvoted: voteByMessage.isUpvoted,
//                 });
//               }
//             }
//           }
//         } catch (error) {
//           console.error(`Error processing chat ${chat.id}: ${error}`);
//         }
//       }
//     }

//     for (let j = 0; j < newMessagesToInsert.length; j += INSERT_BATCH_SIZE) {
//       const messageBatch = newMessagesToInsert.slice(j, j + INSERT_BATCH_SIZE);
//       if (messageBatch.length > 0) {
//         const validMessageBatch = messageBatch.map((msg) => ({
//           id: msg.id,
//           chatId: msg.chatId,
//           parts: msg.parts,
//           role: msg.role,
//           attachments: msg.attachments,
//           createdAt: msg.createdAt,
//         }));

//         await db.insert(message).values(validMessageBatch);
//       }
//     }

//     for (let j = 0; j < newVotesToInsert.length; j += INSERT_BATCH_SIZE) {
//       const voteBatch = newVotesToInsert.slice(j, j + INSERT_BATCH_SIZE);
//       if (voteBatch.length > 0) {
//         await db.insert(vote).values(voteBatch);
//       }
//     }
//   }

//   console.info(`Migration completed: ${processedCount} chats processed`);
// }

// migrateMessages()
//   .then(() => {
//     console.info('Script completed successfully');
//     process.exit(0);
//   })
//   .catch((error) => {
//     console.error('Script failed:', error);
//     process.exit(1);
//   });



================================================
FILE: lib/db/migrations/0000_keen_devos.sql
================================================
CREATE TABLE IF NOT EXISTS "Chat" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"createdAt" timestamp NOT NULL,
	"messages" json NOT NULL,
	"userId" uuid NOT NULL
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "User" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"email" varchar(64) NOT NULL,
	"password" varchar(64)
);
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "Chat" ADD CONSTRAINT "Chat_userId_User_id_fk" FOREIGN KEY ("userId") REFERENCES "public"."User"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;



================================================
FILE: lib/db/migrations/0001_sparkling_blue_marvel.sql
================================================
CREATE TABLE IF NOT EXISTS "Suggestion" (
	"id" uuid DEFAULT gen_random_uuid() NOT NULL,
	"documentId" uuid NOT NULL,
	"documentCreatedAt" timestamp NOT NULL,
	"originalText" text NOT NULL,
	"suggestedText" text NOT NULL,
	"description" text,
	"isResolved" boolean DEFAULT false NOT NULL,
	"userId" uuid NOT NULL,
	"createdAt" timestamp NOT NULL,
	CONSTRAINT "Suggestion_id_pk" PRIMARY KEY("id")
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "Document" (
	"id" uuid DEFAULT gen_random_uuid() NOT NULL,
	"createdAt" timestamp NOT NULL,
	"title" text NOT NULL,
	"content" text,
	"userId" uuid NOT NULL,
	CONSTRAINT "Document_id_createdAt_pk" PRIMARY KEY("id","createdAt")
);
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "Suggestion" ADD CONSTRAINT "Suggestion_userId_User_id_fk" FOREIGN KEY ("userId") REFERENCES "public"."User"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "Suggestion" ADD CONSTRAINT "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk" FOREIGN KEY ("documentId","documentCreatedAt") REFERENCES "public"."Document"("id","createdAt") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "Document" ADD CONSTRAINT "Document_userId_User_id_fk" FOREIGN KEY ("userId") REFERENCES "public"."User"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;



================================================
FILE: lib/db/migrations/0002_wandering_riptide.sql
================================================
CREATE TABLE IF NOT EXISTS "Message" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"chatId" uuid NOT NULL,
	"role" varchar NOT NULL,
	"content" json NOT NULL,
	"createdAt" timestamp NOT NULL
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "Vote" (
	"chatId" uuid NOT NULL,
	"messageId" uuid NOT NULL,
	"isUpvoted" boolean NOT NULL,
	CONSTRAINT "Vote_chatId_messageId_pk" PRIMARY KEY("chatId","messageId")
);
--> statement-breakpoint
ALTER TABLE "Chat" ADD COLUMN "title" text NOT NULL;--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "Message" ADD CONSTRAINT "Message_chatId_Chat_id_fk" FOREIGN KEY ("chatId") REFERENCES "public"."Chat"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "Vote" ADD CONSTRAINT "Vote_chatId_Chat_id_fk" FOREIGN KEY ("chatId") REFERENCES "public"."Chat"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "Vote" ADD CONSTRAINT "Vote_messageId_Message_id_fk" FOREIGN KEY ("messageId") REFERENCES "public"."Message"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
ALTER TABLE "Chat" DROP COLUMN IF EXISTS "messages";


================================================
FILE: lib/db/migrations/0003_cloudy_glorian.sql
================================================
ALTER TABLE "Chat" ADD COLUMN "visibility" varchar DEFAULT 'private' NOT NULL;


================================================
FILE: lib/db/migrations/0004_odd_slayback.sql
================================================
ALTER TABLE "Document" ADD COLUMN "text" varchar DEFAULT 'text' NOT NULL;


================================================
FILE: lib/db/migrations/0005_wooden_whistler.sql
================================================
CREATE TABLE IF NOT EXISTS "Message_v2" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"chatId" uuid NOT NULL,
	"role" varchar NOT NULL,
	"parts" json NOT NULL,
	"attachments" json NOT NULL,
	"createdAt" timestamp NOT NULL
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "Vote_v2" (
	"chatId" uuid NOT NULL,
	"messageId" uuid NOT NULL,
	"isUpvoted" boolean NOT NULL,
	CONSTRAINT "Vote_v2_chatId_messageId_pk" PRIMARY KEY("chatId","messageId")
);
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "Message_v2" ADD CONSTRAINT "Message_v2_chatId_Chat_id_fk" FOREIGN KEY ("chatId") REFERENCES "public"."Chat"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "Vote_v2" ADD CONSTRAINT "Vote_v2_chatId_Chat_id_fk" FOREIGN KEY ("chatId") REFERENCES "public"."Chat"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "Vote_v2" ADD CONSTRAINT "Vote_v2_messageId_Message_v2_id_fk" FOREIGN KEY ("messageId") REFERENCES "public"."Message_v2"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;



================================================
FILE: lib/db/migrations/0006_marvelous_frog_thor.sql
================================================
CREATE TABLE IF NOT EXISTS "Stream" (
	"id" uuid DEFAULT gen_random_uuid() NOT NULL,
	"chatId" uuid NOT NULL,
	"createdAt" timestamp NOT NULL,
	CONSTRAINT "Stream_id_pk" PRIMARY KEY("id")
);
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "Stream" ADD CONSTRAINT "Stream_chatId_Chat_id_fk" FOREIGN KEY ("chatId") REFERENCES "public"."Chat"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;



================================================
FILE: lib/db/migrations/meta/0000_snapshot.json
================================================
{
  "id": "715ec9ec-6715-4d0f-9f6c-9b5c7f09827c",
  "prevId": "00000000-0000-0000-0000-000000000000",
  "version": "7",
  "dialect": "postgresql",
  "tables": {
    "public.Chat": {
      "name": "Chat",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "messages": {
          "name": "messages",
          "type": "json",
          "primaryKey": false,
          "notNull": true
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Chat_userId_User_id_fk": {
          "name": "Chat_userId_User_id_fk",
          "tableFrom": "Chat",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.User": {
      "name": "User",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "email": {
          "name": "email",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": true
        },
        "password": {
          "name": "password",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": false
        }
      },
      "indexes": {},
      "foreignKeys": {},
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    }
  },
  "enums": {},
  "schemas": {},
  "sequences": {},
  "_meta": {
    "columns": {},
    "schemas": {},
    "tables": {}
  }
}


================================================
FILE: lib/db/migrations/meta/0001_snapshot.json
================================================
{
  "id": "f3d3437c-4735-4c91-80af-1014048a904e",
  "prevId": "715ec9ec-6715-4d0f-9f6c-9b5c7f09827c",
  "version": "7",
  "dialect": "postgresql",
  "tables": {
    "public.Suggestion": {
      "name": "Suggestion",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "documentId": {
          "name": "documentId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "documentCreatedAt": {
          "name": "documentCreatedAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "originalText": {
          "name": "originalText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "suggestedText": {
          "name": "suggestedText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "description": {
          "name": "description",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "isResolved": {
          "name": "isResolved",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true,
          "default": false
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Suggestion_userId_User_id_fk": {
          "name": "Suggestion_userId_User_id_fk",
          "tableFrom": "Suggestion",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk": {
          "name": "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk",
          "tableFrom": "Suggestion",
          "tableTo": "Document",
          "columnsFrom": [
            "documentId",
            "documentCreatedAt"
          ],
          "columnsTo": [
            "id",
            "createdAt"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Suggestion_id_pk": {
          "name": "Suggestion_id_pk",
          "columns": [
            "id"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.Chat": {
      "name": "Chat",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "messages": {
          "name": "messages",
          "type": "json",
          "primaryKey": false,
          "notNull": true
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Chat_userId_User_id_fk": {
          "name": "Chat_userId_User_id_fk",
          "tableFrom": "Chat",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Document": {
      "name": "Document",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "title": {
          "name": "title",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "content": {
          "name": "content",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Document_userId_User_id_fk": {
          "name": "Document_userId_User_id_fk",
          "tableFrom": "Document",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Document_id_createdAt_pk": {
          "name": "Document_id_createdAt_pk",
          "columns": [
            "id",
            "createdAt"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.User": {
      "name": "User",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "email": {
          "name": "email",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": true
        },
        "password": {
          "name": "password",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": false
        }
      },
      "indexes": {},
      "foreignKeys": {},
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    }
  },
  "enums": {},
  "schemas": {},
  "sequences": {},
  "_meta": {
    "columns": {},
    "schemas": {},
    "tables": {}
  }
}


================================================
FILE: lib/db/migrations/meta/0002_snapshot.json
================================================
{
  "id": "b5d8e862-936f-4419-a50f-97be3e7fe665",
  "prevId": "f3d3437c-4735-4c91-80af-1014048a904e",
  "version": "7",
  "dialect": "postgresql",
  "tables": {
    "public.Suggestion": {
      "name": "Suggestion",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "documentId": {
          "name": "documentId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "documentCreatedAt": {
          "name": "documentCreatedAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "originalText": {
          "name": "originalText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "suggestedText": {
          "name": "suggestedText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "description": {
          "name": "description",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "isResolved": {
          "name": "isResolved",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true,
          "default": false
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Suggestion_userId_User_id_fk": {
          "name": "Suggestion_userId_User_id_fk",
          "tableFrom": "Suggestion",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk": {
          "name": "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk",
          "tableFrom": "Suggestion",
          "tableTo": "Document",
          "columnsFrom": [
            "documentId",
            "documentCreatedAt"
          ],
          "columnsTo": [
            "id",
            "createdAt"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Suggestion_id_pk": {
          "name": "Suggestion_id_pk",
          "columns": [
            "id"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.Chat": {
      "name": "Chat",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "title": {
          "name": "title",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Chat_userId_User_id_fk": {
          "name": "Chat_userId_User_id_fk",
          "tableFrom": "Chat",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Document": {
      "name": "Document",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "title": {
          "name": "title",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "content": {
          "name": "content",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Document_userId_User_id_fk": {
          "name": "Document_userId_User_id_fk",
          "tableFrom": "Document",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Document_id_createdAt_pk": {
          "name": "Document_id_createdAt_pk",
          "columns": [
            "id",
            "createdAt"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.Message": {
      "name": "Message",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "role": {
          "name": "role",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true
        },
        "content": {
          "name": "content",
          "type": "json",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Message_chatId_Chat_id_fk": {
          "name": "Message_chatId_Chat_id_fk",
          "tableFrom": "Message",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.User": {
      "name": "User",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "email": {
          "name": "email",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": true
        },
        "password": {
          "name": "password",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": false
        }
      },
      "indexes": {},
      "foreignKeys": {},
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Vote": {
      "name": "Vote",
      "schema": "",
      "columns": {
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "messageId": {
          "name": "messageId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "isUpvoted": {
          "name": "isUpvoted",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Vote_chatId_Chat_id_fk": {
          "name": "Vote_chatId_Chat_id_fk",
          "tableFrom": "Vote",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Vote_messageId_Message_id_fk": {
          "name": "Vote_messageId_Message_id_fk",
          "tableFrom": "Vote",
          "tableTo": "Message",
          "columnsFrom": [
            "messageId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Vote_chatId_messageId_pk": {
          "name": "Vote_chatId_messageId_pk",
          "columns": [
            "chatId",
            "messageId"
          ]
        }
      },
      "uniqueConstraints": {}
    }
  },
  "enums": {},
  "schemas": {},
  "sequences": {},
  "_meta": {
    "columns": {},
    "schemas": {},
    "tables": {}
  }
}


================================================
FILE: lib/db/migrations/meta/0003_snapshot.json
================================================
{
  "id": "011efa9e-42c7-4ff6-830a-02106f6638c9",
  "prevId": "b5d8e862-936f-4419-a50f-97be3e7fe665",
  "version": "7",
  "dialect": "postgresql",
  "tables": {
    "public.Chat": {
      "name": "Chat",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "title": {
          "name": "title",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "visibility": {
          "name": "visibility",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true,
          "default": "'private'"
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Chat_userId_User_id_fk": {
          "name": "Chat_userId_User_id_fk",
          "tableFrom": "Chat",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Document": {
      "name": "Document",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "title": {
          "name": "title",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "content": {
          "name": "content",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Document_userId_User_id_fk": {
          "name": "Document_userId_User_id_fk",
          "tableFrom": "Document",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Document_id_createdAt_pk": {
          "name": "Document_id_createdAt_pk",
          "columns": [
            "id",
            "createdAt"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.Message": {
      "name": "Message",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "role": {
          "name": "role",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true
        },
        "content": {
          "name": "content",
          "type": "json",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Message_chatId_Chat_id_fk": {
          "name": "Message_chatId_Chat_id_fk",
          "tableFrom": "Message",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Suggestion": {
      "name": "Suggestion",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "documentId": {
          "name": "documentId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "documentCreatedAt": {
          "name": "documentCreatedAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "originalText": {
          "name": "originalText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "suggestedText": {
          "name": "suggestedText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "description": {
          "name": "description",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "isResolved": {
          "name": "isResolved",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true,
          "default": false
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Suggestion_userId_User_id_fk": {
          "name": "Suggestion_userId_User_id_fk",
          "tableFrom": "Suggestion",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk": {
          "name": "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk",
          "tableFrom": "Suggestion",
          "tableTo": "Document",
          "columnsFrom": [
            "documentId",
            "documentCreatedAt"
          ],
          "columnsTo": [
            "id",
            "createdAt"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Suggestion_id_pk": {
          "name": "Suggestion_id_pk",
          "columns": [
            "id"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.User": {
      "name": "User",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "email": {
          "name": "email",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": true
        },
        "password": {
          "name": "password",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": false
        }
      },
      "indexes": {},
      "foreignKeys": {},
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Vote": {
      "name": "Vote",
      "schema": "",
      "columns": {
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "messageId": {
          "name": "messageId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "isUpvoted": {
          "name": "isUpvoted",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Vote_chatId_Chat_id_fk": {
          "name": "Vote_chatId_Chat_id_fk",
          "tableFrom": "Vote",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Vote_messageId_Message_id_fk": {
          "name": "Vote_messageId_Message_id_fk",
          "tableFrom": "Vote",
          "tableTo": "Message",
          "columnsFrom": [
            "messageId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Vote_chatId_messageId_pk": {
          "name": "Vote_chatId_messageId_pk",
          "columns": [
            "chatId",
            "messageId"
          ]
        }
      },
      "uniqueConstraints": {}
    }
  },
  "enums": {},
  "schemas": {},
  "sequences": {},
  "_meta": {
    "columns": {},
    "schemas": {},
    "tables": {}
  }
}


================================================
FILE: lib/db/migrations/meta/0004_snapshot.json
================================================
{
  "id": "30ad8233-1432-428b-93fc-2bb1ba867ff1",
  "prevId": "011efa9e-42c7-4ff6-830a-02106f6638c9",
  "version": "7",
  "dialect": "postgresql",
  "tables": {
    "public.Chat": {
      "name": "Chat",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "title": {
          "name": "title",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "visibility": {
          "name": "visibility",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true,
          "default": "'private'"
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Chat_userId_User_id_fk": {
          "name": "Chat_userId_User_id_fk",
          "tableFrom": "Chat",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Document": {
      "name": "Document",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "title": {
          "name": "title",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "content": {
          "name": "content",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "text": {
          "name": "text",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true,
          "default": "'text'"
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Document_userId_User_id_fk": {
          "name": "Document_userId_User_id_fk",
          "tableFrom": "Document",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Document_id_createdAt_pk": {
          "name": "Document_id_createdAt_pk",
          "columns": [
            "id",
            "createdAt"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.Message": {
      "name": "Message",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "role": {
          "name": "role",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true
        },
        "content": {
          "name": "content",
          "type": "json",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Message_chatId_Chat_id_fk": {
          "name": "Message_chatId_Chat_id_fk",
          "tableFrom": "Message",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Suggestion": {
      "name": "Suggestion",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "documentId": {
          "name": "documentId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "documentCreatedAt": {
          "name": "documentCreatedAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "originalText": {
          "name": "originalText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "suggestedText": {
          "name": "suggestedText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "description": {
          "name": "description",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "isResolved": {
          "name": "isResolved",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true,
          "default": false
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Suggestion_userId_User_id_fk": {
          "name": "Suggestion_userId_User_id_fk",
          "tableFrom": "Suggestion",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk": {
          "name": "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk",
          "tableFrom": "Suggestion",
          "tableTo": "Document",
          "columnsFrom": [
            "documentId",
            "documentCreatedAt"
          ],
          "columnsTo": [
            "id",
            "createdAt"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Suggestion_id_pk": {
          "name": "Suggestion_id_pk",
          "columns": [
            "id"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.User": {
      "name": "User",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "email": {
          "name": "email",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": true
        },
        "password": {
          "name": "password",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": false
        }
      },
      "indexes": {},
      "foreignKeys": {},
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Vote": {
      "name": "Vote",
      "schema": "",
      "columns": {
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "messageId": {
          "name": "messageId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "isUpvoted": {
          "name": "isUpvoted",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Vote_chatId_Chat_id_fk": {
          "name": "Vote_chatId_Chat_id_fk",
          "tableFrom": "Vote",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Vote_messageId_Message_id_fk": {
          "name": "Vote_messageId_Message_id_fk",
          "tableFrom": "Vote",
          "tableTo": "Message",
          "columnsFrom": [
            "messageId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Vote_chatId_messageId_pk": {
          "name": "Vote_chatId_messageId_pk",
          "columns": [
            "chatId",
            "messageId"
          ]
        }
      },
      "uniqueConstraints": {}
    }
  },
  "enums": {},
  "schemas": {},
  "sequences": {},
  "_meta": {
    "columns": {},
    "schemas": {},
    "tables": {}
  }
}


================================================
FILE: lib/db/migrations/meta/0005_snapshot.json
================================================
{
  "id": "c6c102e6-b64e-4f0c-a7a6-32df758de437",
  "prevId": "30ad8233-1432-428b-93fc-2bb1ba867ff1",
  "version": "7",
  "dialect": "postgresql",
  "tables": {
    "public.Chat": {
      "name": "Chat",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "title": {
          "name": "title",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "visibility": {
          "name": "visibility",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true,
          "default": "'private'"
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Chat_userId_User_id_fk": {
          "name": "Chat_userId_User_id_fk",
          "tableFrom": "Chat",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Document": {
      "name": "Document",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "title": {
          "name": "title",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "content": {
          "name": "content",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "text": {
          "name": "text",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true,
          "default": "'text'"
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Document_userId_User_id_fk": {
          "name": "Document_userId_User_id_fk",
          "tableFrom": "Document",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Document_id_createdAt_pk": {
          "name": "Document_id_createdAt_pk",
          "columns": [
            "id",
            "createdAt"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.Message_v2": {
      "name": "Message_v2",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "role": {
          "name": "role",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true
        },
        "parts": {
          "name": "parts",
          "type": "json",
          "primaryKey": false,
          "notNull": true
        },
        "attachments": {
          "name": "attachments",
          "type": "json",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Message_v2_chatId_Chat_id_fk": {
          "name": "Message_v2_chatId_Chat_id_fk",
          "tableFrom": "Message_v2",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Message": {
      "name": "Message",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "role": {
          "name": "role",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true
        },
        "content": {
          "name": "content",
          "type": "json",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Message_chatId_Chat_id_fk": {
          "name": "Message_chatId_Chat_id_fk",
          "tableFrom": "Message",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Suggestion": {
      "name": "Suggestion",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "documentId": {
          "name": "documentId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "documentCreatedAt": {
          "name": "documentCreatedAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "originalText": {
          "name": "originalText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "suggestedText": {
          "name": "suggestedText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "description": {
          "name": "description",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "isResolved": {
          "name": "isResolved",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true,
          "default": false
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Suggestion_userId_User_id_fk": {
          "name": "Suggestion_userId_User_id_fk",
          "tableFrom": "Suggestion",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk": {
          "name": "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk",
          "tableFrom": "Suggestion",
          "tableTo": "Document",
          "columnsFrom": [
            "documentId",
            "documentCreatedAt"
          ],
          "columnsTo": [
            "id",
            "createdAt"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Suggestion_id_pk": {
          "name": "Suggestion_id_pk",
          "columns": [
            "id"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.User": {
      "name": "User",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "email": {
          "name": "email",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": true
        },
        "password": {
          "name": "password",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": false
        }
      },
      "indexes": {},
      "foreignKeys": {},
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Vote_v2": {
      "name": "Vote_v2",
      "schema": "",
      "columns": {
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "messageId": {
          "name": "messageId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "isUpvoted": {
          "name": "isUpvoted",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Vote_v2_chatId_Chat_id_fk": {
          "name": "Vote_v2_chatId_Chat_id_fk",
          "tableFrom": "Vote_v2",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Vote_v2_messageId_Message_v2_id_fk": {
          "name": "Vote_v2_messageId_Message_v2_id_fk",
          "tableFrom": "Vote_v2",
          "tableTo": "Message_v2",
          "columnsFrom": [
            "messageId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Vote_v2_chatId_messageId_pk": {
          "name": "Vote_v2_chatId_messageId_pk",
          "columns": [
            "chatId",
            "messageId"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.Vote": {
      "name": "Vote",
      "schema": "",
      "columns": {
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "messageId": {
          "name": "messageId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "isUpvoted": {
          "name": "isUpvoted",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Vote_chatId_Chat_id_fk": {
          "name": "Vote_chatId_Chat_id_fk",
          "tableFrom": "Vote",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Vote_messageId_Message_id_fk": {
          "name": "Vote_messageId_Message_id_fk",
          "tableFrom": "Vote",
          "tableTo": "Message",
          "columnsFrom": [
            "messageId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Vote_chatId_messageId_pk": {
          "name": "Vote_chatId_messageId_pk",
          "columns": [
            "chatId",
            "messageId"
          ]
        }
      },
      "uniqueConstraints": {}
    }
  },
  "enums": {},
  "schemas": {},
  "sequences": {},
  "_meta": {
    "columns": {},
    "schemas": {},
    "tables": {}
  }
}


================================================
FILE: lib/db/migrations/meta/0006_snapshot.json
================================================
{
  "id": "443de550-b7e8-4bfb-b229-c12dc6c132f0",
  "prevId": "c6c102e6-b64e-4f0c-a7a6-32df758de437",
  "version": "7",
  "dialect": "postgresql",
  "tables": {
    "public.Chat": {
      "name": "Chat",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "title": {
          "name": "title",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "visibility": {
          "name": "visibility",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true,
          "default": "'private'"
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Chat_userId_User_id_fk": {
          "name": "Chat_userId_User_id_fk",
          "tableFrom": "Chat",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Document": {
      "name": "Document",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "title": {
          "name": "title",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "content": {
          "name": "content",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "text": {
          "name": "text",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true,
          "default": "'text'"
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Document_userId_User_id_fk": {
          "name": "Document_userId_User_id_fk",
          "tableFrom": "Document",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Document_id_createdAt_pk": {
          "name": "Document_id_createdAt_pk",
          "columns": [
            "id",
            "createdAt"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.Message_v2": {
      "name": "Message_v2",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "role": {
          "name": "role",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true
        },
        "parts": {
          "name": "parts",
          "type": "json",
          "primaryKey": false,
          "notNull": true
        },
        "attachments": {
          "name": "attachments",
          "type": "json",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Message_v2_chatId_Chat_id_fk": {
          "name": "Message_v2_chatId_Chat_id_fk",
          "tableFrom": "Message_v2",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Message": {
      "name": "Message",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "role": {
          "name": "role",
          "type": "varchar",
          "primaryKey": false,
          "notNull": true
        },
        "content": {
          "name": "content",
          "type": "json",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Message_chatId_Chat_id_fk": {
          "name": "Message_chatId_Chat_id_fk",
          "tableFrom": "Message",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Stream": {
      "name": "Stream",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Stream_chatId_Chat_id_fk": {
          "name": "Stream_chatId_Chat_id_fk",
          "tableFrom": "Stream",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Stream_id_pk": {
          "name": "Stream_id_pk",
          "columns": [
            "id"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.Suggestion": {
      "name": "Suggestion",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "documentId": {
          "name": "documentId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "documentCreatedAt": {
          "name": "documentCreatedAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        },
        "originalText": {
          "name": "originalText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "suggestedText": {
          "name": "suggestedText",
          "type": "text",
          "primaryKey": false,
          "notNull": true
        },
        "description": {
          "name": "description",
          "type": "text",
          "primaryKey": false,
          "notNull": false
        },
        "isResolved": {
          "name": "isResolved",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true,
          "default": false
        },
        "userId": {
          "name": "userId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "createdAt": {
          "name": "createdAt",
          "type": "timestamp",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Suggestion_userId_User_id_fk": {
          "name": "Suggestion_userId_User_id_fk",
          "tableFrom": "Suggestion",
          "tableTo": "User",
          "columnsFrom": [
            "userId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk": {
          "name": "Suggestion_documentId_documentCreatedAt_Document_id_createdAt_fk",
          "tableFrom": "Suggestion",
          "tableTo": "Document",
          "columnsFrom": [
            "documentId",
            "documentCreatedAt"
          ],
          "columnsTo": [
            "id",
            "createdAt"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Suggestion_id_pk": {
          "name": "Suggestion_id_pk",
          "columns": [
            "id"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.User": {
      "name": "User",
      "schema": "",
      "columns": {
        "id": {
          "name": "id",
          "type": "uuid",
          "primaryKey": true,
          "notNull": true,
          "default": "gen_random_uuid()"
        },
        "email": {
          "name": "email",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": true
        },
        "password": {
          "name": "password",
          "type": "varchar(64)",
          "primaryKey": false,
          "notNull": false
        }
      },
      "indexes": {},
      "foreignKeys": {},
      "compositePrimaryKeys": {},
      "uniqueConstraints": {}
    },
    "public.Vote_v2": {
      "name": "Vote_v2",
      "schema": "",
      "columns": {
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "messageId": {
          "name": "messageId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "isUpvoted": {
          "name": "isUpvoted",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Vote_v2_chatId_Chat_id_fk": {
          "name": "Vote_v2_chatId_Chat_id_fk",
          "tableFrom": "Vote_v2",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Vote_v2_messageId_Message_v2_id_fk": {
          "name": "Vote_v2_messageId_Message_v2_id_fk",
          "tableFrom": "Vote_v2",
          "tableTo": "Message_v2",
          "columnsFrom": [
            "messageId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Vote_v2_chatId_messageId_pk": {
          "name": "Vote_v2_chatId_messageId_pk",
          "columns": [
            "chatId",
            "messageId"
          ]
        }
      },
      "uniqueConstraints": {}
    },
    "public.Vote": {
      "name": "Vote",
      "schema": "",
      "columns": {
        "chatId": {
          "name": "chatId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "messageId": {
          "name": "messageId",
          "type": "uuid",
          "primaryKey": false,
          "notNull": true
        },
        "isUpvoted": {
          "name": "isUpvoted",
          "type": "boolean",
          "primaryKey": false,
          "notNull": true
        }
      },
      "indexes": {},
      "foreignKeys": {
        "Vote_chatId_Chat_id_fk": {
          "name": "Vote_chatId_Chat_id_fk",
          "tableFrom": "Vote",
          "tableTo": "Chat",
          "columnsFrom": [
            "chatId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        },
        "Vote_messageId_Message_id_fk": {
          "name": "Vote_messageId_Message_id_fk",
          "tableFrom": "Vote",
          "tableTo": "Message",
          "columnsFrom": [
            "messageId"
          ],
          "columnsTo": [
            "id"
          ],
          "onDelete": "no action",
          "onUpdate": "no action"
        }
      },
      "compositePrimaryKeys": {
        "Vote_chatId_messageId_pk": {
          "name": "Vote_chatId_messageId_pk",
          "columns": [
            "chatId",
            "messageId"
          ]
        }
      },
      "uniqueConstraints": {}
    }
  },
  "enums": {},
  "schemas": {},
  "sequences": {},
  "_meta": {
    "columns": {},
    "schemas": {},
    "tables": {}
  }
}


================================================
FILE: lib/db/migrations/meta/_journal.json
================================================
{
  "version": "7",
  "dialect": "postgresql",
  "entries": [
    {
      "idx": 0,
      "version": "7",
      "when": 1728598022383,
      "tag": "0000_keen_devos",
      "breakpoints": true
    },
    {
      "idx": 1,
      "version": "7",
      "when": 1730207363999,
      "tag": "0001_sparkling_blue_marvel",
      "breakpoints": true
    },
    {
      "idx": 2,
      "version": "7",
      "when": 1730725226313,
      "tag": "0002_wandering_riptide",
      "breakpoints": true
    },
    {
      "idx": 3,
      "version": "7",
      "when": 1733403031014,
      "tag": "0003_cloudy_glorian",
      "breakpoints": true
    },
    {
      "idx": 4,
      "version": "7",
      "when": 1733945232355,
      "tag": "0004_odd_slayback",
      "breakpoints": true
    },
    {
      "idx": 5,
      "version": "7",
      "when": 1741934630596,
      "tag": "0005_wooden_whistler",
      "breakpoints": true
    },
    {
      "idx": 6,
      "version": "7",
      "when": 1746118166211,
      "tag": "0006_marvelous_frog_thor",
      "breakpoints": true
    }
  ]
}


================================================
FILE: lib/editor/config.ts
================================================
import { textblockTypeInputRule } from 'prosemirror-inputrules';
import { Schema } from 'prosemirror-model';
import { schema } from 'prosemirror-schema-basic';
import { addListNodes } from 'prosemirror-schema-list';
import type { Transaction } from 'prosemirror-state';
import type { EditorView } from 'prosemirror-view';
import type { MutableRefObject } from 'react';

import { buildContentFromDocument } from './functions';

export const documentSchema = new Schema({
  nodes: addListNodes(schema.spec.nodes, 'paragraph block*', 'block'),
  marks: schema.spec.marks,
});

export function headingRule(level: number) {
  return textblockTypeInputRule(
    new RegExp(`^(#{1,${level}})\\s$`),
    documentSchema.nodes.heading,
    () => ({ level }),
  );
}

export const handleTransaction = ({
  transaction,
  editorRef,
  onSaveContent,
}: {
  transaction: Transaction;
  editorRef: MutableRefObject<EditorView | null>;
  onSaveContent: (updatedContent: string, debounce: boolean) => void;
}) => {
  if (!editorRef || !editorRef.current) return;

  const newState = editorRef.current.state.apply(transaction);
  editorRef.current.updateState(newState);

  if (transaction.docChanged && !transaction.getMeta('no-save')) {
    const updatedContent = buildContentFromDocument(newState.doc);

    if (transaction.getMeta('no-debounce')) {
      onSaveContent(updatedContent, false);
    } else {
      onSaveContent(updatedContent, true);
    }
  }
};



================================================
FILE: lib/editor/diff.js
================================================
// Modified from https://github.com/hamflx/prosemirror-diff/blob/master/src/diff.js

import { diff_match_patch } from 'diff-match-patch';
import { Fragment, Node } from 'prosemirror-model';

export const DiffType = {
  Unchanged: 0,
  Deleted: -1,
  Inserted: 1,
};

export const patchDocumentNode = (schema, oldNode, newNode) => {
  assertNodeTypeEqual(oldNode, newNode);

  const finalLeftChildren = [];
  const finalRightChildren = [];

  const oldChildren = normalizeNodeContent(oldNode);
  const newChildren = normalizeNodeContent(newNode);
  const oldChildLen = oldChildren.length;
  const newChildLen = newChildren.length;
  const minChildLen = Math.min(oldChildLen, newChildLen);

  let left = 0;
  let right = 0;

  for (; left < minChildLen; left++) {
    const oldChild = oldChildren[left];
    const newChild = newChildren[left];
    if (!isNodeEqual(oldChild, newChild)) {
      break;
    }
    finalLeftChildren.push(...ensureArray(oldChild));
  }

  for (; right + left + 1 < minChildLen; right++) {
    const oldChild = oldChildren[oldChildLen - right - 1];
    const newChild = newChildren[newChildLen - right - 1];
    if (!isNodeEqual(oldChild, newChild)) {
      break;
    }
    finalRightChildren.unshift(...ensureArray(oldChild));
  }

  const diffOldChildren = oldChildren.slice(left, oldChildLen - right);
  const diffNewChildren = newChildren.slice(left, newChildLen - right);

  if (diffOldChildren.length && diffNewChildren.length) {
    const matchedNodes = matchNodes(
      schema,
      diffOldChildren,
      diffNewChildren,
    ).sort((a, b) => b.count - a.count);
    const bestMatch = matchedNodes[0];
    if (bestMatch) {
      const { oldStartIndex, newStartIndex, oldEndIndex, newEndIndex } =
        bestMatch;
      const oldBeforeMatchChildren = diffOldChildren.slice(0, oldStartIndex);
      const newBeforeMatchChildren = diffNewChildren.slice(0, newStartIndex);

      finalLeftChildren.push(
        ...patchRemainNodes(
          schema,
          oldBeforeMatchChildren,
          newBeforeMatchChildren,
        ),
      );
      finalLeftChildren.push(
        ...diffOldChildren.slice(oldStartIndex, oldEndIndex),
      );

      const oldAfterMatchChildren = diffOldChildren.slice(oldEndIndex);
      const newAfterMatchChildren = diffNewChildren.slice(newEndIndex);

      finalRightChildren.unshift(
        ...patchRemainNodes(
          schema,
          oldAfterMatchChildren,
          newAfterMatchChildren,
        ),
      );
    } else {
      finalLeftChildren.push(
        ...patchRemainNodes(schema, diffOldChildren, diffNewChildren),
      );
    }
  } else {
    finalLeftChildren.push(
      ...patchRemainNodes(schema, diffOldChildren, diffNewChildren),
    );
  }

  return createNewNode(oldNode, [...finalLeftChildren, ...finalRightChildren]);
};

const matchNodes = (schema, oldChildren, newChildren) => {
  const matches = [];
  for (
    let oldStartIndex = 0;
    oldStartIndex < oldChildren.length;
    oldStartIndex++
  ) {
    const oldStartNode = oldChildren[oldStartIndex];
    const newStartIndex = findMatchNode(newChildren, oldStartNode);

    if (newStartIndex !== -1) {
      let oldEndIndex = oldStartIndex + 1;
      let newEndIndex = newStartIndex + 1;
      for (
        ;
        oldEndIndex < oldChildren.length && newEndIndex < newChildren.length;
        oldEndIndex++, newEndIndex++
      ) {
        const oldEndNode = oldChildren[oldEndIndex];
        if (!isNodeEqual(newChildren[newEndIndex], oldEndNode)) {
          break;
        }
      }
      matches.push({
        oldStartIndex,
        newStartIndex,
        oldEndIndex,
        newEndIndex,
        count: newEndIndex - newStartIndex,
      });
    }
  }
  return matches;
};

const findMatchNode = (children, node, startIndex = 0) => {
  for (let i = startIndex; i < children.length; i++) {
    if (isNodeEqual(children[i], node)) {
      return i;
    }
  }
  return -1;
};

const patchRemainNodes = (schema, oldChildren, newChildren) => {
  const finalLeftChildren = [];
  const finalRightChildren = [];
  const oldChildLen = oldChildren.length;
  const newChildLen = newChildren.length;
  let left = 0;
  let right = 0;
  while (oldChildLen - left - right > 0 && newChildLen - left - right > 0) {
    const leftOldNode = oldChildren[left];
    const leftNewNode = newChildren[left];
    const rightOldNode = oldChildren[oldChildLen - right - 1];
    const rightNewNode = newChildren[newChildLen - right - 1];
    let updateLeft =
      !isTextNode(leftOldNode) && matchNodeType(leftOldNode, leftNewNode);
    let updateRight =
      !isTextNode(rightOldNode) && matchNodeType(rightOldNode, rightNewNode);
    if (Array.isArray(leftOldNode) && Array.isArray(leftNewNode)) {
      finalLeftChildren.push(
        ...patchTextNodes(schema, leftOldNode, leftNewNode),
      );
      left += 1;
      continue;
    }

    if (updateLeft && updateRight) {
      const equalityLeft = computeChildEqualityFactor(leftOldNode, leftNewNode);
      const equalityRight = computeChildEqualityFactor(
        rightOldNode,
        rightNewNode,
      );
      if (equalityLeft < equalityRight) {
        updateLeft = false;
      } else {
        updateRight = false;
      }
    }
    if (updateLeft) {
      finalLeftChildren.push(
        patchDocumentNode(schema, leftOldNode, leftNewNode),
      );
      left += 1;
    } else if (updateRight) {
      finalRightChildren.unshift(
        patchDocumentNode(schema, rightOldNode, rightNewNode),
      );
      right += 1;
    } else {
      // Delete and insert
      finalLeftChildren.push(
        createDiffNode(schema, leftOldNode, DiffType.Deleted),
      );
      finalLeftChildren.push(
        createDiffNode(schema, leftNewNode, DiffType.Inserted),
      );
      left += 1;
    }
  }

  const deleteNodeLen = oldChildLen - left - right;
  const insertNodeLen = newChildLen - left - right;
  if (deleteNodeLen) {
    finalLeftChildren.push(
      ...oldChildren
        .slice(left, left + deleteNodeLen)
        .flat()
        .map((node) => createDiffNode(schema, node, DiffType.Deleted)),
    );
  }

  if (insertNodeLen) {
    finalRightChildren.unshift(
      ...newChildren
        .slice(left, left + insertNodeLen)
        .flat()
        .map((node) => createDiffNode(schema, node, DiffType.Inserted)),
    );
  }

  return [...finalLeftChildren, ...finalRightChildren];
};

// Updated function to perform sentence-level diffs
export const patchTextNodes = (schema, oldNode, newNode) => {
  const dmp = new diff_match_patch();

  // Concatenate the text from the text nodes
  const oldText = oldNode.map((n) => getNodeText(n)).join('');
  const newText = newNode.map((n) => getNodeText(n)).join('');

  // Tokenize the text into sentences
  const oldSentences = tokenizeSentences(oldText);
  const newSentences = tokenizeSentences(newText);

  // Map sentences to unique characters
  const { chars1, chars2, lineArray } = sentencesToChars(
    oldSentences,
    newSentences,
  );

  // Perform the diff
  let diffs = dmp.diff_main(chars1, chars2, false);

  // Convert back to sentences
  diffs = diffs.map(([type, text]) => {
    const sentences = text
      .split('')
      .map((char) => lineArray[char.charCodeAt(0)]);
    return [type, sentences];
  });

  // Map diffs to nodes
  const res = diffs.flatMap(([type, sentences]) => {
    return sentences.map((sentence) => {
      const node = createTextNode(
        schema,
        sentence,
        type !== DiffType.Unchanged ? [createDiffMark(schema, type)] : [],
      );
      return node;
    });
  });

  return res;
};

// Function to tokenize text into sentences
const tokenizeSentences = (text) => {
  return text.match(/[^.!?]+[.!?]*\s*/g) || [];
};

// Function to map sentences to unique characters
const sentencesToChars = (oldSentences, newSentences) => {
  const lineArray = [];
  const lineHash = {};
  let lineStart = 0;

  const chars1 = oldSentences
    .map((sentence) => {
      const line = sentence;
      if (line in lineHash) {
        return String.fromCharCode(lineHash[line]);
      }
      lineHash[line] = lineStart;
      lineArray[lineStart] = line;
      lineStart++;
      return String.fromCharCode(lineHash[line]);
    })
    .join('');

  const chars2 = newSentences
    .map((sentence) => {
      const line = sentence;
      if (line in lineHash) {
        return String.fromCharCode(lineHash[line]);
      }
      lineHash[line] = lineStart;
      lineArray[lineStart] = line;
      lineStart++;
      return String.fromCharCode(lineHash[line]);
    })
    .join('');

  return { chars1, chars2, lineArray };
};

export const computeChildEqualityFactor = (node1, node2) => {
  return 0;
};

export const assertNodeTypeEqual = (node1, node2) => {
  if (getNodeProperty(node1, 'type') !== getNodeProperty(node2, 'type')) {
    throw new Error(`node type not equal: ${node1.type} !== ${node2.type}`);
  }
};

export const ensureArray = (value) => {
  return Array.isArray(value) ? value : [value];
};

export const isNodeEqual = (node1, node2) => {
  const isNode1Array = Array.isArray(node1);
  const isNode2Array = Array.isArray(node2);
  if (isNode1Array !== isNode2Array) {
    return false;
  }
  if (isNode1Array) {
    return (
      node1.length === node2.length &&
      node1.every((node, index) => isNodeEqual(node, node2[index]))
    );
  }

  const type1 = getNodeProperty(node1, 'type');
  const type2 = getNodeProperty(node2, 'type');
  if (type1 !== type2) {
    return false;
  }
  if (isTextNode(node1)) {
    const text1 = getNodeProperty(node1, 'text');
    const text2 = getNodeProperty(node2, 'text');
    if (text1 !== text2) {
      return false;
    }
  }
  const attrs1 = getNodeAttributes(node1);
  const attrs2 = getNodeAttributes(node2);
  const attrs = [...new Set([...Object.keys(attrs1), ...Object.keys(attrs2)])];
  for (const attr of attrs) {
    if (attrs1[attr] !== attrs2[attr]) {
      return false;
    }
  }
  const marks1 = getNodeMarks(node1);
  const marks2 = getNodeMarks(node2);
  if (marks1.length !== marks2.length) {
    return false;
  }
  for (let i = 0; i < marks1.length; i++) {
    if (!isNodeEqual(marks1[i], marks2[i])) {
      return false;
    }
  }
  const children1 = getNodeChildren(node1);
  const children2 = getNodeChildren(node2);
  if (children1.length !== children2.length) {
    return false;
  }
  for (let i = 0; i < children1.length; i++) {
    if (!isNodeEqual(children1[i], children2[i])) {
      return false;
    }
  }
  return true;
};

export const normalizeNodeContent = (node) => {
  const content = getNodeChildren(node) ?? [];
  const res = [];
  for (let i = 0; i < content.length; i++) {
    const child = content[i];
    if (isTextNode(child)) {
      const textNodes = [];
      for (
        let textNode = content[i];
        i < content.length && isTextNode(textNode);
        textNode = content[++i]
      ) {
        textNodes.push(textNode);
      }
      i--;
      res.push(textNodes);
    } else {
      res.push(child);
    }
  }
  return res;
};

export const getNodeProperty = (node, property) => {
  if (property === 'type') {
    return node.type?.name;
  }
  return node[property];
};

export const getNodeAttribute = (node, attribute) =>
  node.attrs ? node.attrs[attribute] : undefined;

export const getNodeAttributes = (node) => (node.attrs ? node.attrs : {});

export const getNodeMarks = (node) => node.marks ?? [];

export const getNodeChildren = (node) => node.content?.content ?? [];

export const getNodeText = (node) => node.text;

export const isTextNode = (node) => node.type?.name === 'text';

export const matchNodeType = (node1, node2) =>
  node1.type?.name === node2.type?.name ||
  (Array.isArray(node1) && Array.isArray(node2));

export const createNewNode = (oldNode, children) => {
  if (!oldNode.type) {
    throw new Error('oldNode.type is undefined');
  }
  return new Node(
    oldNode.type,
    oldNode.attrs,
    Fragment.fromArray(children),
    oldNode.marks,
  );
};

export const createDiffNode = (schema, node, type) => {
  return mapDocumentNode(node, (node) => {
    if (isTextNode(node)) {
      return createTextNode(schema, getNodeText(node), [
        ...(node.marks || []),
        createDiffMark(schema, type),
      ]);
    }
    return node;
  });
};

function mapDocumentNode(node, mapper) {
  const copy = node.copy(
    Fragment.from(
      node.content.content
        .map((node) => mapDocumentNode(node, mapper))
        .filter((n) => n),
    ),
  );
  return mapper(copy) || copy;
}

export const createDiffMark = (schema, type) => {
  if (type === DiffType.Inserted) {
    return schema.mark('diffMark', { type });
  }
  if (type === DiffType.Deleted) {
    return schema.mark('diffMark', { type });
  }
  throw new Error('type is not valid');
};

export const createTextNode = (schema, content, marks = []) => {
  return schema.text(content, marks);
};

export const diffEditor = (schema, oldDoc, newDoc) => {
  const oldNode = Node.fromJSON(schema, oldDoc);
  const newNode = Node.fromJSON(schema, newDoc);
  return patchDocumentNode(schema, oldNode, newNode);
};



================================================
FILE: lib/editor/functions.tsx
================================================
'use client';

import { defaultMarkdownSerializer } from 'prosemirror-markdown';
import { DOMParser, type Node } from 'prosemirror-model';
import { Decoration, DecorationSet, type EditorView } from 'prosemirror-view';
import { renderToString } from 'react-dom/server';

import { Response } from '@/components/elements/response';

import { documentSchema } from './config';
import { createSuggestionWidget, type UISuggestion } from './suggestions';

export const buildDocumentFromContent = (content: string) => {
  const parser = DOMParser.fromSchema(documentSchema);
  const stringFromMarkdown = renderToString(<Response>{content}</Response>);
  const tempContainer = document.createElement('div');
  tempContainer.innerHTML = stringFromMarkdown;
  return parser.parse(tempContainer);
};

export const buildContentFromDocument = (document: Node) => {
  return defaultMarkdownSerializer.serialize(document);
};

export const createDecorations = (
  suggestions: Array<UISuggestion>,
  view: EditorView,
) => {
  const decorations: Array<Decoration> = [];

  for (const suggestion of suggestions) {
    decorations.push(
      Decoration.inline(
        suggestion.selectionStart,
        suggestion.selectionEnd,
        {
          class: 'suggestion-highlight',
        },
        {
          suggestionId: suggestion.id,
          type: 'highlight',
        },
      ),
    );

    decorations.push(
      Decoration.widget(
        suggestion.selectionStart,
        (view) => {
          const { dom } = createSuggestionWidget(suggestion, view);
          return dom;
        },
        {
          suggestionId: suggestion.id,
          type: 'widget',
        },
      ),
    );
  }

  return DecorationSet.create(view.state.doc, decorations);
};



================================================
FILE: lib/editor/react-renderer.tsx
================================================
import { createRoot } from 'react-dom/client';

export class ReactRenderer {
  static render(component: React.ReactElement, dom: HTMLElement) {
    const root = createRoot(dom);
    root.render(component);

    return {
      destroy: () => root.unmount(),
    };
  }
}



================================================
FILE: lib/editor/suggestions.tsx
================================================
import type { Node } from 'prosemirror-model';
import { Plugin, PluginKey } from 'prosemirror-state';
import {
  type Decoration,
  DecorationSet,
  type EditorView,
} from 'prosemirror-view';
import { createRoot } from 'react-dom/client';

import { Suggestion as PreviewSuggestion } from '@/components/suggestion';
import type { Suggestion } from '@/lib/db/schema';
import type { ArtifactKind } from '@/components/artifact';

export interface UISuggestion extends Suggestion {
  selectionStart: number;
  selectionEnd: number;
}

interface Position {
  start: number;
  end: number;
}

function findPositionsInDoc(doc: Node, searchText: string): Position | null {
  let positions: { start: number; end: number } | null = null;

  doc.nodesBetween(0, doc.content.size, (node, pos) => {
    if (node.isText && node.text) {
      const index = node.text.indexOf(searchText);

      if (index !== -1) {
        positions = {
          start: pos + index,
          end: pos + index + searchText.length,
        };

        return false;
      }
    }

    return true;
  });

  return positions;
}

export function projectWithPositions(
  doc: Node,
  suggestions: Array<Suggestion>,
): Array<UISuggestion> {
  return suggestions.map((suggestion) => {
    const positions = findPositionsInDoc(doc, suggestion.originalText);

    if (!positions) {
      return {
        ...suggestion,
        selectionStart: 0,
        selectionEnd: 0,
      };
    }

    return {
      ...suggestion,
      selectionStart: positions.start,
      selectionEnd: positions.end,
    };
  });
}

export function createSuggestionWidget(
  suggestion: UISuggestion,
  view: EditorView,
  artifactKind: ArtifactKind = 'text',
): { dom: HTMLElement; destroy: () => void } {
  const dom = document.createElement('span');
  const root = createRoot(dom);

  dom.addEventListener('mousedown', (event) => {
    event.preventDefault();
    view.dom.blur();
  });

  const onApply = () => {
    const { state, dispatch } = view;

    const decorationTransaction = state.tr;
    const currentState = suggestionsPluginKey.getState(state);
    const currentDecorations = currentState?.decorations;

    if (currentDecorations) {
      const newDecorations = DecorationSet.create(
        state.doc,
        currentDecorations.find().filter((decoration: Decoration) => {
          return decoration.spec.suggestionId !== suggestion.id;
        }),
      );

      decorationTransaction.setMeta(suggestionsPluginKey, {
        decorations: newDecorations,
        selected: null,
      });
      dispatch(decorationTransaction);
    }

    const textTransaction = view.state.tr.replaceWith(
      suggestion.selectionStart,
      suggestion.selectionEnd,
      state.schema.text(suggestion.suggestedText),
    );

    textTransaction.setMeta('no-debounce', true);

    dispatch(textTransaction);
  };

  root.render(
    <PreviewSuggestion
      suggestion={suggestion}
      onApply={onApply}
      artifactKind={artifactKind}
    />,
  );

  return {
    dom,
    destroy: () => {
      // Wrapping unmount in setTimeout to avoid synchronous unmounting during render
      setTimeout(() => {
        root.unmount();
      }, 0);
    },
  };
}

export const suggestionsPluginKey = new PluginKey('suggestions');
export const suggestionsPlugin = new Plugin({
  key: suggestionsPluginKey,
  state: {
    init() {
      return { decorations: DecorationSet.empty, selected: null };
    },
    apply(tr, state) {
      const newDecorations = tr.getMeta(suggestionsPluginKey);
      if (newDecorations) return newDecorations;

      return {
        decorations: state.decorations.map(tr.mapping, tr.doc),
        selected: state.selected,
      };
    },
  },
  props: {
    decorations(state) {
      return this.getState(state)?.decorations ?? DecorationSet.empty;
    },
  },
});



================================================
FILE: tests/fixtures.ts
================================================
import { expect as baseExpect, test as baseTest } from '@playwright/test';
import { createAuthenticatedContext, type UserContext } from './helpers';
import { getUnixTime } from 'date-fns';

interface Fixtures {
  adaContext: UserContext;
  babbageContext: UserContext;
  curieContext: UserContext;
}

export const test = baseTest.extend<{}, Fixtures>({
  adaContext: [
    async ({ browser }, use, workerInfo) => {
      const ada = await createAuthenticatedContext({
        browser,
        name: `ada-${workerInfo.workerIndex}-${getUnixTime(new Date())}`,
      });

      await use(ada);
      await ada.context.close();
    },
    { scope: 'worker' },
  ],
  babbageContext: [
    async ({ browser }, use, workerInfo) => {
      const babbage = await createAuthenticatedContext({
        browser,
        name: `babbage-${workerInfo.workerIndex}-${getUnixTime(new Date())}`,
      });

      await use(babbage);
      await babbage.context.close();
    },
    { scope: 'worker' },
  ],
  curieContext: [
    async ({ browser }, use, workerInfo) => {
      const curie = await createAuthenticatedContext({
        browser,
        name: `curie-${workerInfo.workerIndex}-${getUnixTime(new Date())}`,
        chatModel: 'chat-model-reasoning',
      });

      await use(curie);
      await curie.context.close();
    },
    { scope: 'worker' },
  ],
});

export const expect = baseExpect;



================================================
FILE: tests/helpers.ts
================================================
import fs from 'node:fs';
import path from 'node:path';
import {
  type APIRequestContext,
  type Browser,
  type BrowserContext,
  expect,
  type Page,
} from '@playwright/test';
import { generateId } from 'ai';
import { ChatPage } from './pages/chat';
import { getUnixTime } from 'date-fns';

export type UserContext = {
  context: BrowserContext;
  page: Page;
  request: APIRequestContext;
};

export async function createAuthenticatedContext({
  browser,
  name,
  chatModel = 'chat-model',
}: {
  browser: Browser;
  name: string;
  chatModel?: 'chat-model' | 'chat-model-reasoning';
}): Promise<UserContext> {
  const directory = path.join(__dirname, '../playwright/.sessions');

  if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
  }

  const storageFile = path.join(directory, `${name}.json`);

  const context = await browser.newContext();
  const page = await context.newPage();

  const email = `test-${name}@playwright.com`;
  const password = generateId();

  await page.goto('http://localhost:3000/register');
  await page.getByPlaceholder('user@acme.com').click();
  await page.getByPlaceholder('user@acme.com').fill(email);
  await page.getByLabel('Password').click();
  await page.getByLabel('Password').fill(password);
  await page.getByRole('button', { name: 'Sign Up' }).click();

  await expect(page.getByTestId('toast')).toContainText(
    'Account created successfully!',
  );

  const chatPage = new ChatPage(page);
  await chatPage.createNewChat();
  await chatPage.chooseModelFromSelector('chat-model-reasoning');
  await expect(chatPage.getSelectedModel()).resolves.toEqual('Reasoning model');

  await page.waitForTimeout(1000);
  await context.storageState({ path: storageFile });
  await page.close();

  const newContext = await browser.newContext({ storageState: storageFile });
  const newPage = await newContext.newPage();

  return {
    context: newContext,
    page: newPage,
    request: newContext.request,
  };
}

export function generateRandomTestUser() {
  const email = `test-${getUnixTime(new Date())}@playwright.com`;
  const password = generateId();

  return {
    email,
    password,
  };
}



================================================
FILE: tests/e2e/artifacts.test.ts
================================================
import { expect, test } from '../fixtures';
import { ChatPage } from '../pages/chat';
import { ArtifactPage } from '../pages/artifact';

test.describe('Artifacts activity', () => {
  let chatPage: ChatPage;
  let artifactPage: ArtifactPage;

  test.beforeEach(async ({ page }) => {
    chatPage = new ChatPage(page);
    artifactPage = new ArtifactPage(page);

    await chatPage.createNewChat();
  });

  test('Create a text artifact', async () => {
    test.fixme();
    await chatPage.createNewChat();

    await chatPage.sendUserMessage(
      'Help me write an essay about Silicon Valley',
    );
    await artifactPage.isGenerationComplete();

    expect(artifactPage.artifact).toBeVisible();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    expect(assistantMessage.content).toBe(
      'A document was created and is now visible to the user.',
    );

    await chatPage.hasChatIdInUrl();
  });

  test('Toggle artifact visibility', async () => {
    test.fixme();
    await chatPage.createNewChat();

    await chatPage.sendUserMessage(
      'Help me write an essay about Silicon Valley',
    );
    await artifactPage.isGenerationComplete();

    expect(artifactPage.artifact).toBeVisible();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    expect(assistantMessage.content).toBe(
      'A document was created and is now visible to the user.',
    );

    await artifactPage.closeArtifact();
    await chatPage.isElementNotVisible('artifact');
  });

  test('Send follow up message after generation', async () => {
    test.fixme();
    await chatPage.createNewChat();

    await chatPage.sendUserMessage(
      'Help me write an essay about Silicon Valley',
    );
    await artifactPage.isGenerationComplete();

    expect(artifactPage.artifact).toBeVisible();

    const assistantMessage = await artifactPage.getRecentAssistantMessage();
    expect(assistantMessage.content).toBe(
      'A document was created and is now visible to the user.',
    );

    await artifactPage.sendUserMessage('Thanks!');
    await artifactPage.isGenerationComplete();

    const secondAssistantMessage = await chatPage.getRecentAssistantMessage();
    expect(secondAssistantMessage.content).toBe("You're welcome!");
  });
});



================================================
FILE: tests/e2e/chat.test.ts
================================================
import { ChatPage } from '../pages/chat';
import { test, expect } from '../fixtures';

test.describe('Chat activity', () => {
  let chatPage: ChatPage;

  test.beforeEach(async ({ page }) => {
    chatPage = new ChatPage(page);
    await chatPage.createNewChat();
  });

  test('Send a user message and receive response', async () => {
    await chatPage.sendUserMessage('Why is grass green?');
    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    expect(assistantMessage.content).toContain("It's just green duh!");
  });

  test('Redirect to /chat/:id after submitting message', async () => {
    await chatPage.sendUserMessage('Why is grass green?');
    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    expect(assistantMessage.content).toContain("It's just green duh!");
    await chatPage.hasChatIdInUrl();
  });

  test('Send a user message from suggestion', async () => {
    await chatPage.sendUserMessageFromSuggestion();
    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    expect(assistantMessage.content).toContain(
      'With Next.js, you can ship fast!',
    );
  });

  test('Toggle between send/stop button based on activity', async () => {
    await expect(chatPage.sendButton).toBeVisible();
    await expect(chatPage.sendButton).toBeDisabled();

    await chatPage.sendUserMessage('Why is grass green?');

    await expect(chatPage.sendButton).not.toBeVisible();
    await expect(chatPage.stopButton).toBeVisible();

    await chatPage.isGenerationComplete();

    await expect(chatPage.stopButton).not.toBeVisible();
    await expect(chatPage.sendButton).toBeVisible();
  });

  test('Stop generation during submission', async () => {
    await chatPage.sendUserMessage('Why is grass green?');
    await expect(chatPage.stopButton).toBeVisible();
    await chatPage.stopButton.click();
    await expect(chatPage.sendButton).toBeVisible();
  });

  test('Edit user message and resubmit', async () => {
    await chatPage.sendUserMessage('Why is grass green?');
    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    expect(assistantMessage.content).toContain("It's just green duh!");

    const userMessage = await chatPage.getRecentUserMessage();
    await userMessage.edit('Why is the sky blue?');

    await chatPage.isGenerationComplete();

    const updatedAssistantMessage = await chatPage.getRecentAssistantMessage();
    expect(updatedAssistantMessage.content).toContain("It's just blue duh!");
  });

  test('Hide suggested actions after sending message', async () => {
    await chatPage.isElementVisible('suggested-actions');
    await chatPage.sendUserMessageFromSuggestion();
    await chatPage.isElementNotVisible('suggested-actions');
  });

  test('Upload file and send image attachment with message', async () => {
    await chatPage.addImageAttachment();

    await chatPage.isElementVisible('attachments-preview');
    await chatPage.isElementVisible('input-attachment-loader');
    await chatPage.isElementNotVisible('input-attachment-loader');

    await chatPage.sendUserMessage('Who painted this?');

    const userMessage = await chatPage.getRecentUserMessage();
    expect(userMessage.attachments).toHaveLength(1);

    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    expect(assistantMessage.content).toBe('This painting is by Monet!');
  });

  test('Call weather tool', async () => {
    await chatPage.sendUserMessage("What's the weather in sf?");
    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();

    expect(assistantMessage.content).toBe(
      'The current temperature in San Francisco is 17°C.',
    );
  });

  test('Upvote message', async () => {
    await chatPage.sendUserMessage('Why is the sky blue?');
    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    await assistantMessage.upvote();
    await chatPage.isVoteComplete();
  });

  test('Downvote message', async () => {
    await chatPage.sendUserMessage('Why is the sky blue?');
    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    await assistantMessage.downvote();
    await chatPage.isVoteComplete();
  });

  test('Update vote', async () => {
    await chatPage.sendUserMessage('Why is the sky blue?');
    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    await assistantMessage.upvote();
    await chatPage.isVoteComplete();

    await assistantMessage.downvote();
    await chatPage.isVoteComplete();
  });

  test('Create message from url query', async ({ page }) => {
    await page.goto('/?query=Why is the sky blue?');

    await chatPage.isGenerationComplete();

    const userMessage = await chatPage.getRecentUserMessage();
    expect(userMessage.content).toBe('Why is the sky blue?');

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    expect(assistantMessage.content).toContain("It's just blue duh!");
  });

  test('auto-scrolls to bottom after submitting new messages', async () => {
    test.fixme();
    await chatPage.sendMultipleMessages(5, (i) => `filling message #${i}`);
    await chatPage.waitForScrollToBottom();
  });

  test('scroll button appears when user scrolls up, hides on click', async () => {
    test.fixme();
    await chatPage.sendMultipleMessages(5, (i) => `filling message #${i}`);
    await expect(chatPage.scrollToBottomButton).not.toBeVisible();

    await chatPage.scrollToTop();
    await expect(chatPage.scrollToBottomButton).toBeVisible();

    await chatPage.scrollToBottomButton.click();
    await chatPage.waitForScrollToBottom();
    await expect(chatPage.scrollToBottomButton).not.toBeVisible();
  });
});



================================================
FILE: tests/e2e/reasoning.test.ts
================================================
import { ChatPage } from '../pages/chat';
import { test, expect } from '../fixtures';

test.describe('chat activity with reasoning', () => {
  let chatPage: ChatPage;

  test.beforeEach(async ({ curieContext }) => {
    chatPage = new ChatPage(curieContext.page);
    await chatPage.createNewChat();
  });

  test('Curie can send message and generate response with reasoning', async () => {
    await chatPage.sendUserMessage('Why is the sky blue?');
    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    expect(assistantMessage.content).toBe("It's just blue duh!");

    expect(assistantMessage.reasoning).toBe(
      'The sky is blue because of rayleigh scattering!',
    );
  });

  test('Curie can toggle reasoning visibility', async () => {
    await chatPage.sendUserMessage('Why is the sky blue?');
    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    const reasoningElement =
      assistantMessage.element.getByTestId('message-reasoning');
    expect(reasoningElement).toBeVisible();

    await assistantMessage.toggleReasoningVisibility();
    await expect(reasoningElement).not.toBeVisible();

    await assistantMessage.toggleReasoningVisibility();
    await expect(reasoningElement).toBeVisible();
  });

  test('Curie can edit message and resubmit', async () => {
    await chatPage.sendUserMessage('Why is the sky blue?');
    await chatPage.isGenerationComplete();

    const assistantMessage = await chatPage.getRecentAssistantMessage();
    const reasoningElement =
      assistantMessage.element.getByTestId('message-reasoning');
    expect(reasoningElement).toBeVisible();

    const userMessage = await chatPage.getRecentUserMessage();

    await userMessage.edit('Why is grass green?');
    await chatPage.isGenerationComplete();

    const updatedAssistantMessage = await chatPage.getRecentAssistantMessage();

    expect(updatedAssistantMessage.content).toBe("It's just green duh!");

    expect(updatedAssistantMessage.reasoning).toBe(
      'Grass is green because of chlorophyll absorption!',
    );
  });
});



================================================
FILE: tests/e2e/session.test.ts
================================================
import { expect, test } from '../fixtures';
import { AuthPage } from '../pages/auth';
import { generateRandomTestUser } from '../helpers';
import { ChatPage } from '../pages/chat';
import { getMessageByErrorCode } from '@/lib/errors';

test.describe
  .serial('Guest Session', () => {
    test('Authenticate as guest user when a new session is loaded', async ({
      page,
    }) => {
      const response = await page.goto('/');

      if (!response) {
        throw new Error('Failed to load page');
      }

      let request = response.request();

      const chain = [];

      while (request) {
        chain.unshift(request.url());
        request = request.redirectedFrom();
      }

      expect(chain).toEqual([
        'http://localhost:3000/',
        'http://localhost:3000/api/auth/guest?redirectUrl=http%3A%2F%2Flocalhost%3A3000%2F',
        'http://localhost:3000/',
      ]);
    });

    test('Log out is not available for guest users', async ({ page }) => {
      await page.goto('/');

      const sidebarToggleButton = page.getByTestId('sidebar-toggle-button');
      await sidebarToggleButton.click();

      const userNavButton = page.getByTestId('user-nav-button');
      await expect(userNavButton).toBeVisible();

      await userNavButton.click();
      const userNavMenu = page.getByTestId('user-nav-menu');
      await expect(userNavMenu).toBeVisible();

      const authMenuItem = page.getByTestId('user-nav-item-auth');
      await expect(authMenuItem).toContainText('Login to your account');
    });

    test('Do not authenticate as guest user when an existing non-guest session is active', async ({
      adaContext,
    }) => {
      const response = await adaContext.page.goto('/');

      if (!response) {
        throw new Error('Failed to load page');
      }

      let request = response.request();

      const chain = [];

      while (request) {
        chain.unshift(request.url());
        request = request.redirectedFrom();
      }

      expect(chain).toEqual(['http://localhost:3000/']);
    });

    test('Allow navigating to /login as guest user', async ({ page }) => {
      await page.goto('/login');
      await page.waitForURL('/login');
      await expect(page).toHaveURL('/login');
    });

    test('Allow navigating to /register as guest user', async ({ page }) => {
      await page.goto('/register');
      await page.waitForURL('/register');
      await expect(page).toHaveURL('/register');
    });

    test('Do not show email in user menu for guest user', async ({ page }) => {
      await page.goto('/');

      const sidebarToggleButton = page.getByTestId('sidebar-toggle-button');
      await sidebarToggleButton.click();

      const userEmail = page.getByTestId('user-email');
      await expect(userEmail).toContainText('Guest');
    });
  });

test.describe
  .serial('Login and Registration', () => {
    let authPage: AuthPage;

    const testUser = generateRandomTestUser();

    test.beforeEach(async ({ page }) => {
      authPage = new AuthPage(page);
    });

    test('Register new account', async () => {
      await authPage.register(testUser.email, testUser.password);
      await authPage.expectToastToContain('Account created successfully!');
    });

    test('Register new account with existing email', async () => {
      await authPage.register(testUser.email, testUser.password);
      await authPage.expectToastToContain('Account already exists!');
    });

    test('Log into account that exists', async ({ page }) => {
      await authPage.login(testUser.email, testUser.password);

      await page.waitForURL('/');
      await expect(page.getByPlaceholder('Send a message...')).toBeVisible();
    });

    test('Display user email in user menu', async ({ page }) => {
      await authPage.login(testUser.email, testUser.password);

      await page.waitForURL('/');
      await expect(page.getByPlaceholder('Send a message...')).toBeVisible();

      const userEmail = await page.getByTestId('user-email');
      await expect(userEmail).toHaveText(testUser.email);
    });

    test('Log out as non-guest user', async () => {
      await authPage.logout(testUser.email, testUser.password);
    });

    test('Do not force create a guest session if non-guest session already exists', async ({
      page,
    }) => {
      await authPage.login(testUser.email, testUser.password);
      await page.waitForURL('/');

      const userEmail = await page.getByTestId('user-email');
      await expect(userEmail).toHaveText(testUser.email);

      await page.goto('/api/auth/guest');
      await page.waitForURL('/');

      const updatedUserEmail = await page.getByTestId('user-email');
      await expect(updatedUserEmail).toHaveText(testUser.email);
    });

    test('Log out is available for non-guest users', async ({ page }) => {
      await authPage.login(testUser.email, testUser.password);
      await page.waitForURL('/');

      authPage.openSidebar();

      const userNavButton = page.getByTestId('user-nav-button');
      await expect(userNavButton).toBeVisible();

      await userNavButton.click();
      const userNavMenu = page.getByTestId('user-nav-menu');
      await expect(userNavMenu).toBeVisible();

      const authMenuItem = page.getByTestId('user-nav-item-auth');
      await expect(authMenuItem).toContainText('Sign out');
    });

    test('Do not navigate to /register for non-guest users', async ({
      page,
    }) => {
      await authPage.login(testUser.email, testUser.password);
      await page.waitForURL('/');

      await page.goto('/register');
      await expect(page).toHaveURL('/');
    });

    test('Do not navigate to /login for non-guest users', async ({ page }) => {
      await authPage.login(testUser.email, testUser.password);
      await page.waitForURL('/');

      await page.goto('/login');
      await expect(page).toHaveURL('/');
    });
  });

test.describe('Entitlements', () => {
  let chatPage: ChatPage;

  test.beforeEach(async ({ page }) => {
    chatPage = new ChatPage(page);
  });

  test('Guest user cannot send more than 20 messages/day', async () => {
    test.fixme();
    await chatPage.createNewChat();

    for (let i = 0; i <= 20; i++) {
      await chatPage.sendUserMessage('Why is the sky blue?');
      await chatPage.isGenerationComplete();
    }

    await chatPage.sendUserMessage('Why is the sky blue?');
    await chatPage.expectToastToContain(
      getMessageByErrorCode('rate_limit:chat'),
    );
  });
});



================================================
FILE: tests/pages/artifact.ts
================================================
import { expect, type Page } from '@playwright/test';

export class ArtifactPage {
  constructor(private page: Page) {}

  public get artifact() {
    return this.page.getByTestId('artifact');
  }

  public get sendButton() {
    return this.artifact.getByTestId('send-button');
  }

  public get stopButton() {
    return this.page.getByTestId('stop-button');
  }

  public get multimodalInput() {
    return this.page.getByTestId('multimodal-input');
  }

  async isGenerationComplete() {
    const response = await this.page.waitForResponse((response) =>
      response.url().includes('/api/chat'),
    );

    await response.finished();
  }

  async sendUserMessage(message: string) {
    await this.artifact.getByTestId('multimodal-input').click();
    await this.artifact.getByTestId('multimodal-input').fill(message);
    await this.artifact.getByTestId('send-button').click();
  }

  async getRecentAssistantMessage() {
    const messageElements = await this.artifact
      .getByTestId('message-assistant')
      .all();
    const lastMessageElement = messageElements[messageElements.length - 1];

    const content = await lastMessageElement
      .getByTestId('message-content')
      .innerText()
      .catch(() => null);

    const reasoningElement = await lastMessageElement
      .getByTestId('message-reasoning')
      .isVisible()
      .then(async (visible) =>
        visible
          ? await lastMessageElement
              .getByTestId('message-reasoning')
              .innerText()
          : null,
      )
      .catch(() => null);

    return {
      element: lastMessageElement,
      content,
      reasoning: reasoningElement,
      async toggleReasoningVisibility() {
        await lastMessageElement
          .getByTestId('message-reasoning-toggle')
          .click();
      },
    };
  }

  async getRecentUserMessage() {
    const messageElements = await this.artifact
      .getByTestId('message-user')
      .all();
    const lastMessageElement = messageElements[messageElements.length - 1];

    const content = await lastMessageElement.innerText();

    const hasAttachments = await lastMessageElement
      .getByTestId('message-attachments')
      .isVisible()
      .catch(() => false);

    const attachments = hasAttachments
      ? await lastMessageElement.getByTestId('message-attachments').all()
      : [];

    const page = this.artifact;

    return {
      element: lastMessageElement,
      content,
      attachments,
      async edit(newMessage: string) {
        await page.getByTestId('message-edit-button').click();
        await page.getByTestId('message-editor').fill(newMessage);
        await page.getByTestId('message-editor-send-button').click();
        await expect(
          page.getByTestId('message-editor-send-button'),
        ).not.toBeVisible();
      },
    };
  }

  async closeArtifact() {
    return this.page.getByTestId('artifact-close-button').click();
  }
}



================================================
FILE: tests/pages/auth.ts
================================================
import type { Page } from '@playwright/test';
import { expect } from '../fixtures';

export class AuthPage {
  constructor(private page: Page) {}

  async gotoLogin() {
    await this.page.goto('/login');
    await expect(this.page.getByRole('heading')).toContainText('Sign In');
  }

  async gotoRegister() {
    await this.page.goto('/register');
    await expect(this.page.getByRole('heading')).toContainText('Sign Up');
  }

  async register(email: string, password: string) {
    await this.gotoRegister();
    await this.page.getByPlaceholder('user@acme.com').click();
    await this.page.getByPlaceholder('user@acme.com').fill(email);
    await this.page.getByLabel('Password').click();
    await this.page.getByLabel('Password').fill(password);
    await this.page.getByRole('button', { name: 'Sign Up' }).click();
  }

  async login(email: string, password: string) {
    await this.gotoLogin();
    await this.page.getByPlaceholder('user@acme.com').click();
    await this.page.getByPlaceholder('user@acme.com').fill(email);
    await this.page.getByLabel('Password').click();
    await this.page.getByLabel('Password').fill(password);
    await this.page.getByRole('button', { name: 'Sign In' }).click();
  }

  async logout(email: string, password: string) {
    await this.login(email, password);
    await this.page.waitForURL('/');

    await this.openSidebar();

    const userNavButton = this.page.getByTestId('user-nav-button');
    await expect(userNavButton).toBeVisible();

    await userNavButton.click();
    const userNavMenu = this.page.getByTestId('user-nav-menu');
    await expect(userNavMenu).toBeVisible();

    const authMenuItem = this.page.getByTestId('user-nav-item-auth');
    await expect(authMenuItem).toContainText('Sign out');

    await authMenuItem.click();

    const userEmail = this.page.getByTestId('user-email');
    await expect(userEmail).toContainText('Guest');
  }

  async expectToastToContain(text: string) {
    await expect(this.page.getByTestId('toast')).toContainText(text);
  }

  async openSidebar() {
    const sidebarToggleButton = this.page.getByTestId('sidebar-toggle-button');
    await sidebarToggleButton.click();
  }
}



================================================
FILE: tests/pages/chat.ts
================================================
import fs from 'node:fs';
import path from 'node:path';
import { chatModels } from '@/lib/ai/models';
import { expect, type Page } from '@playwright/test';

export class ChatPage {
  constructor(private page: Page) {}

  public get sendButton() {
    return this.page.getByTestId('send-button');
  }

  public get stopButton() {
    return this.page.getByTestId('stop-button');
  }

  public get multimodalInput() {
    return this.page.getByTestId('multimodal-input');
  }

  public get scrollContainer() {
    return this.page.locator('.overflow-y-scroll');
  }

  public get scrollToBottomButton() {
    return this.page.getByTestId('scroll-to-bottom-button');
  }

  async createNewChat() {
    await this.page.goto('/');
  }

  public getCurrentURL(): string {
    return this.page.url();
  }

  async sendUserMessage(message: string) {
    await this.multimodalInput.click();
    await this.multimodalInput.fill(message);
    await this.sendButton.click();
  }

  async isGenerationComplete() {
    const response = await this.page.waitForResponse((response) =>
      response.url().includes('/api/chat'),
    );

    await response.finished();
  }

  async isVoteComplete() {
    const response = await this.page.waitForResponse((response) =>
      response.url().includes('/api/vote'),
    );

    await response.finished();
  }

  async hasChatIdInUrl() {
    await expect(this.page).toHaveURL(
      /^http:\/\/localhost:3000\/chat\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/,
    );
  }

  async sendUserMessageFromSuggestion() {
    await this.page
      .getByRole('button', { name: 'What are the advantages of' })
      .click();
  }

  async isElementVisible(elementId: string) {
    await expect(this.page.getByTestId(elementId)).toBeVisible();
  }

  async isElementNotVisible(elementId: string) {
    await expect(this.page.getByTestId(elementId)).not.toBeVisible();
  }

  async addImageAttachment() {
    this.page.on('filechooser', async (fileChooser) => {
      const filePath = path.join(
        process.cwd(),
        'public',
        'images',
        'mouth of the seine, monet.jpg',
      );
      const imageBuffer = fs.readFileSync(filePath);

      await fileChooser.setFiles({
        name: 'mouth of the seine, monet.jpg',
        mimeType: 'image/jpeg',
        buffer: imageBuffer,
      });
    });

    await this.page.getByTestId('attachments-button').click();
  }

  public async getSelectedModel() {
    const modelId = await this.page.getByTestId('model-selector').innerText();
    return modelId;
  }

  public async chooseModelFromSelector(chatModelId: string) {
    const chatModel = chatModels.find(
      (chatModel) => chatModel.id === chatModelId,
    );

    if (!chatModel) {
      throw new Error(`Model with id ${chatModelId} not found`);
    }

    await this.page.getByTestId('model-selector').click();
    await this.page.getByTestId(`model-selector-item-${chatModelId}`).click();
    expect(await this.getSelectedModel()).toBe(chatModel.name);
  }

  public async getSelectedVisibility() {
    const visibilityId = await this.page
      .getByTestId('visibility-selector')
      .innerText();
    return visibilityId;
  }

  public async chooseVisibilityFromSelector(
    chatVisibility: 'public' | 'private',
  ) {
    await this.page.getByTestId('visibility-selector').click();
    await this.page
      .getByTestId(`visibility-selector-item-${chatVisibility}`)
      .click();
    expect(await this.getSelectedVisibility()).toBe(chatVisibility);
  }

  async getRecentAssistantMessage() {
    const messageElements = await this.page
      .getByTestId('message-assistant')
      .all();
    const lastMessageElement = messageElements[messageElements.length - 1];

    const content = await lastMessageElement
      .getByTestId('message-content')
      .innerText()
      .catch(() => null);

    const reasoningElement = await lastMessageElement
      .getByTestId('message-reasoning')
      .isVisible()
      .then(async (visible) =>
        visible
          ? await lastMessageElement
              .getByTestId('message-reasoning')
              .innerText()
          : null,
      )
      .catch(() => null);

    return {
      element: lastMessageElement,
      content,
      reasoning: reasoningElement,
      async toggleReasoningVisibility() {
        await lastMessageElement
          .getByTestId('message-reasoning-toggle')
          .click();
      },
      async upvote() {
        await lastMessageElement.getByTestId('message-upvote').click();
      },
      async downvote() {
        await lastMessageElement.getByTestId('message-downvote').click();
      },
    };
  }

  async getRecentUserMessage() {
    const messageElements = await this.page.getByTestId('message-user').all();
    const lastMessageElement = messageElements.at(-1);

    if (!lastMessageElement) {
      throw new Error('No user message found');
    }

    const content = await lastMessageElement
      .getByTestId('message-content')
      .innerText()
      .catch(() => null);

    const hasAttachments = await lastMessageElement
      .getByTestId('message-attachments')
      .isVisible()
      .catch(() => false);

    const attachments = hasAttachments
      ? await lastMessageElement.getByTestId('message-attachments').all()
      : [];

    const page = this.page;

    return {
      element: lastMessageElement,
      content,
      attachments,
      async edit(newMessage: string) {
        await page.getByTestId('message-edit-button').click();
        await page.getByTestId('message-editor').fill(newMessage);
        await page.getByTestId('message-editor-send-button').click();
        await expect(
          page.getByTestId('message-editor-send-button'),
        ).not.toBeVisible();
      },
    };
  }

  async expectToastToContain(text: string) {
    await expect(this.page.getByTestId('toast')).toContainText(text);
  }

  async openSideBar() {
    const sidebarToggleButton = this.page.getByTestId('sidebar-toggle-button');
    await sidebarToggleButton.click();
  }

  public async isScrolledToBottom(): Promise<boolean> {
    return this.scrollContainer.evaluate(
      (el) => Math.abs(el.scrollHeight - el.scrollTop - el.clientHeight) < 1,
    );
  }

  public async waitForScrollToBottom(timeout = 5_000): Promise<void> {
    const start = Date.now();

    while (Date.now() - start < timeout) {
      if (await this.isScrolledToBottom()) return;
      await this.page.waitForTimeout(100);
    }

    throw new Error(`Timed out waiting for scroll bottom after ${timeout}ms`);
  }

  public async sendMultipleMessages(
    count: number,
    makeMessage: (i: number) => string,
  ) {
    for (let i = 0; i < count; i++) {
      await this.sendUserMessage(makeMessage(i));
      await this.isGenerationComplete();
    }
  }

  public async scrollToTop(): Promise<void> {
    await this.scrollContainer.evaluate((element) => {
      element.scrollTop = 0;
    });
  }
}



================================================
FILE: tests/prompts/basic.ts
================================================
import type { ModelMessage } from 'ai';

export const TEST_PROMPTS: Record<string, ModelMessage> = {
  USER_SKY: {
    role: 'user',
    content: [{ type: 'text', text: 'Why is the sky blue?' }],
  },
  USER_GRASS: {
    role: 'user',
    content: [{ type: 'text', text: 'Why is grass green?' }],
  },
  USER_THANKS: {
    role: 'user',
    content: [{ type: 'text', text: 'Thanks!' }],
  },
  USER_NEXTJS: {
    role: 'user',
    content: [
      { type: 'text', text: 'What are the advantages of using Next.js?' },
    ],
  },
  USER_IMAGE_ATTACHMENT: {
    role: 'user',
    content: [
      {
        type: 'file',
        mediaType: '...',
        data: '...',
      },
      {
        type: 'text',
        text: 'Who painted this?',
      },
    ],
  },
  USER_TEXT_ARTIFACT: {
    role: 'user',
    content: [
      {
        type: 'text',
        text: 'Help me write an essay about Silicon Valley',
      },
    ],
  },
  CREATE_DOCUMENT_TEXT_CALL: {
    role: 'user',
    content: [
      {
        type: 'text',
        text: 'Essay about Silicon Valley',
      },
    ],
  },
  CREATE_DOCUMENT_TEXT_RESULT: {
    role: 'tool',
    content: [
      {
        type: 'tool-result',
        toolCallId: 'call_123',
        toolName: 'createDocument',
        output: {
          type: 'json',
          value: {
            id: '3ca386a4-40c6-4630-8ed1-84cbd46cc7eb',
            title: 'Essay about Silicon Valley',
            kind: 'text',
            content: 'A document was created and is now visible to the user.',
          },
        },
      },
    ],
  },
  GET_WEATHER_CALL: {
    role: 'user',
    content: [
      {
        type: 'text',
        text: "What's the weather in sf?",
      },
    ],
  },
  GET_WEATHER_RESULT: {
    role: 'tool',
    content: [
      {
        type: 'tool-result',
        toolCallId: 'call_456',
        toolName: 'getWeather',
        output: {
          type: 'json',
          value: {
            latitude: 37.763283,
            longitude: -122.41286,
            generationtime_ms: 0.06449222564697266,
            utc_offset_seconds: -25200,
            timezone: 'America/Los_Angeles',
            timezone_abbreviation: 'GMT-7',
            elevation: 18,
            current_units: {
              time: 'iso8601',
              interval: 'seconds',
              temperature_2m: '°C',
            },
            current: {
              time: '2025-03-10T14:00',
              interval: 900,
              temperature_2m: 17,
            },
            daily_units: {
              time: 'iso8601',
              sunrise: 'iso8601',
              sunset: 'iso8601',
            },
            daily: {
              time: [
                '2025-03-10',
                '2025-03-11',
                '2025-03-12',
                '2025-03-13',
                '2025-03-14',
                '2025-03-15',
                '2025-03-16',
              ],
              sunrise: [
                '2025-03-10T07:27',
                '2025-03-11T07:25',
                '2025-03-12T07:24',
                '2025-03-13T07:22',
                '2025-03-14T07:21',
                '2025-03-15T07:19',
                '2025-03-16T07:18',
              ],
              sunset: [
                '2025-03-10T19:12',
                '2025-03-11T19:13',
                '2025-03-12T19:14',
                '2025-03-13T19:15',
                '2025-03-14T19:16',
                '2025-03-15T19:17',
                '2025-03-16T19:17',
              ],
            },
          },
        },
      },
    ],
  },
};



================================================
FILE: tests/prompts/routes.ts
================================================
import { generateUUID } from '@/lib/utils';

export const TEST_PROMPTS = {
  SKY: {
    MESSAGE: {
      id: generateUUID(),
      createdAt: new Date().toISOString(),
      role: 'user',
      content: 'Why is the sky blue?',
      parts: [{ type: 'text', text: 'Why is the sky blue?' }],
    },
    OUTPUT_STREAM: [
      'data: {"type":"start-step"}',
      'data: {"type":"text-start","id":"STATIC_ID"}',
      'data: {"type":"text-delta","id":"STATIC_ID","delta":"It\'s "}',
      'data: {"type":"text-delta","id":"STATIC_ID","delta":"just "}',
      'data: {"type":"text-delta","id":"STATIC_ID","delta":"blue "}',
      'data: {"type":"text-delta","id":"STATIC_ID","delta":"duh! "}',
      'data: {"type":"text-end","id":"STATIC_ID"}',
      'data: {"type":"finish-step"}',
      'data: {"type":"finish"}',
      'data: [DONE]',
    ],
  },
  GRASS: {
    MESSAGE: {
      id: generateUUID(),
      createdAt: new Date().toISOString(),
      role: 'user',
      content: 'Why is grass green?',
      parts: [{ type: 'text', text: 'Why is grass green?' }],
    },
    OUTPUT_STREAM: [
      'data: {"type":"start-step"}',
      'data: {"type":"text-start","id":"STATIC_ID"}',
      'data: {"type":"text-delta","id":"STATIC_ID","delta":"It\'s "}',
      'data: {"type":"text-delta","id":"STATIC_ID","delta":"just "}',
      'data: {"type":"text-delta","id":"STATIC_ID","delta":"green "}',
      'data: {"type":"text-delta","id":"STATIC_ID","delta":"duh! "}',
      'data: {"type":"text-end","id":"STATIC_ID"}',
      'data: {"type":"finish-step"}',
      'data: {"type":"finish"}',
      'data: [DONE]',
    ],
  },
};



================================================
FILE: tests/prompts/utils.ts
================================================
import { generateId, type ModelMessage } from 'ai';
import { TEST_PROMPTS } from './basic';
import type { LanguageModelV2StreamPart } from '@ai-sdk/provider';

export function compareMessages(
  firstMessage: ModelMessage,
  secondMessage: ModelMessage,
): boolean {
  if (firstMessage.role !== secondMessage.role) return false;

  if (
    !Array.isArray(firstMessage.content) ||
    !Array.isArray(secondMessage.content)
  ) {
    return false;
  }

  if (firstMessage.content.length !== secondMessage.content.length) {
    return false;
  }

  for (let i = 0; i < firstMessage.content.length; i++) {
    const item1 = firstMessage.content[i];
    const item2 = secondMessage.content[i];

    if (item1.type !== item2.type) return false;

    if (item1.type === 'file' && item2.type === 'file') {
      // if (item1.image.toString() !== item2.image.toString()) return false;
      // if (item1.mimeType !== item2.mimeType) return false;
    } else if (item1.type === 'text' && item2.type === 'text') {
      if (item1.text !== item2.text) return false;
    } else if (item1.type === 'tool-result' && item2.type === 'tool-result') {
      if (item1.toolCallId !== item2.toolCallId) return false;
    } else {
      return false;
    }
  }

  return true;
}

const textToDeltas = (text: string): LanguageModelV2StreamPart[] => {
  const id = generateId();

  const deltas = text.split(' ').map((char) => ({
    id,
    type: 'text-delta' as const,
    delta: `${char} `,
  }));

  return [{ id, type: 'text-start' }, ...deltas, { id, type: 'text-end' }];
};

const reasoningToDeltas = (text: string): LanguageModelV2StreamPart[] => {
  const id = generateId();

  const deltas = text.split(' ').map((char) => ({
    id,
    type: 'reasoning-delta' as const,
    delta: `${char} `,
  }));

  return [
    { id, type: 'reasoning-start' },
    ...deltas,
    { id, type: 'reasoning-end' },
  ];
};

export const getResponseChunksByPrompt = (
  prompt: ModelMessage[],
  isReasoningEnabled = false,
): LanguageModelV2StreamPart[] => {
  const recentMessage = prompt.at(-1);

  if (!recentMessage) {
    throw new Error('No recent message found!');
  }

  if (isReasoningEnabled) {
    if (compareMessages(recentMessage, TEST_PROMPTS.USER_SKY)) {
      return [
        ...reasoningToDeltas('The sky is blue because of rayleigh scattering!'),
        ...textToDeltas("It's just blue duh!"),
        {
          type: 'finish',
          finishReason: 'stop',
          usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
        },
      ];
    } else if (compareMessages(recentMessage, TEST_PROMPTS.USER_GRASS)) {
      return [
        ...reasoningToDeltas(
          'Grass is green because of chlorophyll absorption!',
        ),
        ...textToDeltas("It's just green duh!"),
        {
          type: 'finish',
          finishReason: 'stop',
          usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
        },
      ];
    }
  }

  if (compareMessages(recentMessage, TEST_PROMPTS.USER_THANKS)) {
    return [
      ...textToDeltas("You're welcome!"),
      {
        type: 'finish',
        finishReason: 'stop',
        usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
      },
    ];
  } else if (compareMessages(recentMessage, TEST_PROMPTS.USER_GRASS)) {
    return [
      ...textToDeltas("It's just green duh!"),
      {
        type: 'finish',
        finishReason: 'stop',
        usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
      },
    ];
  } else if (compareMessages(recentMessage, TEST_PROMPTS.USER_SKY)) {
    return [
      ...textToDeltas("It's just blue duh!"),
      {
        type: 'finish',
        finishReason: 'stop',
        usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
      },
    ];
  } else if (compareMessages(recentMessage, TEST_PROMPTS.USER_NEXTJS)) {
    return [
      ...textToDeltas('With Next.js, you can ship fast!'),

      {
        type: 'finish',
        finishReason: 'stop',
        usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
      },
    ];
  } else if (
    compareMessages(recentMessage, TEST_PROMPTS.USER_IMAGE_ATTACHMENT)
  ) {
    return [
      ...textToDeltas('This painting is by Monet!'),
      {
        type: 'finish',
        finishReason: 'stop',
        usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
      },
    ];
  } else if (compareMessages(recentMessage, TEST_PROMPTS.USER_TEXT_ARTIFACT)) {
    const toolCallId = generateId();

    return [
      {
        id: toolCallId,
        type: 'tool-input-start',
        toolName: 'createDocument',
      },
      {
        id: toolCallId,
        type: 'tool-input-delta',
        delta: JSON.stringify({
          title: 'Essay about Silicon Valley',
          kind: 'text',
        }),
      },
      {
        id: toolCallId,
        type: 'tool-input-end',
      },
      {
        toolCallId: toolCallId,
        type: 'tool-result',
        toolName: 'createDocument',
        result: {
          id: 'doc_123',
          title: 'Essay about Silicon Valley',
          kind: 'text',
        },
      },
      {
        type: 'finish',
        finishReason: 'stop',
        usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
      },
    ];
  } else if (
    compareMessages(recentMessage, TEST_PROMPTS.CREATE_DOCUMENT_TEXT_CALL)
  ) {
    return [
      ...textToDeltas(`\n
# Silicon Valley: The Epicenter of Innovation

## Origins and Evolution

Silicon Valley, nestled in the southern part of the San Francisco Bay Area, emerged as a global technology hub in the late 20th century. Its transformation began in the 1950s when Stanford University encouraged its graduates to start their own companies nearby, leading to the formation of pioneering semiconductor firms that gave the region its name.

## The Innovation Ecosystem

What makes Silicon Valley unique is its perfect storm of critical elements: prestigious universities like Stanford and Berkeley, abundant venture capital, a culture that celebrates risk-taking, and a dense network of talented individuals. This ecosystem has consistently nurtured groundbreaking technologies from personal computers to social media platforms to artificial intelligence.

## Challenges and Criticisms

Despite its remarkable success, Silicon Valley faces significant challenges including extreme income inequality, housing affordability crises, and questions about technology's impact on society. Critics argue the region has developed a monoculture that sometimes struggles with diversity and inclusion.

## Future Prospects

As we move forward, Silicon Valley continues to reinvent itself. While some predict its decline due to remote work trends and competition from other tech hubs, the region's adaptability and innovative spirit suggest it will remain influential in shaping our technological future for decades to come.
`),
      {
        type: 'finish',
        finishReason: 'stop',
        usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
      },
    ];
  } else if (
    compareMessages(recentMessage, TEST_PROMPTS.CREATE_DOCUMENT_TEXT_RESULT)
  ) {
    return [
      ...textToDeltas('A document was created and is now visible to the user.'),
      {
        type: 'finish',
        finishReason: 'stop',
        usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
      },
    ];
  } else if (compareMessages(recentMessage, TEST_PROMPTS.GET_WEATHER_CALL)) {
    return [
      {
        type: 'tool-call',
        toolCallId: 'call_456',
        toolName: 'getWeather',
        input: JSON.stringify({ latitude: 37.7749, longitude: -122.4194 }),
      },
      {
        type: 'finish',
        finishReason: 'stop',
        usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
      },
    ];
  } else if (compareMessages(recentMessage, TEST_PROMPTS.GET_WEATHER_RESULT)) {
    return [
      ...textToDeltas('The current temperature in San Francisco is 17°C.'),
      {
        type: 'finish',
        finishReason: 'stop',
        usage: { inputTokens: 3, outputTokens: 10, totalTokens: 13 },
      },
    ];
  }

  return [{ id: '6', type: 'text-delta', delta: 'Unknown test prompt!' }];
};



================================================
FILE: tests/routes/chat.test.ts
================================================
import { generateUUID } from '@/lib/utils';
import { expect, test } from '../fixtures';
import { TEST_PROMPTS } from '../prompts/routes';
import { getMessageByErrorCode } from '@/lib/errors';

const chatIdsCreatedByAda: Array<string> = [];

// Helper function to normalize stream data for comparison
function normalizeStreamData(lines: string[]): string[] {
  return lines.map((line) => {
    if (line.startsWith('data: ')) {
      try {
        const data = JSON.parse(line.slice(6)); // Remove 'data: ' prefix
        if (data.id) {
          // Replace dynamic id with a static one for comparison
          return `data: ${JSON.stringify({ ...data, id: 'STATIC_ID' })}`;
        }
        return line;
      } catch {
        return line; // Return as-is if it's not valid JSON
      }
    }
    return line;
  });
}

test.describe
  .serial('/api/chat', () => {
    test('Ada cannot invoke a chat generation with empty request body', async ({
      adaContext,
    }) => {
      const response = await adaContext.request.post('/api/chat', {
        data: JSON.stringify({}),
      });
      expect(response.status()).toBe(400);

      const { code, message } = await response.json();
      expect(code).toEqual('bad_request:api');
      expect(message).toEqual(getMessageByErrorCode('bad_request:api'));
    });

    test('Ada can invoke chat generation', async ({ adaContext }) => {
      const chatId = generateUUID();

      const response = await adaContext.request.post('/api/chat', {
        data: {
          id: chatId,
          message: TEST_PROMPTS.SKY.MESSAGE,
          selectedChatModel: 'chat-model',
          selectedVisibilityType: 'private',
        },
      });
      expect(response.status()).toBe(200);

      const text = await response.text();
      const lines = text.split('\n');

      const [_, ...rest] = lines;
      const actualNormalized = normalizeStreamData(rest.filter(Boolean));
      const expectedNormalized = normalizeStreamData(
        TEST_PROMPTS.SKY.OUTPUT_STREAM,
      );

      expect(actualNormalized).toEqual(expectedNormalized);

      chatIdsCreatedByAda.push(chatId);
    });

    test("Babbage cannot append message to Ada's chat", async ({
      babbageContext,
    }) => {
      const [chatId] = chatIdsCreatedByAda;

      const response = await babbageContext.request.post('/api/chat', {
        data: {
          id: chatId,
          message: TEST_PROMPTS.GRASS.MESSAGE,
          selectedChatModel: 'chat-model',
          selectedVisibilityType: 'private',
        },
      });
      expect(response.status()).toBe(403);

      const { code, message } = await response.json();
      expect(code).toEqual('forbidden:chat');
      expect(message).toEqual(getMessageByErrorCode('forbidden:chat'));
    });

    test("Babbage cannot delete Ada's chat", async ({ babbageContext }) => {
      const [chatId] = chatIdsCreatedByAda;

      const response = await babbageContext.request.delete(
        `/api/chat?id=${chatId}`,
      );
      expect(response.status()).toBe(403);

      const { code, message } = await response.json();
      expect(code).toEqual('forbidden:chat');
      expect(message).toEqual(getMessageByErrorCode('forbidden:chat'));
    });

    test('Ada can delete her own chat', async ({ adaContext }) => {
      const [chatId] = chatIdsCreatedByAda;

      const response = await adaContext.request.delete(
        `/api/chat?id=${chatId}`,
      );
      expect(response.status()).toBe(200);

      const deletedChat = await response.json();
      expect(deletedChat).toMatchObject({ id: chatId });
    });

    test('Ada cannot resume stream of chat that does not exist', async ({
      adaContext,
    }) => {
      const response = await adaContext.request.get(
        `/api/chat/${generateUUID()}/stream`,
      );
      expect(response.status()).toBe(404);
    });

    test('Ada can resume chat generation', async ({ adaContext }) => {
      const chatId = generateUUID();

      const firstRequest = adaContext.request.post('/api/chat', {
        data: {
          id: chatId,
          message: {
            id: generateUUID(),
            role: 'user',
            content: 'Help me write an essay about Silcon Valley',
            parts: [
              {
                type: 'text',
                text: 'Help me write an essay about Silicon Valley',
              },
            ],
            createdAt: new Date().toISOString(),
          },
          selectedChatModel: 'chat-model',
          selectedVisibilityType: 'private',
        },
      });

      await new Promise((resolve) => setTimeout(resolve, 1000));

      const secondRequest = adaContext.request.get(
        `/api/chat/${chatId}/stream`,
      );

      const [firstResponse, secondResponse] = await Promise.all([
        firstRequest,
        secondRequest,
      ]);

      const [firstStatusCode, secondStatusCode] = await Promise.all([
        firstResponse.status(),
        secondResponse.status(),
      ]);

      expect(firstStatusCode).toBe(200);
      expect(secondStatusCode).toBe(200);

      const [firstResponseBody, secondResponseBody] = await Promise.all([
        await firstResponse.body(),
        await secondResponse.body(),
      ]);

      expect(firstResponseBody.toString()).toEqual(
        secondResponseBody.toString(),
      );
    });

    test('Ada can resume chat generation that has ended during request', async ({
      adaContext,
    }) => {
      const chatId = generateUUID();

      const firstRequest = await adaContext.request.post('/api/chat', {
        data: {
          id: chatId,
          message: {
            id: generateUUID(),
            role: 'user',
            content: 'Help me write an essay about Silcon Valley',
            parts: [
              {
                type: 'text',
                text: 'Help me write an essay about Silicon Valley',
              },
            ],
            createdAt: new Date().toISOString(),
          },
          selectedChatModel: 'chat-model',
          selectedVisibilityType: 'private',
        },
      });

      const secondRequest = adaContext.request.get(
        `/api/chat/${chatId}/stream`,
      );

      const [firstResponse, secondResponse] = await Promise.all([
        firstRequest,
        secondRequest,
      ]);

      const [firstStatusCode, secondStatusCode] = await Promise.all([
        firstResponse.status(),
        secondResponse.status(),
      ]);

      expect(firstStatusCode).toBe(200);
      expect(secondStatusCode).toBe(200);

      const [, secondResponseContent] = await Promise.all([
        firstResponse.text(),
        secondResponse.text(),
      ]);

      expect(secondResponseContent).toContain('appendMessage');
    });

    test('Ada cannot resume chat generation that has ended', async ({
      adaContext,
    }) => {
      const chatId = generateUUID();

      const firstResponse = await adaContext.request.post('/api/chat', {
        data: {
          id: chatId,
          message: {
            id: generateUUID(),
            role: 'user',
            content: 'Help me write an essay about Silcon Valley',
            parts: [
              {
                type: 'text',
                text: 'Help me write an essay about Silicon Valley',
              },
            ],
            createdAt: new Date().toISOString(),
          },
          selectedChatModel: 'chat-model',
          selectedVisibilityType: 'private',
        },
      });

      const firstStatusCode = firstResponse.status();
      expect(firstStatusCode).toBe(200);

      await firstResponse.text();
      await new Promise((resolve) => setTimeout(resolve, 15 * 1000));
      await new Promise((resolve) => setTimeout(resolve, 15000));
      const secondResponse = await adaContext.request.get(
        `/api/chat/${chatId}/stream`,
      );

      const secondStatusCode = secondResponse.status();
      expect(secondStatusCode).toBe(200);

      const secondResponseContent = await secondResponse.text();
      expect(secondResponseContent).toEqual('');
    });

    test('Babbage cannot resume a private chat generation that belongs to Ada', async ({
      adaContext,
      babbageContext,
    }) => {
      const chatId = generateUUID();

      const firstRequest = adaContext.request.post('/api/chat', {
        data: {
          id: chatId,
          message: {
            id: generateUUID(),
            role: 'user',
            content: 'Help me write an essay about Silcon Valley',
            parts: [
              {
                type: 'text',
                text: 'Help me write an essay about Silicon Valley',
              },
            ],
            createdAt: new Date().toISOString(),
          },
          selectedChatModel: 'chat-model',
          selectedVisibilityType: 'private',
        },
      });

      await new Promise((resolve) => setTimeout(resolve, 1000));

      const secondRequest = babbageContext.request.get(
        `/api/chat/${chatId}/stream`,
      );

      const [firstResponse, secondResponse] = await Promise.all([
        firstRequest,
        secondRequest,
      ]);

      const [firstStatusCode, secondStatusCode] = await Promise.all([
        firstResponse.status(),
        secondResponse.status(),
      ]);

      expect(firstStatusCode).toBe(200);
      expect(secondStatusCode).toBe(403);
    });

    test('Babbage can resume a public chat generation that belongs to Ada', async ({
      adaContext,
      babbageContext,
    }) => {
      test.fixme();
      const chatId = generateUUID();

      const firstRequest = adaContext.request.post('/api/chat', {
        data: {
          id: chatId,
          message: {
            id: generateUUID(),
            role: 'user',
            content: 'Help me write an essay about Silicon Valley',
            parts: [
              {
                type: 'text',
                text: 'Help me write an essay about Silicon Valley',
              },
            ],
            createdAt: new Date().toISOString(),
          },
          selectedChatModel: 'chat-model',
          selectedVisibilityType: 'public',
        },
      });

      await new Promise((resolve) => setTimeout(resolve, 10 * 1000));

      const secondRequest = babbageContext.request.get(
        `/api/chat/${chatId}/stream`,
      );

      const [firstResponse, secondResponse] = await Promise.all([
        firstRequest,
        secondRequest,
      ]);

      const [firstStatusCode, secondStatusCode] = await Promise.all([
        firstResponse.status(),
        secondResponse.status(),
      ]);

      expect(firstStatusCode).toBe(200);
      expect(secondStatusCode).toBe(200);

      const [firstResponseContent, secondResponseContent] = await Promise.all([
        firstResponse.text(),
        secondResponse.text(),
      ]);

      expect(firstResponseContent).toEqual(secondResponseContent);
    });
  });



================================================
FILE: tests/routes/document.test.ts
================================================
import type { Document } from '@/lib/db/schema';
import { generateUUID } from '@/lib/utils';
import { expect, test } from '../fixtures';
import { getMessageByErrorCode } from '@/lib/errors';

const documentsCreatedByAda: Array<Document> = [];

test.describe
  .serial('/api/document', () => {
    test('Ada cannot retrieve a document without specifying an id', async ({
      adaContext,
    }) => {
      const response = await adaContext.request.get('/api/document');
      expect(response.status()).toBe(400);

      const { code, message } = await response.json();
      expect(code).toEqual('bad_request:api');
      expect(message).toEqual(getMessageByErrorCode(code));
    });

    test('Ada cannot retrieve a document that does not exist', async ({
      adaContext,
    }) => {
      const documentId = generateUUID();

      const response = await adaContext.request.get(
        `/api/document?id=${documentId}`,
      );
      expect(response.status()).toBe(404);

      const { code, message } = await response.json();
      expect(code).toEqual('not_found:document');
      expect(message).toEqual(getMessageByErrorCode(code));
    });

    test('Ada can create a document', async ({ adaContext }) => {
      const documentId = generateUUID();

      const draftDocument = {
        title: "Ada's Document",
        kind: 'text',
        content: 'Created by Ada',
      };

      const response = await adaContext.request.post(
        `/api/document?id=${documentId}`,
        {
          data: draftDocument,
        },
      );
      expect(response.status()).toBe(200);

      const [createdDocument] = await response.json();
      expect(createdDocument).toMatchObject(draftDocument);

      documentsCreatedByAda.push(createdDocument);
    });

    test('Ada can retrieve a created document', async ({ adaContext }) => {
      const [document] = documentsCreatedByAda;

      const response = await adaContext.request.get(
        `/api/document?id=${document.id}`,
      );
      expect(response.status()).toBe(200);

      const retrievedDocuments = await response.json();
      expect(retrievedDocuments).toHaveLength(1);

      const [retrievedDocument] = retrievedDocuments;
      expect(retrievedDocument).toMatchObject(document);
    });

    test('Ada can save a new version of the document', async ({
      adaContext,
    }) => {
      const [firstDocument] = documentsCreatedByAda;

      const draftDocument = {
        title: "Ada's Document",
        kind: 'text',
        content: 'Updated by Ada',
      };

      const response = await adaContext.request.post(
        `/api/document?id=${firstDocument.id}`,
        {
          data: draftDocument,
        },
      );
      expect(response.status()).toBe(200);

      const [createdDocument] = await response.json();
      expect(createdDocument).toMatchObject(draftDocument);

      documentsCreatedByAda.push(createdDocument);
    });

    test('Ada can retrieve all versions of her documents', async ({
      adaContext,
    }) => {
      const [firstDocument, secondDocument] = documentsCreatedByAda;

      const response = await adaContext.request.get(
        `/api/document?id=${firstDocument.id}`,
      );
      expect(response.status()).toBe(200);

      const retrievedDocuments = await response.json();
      expect(retrievedDocuments).toHaveLength(2);

      const [firstRetrievedDocument, secondRetrievedDocument] =
        retrievedDocuments;
      expect(firstRetrievedDocument).toMatchObject(firstDocument);
      expect(secondRetrievedDocument).toMatchObject(secondDocument);
    });

    test('Ada cannot delete a document without specifying an id', async ({
      adaContext,
    }) => {
      const response = await adaContext.request.delete(`/api/document`);
      expect(response.status()).toBe(400);

      const { code, message } = await response.json();
      expect(code).toEqual('bad_request:api');
      expect(message).toEqual(getMessageByErrorCode(code));
    });

    test('Ada cannot delete a document without specifying a timestamp', async ({
      adaContext,
    }) => {
      const [firstDocument] = documentsCreatedByAda;

      const response = await adaContext.request.delete(
        `/api/document?id=${firstDocument.id}`,
      );
      expect(response.status()).toBe(400);

      const { code, message } = await response.json();
      expect(code).toEqual('bad_request:api');
      expect(message).toEqual(getMessageByErrorCode(code));
    });

    test('Ada can delete a document by specifying id and timestamp', async ({
      adaContext,
    }) => {
      const [firstDocument, secondDocument] = documentsCreatedByAda;

      const response = await adaContext.request.delete(
        `/api/document?id=${firstDocument.id}&timestamp=${firstDocument.createdAt}`,
      );
      expect(response.status()).toBe(200);

      const deletedDocuments = await response.json();
      expect(deletedDocuments).toHaveLength(1);

      const [deletedDocument] = deletedDocuments;
      expect(deletedDocument).toMatchObject(secondDocument);
    });

    test('Ada can retrieve documents without deleted versions', async ({
      adaContext,
    }) => {
      const [firstDocument] = documentsCreatedByAda;

      const response = await adaContext.request.get(
        `/api/document?id=${firstDocument.id}`,
      );
      expect(response.status()).toBe(200);

      const retrievedDocuments = await response.json();
      expect(retrievedDocuments).toHaveLength(1);

      const [firstRetrievedDocument] = retrievedDocuments;
      expect(firstRetrievedDocument).toMatchObject(firstDocument);
    });

    test("Babbage cannot update Ada's document", async ({ babbageContext }) => {
      const [firstDocument] = documentsCreatedByAda;

      const draftDocument = {
        title: "Babbage's Document",
        kind: 'text',
        content: 'Created by Babbage',
      };

      const response = await babbageContext.request.post(
        `/api/document?id=${firstDocument.id}`,
        {
          data: draftDocument,
        },
      );
      expect(response.status()).toBe(403);

      const { code, message } = await response.json();
      expect(code).toEqual('forbidden:document');
      expect(message).toEqual(getMessageByErrorCode(code));
    });

    test("Ada's documents did not get updated", async ({ adaContext }) => {
      const [firstDocument] = documentsCreatedByAda;

      const response = await adaContext.request.get(
        `/api/document?id=${firstDocument.id}`,
      );
      expect(response.status()).toBe(200);

      const documentsRetrieved = await response.json();
      expect(documentsRetrieved).toHaveLength(1);
    });
  });



================================================
FILE: .github/workflows/lint.yml
================================================
name: Lint
on:
  push:

jobs:
  build:
    runs-on: ubuntu-22.04
    strategy:
      matrix:
        node-version: [20]
    steps:
      - uses: actions/checkout@v4
      - name: Install pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9.12.3
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: "pnpm"
      - name: Install dependencies
        run: pnpm install
      - name: Run lint
        run: pnpm lint
1


================================================
FILE: .github/workflows/playwright.yml
================================================
name: Playwright Tests
on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    timeout-minutes: 30
    runs-on: ubuntu-latest
    env:
      AUTH_SECRET: ${{ secrets.AUTH_SECRET }}
      POSTGRES_URL: ${{ secrets.POSTGRES_URL }}
      BLOB_READ_WRITE_TOKEN: ${{ secrets.BLOB_READ_WRITE_TOKEN }}
      REDIS_URL: ${{ secrets.REDIS_URL }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - uses: actions/setup-node@v4
        with:
          node-version: lts/*

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: latest
          run_install: false

      - name: Get pnpm store directory
        id: pnpm-cache
        shell: bash
        run: |
          echo "STORE_PATH=$(pnpm store path)" >> $GITHUB_OUTPUT

      - uses: actions/cache@v3
        with:
          path: ${{ steps.pnpm-cache.outputs.STORE_PATH }}
          key: ${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}
          restore-keys: |
            ${{ runner.os }}-pnpm-store-

      - uses: actions/setup-node@v4
        with:
          node-version: lts/*
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Cache Playwright browsers
        uses: actions/cache@v3
        id: playwright-cache
        with:
          path: ~/.cache/ms-playwright
          key: ${{ runner.os }}-playwright-${{ hashFiles('**/pnpm-lock.yaml') }}

      - name: Install Playwright Browsers
        if: steps.playwright-cache.outputs.cache-hit != 'true'
        run: pnpm exec playwright install --with-deps chromium

      - name: Run Playwright tests
        run: pnpm test

      - uses: actions/upload-artifact@v4
        if: always() && !cancelled()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7