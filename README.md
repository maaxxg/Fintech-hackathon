# Fintech Hackathon – HPB Re‑branding (Web Branch)

## 📖 Projektni pregled
Ovo je **SvelteKit** aplikacija za internu upotrebu bankarskih menadžera – prikaz klijenata, analizu rizika i vrijednosti, te preporuke za zadržavanje klijenata.  
U posljednjem razvojnome ciklusu ("web" branch) fokusirali smo se na:
1. **Popravak bug‑a u autentifikaciji**
2. **Omogućavanje pristupa s mobilnih uređaja**
3. **Potpuno re‑brandiranje prema HPB‑vizualnom identitetu**
4. **Redizajn login stranice**
5. **Zamjena favicona**
6. **Priprema za buduću API integraciju**

---

## 🛠️ Tehnološki stack
- **Framework**: SvelteKit (TypeScript)
- **Styling**: Tailwind CSS v4 (utility‑first)
- **Auth**: Firebase Authentication
- **Database**: Cloud Firestore (mock podaci u razvoju)
- **Build**: Vite (defaultni SvelteKit dev‑server)

---

## 🌿 Git workflow & branch struktura
```
main                ← stabilna produkcija
│
└─ web             ← radna grana za UI/UX i branding (trenutni rad)
   ├─ feature/auth‑fix
   ├─ feature/mobile‑access
   ├─ feature/hpb‑branding
   └─ feature/login‑redesign
```
- **feature/auth‑fix** – popravak `authStore.ts`
- **feature/mobile‑access** – `npm run dev -- --host`
- **feature/hpb‑branding** – zamjena boja, logo, tipografija
- **feature/login‑redesign** – stiliziranje lijevog panela i dodavanje loga

Svaka funkcionalnost je razvijana u zasebnoj grani, a zatim **merge‑ana** u `web` putem pull‑requesta. Nakon što je `web` stabilan, merge‑amo ga u `main`.

---

## 🚀 Detaljan razvojni proces
### 1️⃣ Postavljanje okruženja
```bash
# Kloniranje repozitorija
git clone <repo‑url>
cd Fintech-hackathon

# Instalacija ovisnosti
npm install
```
### 2️⃣ Popravak bug‑a u autentifikaciji
- **Datoteka**: `src/lib/stores/authStore.ts`
- Problem: `authLoading` ostaje `true` kad `onAuthChange` baci grešku → beskonačno učitavanje.
- Rješenje: `try … finally` blok oko `onAuthChange` logike.
- Commit:
```bash
git checkout -b feature/auth-fix
git add src/lib/stores/authStore.ts
git commit -m "Fix infinite loading on auth error"
```
### 3️⃣ Omogućavanje pristupa s mobilnih uređaja
- Pokretanje dev‑servera s `--host` flagom kako bi se izložila lokalna IP adresa.
- **Komanda**:
```bash
npm run dev -- --host
```
- Testirano na Android i iOS uređajima (isti Wi‑Fi) – aplikacija je dostupna na `http://<LAN‑IP>:5173`.
- Commit:
```bash
git checkout -b feature/mobile-access
git commit -am "Add dev server host flag for mobile testing"
```
### 4️⃣ HPB re‑branding (boje, tipografija, logo)
#### a) Globalna zamjena boja
- Pretražili smo sve `.svelte` datoteke i zamijenili `blue-` Tailwind klase s `red-` (HPB crvena).
- Upotrijebili smo `sed` skriptu:
```bash
find src -name "*.svelte" -exec sed -i '' 's/blue-/red-/g' {} +
```
#### b) Zamjena loga u navigacijskoj traci
- **Datoteka**: `src/lib/components/Navbar.svelte`
- Stara slika (`Hpb-logo.svg.png`) zamijenjena s `logo-snip.png`.
- Dodani su stilovi: tamnosiva pozadina, bijeli tekst, hover efekti.
#### c) Bočna traka (Sidebar)
- `src/lib/components/Sidebar.svelte` ažuriran da koristi `logo-snip.png`.
#### d) Naslovna traka (navbar) – “Contract Recommendations”
- Boje promijenjene u neutralne sive/bijele tonove.
- Dodan je podcrtani hover‑efekt.
- Commit:
```bash
git checkout -b feature/hpb-branding
git add src/lib/components/*.svelte src/**/*.svelte
git commit -m "Apply HPB red palette and logo across UI"
```
### 5️⃣ Redizajn login stranice
- **Cilj**: lijevi panel u HPB‑crvenoj boji, bijeli tekst, logo‑snip uz tanki crni okvir.
- **Datoteka**: `src/routes/login/+page.svelte`
- Promjene:
  - `border‑red‑600 bg‑red‑600` za panel.
  - `border border‑black` na `<img>` logu.
  - Svaki `red‑` stil svijetliji (npr. `text‑white`, `bg‑gray‑300`).
  - Dodan je `logo‑snip.png` uz HPB naslov.
