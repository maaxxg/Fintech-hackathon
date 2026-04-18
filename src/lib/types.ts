// Manager document from Firestore 'managers' collection
export interface Manager {
	uid: string;
	name: string;
	email: string;
	role: string;
	branch: string;
}

// Client document from Firestore 'clients' collection
export interface Client {
	id: string;
	managerId: string;
	name: string;
	riskScore: number;
	riskExplanation: string;
	valueScore: number;
	valueExplanation: string;
	email: string;
	phone: string;
	accountType: string;
	joinDate: string;
	[key: string]: any;
}

// Personalized cashback offer from external API
export interface RetentionMethod {
	title: string;
	description: string;
	reason: string;
	percentage: number;
	expectedMonthlyCashback: number;
	durationMonths: number;
	offerId: string;
	minMonthlySpend: number;
	priority: 'high' | 'medium' | 'low';
}

// Filter state
export interface FilterState {
	search: string;
	riskMin: number;
	riskMax: number;
	valueMin: number;
	valueMax: number;
}
