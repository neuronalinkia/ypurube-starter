"""
Genera imágenes vía Higgsfield Unlimited (sin créditos).
SIEMPRE usar este script. NUNCA el MCP generate_image — ese descuenta créditos.

Uso básico:
  python core/generar_imagen.py "prompt" archivo.png --out-dir ep01/images/video/b1

Varios en paralelo (separados por |):
  python core/generar_imagen.py "prompt1|out1.png" "prompt2|out2.png" --out-dir ...

Con imagen de referencia de personaje:
  python core/generar_imagen.py "prompt|out.png" --ref ep01/scripts/character_ref.png --out-dir ...

Reglas técnicas (NO cambiar):
  - channel="chrome"   → Playwright Chromium crashea en Windows
  - headless=False     → en headless el click Generate no dispara la petición HTTP
  - keyboard.type en chunks de 40 chars → innerText/fill() no actualiza el estado React
"""

import sys
import io
import json
import time
import argparse
import requests
from pathlib import Path

# Perfil de Chrome persistente donde está la sesión de Higgsfield.
# Primera vez: el script abrirá el browser — iniciar sesión manualmente.
# Las siguientes veces la sesión persiste automáticamente.
PROFILE_DIR = Path.home() / ".higgsfield-session"
HF_URL      = "https://higgsfield.ai/ai/image?model=nano-banana-pro"
BATCH_SIZE  = 4

_jwt_cache = {"token": None, "expires": 0}


def get_jwt(page):
    now = time.time()
    if _jwt_cache["token"] and now < _jwt_cache["expires"]:
        return _jwt_cache["token"]

    token = page.evaluate("""async () => {
        try {
            if (window.Clerk && window.Clerk.session) {
                const t = await window.Clerk.session.getToken();
                if (t) return t;
            }
        } catch(e) {}
        try {
            const clientR = await fetch(
                'https://clerk.higgsfield.ai/v1/client?__clerk_api_version=2025-11-10&_clerk_js_version=5.125.7',
                {credentials: 'include'}
            );
            const clientD = await clientR.json();
            const sessionId = clientD?.response?.last_active_session_id
                || clientD?.client?.last_active_session_id;
            if (!sessionId) return null;
            const r = await fetch(
                `https://clerk.higgsfield.ai/v1/client/sessions/${sessionId}/tokens?__clerk_api_version=2025-11-10&_clerk_js_version=5.125.7`,
                {method: 'POST', credentials: 'include'}
            );
            const d = await r.json();
            return d.jwt || null;
        } catch(e) { return null; }
    }""")

    if not token:
        raise RuntimeError("No se pudo obtener JWT — sesion expirada")

    _jwt_cache["token"] = token
    _jwt_cache["expires"] = now + 50
    return token


def is_logged_in(page):
    try:
        return page.evaluate("""() => {
            if (window.Clerk && window.Clerk.user) return true;
            const c = document.cookie;
            return c.includes('__client_uat') && !c.includes('__client_uat=0');
        }""")
    except Exception:
        return False


def upload_reference(page, jwt, image_path):
    """Sube imagen de referencia. Devuelve media_id o None."""
    result = page.evaluate("""async (jwt) => {
        const r = await fetch('https://fnf.higgsfield.ai/media/batch', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + jwt, 'Content-Type': 'application/json' },
            body: JSON.stringify({"mimetypes": ["image/png"]})
        });
        return { status: r.status, text: await r.text() };
    }""", jwt)
    if result["status"] != 200:
        print(f"  media/batch error {result['status']}: {result['text'][:100]}")
        return None
    batch      = json.loads(result["text"])
    media_id   = batch[0]["id"]
    upload_url = batch[0]["upload_url"]

    image_path = Path(image_path)
    if image_path.suffix.lower() in (".jpg", ".jpeg"):
        from PIL import Image as PilImage
        buf = io.BytesIO()
        PilImage.open(image_path).convert("RGB").save(buf, format="PNG")
        img_data = buf.getvalue()
    else:
        img_data = image_path.read_bytes()

    r2 = requests.put(upload_url, data=img_data,
                      headers={"Content-Type": "image/png"}, timeout=120)
    if r2.status_code not in (200, 204):
        print(f"  S3 upload error {r2.status_code}")
        return None

    page.evaluate(f"""async () => {{
        await fetch('https://fnf.higgsfield.ai/media/{media_id}/upload', {{
            method: 'POST',
            headers: {{ 'Authorization': 'Bearer {jwt}' }}
        }});
    }}""")
    return media_id


