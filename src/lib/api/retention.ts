import type { RetentionMethod } from '$lib/types';

const API_BASE_URL: string = 'http://localhost:8000';

export async function getRetentionMethods(clientId: string): Promise<RetentionMethod[]> {
	try {
		const res = await fetch(`${API_BASE_URL}/clients/${clientId}/recommend`);
		if (!res.ok) {
			console.warn(`Retention API returned ${res.status} for client ${clientId}`);
			return [];
		}
		const data = await res.json();
		if (!data.offers || data.offers.length === 0) {
			return [];
		}
		return data.offers.map((offer: {
			category: string;
			description: string;
			reason: string;
			percentage: number;
			expected_monthly_cashback: number;
			duration_months: number;
			offer_id: string;
			min_monthly_spend: number;
		}) => ({
			title: offer.category.replace(/_/g, ' '),
			description: offer.description,
			reason: offer.reason,
			percentage: offer.percentage,
			expectedMonthlyCashback: offer.expected_monthly_cashback,
			durationMonths: offer.duration_months,
			offerId: offer.offer_id,
			minMonthlySpend: offer.min_monthly_spend,
			priority: 'high' as const
		}));
	} catch (err) {
		console.warn('Retention API unavailable:', err);
		return [];
	}
}
