"""Cesky 'Essentials Index' po vzoru United For ALICE.
Vahy = kos MDM 2025 (bez uspor), ceny = HICP Eurostat (prc_hicp_aind, CZ, rocni prumery).
Fixni vahy (Laspeyres), vysledek srovnan s celkovym HICP (CP00)."""
import json
d = json.load(open("hicp_cz.json"))
ci = d["dimension"]["coicop"]["category"]["index"]; ti = d["dimension"]["time"]["category"]["index"]
nT = len(ti); val = d["value"]
def s(code): return {t: val.get(str(ci[code]*nT + k)) for t, k in ti.items()}
W = {"CP041": 15342*.6, "CP045": 15342*.4*.85, "CP044": 15342*.4*.15, "CP01": 8286,
     "CP03": 1247, "CP07": 2208, "CP06": 1730, "CP08": 1378, "CP09": 4030}
tot = sum(W.values()); W = {k: v/tot for k, v in W.items()}
S = {k: s(k) for k in list(W) + ["CP00"]}
years = [t for t in sorted(ti) if all(S[k][t] for k in S)]
b = years[0]
ess = {t: 100*sum(W[k]*S[k][t]/S[k][b] for k in W) for t in years}
cpi = {t: 100*S["CP00"][t]/S["CP00"][b] for t in years}
Z = ["CP041", "CP045", "CP044", "CP01", "CP07"]  # uzky kos: najem, energie, voda, jidlo, doprava
zt = sum(W[k] for k in Z)
zak = {t: 100*sum(W[k]*S[k][t]/S[k][b] for k in Z)/zt for t in years}
rows = [{"rok": int(t), "essentials": round(ess[t], 1), "zaklad": round(zak[t], 1), "hicp": round(cpi[t], 1)} for t in years]
n = len(years)-1
out = {"zaklad": b, "rady": rows, "vahy_pct": {k: round(100*v, 1) for k, v in W.items()},
 "rocne_essentials": round(100*((ess[years[-1]]/100)**(1/n)-1), 2),
 "rocne_zaklad": round(100*((zak[years[-1]]/100)**(1/n)-1), 2),
 "rocne_hicp": round(100*((cpi[years[-1]]/100)**(1/n)-1), 2),
 "slozky_kumul": {k: round(100*(S[k][years[-1]]/S[k][b]-1), 1) for k in S}}
# 2026: leden-zari 2026 vs stejne mesice 2025, HICP prc_hicp_minr (COICOP 2018), Eurostat
CH26 = {"CP00": 1.5, "CP01": -2.1, "CP03": -2.7, "CP041": 6.1, "CP044": 3.5, "CP045": -7.0,
        "CP06": 3.8, "CP07": 6.2, "CP08": 2.4, "CP09": 2.1}
for k in S: S[k]["2026"] = S[k][years[-1]]*(1+CH26[k]/100)
t = "2026"
e26 = 100*sum(W[k]*S[k][t]/S[k][b] for k in W); z26 = 100*sum(W[k]*S[k][t]/S[k][b] for k in Z)/zt
out["rady"].append({"rok": 2026, "essentials": round(e26, 1), "zaklad": round(z26, 1), "hicp": round(100*S["CP00"][t]/S["CP00"][b], 1), "odhad": "leden-zari"})
out["zmeny_2026"] = CH26
json.dump(out, open("essentials.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False))
