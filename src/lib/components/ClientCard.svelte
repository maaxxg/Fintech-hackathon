<script lang="ts">
	import ScoreBadge from './ScoreBadge.svelte';
	import type { Client } from '$lib/types';

	let { client }: { client: Client } = $props();
</script>

<a
	href="/client/{client.id}"
	id="client-{client.id}"
	class="grid grid-cols-[1fr_auto_auto] gap-4 items-center px-3 py-1.5 border-b border-blue-50 border-l-[3px] border-l-transparent hover:border-l-blue-600 hover:bg-blue-50/60 transition-colors no-underline text-inherit group last:border-b-0 cursor-pointer"
>
	<div class="flex flex-col pl-1">
		<span class="font-bold text-blue-950 group-hover:text-blue-600 transition-colors text-xs tracking-widest uppercase">{client.name}</span>
		<div class="flex items-center text-blue-400 mt-0.5">
			<span class="text-[10px] font-bold uppercase tracking-widest">{client.accountType}</span>
		</div>
	</div>
	
	<div class="w-12 flex justify-center">
		<ScoreBadge label="" score={client.riskScore} type="risk" />
	</div>
	<div class="w-12 flex justify-center">
		<ScoreBadge label="" score={client.valueScore} type="value" />
	</div>
</a>
