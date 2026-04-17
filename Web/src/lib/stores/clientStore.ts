import { writable, derived } from 'svelte/store';
import { getClientsByManager } from '$lib/firebase/firestore';
import type { Client, FilterState } from '$lib/types';

export const clients = writable<Client[]>([]);
export const clientsLoading = writable<boolean>(false);
export const filters = writable<FilterState>({
	search: '',
	riskMin: 0,
	riskMax: 100,
	valueMin: 0,
	valueMax: 100
});

// Derived store: filtered clients
export const filteredClients = derived(
	[clients, filters],
	([$clients, $filters]: [Client[], FilterState]) => {
		return $clients.filter((client: Client) => {
			const matchesSearch = client.name.toLowerCase().includes($filters.search.toLowerCase());
			const matchesRisk =
				client.riskScore >= $filters.riskMin && client.riskScore <= $filters.riskMax;
			const matchesValue =
				client.valueScore >= $filters.valueMin && client.valueScore <= $filters.valueMax;
			return matchesSearch && matchesRisk && matchesValue;
		});
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
