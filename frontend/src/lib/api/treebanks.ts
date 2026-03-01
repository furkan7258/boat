import { api } from './client';
import type { TreebankRead, TreebankWithProgress, AgreementResponse } from './types';

export function listTreebanks() {
	return api.get<TreebankWithProgress[]>('/treebanks');
}

export function getTreebank(id: number) {
	return api.get<TreebankRead>(`/treebanks/${id}`);
}

export function createTreebank(title: string, language: string) {
	return api.post<TreebankRead>('/treebanks', { title, language });
}

export function deleteTreebank(id: number) {
	return api.del(`/treebanks/${id}`);
}

export function uploadConllu(id: number, file: File) {
	const formData = new FormData();
	formData.append('file', file);
	return api.upload<{ sentences_created: number }>(`/treebanks/${id}/upload`, formData);
}

export async function exportConllu(id: number) {
	const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
	const headers: Record<string, string> = {};
	if (token) headers['Authorization'] = `Bearer ${token}`;
	const res = await fetch(`/api/treebanks/${id}/export`, { headers });
	if (!res.ok) throw new Error('Export failed');
	const blob = await res.blob();
	const url = URL.createObjectURL(blob);
	const a = document.createElement('a');
	a.href = url;
	a.download = `treebank-${id}.conllu`;
	a.click();
	URL.revokeObjectURL(url);
}

export function getAgreement(id: number) {
	return api.get<AgreementResponse>(`/treebanks/${id}/agreement`);
}

export function getLanguages() {
	return api.get<Record<string, string>>('/treebanks/languages');
}
