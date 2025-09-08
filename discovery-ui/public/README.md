# Public Assets Directory

This directory contains static assets served directly by Next.js.

## Directory Structure

- `fonts/` - Custom font files (.woff, .woff2, .ttf, .eot)
- `images/` - Static images, logos, graphics (.png, .jpg, .svg, .webp)
- `icons/` - Icon files and favicons

## Usage

### Fonts
```css
/* In your CSS files */
@font-face {
  font-family: 'YourFont';
  src: url('/fonts/your-font.woff2') format('woff2');
}
```

### Images
```tsx
// In React components
import Image from 'next/image'

<Image src="/images/logo.png" alt="Logo" width={100} height={100} />

// Or regular img tag
<img src="/images/logo.png" alt="Logo" />
```

### Icons
```tsx
<img src="/icons/favicon.ico" alt="Favicon" />
```

## Notes

- Files in this directory are served from the root path (`/`)
- No build step required - files are served as-is
- Optimize images for web (use WebP, compress, etc.)
- Font files should be properly licensed for web use
