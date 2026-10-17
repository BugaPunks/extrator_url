<script setup>
import { ref } from 'vue';
import InputChannel from '../Components/InputChannel.vue';
import ResultsArea from '../Components/ResultsArea.vue';
import ExportButtons from '../Components/ExportButtons.vue';
import LoadingSpinner from '../Components/LoadingSpinner.vue';

const canal = ref('');
const incluirTitulos = ref(false);
const maxUrlsPorArchivo = ref(0);
const loading = ref(false);
const results = ref([]);
const error = ref(null);
const successMessage = ref(null);

// Obtener CSRF token de la meta tag
const getCsrfToken = () => {
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    return metaTag ? metaTag.getAttribute('content') : '';
};

const extraerUrls = async () => {
    error.value = null;
    successMessage.value = null;
    loading.value = true;
    results.value = [];

    try {
        const response = await fetch('/extraer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                canal: canal.value,
                incluir_titulos: incluirTitulos.value,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            error.value = data.error || 'Error al extraer URLs';
            results.value = [];
        } else {
            if (data.error) {
                error.value = data.error;
                results.value = [];
            } else {
                results.value = data.results || [];
                successMessage.value = data.success_message || 'Extracción completada';
            }
        }
    } catch (err) {
        error.value = 'Error de red: ' + err.message;
        results.value = [];
    } finally {
        loading.value = false;
    }
};

const exportar = async (dividido = false) => {
    if (!results.value || results.value.length === 0) {
        error.value = 'No hay URLs para exportar';
        return;
    }

    error.value = null;

    try {
        const response = await fetch('/exportar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                results: results.value,
                incluir_titulos: incluirTitulos.value,
                max_urls_por_archivo: maxUrlsPorArchivo.value,
                dividido: dividido,
            }),
        });

        if (!response.ok) {
            let mensaje = 'Error al exportar';
            try {
                const data = await response.json();
                mensaje = data.error || mensaje;
            } catch (e) {
                // respuesta sin JSON
            }
            error.value = mensaje;
            return;
        }

        const filename = getFilenameFromResponse(response);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    } catch (err) {
        error.value = 'Error de red: ' + err.message;
    }
};

const getFilenameFromResponse = (response) => {
    const disposition = response.headers.get('Content-Disposition') || '';
    const match = /filename\*?=(?:UTF-8'')?"?([^";]+)"?/i.exec(disposition);
    return match ? decodeURIComponent(match[1]) : 'urls_videos.txt';
};
</script>

<template>
    <div class="mx-auto max-w-6xl p-4 sm:p-8">
        <div class="mb-6 rounded-lg bg-white p-6 shadow-md">
            <h1 class="mb-4 text-3xl font-bold text-slate-900">Extractor de URLs de YouTube</h1>
            <p class="text-slate-600">Ingresa la URL o handle de un canal de YouTube para extraer todas las URLs de sus videos.</p>
        </div>

        <div class="mb-6 rounded-lg bg-white p-6 shadow-md">
            <form @submit.prevent="extraerUrls">
                <div class="flex flex-col gap-4">
                    <InputChannel v-model="canal" :disabled="loading" />
                    
                    <div class="flex items-center gap-2 text-sm text-slate-900">
                        <input type="checkbox" id="incluirTitulos" class="h-[18px] w-[18px] accent-blue-500" v-model="incluirTitulos" :disabled="loading" />
                        <label for="incluirTitulos" class="cursor-pointer">Incluir títulos de videos</label>
                    </div>

                    <div>
                        <label class="mb-2 block text-sm font-medium text-slate-900" for="maxUrls">Máx. URLs por archivo (0 = archivo único)</label>
                        <input 
                            type="number" 
                            id="maxUrls" 
                            class="w-full rounded-md border border-slate-200 bg-white px-3.5 py-2.5 text-sm text-slate-900 transition focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-500/20 disabled:cursor-not-allowed disabled:opacity-60" 
                            v-model.number="maxUrlsPorArchivo" 
                            min="0" 
                            :disabled="loading"
                        />
                    </div>

                    <button 
                        type="submit" 
                        class="inline-flex w-full items-center justify-center gap-2 rounded-md bg-blue-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-blue-600 disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto" 
                        :disabled="loading || !canal"
                    >
                        <span v-if="!loading">Extraer URLs</span>
                        <span v-else>Procesando...</span>
                    </button>
                </div>
            </form>
        </div>

        <div v-if="loading" class="mb-6 rounded-lg bg-white p-6 shadow-md">
            <div class="flex items-center gap-4">
                <LoadingSpinner />
                <p class="text-sm text-slate-900">
                    <span>Obteniendo lista de videos...</span>
                </p>
            </div>
        </div>

        <div v-if="error" class="mb-6 rounded-lg bg-white p-6 shadow-md">
            <p class="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-600">{{ error }}</p>
        </div>

        <div v-if="successMessage" class="mb-6 rounded-lg bg-white p-6 shadow-md">
            <p class="rounded-md border border-green-500/30 bg-green-500/10 p-3 text-sm text-green-600">{{ successMessage }}</p>
        </div>

        <div v-if="results && results.length > 0" class="mb-6 rounded-lg bg-white p-6 shadow-md">
            <ResultsArea :results="results" :incluir-titulos="incluirTitulos" />
            <div class="mt-4">
                <ExportButtons 
                    @export-unico="() => exportar(false)" 
                    @export-dividido="() => exportar(true)" 
                    :has-results="results.length > 0"
                    :max-urls="maxUrlsPorArchivo"
                />
            </div>
        </div>
    </div>
</template>
