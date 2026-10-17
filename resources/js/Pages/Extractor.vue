<script setup>
import { ref } from 'vue';
import { router, usePage } from '@inertiajs/vue3';
import InputChannel from '../Components/InputChannel.vue';
import ResultsArea from '../Components/ResultsArea.vue';
import ExportButtons from '../Components/ExportButtons.vue';
import LoadingSpinner from '../Components/LoadingSpinner.vue';

const page = usePage();

const canal = ref(page.props.canal || '');
const incluirTitulos = ref(page.props.incluir_titulos || false);
const maxUrlsPorArchivo = ref(page.props.max_urls_por_archivo || 0);
const loading = ref(false);
const results = ref(page.props.results || []);
const error = ref(page.props.error || null);
const successMessage = ref(page.props.success_message || null);

const extraerUrls = () => {
    error.value = null;
    successMessage.value = null;
    loading.value = true;
    results.value = [];

    router.post('/extraer', {
        canal: canal.value,
        incluir_titulos: incluirTitulos.value,
    }, {
        preserveScroll: true,
        onSuccess: (response) => {
            loading.value = false;
            if (response.props.error) {
                error.value = response.props.error;
            } else {
                results.value = response.props.results || [];
                if (response.props.success_message) {
                    successMessage.value = response.props.success_message;
                }
            }
        },
        onError: (errors) => {
            loading.value = false;
            error.value = errors.message || 'Error al extraer URLs';
        },
    });
};

const exportar = (dividido = false) => {
    if (!results.value || results.value.length === 0) {
        error.value = 'No hay URLs para exportar';
        return;
    }

    const formData = new FormData();
    formData.append('results', JSON.stringify(results.value));
    formData.append('incluir_titulos', incluirTitulos.value);
    formData.append('max_urls_por_archivo', maxUrlsPorArchivo.value);
    formData.append('dividido', dividido);

    window.location.href = '/exportar?' + new URLSearchParams({
        results: JSON.stringify(results.value),
        incluir_titulos: incluirTitulos.value,
        max_urls_por_archivo: maxUrlsPorArchivo.value,
        dividido: dividido,
    }).toString();
};
</script>

<template>
    <div class="container">
        <div class="card">
            <h1 class="h1">Extractor de URLs de YouTube</h1>
            <p>Ingresa la URL o handle de un canal de YouTube para extraer todas las URLs de sus videos.</p>
        </div>

        <div class="card">
            <form @submit.prevent="extraerUrls">
                <div class="flex-col">
                    <InputChannel v-model="canal" :disabled="loading" />
                    
                    <div class="checkbox-label">
                        <input type="checkbox" id="incluirTitulos" class="checkbox" v-model="incluirTitulos" :disabled="loading" />
                        <label for="incluirTitulos">Incluir títulos de videos</label>
                    </div>

                    <div>
                        <label class="label" for="maxUrls">Máx. URLs por archivo (0 = archivo único)</label>
                        <input 
                            type="number" 
                            id="maxUrls" 
                            class="input" 
                            v-model.number="maxUrlsPorArchivo" 
                            min="0" 
                            :disabled="loading"
                        />
                    </div>

                    <button 
                        type="submit" 
                        class="btn btn-primary" 
                        :disabled="loading || !canal"
                    >
                        <span v-if="!loading">Extraer URLs</span>
                        <span v-else>Procesando...</span>
                    </button>
                </div>
            </form>
        </div>

        <div v-if="loading" class="card">
            <LoadingSpinner />
            <p class="loading-message">
                <span>Obteniendo lista de videos...</span>
            </p>
        </div>

        <div v-if="error" class="card">
            <p class="error-message">{{ error }}</p>
        </div>

        <div v-if="successMessage" class="card">
            <p class="success-message">{{ successMessage }}</p>
        </div>

        <div v-if="results && results.length > 0" class="card">
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
