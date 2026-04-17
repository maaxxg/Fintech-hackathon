<script lang="ts">
  import { filteredClients } from '$lib/stores/clientStore';

  let totalClients = $derived($filteredClients.length);
  let avgRisk = $derived(
    totalClients > 0
      ? Math.round($filteredClients.reduce((sum, c) => sum + c.riskScore, 0) / totalClients)
      : 0
  );
  let avgValue = $derived(
    totalClients > 0
      ? Math.round($filteredClients.reduce((sum, c) => sum + c.valueScore, 0) / totalClients)
      : 0
  );
  let highRisk = $derived($filteredClients.filter(c => c.riskScore >= 70).length);
</script>

<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4" id="dashboard-stats">
  <div class="bg-white border border-blue-100 rounded-none p-4">
    <span class="text-[11px] font-bold text-blue-500 uppercase tracking-widest block mb-1">Total Clients</span>
    <span class="text-2xl font-extrabold text-blue-950">{totalClients}</span>
  </div>
  <div class="bg-white border border-blue-100 rounded-none p-4">
    <span class="text-[11px] font-bold text-blue-500 uppercase tracking-widest block mb-1">Avg Risk</span>
    <span class="text-2xl font-extrabold text-blue-950">{avgRisk}</span>
  </div>
  <div class="bg-white border border-blue-100 rounded-none p-4">
    <span class="text-[11px] font-bold text-blue-500 uppercase tracking-widest block mb-1">Avg Value</span>
    <span class="text-2xl font-extrabold text-blue-950">{avgValue}</span>
  </div>
  <div class="bg-white border border-blue-100 rounded-none p-4">
    <span class="text-[11px] font-bold text-blue-500 uppercase tracking-widest block mb-1">High Risk</span>
    <span class="text-2xl font-extrabold text-blue-950">{highRisk}</span>
  </div>
</div>
