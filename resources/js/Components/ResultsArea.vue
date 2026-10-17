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
        <label class="label">Resultados ({{ results.length }} URLs)</label>
        <textarea 
            class="textarea" 
            readonly 
            :value="formattedResults()"
        ></textarea>
    </div>
</template>

<style scoped>
/* Estilos especificos del componente */
</style>
