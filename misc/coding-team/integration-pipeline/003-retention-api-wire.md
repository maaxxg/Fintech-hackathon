# Task 003: Wire real FastAPI in retention.ts

## Context

`src/lib/api/retention.ts` currently points to a placeholder URL and returns mock `RetentionMethod[]` on error. The real FastAPI endpoint is `GET /clients/{client_id}/recommend` on `http://localhost:8000`.

The API returns:
```json
{
  "customer_id": "12345",
  "recommended_offer": {
    "offer_id": "OFF-001",
    "category": "GROCERIES",
    "percentage": 3.0,
    "duration_months": 3,
    "min_monthly_spend": 100,
    "description": "3% cashback na trgovine prehrane na 3 mjeseca",
    "reason": "35% spending share in groceries",
    "expected_monthly_cashback": 15.0
  }
}
```
Or `recommended_offer: null` when no eligible offers.

The existing `RetentionMethod` type is `{ title, description, priority }`. The `RetentionCard.svelte` component renders these fields. We need to map the API response into this shape.

## Objective

Update `retention.ts` to call the real API and map the response to `RetentionMethod[]`.

## Scope

File: `src/lib/api/retention.ts`

## Changes

1. Set `API_BASE_URL` to `http://localhost:8000`
2. Change the fetch URL to `${API_BASE_URL}/clients/${clientId}/recommend`
3. Map the API response:
   - If `recommended_offer` is not null, return a single-element array:
     ```ts
     [{
       title: data.recommended_offer.category.replace(/_/g, ' '),
       description: `${data.recommended_offer.description} (${data.recommended_offer.reason}). Expected cashback: ${data.recommended_offer.expected_monthly_cashback} EUR/month.`,
       priority: 'high' as const
     }]
     ```
   - If `recommended_offer` is null, return empty array `[]`
4. On fetch error (network failure, non-ok response), return empty array `[]` and log a warning. Do NOT return mock data -- the mock data is misleading now that we have a real API.

## Non-goals
- Do NOT change the `RetentionMethod` type or `RetentionCard.svelte`
- Do NOT add new types
- Do NOT add environment variable handling for the URL

## Acceptance criteria
- Successful API call with an offer maps to a single `RetentionMethod` in the returned array
- Successful API call with `recommended_offer: null` returns `[]`
- Network/API errors return `[]` without crashing
