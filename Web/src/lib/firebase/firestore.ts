import { db } from './config';
import { collection, query, getDocs, doc, getDoc } from 'firebase/firestore';
import type { Manager, Client } from '$lib/types';

export async function getManager(uid: string): Promise<Manager | null> {
	const docRef = doc(db, 'managers', uid);
	const docSnap = await getDoc(docRef);
	if (!docSnap.exists()) return null;
	return { uid: docSnap.id, ...docSnap.data() } as Manager;
}

export async function getClientsByManager(managerId: string): Promise<Client[]> {
	const q = query(collection(db, 'clients'));
	const snapshot = await getDocs(q);
	return snapshot.docs.map((d) => ({ id: d.id, ...d.data() }) as Client);
}

export async function getClient(clientId: string): Promise<Client | null> {
	const docRef = doc(db, 'clients', clientId);
	const docSnap = await getDoc(docRef);
	if (!docSnap.exists()) return null;
	return { id: docSnap.id, ...docSnap.data() } as Client;
}
