<!--
  SDSC Slides — persistent footer for Slidev.

  This project variant adds a same-height Renku logo next to the SDSC logo on
  content slides because the deck is about Renku-powered experimentation.
-->
<template>
  <footer v-if="!hide" class="sdsc-footer">
    <span class="sdsc-footer-brand">
      <span class="sdsc-footer-logo-lockup">
        <img class="sdsc-logo-light footer-logo" :src="'/SDSC_Logo_RGB.png'" alt="Swiss Data Science Center" />
        <img class="sdsc-logo-dark footer-logo" :src="'/SDSC_Logo_White.png'" alt="Swiss Data Science Center" />
        <img class="renku-footer-logo footer-logo" :src="'/renku-logo.svg'" alt="Renku" />
      </span>
    </span>
    <span v-if="event" class="sdsc-footer-event">{{ event }}</span>
    <span class="sdsc-footer-page">{{ pageLabel }}</span>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useNav } from '@slidev/client'

const HIDE_ON = ['cover', 'intro', 'section', 'quote', 'end']
const { currentPage, total, slides, currentSlideRoute } = useNav()

const layout = computed(
  () => (currentSlideRoute.value?.meta?.slide?.frontmatter?.layout as string) || 'default',
)
const hide = computed(() => HIDE_ON.includes(layout.value))
const event = computed(
  () => (slides.value?.[0]?.meta?.slide?.frontmatter?.footer as string) || '',
)
const pageLabel = computed(() => `${currentPage.value} / ${total.value}`)
</script>
