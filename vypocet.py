"""Odhad MDM 2026: kos 2025 (Platforma MDM) x mezirocni zmeny cen CSU (rijen 2026).
Polozky bez zverejneneho cisla CSU jsou PREDPOKLADY a jsou oznacene."""
import json
kos25 = {  # Kc mesicne, cisty prijem, mimo Prahu/Brno ; Praha/Brno lisi bydleni a jidlo
 "bydleni": (15342, 21392), "jidlo": (8286, 8530), "obleceni": (1247,1247),
 "doprava": (2208,2208), "zdravi": (1730,1730), "telekom": (1378,1378),
 "volny_cas": (4030,4030)}
najem, energie = 0.6, 0.4   # predpoklad: podil najmu a energii/sluzeb v bydleni
energie_zmena = 0.5*-10.3 + 0.25*-3.6 + 0.15*1.6 + 0.10*3.85  # CSU 10/2026, vahy predpoklad
zmeny = {
 "bydleni": najem*6.4 + energie*energie_zmena,   # CSU najemne +6,4 %
 "jidlo": -4.0,                                  # CSU
 "obleceni": -3.5,                               # CSU odevy -2,6, obuv -5,3
 "doprava": 0.35*35.6 + 0.65*1.0,                # PHM +35,6 % (CSU); podil PHM 35 % predpoklad
 "zdravi": 3.0, "telekom": 1.5, "volny_cas": 3.0 # PREDPOKLAD (~ jadrova inflace)
}
def hruba(cista):  # 2026: SP 7,1 %, ZP 4,5 %, dan 15 %, sleva poplatnik 2570, dite 1267
    g = cista
    for _ in range(100):
        dan = max(0, 0.15*g - 2570 - 1267)
        g = g + (cista - (g - 0.116*g - dan))
    return round(g)
out = {}
for i, reg in enumerate(["mimo", "praha"]):
    k = {p: round(v[i]*(1+zmeny[p]/100)) for p, v in kos25.items()}
    k["uspory"] = round(5082*sum(k.values())/sum(v[i] for v in kos25.values()))  # uspory rostou s kosem
    k25 = {p: v[i] for p, v in kos25.items()}; k25["uspory"] = 5082
    out[reg] = {"kos2025": k25, "kos2026": k, "cista2026": sum(k.values()),
                "hruba2025_check": hruba(sum(k25.values())), "hruba2026": hruba(sum(k.values()))}
out["zmeny_pct"] = {p: round(v,1) for p, v in zmeny.items()}
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open("data.json","w"), ensure_ascii=False, indent=1)
