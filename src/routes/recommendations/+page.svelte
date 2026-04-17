<script lang="ts">
	import { clients } from '$lib/stores/clientStore';

	// Categories from unique_categories.txt
	interface Recommendation {
		id: number;
		field: string;
		score: number;
		spendVolume: string;
		// Which risk/value segments gravitate to this category
		riskAffinityMin: number;
		riskAffinityMax: number;
		valueAffinityMin: number;
		valueAffinityMax: number;
	}

	const categories = [
		'JAVNA UPRAVA I OBRANA',
		'DJELATNOSTI ZDRAVSTVENE ZAŠTITE I SOCIJALNE SKRBI',
		'DJELATNOSTI PRUŽANJA SMJEŠTAJA TE PRIPREME I USLUŽIVANJA HRANE',
		'INFORMACIJE I KOMUNIKACIJE',
		'OPSKRBA VODOM',
		'FINANCIJSKE DJELATNOSTI I DJELATNOSTI OSIGURANJA',
		'OPSKRBA ELEKTRIČNOM ENERGIJOM, PLINOM, PAROM I KLIMATIZACIJA',
		'PRERAĐIVAČKA INDUSTRIJA',
		'TRGOVINA NA VELIKO I NA MALO',
		'UMJETNOST, ZABAVA I REKREACIJA',
		'GRAĐEVINARSTVO',
		'POLJOPRIVREDA, ŠUMARSTVO I RIBARSTVO',
		'POSLOVANJE NEKRETNINAMA',
		'ADMINISTRATIVNE I POMOČNE USLUŽNE DJELATNOSTI',
		'STRUČNE, ZNANSTVENE I TEHNIČKE DJELATNOSTI',
		'OSTALE USLUŽNE DJELATNOSTI',
		'OBRAZOVANJE',
		'PRIJEVOZ I SKLADIŠTENJE',
		'PROIZVODNJA SVJEŽIH PECIVA I SLIČNIH PROIZVODA TE KOLAĆA',
		'Professional services and membership organizations',
		'Retail outlets',
		'Miscellaneous outlets',
		'Utilities',
		'Service providers',
		'Clothing outlets',
		'Repair services',
		'Transportation',
		'Amusement and entertainment',
		'Business services',
		'Contracted services',
		'Government services',
		'Agricultural services'
	];

	// Seed-based pseudo-random so values stay stable across renders
	function seededRandom(seed: number): number {
		const x = Math.sin(seed * 9301 + 49297) * 49297;
		return x - Math.floor(x);
	}

	const recommendations: Recommendation[] = categories.map((cat, i) => {
		const s1 = seededRandom(i + 1);
		const s2 = seededRandom(i + 100);
		const s3 = seededRandom(i + 200);
		const s4 = seededRandom(i + 300);

		const rMin = Math.floor(s1 * 60);
		const rMax = rMin + 20 + Math.floor(s2 * 30);
		const vMin = Math.floor(s3 * 60);
		const vMax = vMin + 20 + Math.floor(s4 * 30);

		const score = 30 + Math.floor(seededRandom(i + 500) * 70);
		const spendBase = 100 + Math.floor(seededRandom(i + 600) * 4000);
		const spendStr =
			spendBase >= 1000 ? `€${(spendBase / 1000).toFixed(1)}M/mo` : `€${spendBase}k/mo`;

		return {
			id: i + 1,
			field: cat,
			score,
			spendVolume: spendStr,
			riskAffinityMin: Math.min(rMin, 80),
			riskAffinityMax: Math.min(rMax, 100),
			valueAffinityMin: Math.min(vMin, 80),
			valueAffinityMax: Math.min(vMax, 100)
		};
	});

	// Filter state
	type FilterMode = 'all' | 'risk' | 'value';

	let activeFilters = $state<Set<FilterMode>>(new Set(['all']));
	let riskMin = $state(0);
	let riskMax = $state(100);
	let valueMin = $state(0);
	let valueMax = $state(100);

	function toggleFilter(mode: FilterMode) {
		if (mode === 'all') {
			// "View All" is exclusive — selecting it clears risk/value
			activeFilters = new Set(['all']);
			riskMin = 0;
			riskMax = 100;
			valueMin = 0;
			valueMax = 100;
		} else {
			// Remove 'all' if a specific filter is toggled
			const next = new Set(activeFilters);
			next.delete('all');
			if (next.has(mode)) {
				next.delete(mode);
			} else {
				next.add(mode);
			}
			// If nothing is left, revert to 'all'
			if (next.size === 0) {
				activeFilters = new Set(['all']);
			} else {
				activeFilters = next;
			}
		}
	}

	function isActive(mode: FilterMode): boolean {
		return activeFilters.has(mode);
	}

	// Determine which clients match the active risk/value ranges
	let matchingClientCount = $derived.by(() => {
		if (activeFilters.has('all')) return $clients.length;
		return $clients.filter((c) => {
			const riskOk = !activeFilters.has('risk') || (c.riskScore >= riskMin && c.riskScore <= riskMax);
			const valOk =
				!activeFilters.has('value') || (c.valueScore >= valueMin && c.valueScore <= valueMax);
			return riskOk && valOk;
		}).length;
	});

	// Assign letter rating based on score
	function getRating(score: number): 'A' | 'B' | 'C' | 'D' | 'E' {
		if (score >= 85) return 'A';
		if (score >= 70) return 'B';
		if (score >= 55) return 'C';
		if (score >= 40) return 'D';
		return 'E';
	}

	function getRatingColor(rating: string): string {
		switch (rating) {
			case 'A':
				return 'bg-emerald-50 text-emerald-700 border-emerald-300';
			case 'B':
				return 'bg-lime-50 text-lime-700 border-lime-300';
			case 'C':
				return 'bg-yellow-50 text-yellow-700 border-yellow-300';
			case 'D':
				return 'bg-orange-50 text-orange-700 border-orange-300';
			case 'E':
				return 'bg-red-50 text-red-700 border-red-300';
			default:
				return 'bg-gray-50 text-gray-700 border-gray-300';
		}
	}

	// Filtered recommendations: if a filter is active, show categories
	// whose affinity range overlaps with the selected client range.
	// Always sorted by score descending (A first, E last).
	let filteredRecommendations = $derived.by(() => {
		let result =
			activeFilters.has('all')
				? [...recommendations]
				: recommendations.filter((rec) => {
						const riskOk =
							!activeFilters.has('risk') ||
							(rec.riskAffinityMax >= riskMin && rec.riskAffinityMin <= riskMax);
						const valOk =
							!activeFilters.has('value') ||
							(rec.valueAffinityMax >= valueMin && rec.valueAffinityMin <= valueMax);
						return riskOk && valOk;
					});
		return result.sort((a, b) => b.score - a.score);
	});
