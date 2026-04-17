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

	let additionalDetails = $derived(
		client
			? Object.entries(client).filter(
					([key, val]) =>
						![
							'id',
							'managerId',
							'name',
							'riskScore',
							'riskExplanation',
							'valueScore',
							'valueExplanation',
							'email',
							'phone',
							'accountType',
							'joinDate',
							'split',
							'IDENTIFIKATOR_KLIJENTA'
						].includes(key) &&
						val !== null &&
						val !== ''
				)
			: []
	);

	function fixCroatianLetters(text: any): string {
		if (typeof text !== 'string') return String(text);
		return text
			.replace(/È/g, 'Č')
			.replace(/è/g, 'č')
			.replace(/Æ/g, 'Ć')
			.replace(/æ/g, 'ć')
			.replace(/Ð/g, 'Đ')
			.replace(/ð/g, 'đ')
			// Fix hardcoded key names using unicode escapes for Ž and ž (\u017D and \u017E)
			.replace(/ZUPANIJA/g, '\u017DupaniJA')
			.replace(/Zupanija/g, '\u017Dupanija')
			.replace(/zupanija/g, '\u017Eupanija')
			.replace(/POSTANSKI/g, 'PO\u0160TANSKI')
			.replace(/Postanski/g, 'Po\u0161tanski')
			.replace(/DRZAVA/g, 'DR\u017DAVA')
			.replace(/Drzava/g, 'Dr\u017Eava')
			.replace(/STATISTICKA/g, 'STATISTI\u010CKA')
			.replace(/POCETKA/g, 'PO\u010CETKA')
			.replace(/STRUCNA/g, 'STRU\u010CNA')
			.replace(/VLASNISTVA/g, 'VLASNI\u0160TVA')
			.replace(/KUCANSTVA/g, 'KU\u0106ANSTVA')
			.replace(/UZDRZAVANIH/g, 'UZDR\u017DAVANIH')
			.replace(/BRACNI/g, 'BRA\u010CNI')
			.replace(/MREZA/g, 'MRE\u017DA')
			.replace(/TRZISTE/g, 'TR\u017DI\u0160TE')
			// Handle mojibake/hex artifacts for Ž/ž/Š/š
			.replace(/\u008E/g, '\u017D')
			.replace(/\u009E/g, '\u017E')
			.replace(/\u008A/g, 'Š')
			.replace(/\u009A/g, 'š')
			.replace(/\u00C5\u00BD/g, '\u017D')
			.replace(/\u00C5\u00be/g, '\u017E')
			// Final normalization pass
			.replace(/Ž/g, '\u017D')
			.replace(/ž/g, '\u017E');
	}

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
	<title>{client ? client.name : 'Client Detail'} — HPB</title>
	<meta name="description" content="Client details and retention methods" />
</svelte:head>

