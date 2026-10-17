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
    <div class="flex" v-if="hasResults">
        <button 
            class="btn btn-success" 
            @click="emit('exportUnico')"
            :disabled="!hasResults"
        >
            Descargar .txt único
        </button>
        
        <button 
            v-if="showDivided()" 
            class="btn btn-secondary" 
            @click="emit('exportDividido')"
            :disabled="!hasResults"
        >
            Descargar .txt divididos
        </button>
    </div>
</template>
