<script setup>
const props = defineProps({
    results: {
        type: Array,
        required: true,
    },
    incluirTitulos: {
        type: Boolean,
        default: false,
    },
});

const formattedResults = () => {
    return props.results.map(([titulo, url]) => {
        return props.incluirTitulos ? `${titulo} - ${url}` : url;
    }).join('\n');
};
</script>

<template>
    <div>
        <label class="mb-2 block text-sm font-medium text-slate-900">Resultados ({{ results.length }} URLs)</label>
        <textarea
            class="min-h-[200px] w-full rounded-md border border-slate-200 bg-slate-100 p-3 text-sm text-slate-900 transition focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-500/20"
            readonly
            :value="formattedResults()"
        ></textarea>
    </div>
</template>
