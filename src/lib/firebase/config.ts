import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
	apiKey: 'AIzaSyBOXa68ARtiUgRqP2GgbieP_1rKueF4sHc',
	authDomain: 'fintech-hackathon-198cc.firebaseapp.com',
	projectId: 'fintech-hackathon-198cc',
	storageBucket: 'fintech-hackathon-198cc.firebasestorage.app',
	messagingSenderId: '621667564820',
	appId: '1:621667564820:web:c3d9143c3d3c028613d601',
	measurementId: 'G-NN9MKX8063'
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
