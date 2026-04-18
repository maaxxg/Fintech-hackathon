<script lang="ts">
	import ScoreBadge from './ScoreBadge.svelte';
	import type { Client } from '$lib/types';
	import { computePriority, type PriorityAction } from '$lib/priority';

	let { client }: { client: Client } = $props();

	let priority = $derived(computePriority(client.riskScore, client.valueScore));

	const actionLabel: Record<PriorityAction, string> = {
		high_priority_retention: 'Retain',
		let_go: 'Let Go',
		monitor_high_value: 'Monitor',
		nurture: 'Nurture',
		no_action: 'No Action'
	};

	const actionClass: Record<PriorityAction, string> = {
		high_priority_retention: 'bg-red-600 text-white border-red-700',
		let_go: 'bg-gray-200 text-gray-600 border-gray-300',
		monitor_high_value: 'bg-amber-100 text-amber-800 border-amber-300',
		nurture: 'bg-green-100 text-green-800 border-green-300',
		no_action: 'bg-white text-red-300 border-red-100'
	};
</script>

<a
	href="/client/{client.id}"
	id="client-{client.id}"
	class="group grid cursor-pointer grid-cols-[1fr_auto_auto_auto] items-center gap-4 border-b border-l-[3px] border-red-50 border-l-transparent px-3 py-1.5 text-inherit no-underline transition-colors last:border-b-0 hover:border-l-red-600 hover:bg-red-50/60"
>
	<div class="flex flex-col pl-1">
		<span
			class="text-xs font-bold tracking-widest text-red-950 uppercase transition-colors group-hover:text-red-600"
			>{client.name}</span
		>
		<div class="mt-0.5 flex items-center text-red-400">
			<span class="text-[10px] font-bold tracking-widest uppercase">{client.accountType}</span>
		</div>
	</div>

	<div class="flex items-center justify-center">
		<span
			class="inline-flex items-center rounded-none border px-1.5 py-0.5 font-mono text-[10px] font-bold tracking-widest uppercase {actionClass[
				priority.action
			]}"
		>
			{actionLabel[priority.action]}
		</span>
	</div>

	<div class="flex w-12 justify-center">
		<ScoreBadge label="" score={client.riskScore} />
	</div>
	<div class="flex w-12 justify-center">
		<ScoreBadge label="" score={client.valueScore} />
	</div>
</a>
