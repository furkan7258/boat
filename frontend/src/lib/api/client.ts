import { get } from 'svelte/store';
import { appMode, serverUrl } from '$stores/mode';

const BASE = '/api';

export class ApiError extends Error {
	constructor(
		public status: number,
		public detail: string
	) {
		super(detail);
	}
}

function isTauriOffline(): boolean {
	return get(appMode) === 'offline';
}

function getBaseUrl(): string {
	const mode = get(appMode);
	if (mode === 'connected') {
		const url = get(serverUrl);
		return url ? `${url}/api` : BASE;
	}
	return BASE;
}

async function request<T>(
	path: string,
	options: RequestInit = {}
): Promise<T> {
	// In offline mode, route through Tauri backend
	if (isTauriOffline()) {
		const { tauriRequest } = await import('./tauri-backend');
		const method = options.method ?? 'GET';
		const body = options.body ? JSON.parse(options.body as string) : undefined;
		return tauriRequest<T>(method, path, body);
	}

	// Web or connected mode — use fetch
	const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
	const headers: Record<string, string> = {
		'Content-Type': 'application/json',
		...((options.headers as Record<string, string>) ?? {})
	};
	if (token) {
		headers['Authorization'] = `Bearer ${token}`;
	}
	// Remove Content-Type for FormData (browser sets multipart boundary)
	if (options.body instanceof FormData) {
		delete headers['Content-Type'];
	}
	const base = getBaseUrl();
	const res = await fetch(`${base}${path}`, { ...options, headers });
	if (!res.ok) {
		if (res.status === 401 && typeof window !== 'undefined') {
			localStorage.removeItem('token');
			window.location.href = '/login';
		}
		const body = await res.json().catch(() => ({ detail: res.statusText }));
		throw new ApiError(res.status, body.detail ?? res.statusText);
	}
	if (res.status === 204) return undefined as T;
	return res.json();
}

export const api = {
	get: <T>(path: string) => request<T>(path),
	post: <T>(path: string, body?: unknown) =>
		request<T>(path, { method: 'POST', body: body ? JSON.stringify(body) : undefined }),
	patch: <T>(path: string, body: unknown) =>
		request<T>(path, { method: 'PATCH', body: JSON.stringify(body) }),
	put: <T>(path: string, body: unknown) =>
		request<T>(path, { method: 'PUT', body: JSON.stringify(body) }),
	del: <T>(path: string) => request<T>(path, { method: 'DELETE' }),
	upload: <T>(path: string, formData: FormData) =>
		request<T>(path, { method: 'POST', body: formData })
};
