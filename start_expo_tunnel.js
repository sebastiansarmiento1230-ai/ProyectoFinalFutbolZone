const http = require("http");
const fs = require("fs");
const path = require("path");
const { spawn, exec } = require("child_process");

const ROOT_DIR = __dirname;
const DIST_DIR = path.join(ROOT_DIR, "frontend", "dist");
const PORT = 5173;

const MIME_TYPES = {
  ".html": "text/html",
  ".js": "text/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".woff": "font/woff",
  ".woff2": "font/woff2"
};

console.log("=========================================================");
console.log("  ⚽ FUTBOLZONE — LANZADOR DE EXPOSICIÓN (SENA ADSO) ⚽");
console.log("=========================================================");

// 1. Iniciar Servidor Web Nativo
const server = http.createServer((req, res) => {
  let reqPath = req.url.split("?")[0];
  if (reqPath === "/") reqPath = "/index.html";

  let filePath = path.join(DIST_DIR, reqPath);
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    filePath = path.join(DIST_DIR, "index.html");
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || "application/octet-stream";

  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(500, { "Content-Type": "text/plain" });
      res.end("Error al cargar archivo.");
      return;
    }
    res.writeHead(200, { "Content-Type": contentType });
    res.end(content);
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`\n[1/2] Servidor local FutbolZone listo en http://localhost:${PORT}`);
  console.log("[2/2] Conectando túnel público HTTPS mundial con Cloudflare...");

  // 2. Iniciar Cloudflare Tunnel
  const cfProc = spawn(
    process.platform === "win32" ? "npx.cmd" : "npx",
    ["--yes", "cloudflared", "tunnel", "--url", `http://localhost:${PORT}`],
    { stdio: ["ignore", "pipe", "pipe"], shell: true }
  );

  let tunnelFound = false;

  function procesarSalida(data) {
    const line = data.toString();
    const match = line.match(/https:\/\/[a-zA-Z0-9-]+\.trycloudflare\.com/);
    if (match && !tunnelFound) {
      tunnelFound = true;
      const url = match[0];

      const contenidoTxt = [
        "=========================================================",
        "  ⚽ ENLACE DIRECTO PARA TU EXPOSICIÓN - FUTBOLZONE ⚽",
        "=========================================================",
        "",
        `🌐 ENLACE PÚBLICO HTTPS (ÁBRELO DESDE CUALQUIER COMPUTADOR O CELULAR):`,
        `   ${url}`,
        "",
        `🏠 ENLACE LOCAL (EN ESTE COMPUTADOR):`,
        `   http://localhost:5173`,
        "",
        `📡 ENLACE EN RED LOCAL WIFI:`,
        `   http://192.168.0.19:5173`,
        "",
        "🔑 CREDENCIALES DE ACCESO:",
        "   - Rol Administrador: admin@futbolzone.com  | Clave: admin123",
        "   - Rol Cliente:       cliente@futbolzone.com| Clave: cliente123",
        "",
        "📌 NOTA:",
        "   No cierres esta ventana de comando durante tu exposición.",
        "   El enlace funcionará perfectamente mientras la ventana esté abierta.",
        "========================================================="
      ].join("\r\n");

      fs.writeFileSync(path.join(ROOT_DIR, "URL_EXPOSICION.txt"), contenidoTxt, "utf8");

      console.log("\n" + "=".repeat(65));
      console.log("🎉 ¡ENLACE PÚBLICO LISTO PARA TU EXPOSICIÓN!");
      console.log(`🌐 ENLACE PÚBLICO HTTPS: ${url}`);
      console.log(`🏠 ENLACE LOCAL:        http://localhost:5173`);
      console.log("=".repeat(65));
      console.log("\n🔑 CREDENCIALES:");
      console.log("   Admin:   admin@futbolzone.com   | admin123");
      console.log("   Cliente: cliente@futbolzone.com | cliente123");
      console.log("\nGuardado en el archivo: URL_EXPOSICION.txt");
      console.log("Abriendo en tu navegador predeterminado...\n");

      const openCmd = process.platform === "win32" ? `start "" "${url}"` : `open "${url}"`;
      exec(openCmd);
    }
  }

  cfProc.stdout.on("data", procesarSalida);
  cfProc.stderr.on("data", procesarSalida);

  process.on("SIGINT", () => {
    try { cfProc.kill(); } catch (e) {}
    process.exit(0);
  });
});