</script>

<svelte:head>
	<title>Contract Recommendations — HPB</title>
</svelte:head>

<div class="mx-auto min-h-screen max-w-7xl bg-gray-50/50 p-6">
	<div class="mb-8 border-b border-red-200 pb-4">
		<h1 class="m-0 text-3xl font-extrabold tracking-widest text-red-950 uppercase">
			Contract Partnerships
		</h1>
		<p class="mt-2 text-[11px] font-bold tracking-widest text-red-500 uppercase">
			Top recommended sectors for merchant contracting based on client spending volume.
		</p>
	</div>

	<!-- Filter Controls (replaces old stats cards area) -->
	<div class="mb-8 rounded-none border border-red-100 bg-white p-5" id="recommendation-filters">
		<div class="mb-4 flex items-center justify-between border-b border-red-100 pb-3">
			<h2 class="m-0 text-[11px] font-bold tracking-widest text-red-950 uppercase">
				Filter Mode
			</h2>
			<span class="text-[10px] font-bold tracking-widest text-red-400 uppercase">
				{matchingClientCount} clients matched · {filteredRecommendations.length} sectors shown
			</span>
		</div>

		<!-- Three filter toggle buttons -->
		<div class="mb-5 flex flex-wrap gap-3">
			<button
				onclick={() => toggleFilter('all')}
				class="border px-5 py-2 text-[10px] font-bold tracking-widest uppercase transition-all duration-200 {isActive(
					'all'
				)
					? 'border-red-600 bg-red-600 text-white shadow-md'
					: 'border-red-200 text-red-600 hover:border-red-400 hover:bg-red-50'}"
				id="filter-view-all"
			>
				View All
			</button>
			<button
				onclick={() => toggleFilter('risk')}
				class="border px-5 py-2 text-[10px] font-bold tracking-widest uppercase transition-all duration-200 {isActive(
					'risk'
				)
					? 'border-red-600 bg-red-600 text-white shadow-md'
					: 'border-red-200 text-red-600 hover:border-red-400 hover:bg-red-50'}"
				id="filter-risk-score"
			>
				By Risk Score
			</button>
			<button
				onclick={() => toggleFilter('value')}
				class="border px-5 py-2 text-[10px] font-bold tracking-widest uppercase transition-all duration-200 {isActive(
					'value'
				)
					? 'border-red-600 bg-red-600 text-white shadow-md'
					: 'border-red-200 text-red-600 hover:border-red-400 hover:bg-red-50'}"
				id="filter-value-score"
			>
				By Value Score
			</button>
		</div>

		<!-- Risk Score range (visible when risk filter active) -->
		{#if isActive('risk')}
			<div
				class="mb-4 flex flex-wrap items-center gap-3 border-t border-red-50 pt-4"
				id="risk-range"
			>
				<span class="text-[10px] font-bold tracking-widest text-red-900/70 uppercase"
					>Risk Score Range:</span
				>
				<div class="flex items-center gap-1.5">
					<input
						id="rec-risk-min"
						type="number"
						min="0"
						max="100"
						bind:value={riskMin}
						class="w-20 rounded-none border border-red-200 bg-white px-2 py-1.5 text-center text-xs text-red-950 focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:outline-none"
					/>
					<span class="text-xs font-bold text-red-300">—</span>
					<input
						id="rec-risk-max"
						type="number"
						min="0"
						max="100"
						bind:value={riskMax}
						class="w-20 rounded-none border border-red-200 bg-white px-2 py-1.5 text-center text-xs text-red-950 focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:outline-none"
					/>
				</div>
			</div>
		{/if}

		<!-- Value Score range (visible when value filter active) -->
		{#if isActive('value')}
			<div class="flex flex-wrap items-center gap-3 border-t border-red-50 pt-4" id="value-range">
				<span class="text-[10px] font-bold tracking-widest text-red-900/70 uppercase"
					>Value Score Range:</span
				>
				<div class="flex items-center gap-1.5">
					<input
						id="rec-value-min"
						type="number"
						min="0"
						max="100"
						bind:value={valueMin}
						class="w-20 rounded-none border border-red-200 bg-white px-2 py-1.5 text-center text-xs text-red-950 focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:outline-none"
					/>
					<span class="text-xs font-bold text-red-300">—</span>
					<input
						id="rec-value-max"
						type="number"
						min="0"
						max="100"
						bind:value={valueMax}
						class="w-20 rounded-none border border-red-200 bg-white px-2 py-1.5 text-center text-xs text-red-950 focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:outline-none"
					/>
				</div>
			</div>
		{/if}
	</div>

	<!-- Section heading -->
	<div class="mb-6 border-b border-red-100 pb-4">
		<h2 class="m-0 text-[11px] font-bold tracking-widest text-red-950 uppercase">
			Partnership Targets
		</h2>
	</div>

	<!-- Recommendations Grid -->
	<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
		{#each filteredRecommendations as rec (rec.id)}
			<div
				class="group flex cursor-pointer flex-col overflow-hidden rounded-none border border-red-100 bg-white transition-all duration-300 hover:-translate-y-1 hover:border-red-400 hover:shadow-lg"
			>
				<!-- Rating Header -->
				<div
					class="p-3 {getRatingColor(getRating(rec.score))} flex items-center justify-between border-b transition-colors"
				>
					<span class="text-[10px] font-bold tracking-widest uppercase">Partnership Rating</span>
					<span class="text-2xl leading-none font-black">{getRating(rec.score)}</span>
				</div>

				<!-- Content Body -->
				<div class="flex grow flex-col justify-between space-y-4 p-5">
					<div>
						<h3
							class="mb-2 text-sm leading-tight font-extrabold tracking-wider text-red-950 uppercase"
						>
							{rec.field}
						</h3>
						<div class="h-1 w-8 bg-red-200 transition-colors group-hover:bg-red-500"></div>
					</div>

					<div class="pt-2">
						<!-- Score progress bar -->
						<div class="mb-1 flex items-end justify-between">
							<span class="text-[10px] font-bold tracking-widest text-red-400 uppercase"
								>Confidence</span
							>
							<span class="text-lg font-bold text-red-900">{rec.score}%</span>
						</div>
						<div class="mb-3 h-[4px] w-full overflow-hidden border border-red-100 bg-red-50">
							<div class="h-full bg-red-500 transition-all" style="width: {rec.score}%"></div>
						</div>

						<div class="flex items-end justify-between">
							<span class="text-[10px] font-bold tracking-widest text-red-400 uppercase"
								>Est. Spend</span
							>
							<span
								class="border border-red-100 bg-red-50 px-2 py-1 text-xs font-bold text-red-700"
								>{rec.spendVolume}</span
							>
						</div>
					</div>
				</div>
			</div>
		{/each}
	</div>

	{#if filteredRecommendations.length === 0}
		<div class="py-16 text-center">
			<p class="text-sm font-bold tracking-widest text-red-300 uppercase">
				No sectors match the current filter criteria.
			</p>
		</div>
	{/if}
</div>
