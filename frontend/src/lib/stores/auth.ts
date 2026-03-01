import { writable, derived } from 'svelte/store';
import type { UserRead } from '$api/types';
import * as authApi from '$api/auth';

export const user = writable<UserRead | null>(null);
export const isAuthenticated = derived(user, ($user) => $user !== null);
export const isLoading = writable(true);

export async function initialize() {
	const token = localStorage.getItem('token');
	if (!token) {
		isLoading.set(false);
		return;
	}
	try {
		const me = await authApi.getMe();
		user.set(me);
	} catch {
		localStorage.removeItem('token');
	} finally {
		isLoading.set(false);
	}
}

export async function login(username: string, password: string) {
	const { access_token } = await authApi.login(username, password);
	localStorage.setItem('token', access_token);
	const me = await authApi.getMe();
	user.set(me);
}

export async function register(data: {
	username: string;
	email: string;
	password: string;
	first_name: string;
	last_name: string;
}) {
	await authApi.register(data);
	await login(data.username, data.password);
}

export function logout() {
	localStorage.removeItem('token');
	user.set(null);
}

export async function updatePreferences(prefs: Record<string, unknown>) {
	const updated = await authApi.updateMe({ preferences: prefs });
	user.set(updated);
}
