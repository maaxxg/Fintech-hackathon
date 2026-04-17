<script lang="ts">
	// This fake data will later be replaced with real data fetched from the external API/database model.
	interface Recommendation {
		id: number;
		field: string;
		rating: 'A' | 'B' | 'C' | 'D' | 'E';
		score: number;
		spendVolume: string;
	}

	const recommendations: Recommendation[] = [
		{ id: 1, field: 'Gasoline / EV Charging', rating: 'A', score: 98, spendVolume: '€4.2M/mo' },
		{ id: 2, field: 'Supermarkets', rating: 'A', score: 96, spendVolume: '€3.8M/mo' },
		{ id: 3, field: 'Restaurants & Dining', rating: 'A', score: 92, spendVolume: '€2.9M/mo' },
		{ id: 4, field: 'Online Retail', rating: 'B', score: 88, spendVolume: '€2.4M/mo' },
		{ id: 5, field: 'Telecommunications', rating: 'B', score: 86, spendVolume: '€1.9M/mo' },
		{ id: 6, field: 'Healthcare & Pharmacy', rating: 'B', score: 81, spendVolume: '€1.7M/mo' },
		{ id: 7, field: 'Airlines & Travel', rating: 'B', score: 79, spendVolume: '€1.5M/mo' },
		{ id: 8, field: 'Utility Providers', rating: 'B', score: 76, spendVolume: '€1.4M/mo' },
		{ id: 9, field: 'Apparel & Clothing', rating: 'C', score: 72, spendVolume: '€1.2M/mo' },
		{ id: 10, field: 'Hardware & Electronics', rating: 'C', score: 68, spendVolume: '€1.1M/mo' },
		{ id: 11, field: 'Fitness & Gyms', rating: 'C', score: 65, spendVolume: '€950k/mo' },
		{ id: 12, field: 'Home & Gardening', rating: 'C', score: 61, spendVolume: '€890k/mo' },
		{ id: 13, field: 'Digital Streaming', rating: 'C', score: 58, spendVolume: '€840k/mo' },
		{ id: 14, field: 'Public Transit', rating: 'D', score: 52, spendVolume: '€610k/mo' },
		{ id: 15, field: 'Coffee Shops', rating: 'D', score: 49, spendVolume: '€550k/mo' },
		{ id: 16, field: 'Pet Supplies', rating: 'D', score: 46, spendVolume: '€490k/mo' },
		{ id: 17, field: 'Cosmetics & Beauty', rating: 'D', score: 42, spendVolume: '€410k/mo' },
		{ id: 18, field: 'Auto Maintenance', rating: 'E', score: 38, spendVolume: '€320k/mo' },
		{ id: 19, field: 'Gaming & Software', rating: 'E', score: 35, spendVolume: '€290k/mo' },
		{ id: 20, field: 'Fast Food', rating: 'E', score: 31, spendVolume: '€220k/mo' },
		{ id: 21, field: 'Education / Tutors', rating: 'E', score: 28, spendVolume: '€180k/mo' },
		{ id: 22, field: 'Ride Sharing', rating: 'E', score: 24, spendVolume: '€150k/mo' },
		{ id: 23, field: 'Toys & Hobbies', rating: 'E', score: 21, spendVolume: '€120k/mo' }
	];

	function getRatingColor(rating: string) {
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

	let selectedTier = $state('All');
	const tiers = ['All', 'A', 'B', 'C', 'D', 'E'];

	let filteredRecommendations = $derived(
		selectedTier === 'All'
			? recommendations
			: recommendations.filter((r) => r.rating === selectedTier)
	);
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
			Top recommended sectors for merchant contracting based on client spend volume.
		</p>
	</div>

	<!-- Stats & Insight Summary -->
	<div class="mb-8 grid grid-cols-1 gap-6 md:grid-cols-3">
		<div class="flex items-center justify-between rounded-none border border-red-100 bg-white p-5">
			<div>
				<span class="mb-1 block text-[10px] font-bold tracking-widest text-red-500 uppercase"
					>Total Analyzed</span
				>
				<span class="text-2xl font-extrabold text-red-950">23 Fields</span>
			</div>
			<div
				class="flex h-10 w-10 items-center justify-center border border-red-100 bg-red-50 font-bold text-red-600"
			>
				<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
					><path
						stroke-linecap="square"
						stroke-linejoin="miter"
						stroke-width="2"
						d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
					></path></svg
				>
			</div>
		</div>
		<div
			class="flex items-center justify-between rounded-none border border-emerald-100 bg-white p-5"
		>
			<div>
				<span class="mb-1 block text-[10px] font-bold tracking-widest text-emerald-500 uppercase"
					>Highest Priority</span
				>
				<span class="border-b-2 border-emerald-300 text-2xl font-extrabold text-emerald-900"
					>Class A</span
				>
			</div>
		</div>
		<div class="flex items-center justify-between rounded-none border border-red-100 bg-white p-5">
			<div>
				<span class="mb-1 block text-[10px] font-bold tracking-widest text-red-500 uppercase"
					>Next Recalc</span
				>
				<span class="text-lg font-bold tracking-widest text-red-950 uppercase">In 14 Days</span>
			</div>
		</div>
	</div>

	<!-- Filter & Controls -->
	<div
		class="mb-6 flex flex-col items-start justify-between border-b border-red-100 pb-4 md:flex-row md:items-center"
	>
		<h2 class="m-0 mb-4 text-[11px] font-bold tracking-widest text-red-950 uppercase md:mb-0">
			Partnership Targets
		</h2>
		<div class="flex items-center gap-3">
			<span class="text-[10px] font-bold tracking-widest text-red-500 uppercase"
				>Filter Class:</span
			>
			<div class="flex border border-red-200 bg-white">
				{#each tiers as tier}
					<button
						onclick={() => (selectedTier = tier)}
						class="border-r border-red-100 px-4 py-1.5 text-[10px] font-bold tracking-widest uppercase transition-colors last:border-r-0 {selectedTier ===
						tier
							? 'bg-red-600 text-white'
							: 'text-red-600 hover:bg-red-50'}"
					>
						{tier}
					</button>
				{/each}
			</div>
		</div>
	</div>

	<!-- Recommendations Grid -->
	<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
		{#each filteredRecommendations as rec (rec.id)}
			<div
				class="group flex cursor-pointer flex-col overflow-hidden rounded-none border border-red-100 bg-white transition-all duration-300 hover:-translate-y-1 hover:border-red-400 hover:shadow-lg"
			>
				<!-- Rating Header -->
				<div
					class="p-3 {getRatingColor(
						rec.rating
					)} flex items-center justify-between border-b transition-colors"
				>
					<span class="text-[10px] font-bold tracking-widest uppercase">Partnership Rating</span>
					<span class="text-2xl leading-none font-black">{rec.rating}</span>
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
						<div class="mb-1 flex items-end justify-between">
							<span class="text-[10px] font-bold tracking-widest text-red-400 uppercase"
								>Model Score</span
							>
							<span class="text-lg font-bold text-red-900">{rec.score}</span>
						</div>

						<!-- Score progress bar visualization -->
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
</div>
