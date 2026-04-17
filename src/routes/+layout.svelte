<script lang="ts">
	import '../app.css';
	import Navbar from '$lib/components/Navbar.svelte';
	import { page } from '$app/stores';
	import { initAuth } from '$lib/stores/authStore';

	let { children } = $props();

	// Initialize Firebase Auth listener (client-side only)
	initAuth();

	// Don't show navbar on login page
	let isLoginPage = $derived($page.url.pathname === '/login');
</script>

<div class="min-h-screen bg-white text-blue-950 transition-colors">
	{#if isLoginPage}
		{@render children()}
	{:else}
		<Navbar />
		{@render children()}
	{/if}
</div>
