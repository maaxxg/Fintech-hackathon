import { auth } from './config';
import { signInWithEmailAndPassword, signOut, onAuthStateChanged, type User } from 'firebase/auth';

export async function login(email: string, password: string): Promise<void> {
	await signInWithEmailAndPassword(auth, email, password);
}

export async function logout(): Promise<void> {
	await signOut(auth);
}

export function onAuthChange(callback: (user: User | null) => void): () => void {
	return onAuthStateChanged(auth, callback);
}