def submit_job_api(page, jwt, prompt, media_ids):
    """Submit directo a la API con input_images."""
    input_images = [{"id": mid, "type": "media_input"} for mid in media_ids]
    payload = {
        "params": {
            "prompt": prompt,
            "input_images": input_images,
            "width": 1376,
            "height": 768,
            "batch_size": 1,
            "aspect_ratio": "16:9",
            "is_storyboard": False,
            "is_zoom_control": False,
            "use_unlim": True,
            "resolution": "1k",
        },
        "use_unlim": True,
        "use_seedream_bonus": False,
    }
    result = page.evaluate("""async ([jwt, payload]) => {
        const r = await fetch('https://fnf.higgsfield.ai/jobs/nano-banana-2', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + jwt, 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        return { status: r.status, text: await r.text() };
    }""", [jwt, payload])

    if result["status"] not in (200, 201):
        print(f"  API submit HTTP {result['status']}: {result['text'][:200]}")
        return None

    data     = json.loads(result["text"])
    job_sets = data.get("job_sets", [])
    if job_sets:
        return job_sets[0].get("id")
    return data.get("id") or data.get("job_id")


def submit_job(page, jwt, prompt):
    """Envía un job vía UI. Devuelve job_set_id o None."""

    for _ in range(3):
        try:
            removed = page.evaluate("""() => {
                const modals = document.querySelectorAll('div[data-rac]');
                let count = 0;
                modals.forEach(m => {
                    if (m.className && m.className.includes('fixed') && m.className.includes('inset-0')) {
                        m.remove(); count++;
                    }
                });
                return count;
            }""")
            if removed:
                time.sleep(0.3)
            else:
                break
        except Exception:
            break

    try:
        sw = page.evaluate("() => { const sw = document.querySelector('[role=switch]'); return sw ? sw.getAttribute('data-state') : null; }")
        if sw != "on":
            page.evaluate("() => { const sw = document.querySelector('[role=switch]'); if (sw) sw.click(); }")
            time.sleep(0.5)
    except Exception:
        pass

    try:
        prompt_div = page.locator("[id='hf\\:tour-image-prompt']")
        if prompt_div.count() == 0:
            prompt_div = page.locator("[contenteditable=true]").first
        prompt_div.click()
        time.sleep(0.2)
        page.keyboard.press("Control+A")
        page.keyboard.press("Delete")
        time.sleep(0.1)
        for i in range(0, len(prompt), 40):
            page.keyboard.type(prompt[i:i+40], delay=80)
            time.sleep(0.15)
        time.sleep(0.4)
    except Exception as e:
        print(f"  Error escribiendo prompt: {e}")
        return None

    for attempt in range(2):
        try:
            with page.expect_response("**/jobs/nano-banana-2", timeout=20000) as resp_info:
                page.locator("button[type=submit]").first.click()
            resp = resp_info.value

            if resp.status == 429:
                wait = 35 + attempt * 15
                print(f"  Rate limit (429) — esperando {wait}s...")
                time.sleep(wait)
                continue
            if resp.status not in (200, 201):
                print(f"  Submit HTTP {resp.status}: {resp.text()[:150]}")
                return None

            data     = resp.json()
            job_sets = data.get("job_sets", [])
            if job_sets:
                return job_sets[0].get("id")
            return data.get("id") or data.get("job_id")

        except Exception as e:
            print(f"  Excepcion submit (intento {attempt+1}): {e}")
            time.sleep(10)

    return None


