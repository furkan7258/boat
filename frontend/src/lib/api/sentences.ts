import { api } from './client';
import type { SentenceBrief, SentenceRead, AnnotationRead, DiffToken } from './types';

export function listSentences(treebankId: number, skip = 0, limit = 20) {
	return api.get<SentenceBrief[]>(`/sentences/?treebank_id=${treebankId}&skip=${skip}&limit=${limit}`);
}

export function getSentence(id: number) {
	return api.get<SentenceRead>(`/sentences/${id}`);
}

export function createSentence(treebankId: number, sentId: string, text: string) {
	return api.post<SentenceRead>('/sentences/', { treebank_id: treebankId, sent_id: sentId, text });
}

export function deleteSentence(id: number) {
	return api.del(`/sentences/${id}`);
}

export function listSentenceAnnotations(id: number) {
	return api.get<AnnotationRead[]>(`/sentences/${id}/annotations`);
}

export function getSentenceDiff(id: number) {
	return api.get<DiffToken[]>(`/sentences/${id}/diff`);
}
