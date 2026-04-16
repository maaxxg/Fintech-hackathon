// Seed script — populates Firestore with test manager + client data
// Run with: node seed.js

import { initializeApp } from 'firebase/app';
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';
import { getFirestore, doc, setDoc, collection, addDoc } from 'firebase/firestore';

const firebaseConfig = {
	apiKey: 'AIzaSyBOXa68ARtiUgRqP2GgbieP_1rKueF4sHc',
	authDomain: 'fintech-hackathon-198cc.firebaseapp.com',
	projectId: 'fintech-hackathon-198cc',
	storageBucket: 'fintech-hackathon-198cc.firebasestorage.app',
	messagingSenderId: '621667564820',
	appId: '1:621667564820:web:c3d9143c3d3c028613d601'
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

async function seed() {
	// Sign in to get the UID
	const cred = await signInWithEmailAndPassword(auth, 'fran.arapovic@gmail.com', '123456');
	const uid = cred.user.uid;
	console.log('Signed in. UID:', uid);

	// Create manager document (doc ID = UID)
	await setDoc(doc(db, 'managers', uid), {
		name: 'Fran Arapović',
		email: 'fran.arapovic@gmail.com',
		role: 'Senior Relationship Manager',
		branch: 'Downtown'
	});
	console.log('✅ Manager document created');

	// Sample clients
	const clients = [
		{
			managerId: uid,
			name: 'Jane Doe',
			riskScore: 78,
			riskExplanation: 'Client has been exploring competitor offers and recently inquired about account closure procedures.',
			valueScore: 92,
			valueExplanation: 'Premium account holder with high monthly transactions and significant investment portfolio.',
			email: 'jane.doe@example.com',
			phone: '+385 91 234 5678',
			accountType: 'Premium',
			joinDate: '2020-03-15'
		},
		{
			managerId: uid,
			name: 'Marco Petrović',
			riskScore: 45,
			riskExplanation: 'Moderate risk — activity has decreased slightly over the last quarter but no signs of active switching.',
			valueScore: 68,
			valueExplanation: 'Standard business account with steady monthly deposits and moderate loan balance.',
			email: 'marco.petrovic@example.com',
			phone: '+385 92 345 6789',
			accountType: 'Business',
			joinDate: '2019-07-22'
		},
		{
			managerId: uid,
			name: 'Ana Kovačević',
			riskScore: 91,
			riskExplanation: 'High churn risk — has opened accounts at two competing banks and reduced deposit frequency by 60%.',
			valueScore: 85,
			valueExplanation: 'Long-standing VIP client with mortgage, savings, and investment products.',
			email: 'ana.kovacevic@example.com',
			phone: '+385 99 456 7890',
			accountType: 'VIP',
			joinDate: '2017-01-10'
		},
		{
			managerId: uid,
			name: 'Luka Horvat',
			riskScore: 22,
			riskExplanation: 'Low risk — consistently satisfied based on recent survey responses and steady usage patterns.',
			valueScore: 41,
			valueExplanation: 'Basic savings account with small but regular monthly deposits.',
			email: 'luka.horvat@example.com',
			phone: '+385 91 567 8901',
			accountType: 'Basic',
			joinDate: '2022-11-03'
		},
		{
			managerId: uid,
			name: 'Ivana Jurić',
			riskScore: 63,
			riskExplanation: 'Medium-high risk — filed two complaints in the last month regarding service fees.',
			valueScore: 77,
			valueExplanation: 'Active checking and savings accounts with a small business loan.',
			email: 'ivana.juric@example.com',
			phone: '+385 98 678 9012',
			accountType: 'Standard',
			joinDate: '2021-05-18'
		},
		{
			managerId: uid,
			name: 'Tomislav Babić',
			riskScore: 15,
			riskExplanation: 'Very low risk — recently renewed mortgage and added a new investment product.',
			valueScore: 95,
			valueExplanation: 'Highest-value client in portfolio with mortgage, multiple investment funds, and premium credit card.',
			email: 'tomislav.babic@example.com',
			phone: '+385 91 789 0123',
			accountType: 'VIP',
			joinDate: '2015-08-20'
		},
		{
			managerId: uid,
			name: 'Elena Marić',
			riskScore: 55,
			riskExplanation: 'Moderate risk — has not responded to the last two engagement emails and missed a scheduled review.',
			valueScore: 33,
			valueExplanation: 'Student account with low balance but potential for long-term growth.',
			email: 'elena.maric@example.com',
			phone: '+385 92 890 1234',
			accountType: 'Student',
			joinDate: '2023-09-01'
		},
		{
			managerId: uid,
			name: 'Nikola Radić',
			riskScore: 82,
			riskExplanation: 'High risk — large withdrawal last month and cancelled automatic savings transfer.',
			valueScore: 61,
			valueExplanation: 'Mid-tier client with checking account and car loan nearing completion.',
			email: 'nikola.radic@example.com',
			phone: '+385 99 901 2345',
			accountType: 'Standard',
			joinDate: '2020-12-07'
		}
	];

	const clientsCol = collection(db, 'clients');
	for (const client of clients) {
		const docRef = await addDoc(clientsCol, client);
		console.log(`✅ Client "${client.name}" added (ID: ${docRef.id})`);
	}

	console.log('\n🎉 Seed complete! All test data has been added to Firestore.');
	process.exit(0);
}

seed().catch((err) => {
	console.error('❌ Seed failed:', err.message);
	process.exit(1);
});
