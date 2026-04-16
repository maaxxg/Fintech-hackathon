<script lang="ts">
	import ScoreBadge from './ScoreBadge.svelte';
	import type { Client } from '$lib/types';

	let { client }: { client: Client } = $props();
</script>

<a
	href="/client/{client.id}"
	id="client-{client.id}"
	class="flex items-center justify-between p-4 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl cursor-pointer transition-all hover:border-indigo-500 hover:shadow-md hover:-translate-y-0.5 no-underline text-inherit"
>
	<div class="flex items-center gap-3">
		<div
			class="w-11 h-11 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 flex items-center justify-center font-bold text-lg shrink-0"
		>
			{client.name.charAt(0).toUpperCase()}
		</div>
		<div class="flex flex-col">
			<span class="font-semibold text-gray-900 dark:text-gray-100">{client.name}</span>
			<span class="text-xs text-gray-400 dark:text-gray-500">{client.accountType}</span>
		</div>
	</div>
	<div class="flex gap-3">
		<ScoreBadge label="Risk" score={client.riskScore} type="risk" />
		<ScoreBadge label="Value" score={client.valueScore} type="value" />
	</div>
</a>
