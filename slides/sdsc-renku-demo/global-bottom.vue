<!--
  SDSC Slides — persistent footer for Slidev.

  Copy this file to a Slidev project root (alongside slides.md). Slidev renders
  `global-bottom.vue` on top of every slide, so this draws the SDSC footer on
  content slides — the SDSC logo (left), the deck/event name (centred), and the
  page number "n / total" (right) — and hides itself on the cover, section,
  quote, and closing layouts (which are full-bleed brand slides). The logo
  swaps colour -> white in dark mode via the .sdsc-logo-* rules in style.css.

  The centred event name comes from a `footer:` field in the deck headmatter
  (the first slide's frontmatter); leave it unset to show nothing there.

  Requires the logos in `public/`: SDSC_Logo_RGB.png and SDSC_Logo_White.png.
  The footer styling lives in the generated style.css (.sdsc-footer).
-->
<template>
  <footer v-if="!hide" class="sdsc-footer">
    <span class="sdsc-footer-brand">
      <img class="sdsc-logo-light" src="./public/SDSC_Logo_RGB.png" alt="Swiss Data Science Center" />
      <img class="sdsc-logo-dark" src="./public/SDSC_Logo_White.png" alt="Swiss Data Science Center" />
    </span>
    <span v-if="event" class="sdsc-footer-event">{{ event }}</span>
    <span class="sdsc-footer-page">{{ pageLabel }}</span>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useNav } from '@slidev/client'

// Layouts that are full-bleed brand slides — no footer on these.
const HIDE_ON = ['cover', 'intro', 'section', 'quote', 'end']

// global-bottom.vue is rendered ONCE, outside the per-slide component tree, so
// it reads the deck's navigation state (the displayed slide) via useNav() —
// correct when presenting and in the SPA. Note: the all-in-one print export
// (`slidev export`) shares one nav state across pages; export with
// `slidev export --per-slide` for a correct per-slide footer in PDFs.
const { currentPage, total, slides, currentSlideRoute } = useNav()

const layout = computed(
  () => (currentSlideRoute.value?.meta?.slide?.frontmatter?.layout as string) || 'default',
)
const hide = computed(() => HIDE_ON.includes(layout.value))

// Deck-wide event name: read the `footer:` field from the first slide's
// headmatter so it shows on every slide without repeating it.
const event = computed(
  () => (slides.value?.[0]?.meta?.slide?.frontmatter?.footer as string) || '',
)
const pageLabel = computed(() => `${currentPage.value} / ${total.value}`)
</script>