def poll_once(page, jwt, job_id):
    try:
        result = page.evaluate(f"""async () => {{
            const r = await fetch('https://fnf.higgsfield.ai/job-sets/{job_id}', {{
                headers: {{ 'Authorization': 'Bearer {jwt}' }}
            }});
            return {{ status: r.status, text: await r.text() }};
        }}""")

        if result["status"] == 401:
            return ("need_refresh", None)
        if result["status"] != 200:
            return ("pending", None)

        data   = json.loads(result["text"])
        jobs   = data.get("jobs", [])
        job    = jobs[0] if jobs else {}
        status = job.get("status") or data.get("status", "")

        if status == "completed":
            url = job.get("results", {}).get("raw", {}).get("url")
            if not url:
                url = data.get("results", {}).get("raw", {}).get("url")
            return ("completed", url)
        elif status in ("failed", "cancelled", "error", "nsfw", "rejected", "moderated"):
            return ("failed", None)
        return ("pending", None)
    except Exception:
        return ("pending", None)


def download_image(url, dest):
    proxy_url = url.replace("w=1920", "w=4096") if url and "w=1920" in url else url
    for attempt_url in ([proxy_url, url] if proxy_url != url else [url]):
        try:
            r = requests.get(attempt_url, timeout=120, stream=True)
            if r.status_code != 200:
                continue
            Path(dest).parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            size_kb = Path(dest).stat().st_size // 1024
            if size_kb < 10:
                Path(dest).unlink()
                continue
            print(f"  Guardado: {Path(dest).name} ({size_kb}KB)")
            return True
        except Exception as e:
            print(f"  Error descarga: {e}")
    return False


