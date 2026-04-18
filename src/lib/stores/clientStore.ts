import { writable, derived } from 'svelte/store';
import { getClientsByManager } from '$lib/firebase/firestore';
import { computePriority } from '$lib/priority';
import type { Client, FilterState } from '$lib/types';

export const clients = writable<Client[]>([]);
export const clientsLoading = writable<boolean>(false);
export const filters = writable<FilterState>({
	search: '',
	riskMin: 0,
	riskMax: 100,
	valueMin: 0,
	valueMax: 100,
	actions: [],
	sortBy: null,
	sortDir: 'desc'
});

export const filteredClients = derived(
	[clients, filters],
	([$clients, $filters]: [Client[], FilterState]) => {
		let result = $clients.filter((client: Client) => {
			const matchesSearch = client.name.toLowerCase().includes($filters.search.toLowerCase());
			const matchesRisk =
				client.riskScore >= $filters.riskMin && client.riskScore <= $filters.riskMax;
			const matchesValue =
				client.valueScore >= $filters.valueMin && client.valueScore <= $filters.valueMax;
			const matchesAction =
				$filters.actions.length === 0 ||
				$filters.actions.includes(computePriority(client.riskScore, client.valueScore).action);
			return matchesSearch && matchesRisk && matchesValue && matchesAction;
		});

		if ($filters.sortBy) {
			const dir = $filters.sortDir === 'asc' ? 1 : -1;
			result = [...result].sort((a, b) => {
				if ($filters.sortBy === 'risk') return dir * (a.riskScore - b.riskScore);
				if ($filters.sortBy === 'value') return dir * (a.valueScore - b.valueScore);
				if ($filters.sortBy === 'name') return dir * a.name.localeCompare(b.name);
				return 0;
			});
		}

		return result;
	}
);

export async function loadClients(managerId: string): Promise<void> {
	clientsLoading.set(true);
	try {
		const data = await getClientsByManager(managerId);
		clients.set(data);
	} catch (err) {
		console.error('Failed to load clients:', err);
	} finally {
		clientsLoading.set(false);
	}
}
