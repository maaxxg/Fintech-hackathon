export type PriorityAction =
	| 'high_priority_retention'
	| 'let_go'
	| 'monitor_high_value'
	| 'nurture'
	| 'no_action';

export interface PriorityResult {
	priorityScore: number;
	action: PriorityAction;
}

/**
 * Compute priority score and action from churn risk and value scores.
 * @param riskScore - churn risk score, integer 0–100 (100 = highest risk)
 * @param valueScore - client value score, integer 0–100 (100 = highest value)
 */
export function computePriority(riskScore: number, valueScore: number): PriorityResult {
	const priorityScore = (riskScore / 100) * (valueScore / 100);

	let action: PriorityAction;
	if (riskScore >= 55 && valueScore >= 70) {
		action = 'high_priority_retention';
	} else if (riskScore >= 55 && valueScore < 40) {
		action = 'let_go';
	} else if (riskScore >= 30 && valueScore >= 70) {
		action = 'monitor_high_value';
	} else if (riskScore < 30 && valueScore >= 70) {
		action = 'nurture';
	} else {
		action = 'no_action';
	}

	return { priorityScore, action };
}