def run(jobs, out_dir, headless=False, ref_path=None):
    """
    jobs: lista de (prompt, filename)
    out_dir: carpeta de salida
    ref_path: Path opcional a imagen de referencia del personaje
    """
    from playwright.sync_api import sync_playwright

    out_dir = Path(out_dir)

    for lock_name in ["lockfile", "Default/LOCK", "Default/SingletonLock"]:
        lf = PROFILE_DIR / lock_name
        if lf.exists():
            try:
                lf.unlink()
            except Exception:
                pass

    with sync_playwright() as pw:
        browser = pw.chromium.launch_persistent_context(
            str(PROFILE_DIR),
            channel="chrome",
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-extensions",
                "--window-size=1920,1080",
            ],
            viewport={"width": 1920, "height": 1080},
        )

        pages = browser.pages
        page  = pages[0] if pages else browser.new_page()

        print("Navegando a Higgsfield...")
        page.goto(HF_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)

        if not is_logged_in(page):
            if not headless:
                print("\n[!] Inicia sesion en la ventana del navegador.")
                print("    Esperando sesion activa (10 min max)...\n")
                for _ in range(120):
                    time.sleep(5)
                    if is_logged_in(page):
                        print("Sesion detectada.")
                        break
                    print("  Esperando login...", end="\r")
                else:
                    print("\nTimeout.")
                    browser.close()
                    return
            else:
                print("ERROR: Sesion expirada. Ejecuta sin --headless.")
                browser.close()
                return

        page.goto(HF_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        try:
            page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const btn = btns.find(b => b.textContent.trim() === '16:9');
                if (btn) btn.click();
            }""")
            page.wait_for_timeout(500)
        except Exception:
            pass

        print("Sesion OK\n")

        media_ids = []
        if ref_path:
            try:
                jwt_ref = get_jwt(page)
                print(f"  Subiendo referencia: {Path(ref_path).name}...")
                mid = upload_reference(page, jwt_ref, ref_path)
                if mid:
                    media_ids = [mid]
                    print(f"  OK -> {mid[:8]}...")
                else:
                    print("  WARN: sin referencia — generando sin ref")
            except Exception as e:
                print(f"  Error subiendo referencia: {e}")
            print()

        total    = len(jobs)
        ok_count = 0
        pending  = list(jobs)
        active   = {}
        jwt_refreshed_at = time.time()
        jwt = get_jwt(page)

        def try_submit(prompt, dest):
            nonlocal jwt, jwt_refreshed_at
            try:
                jwt = get_jwt(page)
            except Exception as e:
                print(f"  JWT error: {e}")
                return None
            if media_ids:
                job_id = submit_job_api(page, jwt, prompt, media_ids)
                if not job_id:
                    job_id = submit_job(page, jwt, prompt)
            else:
                job_id = submit_job(page, jwt, prompt)
            if not job_id:
                _jwt_cache["expires"] = 0
                jwt = get_jwt(page)
                job_id = submit_job(page, jwt, prompt)
            return job_id

        while pending and len(active) < BATCH_SIZE:
            prompt, filename = pending.pop(0)
            dest = out_dir / filename
            if dest.exists():
                print(f"  Skip (ya existe): {filename}")
                ok_count += 1
                continue
            print(f"  Enviando: {filename}...")
            job_id = try_submit(prompt, dest)
            if job_id:
                active[job_id] = (prompt, dest)
                print(f"  + {filename} -> job {job_id[:8]}")
            time.sleep(6)

        deadline = time.time() + 600 + len(jobs) * 30

        while active and time.time() < deadline:
            if time.time() - jwt_refreshed_at > 50:
                _jwt_cache["expires"] = 0
                jwt = get_jwt(page)
                jwt_refreshed_at = time.time()

            for job_id in list(active.keys()):
                prompt, dest = active[job_id]
                status, url  = poll_once(page, jwt, job_id)

                if status == "need_refresh":
                    _jwt_cache["expires"] = 0
                    jwt = get_jwt(page)
                    jwt_refreshed_at = time.time()

                elif status == "completed":
                    if url and download_image(url, dest):
                        ok_count += 1
                        print(f"  OK {dest.name} ({ok_count}/{total})")
                    else:
                        print(f"  FAIL descarga {dest.name}")
                    del active[job_id]

                    if pending:
                        next_prompt, next_file = pending.pop(0)
                        next_dest = out_dir / next_file
                        if next_dest.exists():
                            print(f"  Skip (ya existe): {next_file}")
                            ok_count += 1
                        else:
                            print(f"  Enviando: {next_file}...")
                            next_id = try_submit(next_prompt, next_dest)
                            if next_id:
                                active[next_id] = (next_prompt, next_dest)
                            time.sleep(6)

                elif status == "failed":
                    print(f"  FAIL {dest.name}")
                    del active[job_id]
                    if pending:
                        next_prompt, next_file = pending.pop(0)
                        next_dest = out_dir / next_file
                        print(f"  Enviando (replace): {next_file}...")
                        next_id = try_submit(next_prompt, next_dest)
                        if next_id:
                            active[next_id] = (next_prompt, next_dest)
                        time.sleep(6)

            if active:
                remaining = [Path(v[1]).name for v in active.values()]
                print(f"  Activos: {len(active)} | En cola: {len(pending)} | {remaining}", end="\r")
                time.sleep(8)

        browser.close()

    print(f"\nCompletado: {ok_count}/{total} imagenes en {out_dir}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jobs", nargs="*",
                        help="'prompt|filename.png'. Si son 2 args sin | los trata como prompt y filename.")
    parser.add_argument("--out-dir", required=True, help="Carpeta de salida")
    parser.add_argument("--ref", default=None, help="Imagen de referencia del personaje")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    ref_path = Path(args.ref) if args.ref else None
    if ref_path and not ref_path.exists():
        print(f"ERROR: No existe la referencia: {ref_path}")
        sys.exit(1)

    job_list = []
    if len(args.jobs) == 2 and "|" not in args.jobs[0]:
        job_list = [(args.jobs[0], args.jobs[1])]
    else:
        for item in args.jobs:
            if "|" in item:
                parts = item.split("|", 1)
                job_list.append((parts[0].strip(), parts[1].strip()))

    if not job_list:
        print("ERROR: Usa: python core/generar_imagen.py 'prompt|file.png' --out-dir carpeta/")
        sys.exit(1)

    print(f"Jobs: {len(job_list)}")
    for p, f in job_list:
        print(f"  [{f}] {p[:80]}")
    print()
    run(job_list, args.out_dir, headless=args.headless, ref_path=ref_path)


if __name__ == "__main__":
    main()
