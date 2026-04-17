import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
	apiKey: 'AIzaSyAhLclbtQZNVp3Sw39-B4ifh490i6rDrTA',
	authDomain: 'fintech-hackathon-2.firebaseapp.com',
	projectId: 'fintech-hackathon-2',
	storageBucket: 'fintech-hackathon-2.firebasestorage.app',
	messagingSenderId: '597235520689',
	appId: '1:597235520689:web:13145be5fb7da0464b3e90',
	measurementId: 'G-Q6BCME89DC'
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
