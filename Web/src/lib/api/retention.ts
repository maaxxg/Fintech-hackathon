import type { RetentionMethod } from '$lib/types';

/**
 * Fetch suggested retention methods for a client.
 * Replace the mock with the real API URL once the API team provides it.
 */
const API_BASE_URL: string = 'https://your-api-url.com'; // TODO: replace with real URL

export async function getRetentionMethods(clientId: string): Promise<RetentionMethod[]> {
	try {
		const res = await fetch(`${API_BASE_URL}/api/retention?clientId=${clientId}`);
		if (!res.ok) throw new Error('API error');
		const data = await res.json();
		return data.methods || [];
	} catch (err) {
		console.warn('Retention API unavailable, using mock data:', err);
		// Mock fallback while API is not ready
		return [
			{
				title: 'Personalized Rate Offer',
				description:
					'Offer a tailored interest rate increase of 0.25% on their primary savings account to demonstrate value.',
				priority: 'high'
			},
			{
				title: 'Dedicated Support Line',
				description:
					'Assign a dedicated relationship manager with priority phone support to improve service experience.',
				priority: 'medium'
			},
			{
				title: 'Fee Waiver Package',
				description:
					'Waive monthly maintenance fees for the next 12 months as a loyalty incentive.',
				priority: 'medium'
			},
			{
				title: 'Financial Planning Session',
				description: 'Offer a complimentary financial planning session to deepen the relationship.',
				priority: 'low'
			}
		];
	}
}
