import { api } from './client';
import type { CommentRead } from './types';

export function listComments(sentenceId: number) {
	return api.get<CommentRead[]>(`/comments/sentences/${sentenceId}/comments`);
}

export function createComment(sentenceId: number, text: string) {
	return api.post<CommentRead>(`/comments/sentences/${sentenceId}/comments`, { text });
}

export function deleteComment(sentenceId: number, commentId: number) {
	return api.del(`/comments/sentences/${sentenceId}/comments/${commentId}`);
}
