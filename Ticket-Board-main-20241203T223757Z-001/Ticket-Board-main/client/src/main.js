import App from './App.svelte';
import { navigate } from 'svelte-routing';

navigate('/loading');

const app = new App({
    target: document.body
});

export default app;