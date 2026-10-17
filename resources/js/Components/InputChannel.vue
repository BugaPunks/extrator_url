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
        <label class="mb-2 block text-sm font-medium text-slate-900" for="canal">URL o handle del canal</label>
        <input
            type="text"
            id="canal"
            class="w-full rounded-md border border-slate-200 bg-white px-3.5 py-2.5 text-sm text-slate-900 transition focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-500/20 disabled:cursor-not-allowed disabled:opacity-60"
            placeholder="Ej: @tucanal, https://www.youtube.com/@tucanal o tucanal"
            :value="modelValue"
            @input="updateValue"
            :disabled="disabled"
            required
        />
        <p class="mt-2 text-xs text-slate-500">
            Ejemplos: @tucanal, https://www.youtube.com/@tucanal/videos, tucanal
        </p>
    </div>
</template>