- Commit:
```bash
git checkout -b feature/login-redesign
git add src/routes/login/+page.svelte
git commit -m "Login page redesign – HPB red theme and logo with black border"
```
### 6️⃣ Zamjena favicona (Safari kompatibilnost)
- **Datoteka**: `src/app.html`
- Zamijenili smo:
  ```html
  <link rel="icon" type="image/png" href="%sveltekit.assets%/logo-snip.png" />
  <link rel="apple-touch-icon" href="%sveltekit.assets%/logo-snip.png" />
  ```
- Ovo funkcionira i u Chrome‑u i u Safari‑ju.
- Commit:
```bash
git checkout -b feature/favicon-update
git add src/app.html
git commit -m "Use logo-snip.png as favicon and apple‑touch‑icon"
```
### 7️⃣ Integracija API‑ja (placeholder)
- **Datoteka**: `src/lib/api/retention.ts`
- Postavljen je `getRetentionMethods` stub koji vraća mock podatke.
- TODO: zamijeniti `BASE_URL` s pravim endpointom kada ga tim dostavi.
- Commit:
```bash
git checkout -b feature/api‑placeholder
git add src/lib/api/retention.ts
git commit -m "Add placeholder for retention API"
```
### 8️⃣ Testiranje & verifikacija
| Korak | Opis | Komanda / akcija |
|------|------|-----------------|
| **Unit testovi** | Pokrenuti sve testove (Jest) – trenutno nema testova, plan za budućnost. | `npm test` |
| **Manual UI test** | Provjeriti sve stranice u pregledniku (desktop + mobilni). | `npm run dev -- --host` |
| **Cross‑browser** | Chrome, Firefox, Safari – provjeriti favicon i logo. | Otvoriti `http://localhost:5173` |
| **Accessibility** | Provjeriti kontrast boja (WCAG AA). | Chrome DevTools > Lighthouse |

### 9️⃣ Merge u `web` i potom u `main`
```bash
# Na svakoj feature grani
git push origin <branch>
# Otvoriti Pull Request na GitHubu → review → merge

# Nakon što su sve feature grane merge‑ane u web
git checkout web
git merge feature/auth-fix
git merge feature/mobile-access
git merge feature/hpb-branding
git merge feature/login-redesign
git merge feature/favicon-update

git push origin web
```

### 🔀 Deploy (produkcija)
- Deploy na Vercel / Netlify (SvelteKit‑compatible) – samo `git push main`.
- `vercel --prod` ili `netlify deploy --prod`.

---

## 📂 Struktura projekta (sažeto)
```
Fintech‑hackathon/
├─ src/
│  ├─ app.html               # glavni HTML (favicon ažuriran)
│  ├─ routes/                # Svelte rute
│  │   ├─ +layout.svelte
│  │   ├─ +page.svelte        # Dashboard (HPB‑crvena tema)
│  │   ├─ login/+page.svelte  # Redizajnirana login stranica
│  │   └─ client/[id]/+page.svelte  # Detalji klijenta
│  ├─ lib/
│  │   ├─ components/        # Navbar, Sidebar, kartice …
│  │   ├─ stores/authStore.ts # popravak bug‑a
│  │   └─ api/retention.ts    # placeholder API
│  └─ static/
│      ├─ logo-snip.png      # novi HPB logo (koristi se i kao favicon)
│      └─ …
├─ README.md                 # Ovaj detaljni opis
└─ package.json
```

---

## 📅 Daljnji koraci / TODO
- **Implementirati stvarni API** – zamijeniti mock u `retention.ts` i dodati tipove.
- **Dodati unit i e2e testove** (Vitest + Playwright).
- **Optimizirati performanse** – lazy‑load komponenti, kod‑splitting.
- **Internationalisation** – podrška za hrvatski i engleski (iOS/Android locale).
- **CI/CD** – postaviti GitHub Actions za lint, test i preview‑deploy.

---

## 🙏 Zahvale
Zahvaljujemo se timu HPB‑a na dostavljenim brand‑materijalima (boje, logo) i na brzom feedbacku tijekom razvoja.

*Ovaj README je namijenjen budućim developerima koji će nastaviti rad na projektu i pruža sve ključne informacije o dosadašnjem razvoju na `web` branchu.*
