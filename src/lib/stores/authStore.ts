import { writable } from 'svelte/store';
import { onAuthChange } from '$lib/firebase/auth';
import { getManager } from '$lib/firebase/firestore';
import type { User } from 'firebase/auth';
import type { Manager } from '$lib/types';

export const user = writable<User | null>(null);
export const manager = writable<Manager | null>(null);
export const authLoading = writable<boolean>(true);

let initialized = false;

export function initAuth(): void {
	if (initialized) return;
	initialized = true;

	onAuthChange(async (firebaseUser: User | null) => {
		if (firebaseUser) {
			user.set(firebaseUser);
			const mgr = await getManager(firebaseUser.uid);
			manager.set(mgr);
		} else {
			user.set(null);
			manager.set(null);
		}
		authLoading.set(false);
	});
}
