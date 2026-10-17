<script setup>
const props = defineProps({
    hasResults: {
        type: Boolean,
        default: false,
    },
    maxUrls: {
        type: Number,
        default: 0,
    },
});

const emit = defineEmits(['exportUnico', 'exportDividido']);

const showDivided = () => {
    return props.hasResults && props.maxUrls > 0;
};
</script>

<template>
    <div class="flex flex-col gap-4 sm:flex-row sm:flex-wrap sm:items-center" v-if="hasResults">
        <button
            class="inline-flex w-full items-center justify-center gap-2 rounded-md bg-green-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-green-600 disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
            @click="emit('exportUnico')"
            :disabled="!hasResults"
        >
            Descargar .txt único
        </button>

        <button
            v-if="showDivided()"
            class="inline-flex w-full items-center justify-center gap-2 rounded-md border border-slate-200 bg-slate-100 px-5 py-2.5 text-sm font-medium text-slate-900 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
            @click="emit('exportDividido')"
            :disabled="!hasResults"
        >
            Descargar .txt divididos
        </button>
    </div>
</template>
