from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="nl" data-theme="dark" data-density="comfortable">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>DTMO — UX Preferences</title><link rel="stylesheet" href="/ui/design-system.css">
<style>:root{color-scheme:dark}body{margin:0;background:#07111c}.prefs{max-width:760px;margin:0 auto;padding:2rem}.card{background:#0d1a29;border:1px solid #20384f;border-radius:14px;padding:1.25rem;margin:1rem 0}.row{display:grid;grid-template-columns:1fr 1fr;gap:1rem}label{display:grid;gap:.4rem}select{padding:.7rem;background:#081522;color:#fff;border:1px solid #29465f;border-radius:8px}.note{color:#9bb0c3}html[data-theme=light] body{background:#f4f7fa;color:#142231}html[data-theme=light] .card{background:#fff;border-color:#cbd7e2}html[data-theme=light] select{background:#fff;color:#142231;border-color:#9eb0c0}html[data-theme=light] .note{color:#4c6072}html[data-density=compact] .card{padding:.8rem}html[data-density=compact] .prefs{padding:1rem}@media(max-width:620px){.row{grid-template-columns:1fr}}</style></head>
<body><main class="prefs"><p><a href="/ui/operations">← Operations</a></p><p class="eyebrow">RC10.6 UX polish</p><h1>Weergavevoorkeuren</h1><p class="note">Deze voorkeuren wijzigen uitsluitend de lokale presentatie. Ze verlenen geen rechten en wijzigen geen server-side gegevens, reviewstatus of share approval.</p><section class="card"><h2>Interface</h2><div class="row"><label for="theme">Thema<select id="theme"><option value="dark">Donker</option><option value="light">Licht</option></select></label><label for="density">Dichtheid<select id="density"><option value="comfortable">Comfortabel</option><option value="compact">Compact</option></select></label></div><p id="status" class="note" role="status" aria-live="polite">Voorkeuren worden alleen in deze browser opgeslagen.</p></section><section class="card"><h2>Governance boundary</h2><p class="note">RBAC, separation of duties, provenance, audit logging, human review en afzonderlijke externe share approval blijven server-side autoritatief.</p></section></main><script>const root=document.documentElement;const theme=document.getElementById('theme');const density=document.getElementById('density');const status=document.getElementById('status');function allowed(v,a,d){return a.includes(v)?v:d}function apply(){const t=allowed(localStorage.getItem('dtmo.theme'),['dark','light'],'dark');const d=allowed(localStorage.getItem('dtmo.density'),['comfortable','compact'],'comfortable');root.dataset.theme=t;root.dataset.density=d;theme.value=t;density.value=d}theme.addEventListener('change',()=>{localStorage.setItem('dtmo.theme',theme.value);apply();status.textContent='Thema lokaal opgeslagen.'});density.addEventListener('change',()=>{localStorage.setItem('dtmo.density',density.value);apply();status.textContent='Dichtheid lokaal opgeslagen.'});apply();</script></body></html>"""


@router.get("/ui/preferences", response_class=HTMLResponse)
def ux_preferences() -> HTMLResponse:
    return HTMLResponse(_PAGE)
