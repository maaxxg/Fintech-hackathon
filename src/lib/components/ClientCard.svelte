<script lang="ts">
	import ScoreBadge from './ScoreBadge.svelte';
	import type { Client } from '$lib/types';

	let { client }: { client: Client } = $props();
</script>

<a
	href="/client/{client.id}"
	id="client-{client.id}"
	class="group grid cursor-pointer grid-cols-[1fr_auto_auto] items-center gap-4 border-b border-l-[3px] border-red-50 border-l-transparent px-3 py-1.5 text-inherit no-underline transition-colors last:border-b-0 hover:border-l-red-600 hover:bg-red-50/60"
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

	<div class="flex w-12 justify-center">
		<ScoreBadge label="" score={client.riskScore} />
	</div>
	<div class="flex w-12 justify-center">
		<ScoreBadge label="" score={client.valueScore} />
	</div>
</a>
