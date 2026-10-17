<script setup>
const props = defineProps({
    modelValue: {
        type: String,
        required: true,
    },
    disabled: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(['update:modelValue']);

const updateValue = (event) => {
    emit('update:modelValue', event.target.value);
};
</script>

<template>
    <div>
        <label class="label" for="canal">URL o handle del canal</label>
        <input 
            type="text" 
            id="canal" 
            class="input" 
            placeholder="Ej: @midudev, https://www.youtube.com/@midudev o midudev"
            :value="modelValue"
            @input="updateValue"
            :disabled="disabled"
            required
        />
        <p class="mt-2" style="font-size: 0.75rem; color: #64748b;">
            Ejemplos: @midudev, https://www.youtube.com/@midudev/videos, midudev
        </p>
    </div>
</template>

<style scoped>
/* Estilos especificos del componente */
</style>
