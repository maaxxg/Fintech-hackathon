<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { user, authLoading } from '$lib/stores/authStore';
	import { goto } from '$app/navigation';
	import { getClient } from '$lib/firebase/firestore';
	import { getRetentionMethods } from '$lib/api/retention';
	import ScoreBadge from '$lib/components/ScoreBadge.svelte';
	import RetentionCard from '$lib/components/RetentionCard.svelte';
	import type { Client, RetentionMethod } from '$lib/types';

	let client = $state<Client | null>(null);
	let retentionMethods = $state<RetentionMethod[]>([]);
	let loading = $state(true);

	$effect(() => {
		if (!$authLoading && !$user) goto('/login');
	});

	onMount(async () => {
		const clientId: string = $page.params.id;
		client = await getClient(clientId);
		retentionMethods = await getRetentionMethods(clientId);
		loading = false;
	});
</script>

<svelte:head>
	<title>{client ? client.name : 'Client Detail'} — ClientGuard</title>
	<meta name="description" content="Client details and retention methods" />
</svelte:head>

{#if loading}
	<div class="flex flex-col justify-center items-center h-[60vh] text-gray-400">
		<div
			class="w-9 h-9 border-3 border-gray-200 dark:border-gray-700 border-t-indigo-500 rounded-full animate-spin mb-4"
		></div>
		<p>Loading client details...</p>
	</div>
{:else if client}
	<div class="max-w-4xl mx-auto px-6 py-8" id="client-detail">
		<!-- Header -->
		<div class="mb-8">
			<a
				href="/"
				class="inline-block text-indigo-500 text-sm font-medium mb-3 hover:opacity-70 transition"
				>← Back to Dashboard</a
			>
			<h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100 m-0">{client.name}</h1>
			<span class="text-sm text-gray-400">{client.accountType} Account</span>
		</div>

		<!-- Client Info -->
		<div
			class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6 mb-5"
		>
			<h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
				Contact Information
			</h2>
			<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
				<div>
					<span class="text-gray-400 dark:text-gray-500 block mb-0.5">Email</span>
					<span class="text-gray-900 dark:text-gray-100">{client.email}</span>
				</div>
				<div>
					<span class="text-gray-400 dark:text-gray-500 block mb-0.5">Phone</span>
					<span class="text-gray-900 dark:text-gray-100">{client.phone}</span>
				</div>
				<div>
					<span class="text-gray-400 dark:text-gray-500 block mb-0.5">Account Type</span>
					<span class="text-gray-900 dark:text-gray-100">{client.accountType}</span>
				</div>
				<div>
					<span class="text-gray-400 dark:text-gray-500 block mb-0.5">Joined</span>
					<span class="text-gray-900 dark:text-gray-100">{client.joinDate}</span>
				</div>
			</div>
		</div>

		<!-- Score Cards Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-8">
			<!-- Risk Score -->
			<div
				class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6"
			>
				<div class="flex justify-between items-center mb-4">
					<h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 m-0">Risk Score</h2>
					<ScoreBadge label="Risk" score={client.riskScore} type="risk" />
				</div>
				<p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
					{client.riskExplanation}
				</p>
			</div>

			<!-- Value Score -->
			<div
				class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-6"
			>
				<div class="flex justify-between items-center mb-4">
					<h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100 m-0">Value Score</h2>
					<ScoreBadge label="Value" score={client.valueScore} type="value" />
				</div>
				<p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
					{client.valueExplanation}
				</p>
			</div>
		</div>

		<!-- Retention Methods -->
		<section id="retention-methods">
			<h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
				Suggested Retention Methods
			</h2>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				{#each retentionMethods as method}
					<RetentionCard {method} />
				{/each}
			</div>
		</section>
	</div>
{:else}
	<div class="text-center py-16 text-gray-400">
		<h2 class="text-xl mb-2">Client not found</h2>
		<a href="/" class="text-indigo-500 hover:underline">Return to dashboard</a>
	</div>
{/if}
