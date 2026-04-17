<script lang="ts">
	import { filters } from '$lib/stores/clientStore';
	import type { FilterState } from '$lib/types';

	function updateFilter<K extends keyof FilterState>(key: K, value: FilterState[K]): void {
		filters.update((f: FilterState) => ({ ...f, [key]: value }));
	}

	function resetFilters(): void {
		filters.set({
			search: '',
			riskMin: 0,
			riskMax: 100,
			valueMin: 0,
			valueMax: 100
		});
	}
</script>

<div class="rounded-none border border-blue-100 bg-white p-4" id="filter-panel">
	<div class="mb-4 flex items-center justify-between border-b border-blue-100 pb-2">
		<h3 class="m-0 text-[10px] font-bold tracking-widest text-blue-950 uppercase">Filters</h3>
		<button
			onclick={resetFilters}
			class="text-[10px] font-bold tracking-widest text-blue-500 uppercase hover:text-blue-800"
		>
			Clear
		</button>
	</div>

	<!-- Search -->
	<div class="mb-4">
		<label
			for="search-filter"
			class="mb-1.5 block text-[10px] font-bold tracking-widest text-blue-900/70 uppercase"
			>Search</label
		>
		<input
			id="search-filter"
			type="text"
			placeholder="Enter name..."
			value={$filters.search}
			oninput={(e) => updateFilter('search', (e.target as HTMLInputElement).value)}
			class="w-full rounded-none border border-blue-200 bg-white px-2.5 py-1.5 text-xs text-blue-950 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
		/>
	</div>

	<!-- Risk Score Range -->
	<div class="mb-4">
		<label class="mb-1.5 block text-[10px] font-bold tracking-widest text-blue-900/70 uppercase"
			>Risk Profile</label
		>
		<div class="flex items-center gap-1.5">
			<input
				id="risk-min"
				type="number"
				min="0"
				max="100"
				value={$filters.riskMin}
				oninput={(e) => updateFilter('riskMin', +(e.target as HTMLInputElement).value)}
				class="flex-1 rounded-none border border-blue-200 bg-white px-2 py-1.5 text-center text-xs text-blue-950 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
			/>
			<span class="text-xs text-blue-200">-</span>
			<input
				id="risk-max"
				type="number"
				min="0"
				max="100"
				value={$filters.riskMax}
				oninput={(e) => updateFilter('riskMax', +(e.target as HTMLInputElement).value)}
				class="flex-1 rounded-none border border-blue-200 bg-white px-2 py-1.5 text-center text-xs text-blue-950 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
			/>
		</div>
	</div>

	<!-- Value Score Range -->
	<div class="mb-1">
		<label class="mb-1.5 block text-[10px] font-bold tracking-widest text-blue-900/70 uppercase"
			>Value Asc.</label
		>
		<div class="flex items-center gap-1.5">
			<input
				id="value-min"
				type="number"
				min="0"
				max="100"
				value={$filters.valueMin}
				oninput={(e) => updateFilter('valueMin', +(e.target as HTMLInputElement).value)}
				class="flex-1 rounded-none border border-blue-200 bg-white px-2 py-1.5 text-center text-xs text-blue-950 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
			/>
			<span class="text-xs text-blue-200">-</span>
			<input
				id="value-max"
				type="number"
				min="0"
				max="100"
				value={$filters.valueMax}
				oninput={(e) => updateFilter('valueMax', +(e.target as HTMLInputElement).value)}
				class="flex-1 rounded-none border border-blue-200 bg-white px-2 py-1.5 text-center text-xs text-blue-950 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
			/>
		</div>
	</div>
</div>
