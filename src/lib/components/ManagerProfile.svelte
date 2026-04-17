<script lang="ts">
	import { manager } from '$lib/stores/authStore';
	import { logout } from '$lib/firebase/auth';
	import { goto } from '$app/navigation';

	async function handleLogout(): Promise<void> {
		await logout();
		goto('/login');
	}
</script>

<div class="rounded-none border border-blue-100 bg-white p-4" id="manager-profile">
	{#if $manager}
		<div class="mb-4 flex items-center gap-3">
			<div
				class="relative flex h-10 w-10 shrink-0 items-center justify-center rounded-none border border-blue-950 bg-blue-900 text-sm font-bold text-white"
			>
				{$manager.name?.charAt(0).toUpperCase() ?? '?'}
				<div
					class="absolute -right-1 -bottom-1 z-10 h-2.5 w-2.5 rounded-none border-2 border-white bg-blue-400"
				></div>
			</div>
			<div class="flex flex-col">
				<span class="text-sm font-bold tracking-wide text-blue-950 uppercase">{$manager.name}</span>
				<span class="mt-0.5 text-[10px] font-bold tracking-widest text-blue-600 uppercase"
					>{$manager.role}</span
				>
			</div>
		</div>
		<button
			onclick={handleLogout}
			class="w-full rounded-none border border-blue-200 bg-white py-1.5 text-xs font-bold tracking-widest text-blue-700 uppercase transition-colors hover:border-blue-300 hover:bg-blue-50"
		>
			Sign Out
		</button>
	{:else}
		<div
			class="flex items-center justify-center py-4 text-[10px] font-bold tracking-widest text-blue-500 uppercase"
		>
			Loading
		</div>
	{/if}
</div>
