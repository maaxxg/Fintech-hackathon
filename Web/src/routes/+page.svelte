<script lang="ts">
	import { user, authLoading } from '$lib/stores/authStore';
	import { loadClients } from '$lib/stores/clientStore';
	import { goto } from '$app/navigation';
	import ClientList from '$lib/components/ClientList.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import DashboardStats from '$lib/components/DashboardStats.svelte';

	$effect(() => {
		if (!$authLoading && !$user) goto('/login');
	});

	$effect(() => {
		if ($user) loadClients($user.uid);
	});
</script>

<svelte:head>
	<title>Dashboard — HPB</title>
	<meta name="description" content="Bank manager client dashboard" />
</svelte:head>

{#if $authLoading}
	<div class="flex h-screen items-center justify-center">
		<div
			class="h-6 w-6 animate-spin rounded-none border-[3px] border-red-100 border-t-red-600"
		></div>
	</div>
{:else if $user}
	<div
		class="mx-auto flex h-[calc(100vh-64px)] max-w-7xl gap-6 p-6 max-md:h-auto max-md:flex-col-reverse"
		id="dashboard"
	>
		<main class="flex min-w-0 flex-1 flex-col">
			<DashboardStats />
			<ClientList />
		</main>
		<Sidebar />
	</div>
{/if}
