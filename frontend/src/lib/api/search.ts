import { api } from './client';
import type { SearchResult } from './types';

export interface SearchQuery {
	field: string;
	value: string;
}

export function search(queries: SearchQuery[], treebankTitle?: string, offset = 0, limit = 20) {
	const params = new URLSearchParams();
	for (const q of queries) {
		params.append(q.field, q.value);
	}
	if (treebankTitle) params.set('treebank_title', treebankTitle);
	params.set('offset', String(offset));
	params.set('limit', String(limit));
	return api.get<SearchResult[]>(`/search?${params}`);
}