{#if loading}
	<div class="flex h-[60vh] flex-col items-center justify-center text-red-500">
		<div
			class="mb-4 h-6 w-6 animate-spin rounded-none border-[3px] border-red-100 border-t-red-600"
		></div>
		<p class="text-[11px] font-bold tracking-widest uppercase">Loading Data...</p>
	</div>
{:else if client}
	<div class="mx-auto max-w-4xl px-6 py-8" id="client-detail">
		<!-- Header -->
		<div class="mb-6 border-b border-red-200 pb-6">

			<div class="flex items-start justify-between">
				<div>
					<h1 class="m-0 mb-1 text-4xl font-extrabold tracking-widest text-red-950 uppercase">
						{client.name}
					</h1>
					<p class="text-[11px] font-bold tracking-widest text-red-500 uppercase">
						ID: {client.id.substring(0, 8)}
					</p>
				</div>
				<span
					class="rounded-none border border-red-200 bg-red-50 px-3 py-1 text-[11px] font-bold tracking-widest text-red-700 uppercase"
				>
					{client.accountType}
				</span>
			</div>
		</div>

		<!-- Strategic Overview (Scores & Actions) -->
		<div class="mb-8 grid grid-cols-1 gap-6 lg:grid-cols-12">
			<!-- Scores Side -->
			<div class="flex flex-col gap-6 lg:col-span-5">
				<!-- Risk Score -->
				<div class="rounded-none border border-red-100 bg-white p-5 shadow-none">
					<div class="mb-1 flex items-center justify-between">
						<h2 class="m-0 text-xs font-bold tracking-widest text-red-950 uppercase">
							Risk Profile
						</h2>
						<ScoreBadge label="" score={client.riskScore} />
					</div>
					<div class="mt-2 mb-3 h-1.5 w-full rounded-none bg-red-50">
						<div
							class="h-full rounded-none bg-red-600 transition-all duration-500"
							style="width: {client.riskScore}%"
						></div>
					</div>
					<p class="text-sm leading-relaxed font-bold tracking-wide text-red-900/80 uppercase">
						{client.riskExplanation}
					</p>
				</div>

				<!-- Value Score -->
				<div class="rounded-none border border-red-100 bg-white p-5 shadow-none">
					<div class="mb-1 flex items-center justify-between">
						<h2 class="m-0 text-xs font-bold tracking-widest text-red-950 uppercase">
							Value Assessment
						</h2>
						<ScoreBadge label="" score={client.valueScore} />
					</div>
					<div class="mt-2 mb-3 h-1.5 w-full rounded-none bg-red-50">
						<div
							class="h-full rounded-none bg-red-600 transition-all duration-500"
							style="width: {client.valueScore}%"
						></div>
					</div>
					<p class="text-sm leading-relaxed font-bold tracking-wide text-red-900/80 uppercase">
						{client.valueExplanation}
					</p>
				</div>
			</div>

			<!-- Retention Methods / Required Actions Side -->
			<div
				class="flex flex-col rounded-none border border-rose-200 bg-rose-50/30 p-5 lg:col-span-7"
			>
				<h2
					class="mb-4 flex items-center gap-2 border-b border-rose-200 pb-2 text-sm font-extrabold tracking-widest text-rose-950 uppercase"
				>
					<svg class="h-5 w-5 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"
						><path
							stroke-linecap="square"
							stroke-linejoin="miter"
							stroke-width="2"
							d="M13 10V3L4 14h7v7l9-11h-7z"
						></path></svg
					>
					Required Actions
				</h2>
				<div class="space-y-4">
					{#each retentionMethods as method}
						<RetentionCard {method} />
					{:else}
						<div
							class="flex items-center justify-center py-6 text-[10px] font-bold tracking-widest uppercase text-rose-400"
						>
							No current required actions.
						</div>
					{/each}
				</div>
			</div>
		</div>

		<!-- Client Info -->
		<div class="mb-6 rounded-none border border-red-100 bg-white p-5 shadow-none">
			<h2
				class="mb-4 border-b border-red-100 pb-2 text-xs font-bold tracking-widest text-red-950 uppercase"
			>
				Entity File
			</h2>
			<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
				<div class="min-w-0">
					<span class="mb-1 block text-[11px] font-bold tracking-widest text-red-500 uppercase"
						>Email</span
					>
					<span class="block text-base font-semibold break-words text-red-950 font-sans" title={client.email}
						>{client.email}</span
					>
				</div>
				<div class="min-w-0">
					<span class="mb-1 block text-[11px] font-bold tracking-widest text-red-500 uppercase"
						>Phone</span
					>
					<span class="block text-base font-semibold break-words text-red-950 font-sans">{client.phone}</span
					>
				</div>
				<div>
					<span class="mb-1 block text-[11px] font-bold tracking-widest text-red-500 uppercase"
						>Account</span
					>
					<span class="text-base font-semibold break-words text-red-950 font-sans">{client.accountType}</span
					>
				</div>
				<div>
					<span class="mb-1 block text-[11px] font-bold tracking-widest text-red-500 uppercase"
						>Joined</span
					>
					<span class="text-base font-semibold break-words text-red-950 font-sans">{client.joinDate}</span>
				</div>
			</div>
		</div>

		<!-- Additional Client Info -->
		{#if additionalDetails.length > 0}
			<div class="mb-8 rounded-none border border-red-100 bg-white p-5 shadow-none">
				<h2
					class="mb-4 border-b border-red-100 pb-2 text-xs font-bold tracking-widest text-red-950 uppercase"
				>
					Extended Profile
				</h2>
				<div class="grid grid-cols-1 gap-6 gap-y-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
					{#each additionalDetails as [key, value]}
						<div class="min-w-0">
							<span
								class="mb-1 block text-[11px] font-bold tracking-widest break-words text-red-500 uppercase"
								style="font-family: system-ui, -apple-system, sans-serif;"
								title={fixCroatianLetters(key.replace(/_/g, ' '))}
							>
								{fixCroatianLetters(key.replace(/_/g, ' '))}
							</span>
							<span
								class="block text-sm font-semibold break-words text-red-950 font-sans"
								style="font-family: system-ui, -apple-system, sans-serif;"
								title={fixCroatianLetters(value)}>{fixCroatianLetters(value)}</span
							>
						</div>
					{/each}
				</div>
			</div>
		{/if}
	</div>
{:else}
	<div class="flex flex-col items-center justify-center py-24 text-center">
		<h2 class="mb-2 text-xl font-bold tracking-widest text-red-950 uppercase">Record Not Found</h2>
		<p class="mb-6 text-sm tracking-widest text-red-500 uppercase">
			Database query returned null.
		</p>
		<a
			href="/"
			class="rounded-none bg-red-600 px-5 py-2.5 text-[11px] font-bold tracking-widest text-white uppercase transition-colors hover:bg-red-700"
		>
			Return Home
		</a>
	</div>
{/if}
