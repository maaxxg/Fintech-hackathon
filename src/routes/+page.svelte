<script lang="ts">
	import { user, authLoading } from '$lib/stores/authStore';
	import { loadClients } from '$lib/stores/clientStore';
	import { goto } from '$app/navigation';
	import ClientList from '$lib/components/ClientList.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';

	$effect(() => {
		if (!$authLoading && !$user) goto('/login');
	});

	$effect(() => {
		if ($user) loadClients($user.uid);
	});
</script>

<svelte:head>
	<title>Dashboard — ClientGuard</title>
	<meta name="description" content="Bank manager client dashboard" />
</svelte:head>

{#if $authLoading}
	<div class="flex justify-center items-center h-screen">
		<div
			class="w-10 h-10 border-3 border-gray-200 dark:border-gray-700 border-t-indigo-500 rounded-full animate-spin"
		></div>
	</div>
{:else if $user}
	<div
		class="flex gap-6 p-6 h-[calc(100vh-64px)] max-w-7xl mx-auto max-md:flex-col-reverse max-md:h-auto"
		id="dashboard"
	>
		<main class="flex-1 flex flex-col min-w-0">
			<ClientList />
		</main>
		<Sidebar />
	</div>
{/if}
