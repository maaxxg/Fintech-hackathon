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
		const clientId = $page.params.id as string;
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
	<div class="flex flex-col justify-center items-center h-[60vh] text-blue-500">
		<div
			class="w-6 h-6 border-[3px] border-blue-100 border-t-blue-600 rounded-none animate-spin mb-4"
		></div>
		<p class="text-[10px] uppercase tracking-widest font-bold">Loading Data...</p>
	</div>
{:else if client}
	<div class="max-w-4xl mx-auto px-6 py-8" id="client-detail">
		<!-- Header -->
		<div class="mb-6 border-b border-blue-200 pb-6">
			<a
				href="/"
				class="inline-flex items-center text-blue-600 text-[10px] uppercase tracking-widest font-bold mb-4 hover:text-blue-800 transition-colors"
			>
				&lt; Back to Dashboard
			</a>
			<div class="flex justify-between items-start">
				<div>
					<h1 class="text-3xl font-extrabold text-blue-950 uppercase tracking-widest m-0 mb-1">
						{client.name}
					</h1>
					<p class="text-[10px] text-blue-500 font-bold tracking-widest uppercase">ID: {client.id.substring(0,8)}</p>
				</div>
				<span class="bg-blue-50 text-blue-700 px-3 py-1 rounded-none text-[10px] font-bold uppercase tracking-widest border border-blue-200">
					{client.accountType}
				</span>
			</div>
		</div>

		<!-- Client Info -->
		<div
			class="bg-white border border-blue-100 rounded-none p-5 mb-6 shadow-none"
		>
			<h2 class="text-[11px] font-bold text-blue-950 uppercase tracking-widest border-b border-blue-100 pb-2 mb-4">
				Entity File
			</h2>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
				<div>
					<span class="text-[10px] font-bold text-blue-500 uppercase tracking-widest block mb-1">Email</span>
					<span class="text-blue-950 text-sm font-semibold">{client.email}</span>
				</div>
				<div>
					<span class="text-[10px] font-bold text-blue-500 uppercase tracking-widest block mb-1">Phone</span>
					<span class="text-blue-950 text-sm font-semibold">{client.phone}</span>
				</div>
				<div>
					<span class="text-[10px] font-bold text-blue-500 uppercase tracking-widest block mb-1">Account</span>
					<span class="text-blue-950 text-sm font-semibold">{client.accountType}</span>
				</div>
				<div>
					<span class="text-[10px] font-bold text-blue-500 uppercase tracking-widest block mb-1">Joined</span>
					<span class="text-blue-950 text-sm font-semibold">{client.joinDate}</span>
				</div>
			</div>
		</div>

		<!-- Score Cards Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
			<!-- Risk Score -->
			<div
				class="bg-white border border-blue-100 rounded-none p-5 shadow-none"
			>
				<div class="flex justify-between items-center mb-3 border-b border-blue-100 pb-2">
					<h2 class="text-[11px] font-bold text-blue-950 uppercase tracking-widest m-0">Risk Profile</h2>
					<ScoreBadge label="" score={client.riskScore} type="risk" />
				</div>
				<p class="text-xs text-blue-900/80 leading-relaxed font-bold uppercase tracking-wide">
					{client.riskExplanation}
				</p>
			</div>

			<!-- Value Score -->
			<div
				class="bg-white border border-blue-100 rounded-none p-5 shadow-none"
			>
				<div class="flex justify-between items-center mb-3 border-b border-blue-100 pb-2">
					<h2 class="text-[11px] font-bold text-blue-950 uppercase tracking-widest m-0">Value Assessment</h2>
					<ScoreBadge label="" score={client.valueScore} type="value" />
				</div>
				<p class="text-xs text-blue-900/80 leading-relaxed font-bold uppercase tracking-wide">
					{client.valueExplanation}
				</p>
			</div>
		</div>

		<!-- Retention Methods -->
		<section id="retention-methods" class="mt-8">
			<h2 class="text-[11px] font-bold text-blue-950 uppercase tracking-widest mb-4 border-b border-blue-200 pb-2">
				Required Actions
			</h2>
			
			<div class="space-y-4">
				{#each retentionMethods as method}
					<RetentionCard {method} />
				{/each}
			</div>
		</section>
	</div>
{:else}
	<div class="flex flex-col items-center justify-center py-24 text-center">
		<h2 class="text-lg font-bold text-blue-950 uppercase tracking-widest mb-2">Record Not Found</h2>
		<p class="text-xs text-blue-500 uppercase tracking-widest mb-6">Database query returned null.</p>
		<a href="/" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-[10px] font-bold uppercase tracking-widest rounded-none transition-colors">
			Return Home
		</a>
	</div>
{/if}
