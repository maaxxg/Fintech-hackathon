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

<div
	class="bg-white border border-blue-100 rounded-none p-4"
	id="filter-panel"
>
	<div class="flex justify-between items-center mb-4 pb-2 border-b border-blue-100">
		<h3 class="text-[10px] font-bold text-blue-950 uppercase tracking-widest m-0">
			Filters
		</h3>
		<button
			onclick={resetFilters}
			class="text-blue-500 text-[10px] font-bold uppercase tracking-widest hover:text-blue-800"
		>
			Clear
		</button>
	</div>

	<!-- Search -->
	<div class="mb-4">
		<label
			for="search-filter"
			class="block text-[10px] font-bold text-blue-900/70 uppercase tracking-widest mb-1.5">Search</label
		>
		<input
			id="search-filter"
			type="text"
			placeholder="Enter name..."
			value={$filters.search}
			oninput={(e) => updateFilter('search', (e.target as HTMLInputElement).value)}
			class="w-full px-2.5 py-1.5 bg-white border border-blue-200 rounded-none text-blue-950 text-xs focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
		/>
	</div>

	<!-- Risk Score Range -->
	<div class="mb-4">
		<label class="block text-[10px] font-bold text-blue-900/70 uppercase tracking-widest mb-1.5"
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
				class="flex-1 px-2 py-1.5 bg-white border border-blue-200 rounded-none text-blue-950 text-xs text-center focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
			/>
			<span class="text-blue-200 text-xs">-</span>
			<input
				id="risk-max"
				type="number"
				min="0"
				max="100"
				value={$filters.riskMax}
				oninput={(e) => updateFilter('riskMax', +(e.target as HTMLInputElement).value)}
				class="flex-1 px-2 py-1.5 bg-white border border-blue-200 rounded-none text-blue-950 text-xs text-center focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
			/>
		</div>
	</div>

	<!-- Value Score Range -->
	<div class="mb-1">
		<label class="block text-[10px] font-bold text-blue-900/70 uppercase tracking-widest mb-1.5"
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
				class="flex-1 px-2 py-1.5 bg-white border border-blue-200 rounded-none text-blue-950 text-xs text-center focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
			/>
			<span class="text-blue-200 text-xs">-</span>
			<input
				id="value-max"
				type="number"
				min="0"
				max="100"
				value={$filters.valueMax}
				oninput={(e) => updateFilter('valueMax', +(e.target as HTMLInputElement).value)}
				class="flex-1 px-2 py-1.5 bg-white border border-blue-200 rounded-none text-blue-950 text-xs text-center focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
			/>
		</div>
	</div>
</div>
