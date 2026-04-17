import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const stored: string | null = browser ? localStorage.getItem('theme') : null;
export const theme = writable<'light' | 'dark'>((stored as 'light' | 'dark') || 'light');

theme.subscribe((value: string) => {
	if (browser) {
		if (value === 'dark') {
			document.documentElement.classList.add('dark');
		} else {
			document.documentElement.classList.remove('dark');
		}
		localStorage.setItem('theme', value);
	}
});

export function toggleTheme(): void {
	theme.update((t: string) => (t === 'light' ? 'dark' : 'light'));
}
