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
	class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-5"
	id="filter-panel"
>
	<div class="flex justify-between items-center mb-4">
		<h3 class="text-base font-semibold text-gray-900 dark:text-gray-100">Filters</h3>
		<button
			onclick={resetFilters}
			class="bg-transparent border-none text-indigo-500 text-xs font-medium cursor-pointer hover:underline"
		>
			Reset
		</button>
	</div>

	<!-- Search -->
	<div class="mb-4">
		<label
			for="search-filter"
			class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Search</label
		>
		<input
			id="search-filter"
			type="text"
			placeholder="Client name..."
			value={$filters.search}
			oninput={(e) => updateFilter('search', (e.target as HTMLInputElement).value)}
			class="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 text-sm placeholder-gray-400 focus:outline-none focus:border-indigo-500 transition"
		/>
	</div>

	<!-- Risk Score Range -->
	<div class="mb-4">
		<label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1"
			>Risk Score Range</label
		>
		<div class="flex items-center gap-2">
			<input
				id="risk-min"
				type="number"
				min="0"
				max="100"
				value={$filters.riskMin}
				oninput={(e) => updateFilter('riskMin', +(e.target as HTMLInputElement).value)}
				class="flex-1 px-2 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 text-sm text-center focus:outline-none focus:border-indigo-500"
			/>
			<span class="text-gray-400">—</span>
			<input
				id="risk-max"
				type="number"
				min="0"
				max="100"
				value={$filters.riskMax}
				oninput={(e) => updateFilter('riskMax', +(e.target as HTMLInputElement).value)}
				class="flex-1 px-2 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 text-sm text-center focus:outline-none focus:border-indigo-500"
			/>
		</div>
	</div>

	<!-- Value Score Range -->
	<div class="mb-4">
		<label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1"
			>Value Score Range</label
		>
		<div class="flex items-center gap-2">
			<input
				id="value-min"
				type="number"
				min="0"
				max="100"
				value={$filters.valueMin}
				oninput={(e) => updateFilter('valueMin', +(e.target as HTMLInputElement).value)}
				class="flex-1 px-2 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 text-sm text-center focus:outline-none focus:border-indigo-500"
			/>
			<span class="text-gray-400">—</span>
			<input
				id="value-max"
				type="number"
				min="0"
				max="100"
				value={$filters.valueMax}
				oninput={(e) => updateFilter('valueMax', +(e.target as HTMLInputElement).value)}
				class="flex-1 px-2 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-gray-100 text-sm text-center focus:outline-none focus:border-indigo-500"
			/>
		</div>
	</div>

	<!-- MORE FILTERS WILL BE ADDED HERE LATER -->
</div>
