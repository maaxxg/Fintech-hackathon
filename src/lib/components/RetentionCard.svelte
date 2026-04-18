<script lang="ts">
	import type { RetentionMethod } from '$lib/types';

	let { method }: { method: RetentionMethod } = $props();
</script>

<div class="rounded-none border border-rose-200 bg-white p-4 shadow-none">
	<!-- Header: category + cashback rate -->
	<div class="mb-3 flex items-start justify-between gap-3">
		<h4 class="m-0 text-[11px] leading-tight font-bold tracking-widest text-rose-950 uppercase">
			{method.title}
		</h4>
		<span class="shrink-0 rounded-none bg-rose-600 px-2 py-1 text-[13px] font-extrabold tracking-tight text-white">
			{method.percentage}% cashback
		</span>
	</div>

	<!-- Description -->
	<p class="mb-3 m-0 text-[10px] leading-relaxed tracking-widest text-rose-900/70 uppercase">
		{method.description}
	</p>

	<!-- Reason badge -->
	<p class="mb-3 m-0 text-[10px] leading-relaxed font-bold tracking-widest text-rose-700 uppercase">
		{method.reason}
	</p>

	<!-- Stats row -->
	<div class="flex flex-wrap gap-3 border-t border-rose-100 pt-3">
		<div class="flex flex-col">
			<span class="text-[9px] font-bold tracking-widest text-rose-400 uppercase">Expected / month</span>
			<span class="text-[12px] font-extrabold text-rose-950">{method.expectedMonthlyCashback.toFixed(2)} EUR</span>
		</div>
		<div class="flex flex-col">
			<span class="text-[9px] font-bold tracking-widest text-rose-400 uppercase">Duration</span>
			<span class="text-[12px] font-extrabold text-rose-950">{method.durationMonths} months</span>
		</div>
		<div class="flex flex-col">
			<span class="text-[9px] font-bold tracking-widest text-rose-400 uppercase">Min. spend</span>
			<span class="text-[12px] font-extrabold text-rose-950">{method.minMonthlySpend} EUR/mo</span>
		</div>
	</div>
</div>
