# Design

Owner: Designer. Design decisions for the visual layer (`main/static/main/css/main.css`, static images, template class names). Source of truth is Figma through the connected connector when it is available; otherwise decisions are written here.

Accessibility requirements from `CLAUDE.md`: text contrast at least 4.5:1, visible focus states, `alt` text on every meaningful image, no information carried by colour alone.

## Source

No Figma file was provided and no Figma link is in the repository, so these decisions were made by the Designer from the accessibility requirements. If a Figma file appears, this document is updated to match it.

## Colours

Defined as CSS custom properties in `main.css`. Contrast is calculated with the WCAG 2.x formula.

| Token | Value | Use | Contrast |
| --- | --- | --- | --- |
| `--color-bg` | `#f4f6fa` | page background | text on it 14.7:1 |
| `--color-surface` | `#ffffff` | content card | text on it 15.9:1 |
| `--color-text` | `#1a2233` | body text | see above |
| `--color-muted` | `#4a5568` | secondary text | 7.53:1 on surface |
| `--color-border` | `#cbd5e1` | card and nav borders | decorative only |
| `--color-primary` | `#1d4ed8` | links, focus ring on light | 6.7:1 on surface |
| `--color-primary-hover` | `#1e3a8a` | link hover | 10.36:1 on surface |
| `--color-header` | `#1e293b` | header background | white text 14.63:1 |
| `--color-focus-on-dark` | `#fbbf24` | focus ring in header | 8.76:1 on header |

The old pink background (`deeppink`) is removed.

## Typography

System font stack: `system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`. No web fonts, so nothing is downloaded.

| Element | Size |
| --- | --- |
| body | 1rem (16px), line height 1.6 |
| h1 | 2rem (1.625rem on small screens) |
| h2 | 1.5rem |
| h3 | 1.25rem |
| h4 | 1.125rem |
| site title | 1.25rem, bold |

## Spacing

Scale in pixels: 4, 8, 16, 24, 32 (`--space-1` to `--space-5`). Border radius 8px. Content width is limited to 720px.

## Components

- **Header** (`.site-header`, `.site-title`): dark bar with the project name.
- **Content card** (`.content`): white surface with a border, centred, holds the page.
- **Navigation** (`.nav`): horizontal list of links that wraps; a border separates it from the page body.
- **Links**: always underlined, so links are not told apart by colour alone. Hover darkens the colour.
- **Focus**: links show a 3px outline with a 2px offset on `:focus-visible`; the header uses the yellow ring.

## Breakpoints

One breakpoint: `max-width: 640px`. The card goes full width without side borders or radius, and the h1 gets smaller. The layout template has a viewport meta tag for this.

## Images

No images are used. The previous sidebar photo was removed (see `docs/ASSETS.md`). Any future meaningful image needs descriptive `alt` text.
