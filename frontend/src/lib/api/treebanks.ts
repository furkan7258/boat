import { api } from './client';
import type { TreebankRead, TreebankWithProgress } from './types';

export function listTreebanks() {
	return api.get<TreebankWithProgress[]>('/treebanks/');
}

export function getTreebank(id: number) {
	return api.get<TreebankRead>(`/treebanks/${id}`);
}

export function createTreebank(title: string, language: string) {
	return api.post<TreebankRead>('/treebanks/', { title, language });
}

export function deleteTreebank(id: number) {
	return api.del(`/treebanks/${id}`);
}

export function uploadConllu(id: number, file: File) {
	const formData = new FormData();
	formData.append('file', file);
	return api.upload<{ created_sentences: number }>(`/treebanks/${id}/upload`, formData);
}

export function exportConllu(id: number): string {
	return `/api/treebanks/${id}/export`;
}

export function getAgreement(id: number) {
	return api.get<{ treebank_id: number; scores: Record<string, unknown>[] }>(`/treebanks/${id}/agreement`);
}

export function getLanguages() {
	return api.get<Record<string, string>>('/treebanks/languages');
}
