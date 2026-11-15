"""Segmentos de referência (decisões 45 a 47) aplicados aos cortes rotulados, para a EDA.

Reproduz o K-means de 30/09 (10 variáveis, k = 4, mesma semente), confere com
segmentos_ampliada_30set.parquet e classifica os ativos de 30/04, 31/05 e 30/06 pelos
centros de 30/09, como em segmentacao_vies_sobrevivencia.py (passos 0 e 1).
Só lê arquivos; grava dados/processados/segmentos_por_corte.parquet.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import segmentacao_ampliada as sa  # noqa: E402
import segmentacao_kmeans as sk  # noqa: E402
from segmentacao_vies_sobrevivencia import CAT_F, CORTES, K, NUM_F, REF  # noqa: E402

PROC = sk.PROC
DESTINO = PROC / "segmentos_por_corte.parquet"
COLUNAS = ["user_id", "corte", "grupo", "persona", "saiu_60d", "plano_atual", "canal_cobranca", "renovacao_desligada"] + NUM_F


def main() -> None:
    entradas = [sk.MASTER, REF, sa.USUARIOS, sk.TREINOS_V2] + [PROC / f"base_assinantes_{c}.parquet" for c in CORTES[:3]]
    hashes = {p: sk.sha(p) for p in entradas}

    m = pd.read_parquet(sk.MASTER)
    sexo, _ = sa.imputar_sexo(m, [])
    cad = pd.to_datetime(pd.read_csv(sa.USUARIOS, dtype=str, usecols=["user_id", "data_cadastro"]).set_index("user_id")["data_cadastro"])
    t = pd.read_parquet(sk.TREINOS_V2, columns=["user_id", "inicio", "tipo"])

    # modelo de referência (30/09)
    a9 = m[m["ativo_no_corte"]].copy()
    a9 = sa.montar(a9, pd.Timestamp(CORTES[3]), t, sexo, cad, None)
    tab_freq, _ = sa.calibrar_frequencia(a9)
    a9["dias_semana"] = a9["dias_semana_declarado"].fillna(sa.aplicar_frequencia(a9["freq_obs_semana"], tab_freq))
    prep, km = sa.ajustar(a9[NUM_F], NUM_F, CAT_F, K)
    ordem = np.argsort(-np.bincount(km.labels_))
    renome = {int(o): i + 1 for i, o in enumerate(ordem)}
    a9["grupo"] = [renome[int(c)] for c in km.labels_]
    ref = pd.read_parquet(REF)
    chk = a9[["user_id", "grupo"]].merge(ref, on="user_id", how="inner", validate="1:1", suffixes=("", "_ref"))
    assert (chk["grupo"] == chk["grupo_ref"]).sum() == len(chk) == len(ref), "o modelo de referência não foi reproduzido"
    print(f"[linhas] referência 30/09 reproduzida: {sk.n(len(chk))} de {sk.n(len(ref))} contas no mesmo grupo")
    pers = ref.drop_duplicates("grupo").set_index("grupo")["persona"].to_dict()

    # cortes rotulados, classificados pelos centros de 30/09
    partes = []
    for c in CORTES[:3]:
        b = pd.read_parquet(PROC / f"base_assinantes_{c}.parquet")
        n0 = len(b)
        b = sa.montar(b, pd.Timestamp(c), t, sexo, cad, tab_freq)
        assert len(b) == n0 and b["user_id"].is_unique
        b["grupo"] = [renome[int(g)] for g in km.predict(prep.transform(b[NUM_F]))]
        b["corte"] = c
        b["persona"] = b["grupo"].map(pers)
        partes.append(b[COLUNAS])
        print(f"[linhas] corte {c}: {sk.n(n0)} → {sk.n(len(b))} (junções 1:1)")
    a9["corte"] = CORTES[3]
    a9["persona"] = a9["grupo"].map(pers)
    a9["saiu_60d"] = pd.NA
    partes.append(a9.reindex(columns=COLUNAS))
    seg = pd.concat(partes, ignore_index=True)
    seg.to_parquet(DESTINO, index=False)
    print(f"[linhas] empilhado: {sk.n(len(seg))} linhas · salvo em {DESTINO.relative_to(sk.RAIZ)}")

    alterados = [p.name for p, h in hashes.items() if sk.sha(p) != h]
    assert not alterados, f"arquivos alterados: {alterados}"
    print("entradas inalteradas (SHA-256)")


if __name__ == "__main__":
    main()
