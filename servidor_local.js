const http = require("http");
const fs = require("fs");
const path = require("path");

const DIST_DIR = path.join(__dirname, "frontend", "dist");
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

const server = http.createServer((req, res) => {
  let reqPath = req.url.split("?")[0];
  if (reqPath === "/") reqPath = "/index.html";

  let filePath = path.join(DIST_DIR, reqPath);

  // SPA fallback: si no existe el archivo, devolver index.html
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
  console.log("=========================================================");
  console.log("  ⚽ SERVIDOR FUTBOLZONE ACTIVO (SISTEMA DE EXPOSICIÓN) ⚽");
  console.log("=========================================================");
  console.log(`\n🚀 Servidor web listo en: http://localhost:${PORT}`);
  console.log("Abriendo navegador predeterminado automáticamente...\n");

  const openCmd = process.platform === "win32" ? `start "" "http://localhost:${PORT}"` : `open "http://localhost:${PORT}"`;
  const { exec } = require("child_process");
  exec(openCmd);
});
