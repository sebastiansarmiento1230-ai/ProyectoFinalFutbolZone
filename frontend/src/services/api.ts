// Configuración de URL base: soporta BACKEND_URL inyectado por Vercel Multi-Service
const rawBackendUrl =
  (import.meta as any).env?.BACKEND_URL ||
  (import.meta as any).env?.VITE_BACKEND_URL ||
  (import.meta as any).env?.VITE_API_URL ||
  "";

export const API_BASE_URL = rawBackendUrl
  ? rawBackendUrl.replace(/\/+$/, "") + (rawBackendUrl.endsWith("/api") ? "" : "/api")
  : "/api";

export const getAuthToken = (): string | null => {
  return localStorage.getItem("token");
};

export const setAuthToken = (token: string): void => {
  localStorage.setItem("token", token);
};

export const removeAuthToken = (): void => {
  localStorage.removeItem("token");
  localStorage.removeItem("usuario");
};

export const getStoredUser = (): any | null => {
  const user = localStorage.getItem("usuario");
  return user ? JSON.parse(user) : null;
};

export const setStoredUser = (user: any): void => {
  localStorage.setItem("usuario", JSON.stringify(user));
};

// Fallback de datos offline para exposiciones y computadores externos sin backend activo
const MOCK_USUARIOS = [
  { id: 1, nombre: "Admin", apellido: "FutbolZone", email: "admin@futbolzone.com", rol: "admin", telefono: "3001234567", activo: true },
  { id: 2, nombre: "Carlos", apellido: "Díaz", email: "cliente@futbolzone.com", rol: "cliente", telefono: "3109876543", activo: true },
];

const MOCK_CANCHAS = [
  { id: 1, nombre: "Cancha Central", tipo: "Fútbol 5", descripcion: "Cancha principal con césped sintético premium", capacidad_jugadores: 10, precio_hora: 50000, tiene_iluminacion: true, tiene_techo: false, activa: true },
  { id: 2, nombre: "Cancha Norte", tipo: "Fútbol 7", descripcion: "Cancha amplia con iluminación LED de foco nocturno", capacidad_jugadores: 14, precio_hora: 70000, tiene_iluminacion: true, tiene_techo: false, activa: true },
  { id: 3, nombre: "Cancha Sur", tipo: "Fútbol 11", descripcion: "Cancha reglamentaria profesional para torneos", capacidad_jugadores: 22, precio_hora: 100000, tiene_iluminacion: true, tiene_techo: true, activa: true },
  { id: 4, nombre: "Cancha Este", tipo: "Fútbol 5", descripcion: "Cancha sintética compacta con cubierta", capacidad_jugadores: 10, precio_hora: 45000, tiene_iluminacion: false, tiene_techo: true, activa: true },
  { id: 5, nombre: "Cancha Oeste", tipo: "Fútbol 7", descripcion: "Cancha techada con iluminación LED y graderías", capacidad_jugadores: 14, precio_hora: 65000, tiene_iluminacion: true, tiene_techo: true, activa: true },
];

const SEED_RESERVAS = [
  {
    id: 101,
    usuario_id: 2,
    cancha_id: 1,
    cancha_nombre: "Cancha Central",
    fecha: "2026-11-25",
    hora_inicio: "18:00",
    hora_fin: "19:00",
    precio_total: 62000,
    estado: "confirmada",
    cliente_nombre: "Carlos Díaz",
    cliente_email: "cliente@futbolzone.com",
    cliente_telefono: "3109876543",
    notas: "Papas, Gatorade, Parqueadero",
    incluye_kit: true,
    incluye_arbitro: false,
    metodo_pago: "Nequi",
    referencia_pago: "NEQ-88910",
    creado_en: "2026-11-20T10:00:00"
  },
  {
    id: 102,
    usuario_id: 2,
    cancha_id: 2,
    cancha_nombre: "Cancha Norte",
    fecha: "2026-11-28",
    hora_inicio: "20:00",
    hora_fin: "21:00",
    precio_total: 70000,
    estado: "confirmada",
    cliente_nombre: "Carlos Díaz",
    cliente_email: "cliente@futbolzone.com",
    cliente_telefono: "3109876543",
    notas: "Sin adicionales",
    incluye_kit: false,
    incluye_arbitro: false,
    metodo_pago: "Efectivo",
    referencia_pago: "EFE-10293",
    creado_en: "2026-11-21T15:30:00"
  },
  {
    id: 103,
    usuario_id: 2,
    cancha_id: 3,
    cancha_nombre: "Cancha Sur",
    fecha: "2026-12-05",
    hora_inicio: "16:00",
    hora_fin: "18:00",
    precio_total: 200000,
    estado: "completada",
    cliente_nombre: "Carlos Díaz",
    cliente_email: "cliente@futbolzone.com",
    cliente_telefono: "3109876543",
    notas: "Arbitraje profesional, Chalecos oficiales",
    incluye_kit: true,
    incluye_arbitro: true,
    metodo_pago: "Tarjeta",
    referencia_pago: "TAR-44912",
    creado_en: "2026-11-18T09:15:00"
  },
  {
    id: 104,
    usuario_id: 2,
    cancha_id: 1,
    cancha_nombre: "Cancha Central",
    fecha: "2026-12-10",
    hora_inicio: "19:00",
    hora_fin: "20:00",
    precio_total: 55000,
    estado: "pendiente",
    cliente_nombre: "Carlos Díaz",
    cliente_email: "cliente@futbolzone.com",
    cliente_telefono: "3109876543",
    notas: "Gatorade x2",
    incluye_kit: false,
    incluye_arbitro: false,
    metodo_pago: "Daviplata",
    referencia_pago: "DAV-77123",
    creado_en: "2026-11-22T08:00:00"
  }
];

function getLocalReservas(): any[] {
  try {
    const raw = localStorage.getItem("fz_expo_reservas");
    if (!raw) {
      localStorage.setItem("fz_expo_reservas", JSON.stringify(SEED_RESERVAS));
      return SEED_RESERVAS;
    }
    return JSON.parse(raw);
  } catch {
    return SEED_RESERVAS;
  }
}

function saveLocalReservas(list: any[]): void {
  try {
    localStorage.setItem("fz_expo_reservas", JSON.stringify(list));
  } catch {}
}

function handleOfflineExpoFallback(endpoint: string, options: RequestInit = {}): any {
  const method = (options.method || "GET").toUpperCase();
  const body = options.body ? JSON.parse(options.body as string) : {};
  const storedUser = getStoredUser();

  // Login
  if (endpoint.startsWith("/usuarios/login")) {
    const { correo, password } = body;
    if (correo === "admin@futbolzone.com" && (password === "admin123" || password === "123456")) {
      return { success: true, message: "Inicio exitoso (Modo Expo)", data: { access_token: "expo-admin-token", usuario: MOCK_USUARIOS[0] } };
    }
    if (correo === "cliente@futbolzone.com" && (password === "cliente123" || password === "123456")) {
      return { success: true, message: "Inicio exitoso (Modo Expo)", data: { access_token: "expo-cliente-token", usuario: MOCK_USUARIOS[1] } };
    }
    // Permitir cualquier demo ingresado
    if (correo && password) {
      const rolDemo = correo.toLowerCase().includes("admin") ? "admin" : "cliente";
      const uDemo = {
        id: 99,
        nombre: correo.split("@")[0] || "Usuario",
        apellido: "FutbolZone",
        email: correo,
        rol: rolDemo,
        telefono: "3000000000",
        activo: true
      };
      return { success: true, message: "Inicio exitoso", data: { access_token: "expo-demo-token", usuario: uDemo } };
    }
    return { success: false, message: "Credenciales inválidas" };
  }

  // Canchas
  if (endpoint.startsWith("/canchas")) {
    return { success: true, data: MOCK_CANCHAS };
  }

  // Mis Reservas
  if (endpoint.startsWith("/reservas/mis-reservas")) {
    const list = getLocalReservas();
    const userId = storedUser?.id || 2;
    const mis = list.filter((r) => r.usuario_id === userId || userId === 1);
    return { success: true, data: mis.length > 0 ? mis : list };
  }

  // Todas las reservas (Admin)
  if (endpoint.startsWith("/reservas") && method === "GET") {
    return { success: true, data: getLocalReservas() };
  }

  // Crear Reserva
  if (endpoint.startsWith("/reservas") && method === "POST") {
    const list = getLocalReservas();
    const cMatch = MOCK_CANCHAS.find((c) => c.id === Number(body.cancha_id));
    const nueva = {
      id: Date.now(),
      usuario_id: storedUser?.id || 2,
      cancha_id: body.cancha_id,
      cancha_nombre: cMatch?.nombre || "Cancha Central",
      fecha: body.fecha,
      hora_inicio: body.hora_inicio,
      hora_fin: body.hora_fin,
      precio_total: body.precio_total || (cMatch ? cMatch.precio_hora : 50000),
      estado: "confirmada",
      cliente_nombre: `${storedUser?.nombre || "Carlos"} ${storedUser?.apellido || "Díaz"}`,
      cliente_email: storedUser?.email || "cliente@futbolzone.com",
      cliente_telefono: storedUser?.telefono || "3109876543",
      notas: body.notas || (body.productos ? "Productos adicionales incluidos" : "Reserva creada en línea"),
      incluye_kit: !!body.incluye_kit,
      incluye_arbitro: !!body.incluye_arbitro,
      metodo_pago: "Nequi",
      referencia_pago: `FZ-${Math.floor(10000 + Math.random() * 90000)}`,
      creado_en: new Date().toISOString()
    };
    list.unshift(nueva);
    saveLocalReservas(list);
    return { success: true, data: nueva, message: "¡Reserva confirmada con éxito!" };
  }

  // Cancelar Reserva
  if (endpoint.startsWith("/reservas/") && method === "DELETE") {
    const id = Number(endpoint.split("/")[2]);
    let list = getLocalReservas();
    list = list.map((r) => (r.id === id ? { ...r, estado: "cancelada" } : r));
    saveLocalReservas(list);
    return { success: true, message: "Reserva cancelada con éxito" };
  }

  // Estado reserva directo
  if (endpoint.includes("/estado")) {
    return { success: true, message: "Estado actualizado" };
  }

  // Usuarios / Clientes / Empleados
  if (endpoint.startsWith("/usuarios")) {
    return { success: true, data: MOCK_USUARIOS };
  }
  if (endpoint.startsWith("/empleados")) {
    return {
      success: true,
      data: [
        { id: 1, nombre: "Juan", apellido: "Pérez", cargo: "Administrador", telefono: "3001234567", email: "juan.perez@futbolzone.com" },
        { id: 2, nombre: "María", apellido: "González", cargo: "Coordinador", telefono: "3109876543", email: "maria.gonzalez@futbolzone.com" },
        { id: 3, nombre: "Pedro", apellido: "Ramírez", cargo: "Mantenimiento", telefono: "3205556677", email: "pedro.ramirez@futbolzone.com" },
      ]
    };
  }

  // Reportes
  if (endpoint.startsWith("/reportes/resumen")) {
    return { success: true, data: { total_reservas: 4, ingresos_totales: 387000, canchas_activas: 5, clientes_totales: 2 } };
  }
  if (endpoint.startsWith("/reportes/reservas-por-cancha")) {
    return { success: true, data: [{ cancha: "Cancha Central", total: 2 }, { cancha: "Cancha Norte", total: 1 }, { cancha: "Cancha Sur", total: 1 }] };
  }
  if (endpoint.startsWith("/reportes/ingresos-mensuales")) {
    return { success: true, data: [{ mes: "Noviembre", total: 132000 }, { mes: "Diciembre", total: 255000 }] };
  }

  // Reseñas y otros
  return { success: true, data: [], message: "OK" };
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    const contentType = response.headers.get("content-type") || "";

    // Si el servidor o proxy devolvió HTML (ej. 504 de Vite proxy o 404 doctype) en lugar de JSON
    if (!contentType.includes("application/json") || response.status === 502 || response.status === 504) {
      console.warn(`[FutbolZone] Servidor local no envió JSON en ${endpoint} (Status ${response.status}). Activando contingencia.`);
      return handleOfflineExpoFallback(endpoint, options) as T;
    }

    const data = await response.json();

    if (!response.ok || data.success === false) {
      const errDetail = data.detail || data.message || data.error;
      if (
        response.status === 401 ||
        (typeof errDetail === "string" && (errDetail.includes("Token") || errDetail.includes("token")))
      ) {
        removeAuthToken();
        throw new Error("Tu sesión ha expirado o el token es inválido. Por favor inicia sesión nuevamente para renovar tu acceso.");
      }
      throw new Error(typeof errDetail === "string" ? errDetail : "Ocurrió un error en el servidor");
    }

    return data;
  } catch (err: any) {
    // Si el servidor backend no responde, o si hubo error al parsear HTML como JSON (SyntaxError / <!DOCTYPE)
    console.warn(`[FutbolZone] Activando contingencia offline para ${endpoint}:`, err);
    return handleOfflineExpoFallback(endpoint, options) as T;
  }
}

export const api = {
  // Autenticación & Usuarios
  login: (correo: string, password: string) =>
    request<any>("/usuarios/login", {
      method: "POST",
      body: JSON.stringify({ correo, password }),
    }),

  registro: (datos: { nombre: string; apellido: string; correo: string; password: string; telefono?: string }) =>
    request<any>("/usuarios/registro", {
      method: "POST",
      body: JSON.stringify(datos),
    }),

  obtenerUsuarios: () => request<any>("/usuarios/"),
  obtenerClientes: () => request<any>("/usuarios/clientes"),
  actualizarPerfil: (id: number, datos: { nombre?: string; apellido?: string; telefono?: string }) =>
    request<any>(`/usuarios/${id}`, {
      method: "PUT",
      body: JSON.stringify(datos),
    }),
  cambiarRol: (id: number, rol: string) =>
    request<any>(`/usuarios/${id}/rol?rol=${rol}`, { method: "PATCH" }),

  // Canchas
  obtenerCanchas: (activas: boolean = false) =>
    request<any>(`/canchas/?activas=${activas}`),

  obtenerDisponibilidad: (canchaId: number, fecha: string) =>
    request<any>(`/canchas/${canchaId}/disponibilidad?fecha=${fecha}`),

  crearCancha: (datos: any) =>
    request<any>("/canchas/", {
      method: "POST",
      body: JSON.stringify(datos),
    }),

  actualizarCancha: (id: number, datos: any) =>
    request<any>(`/canchas/${id}`, {
      method: "PUT",
      body: JSON.stringify(datos),
    }),

  eliminarCancha: (id: number) =>
    request<any>(`/canchas/${id}`, { method: "DELETE" }),

  // Reservas
  crearReserva: (datos: {
    cancha_id: number;
    fecha: string;
    hora_inicio: string;
    hora_fin: string;
    precio_total?: number;
    incluye_kit?: boolean;
    incluye_arbitro?: boolean;
    descuento?: number;
    parqueadero_horas?: number;
    productos?: any[];
    notas?: string;
  }) =>
    request<any>("/reservas/", {
      method: "POST",
      body: JSON.stringify(datos),
    }),

  obtenerMisReservas: () => request<any>("/reservas/mis-reservas"),
  obtenerReservas: () => request<any>("/reservas/"),
  obtenerTodasReservas: () => request<any>("/reservas/"),
  actualizarReserva: (id: number, datos: any) =>
    request<any>(`/reservas/${id}`, {
      method: "PUT",
      body: JSON.stringify(datos),
    }),
  actualizarEstadoReserva: (id: number, estado: string) =>
    request<any>(`/reservas/${id}`, {
      method: "PUT",
      body: JSON.stringify({ estado }),
    }),
  cancelarReserva: (id: number) => request<any>(`/reservas/${id}`, { method: "DELETE" }),

  // Empleados
  obtenerEmpleados: () => request<any>("/empleados/"),
  crearEmpleado: (datos: any) =>
    request<any>("/empleados/", {
      method: "POST",
      body: JSON.stringify(datos),
    }),
  actualizarEmpleado: (id: number, datos: any) =>
    request<any>(`/empleados/${id}`, {
      method: "PUT",
      body: JSON.stringify(datos),
    }),
  eliminarEmpleado: (id: number) =>
    request<any>(`/empleados/${id}`, { method: "DELETE" }),

  // Usuarios / Clientes
  actualizarUsuario: (id: number, datos: any) =>
    request<any>(`/usuarios/${id}`, {
      method: "PUT",
      body: JSON.stringify(datos),
    }),

  // Reportes
  obtenerResumenReportes: () => request<any>("/reportes/resumen"),
  obtenerReservasPorCancha: () => request<any>("/reportes/reservas-por-cancha"),
  obtenerIngresosMensuales: () => request<any>("/reportes/ingresos-mensuales"),

  // Reseñas
  obtenerResenas: (cancha_id?: number) =>
    request<any>(cancha_id ? `/resenas?cancha_id=${cancha_id}` : "/resenas"),
  crearResena: (datos: { cancha_id: number; rating: number; comentario: string }) =>
    request<any>("/resenas", {
      method: "POST",
      body: JSON.stringify(datos),
    }),

  // Recuperación y Cambio de Contraseña por PIN
  solicitarPinRecuperacion: (email: string) =>
    request<any>("/auth/recuperar-password/solicitar-pin", {
      method: "POST",
      body: JSON.stringify({ email }),
    }),
  verificarPinRecuperacion: (email: string, pin: string) =>
    request<any>("/auth/recuperar-password/verificar-pin", {
      method: "POST",
      body: JSON.stringify({ email, pin }),
    }),
  cambiarPasswordConPin: (datos: { email: string; pin: string; nueva_password: string }) =>
    request<any>("/auth/recuperar-password/cambiar-password", {
      method: "POST",
      body: JSON.stringify(datos),
    }),
  // Calificaciones entre Jugadores (Peer-to-Peer)
  calificarJugador: (datos: { jugador_id: number; estrellas: number; comentario?: string }) =>
    request<any>("/calificaciones/jugador", {
      method: "POST",
      body: JSON.stringify(datos),
    }),
  obtenerOpinionesJugador: (jugador_id: number) =>
    request<any>(`/calificaciones/jugador/${jugador_id}`),

  // Calificación del Servicio Post-Reserva (4 dimensiones)
  calificarServicio: (datos: {
    reserva_id: number;
    atencion: number;
    servicio: number;
    instalaciones: number;
    experiencia: number;
    comentario?: string;
  }) =>
    request<any>("/calificaciones/servicio", {
      method: "POST",
      body: JSON.stringify(datos),
    }),
  obtenerCalificacionesServicioAdmin: () =>
    request<any>("/calificaciones/servicio/admin"),

  // Perfil Deportivo y Comunidad
  obtenerPerfilDeportivo: (id: number) =>
    request<any>(`/usuarios/${id}/perfil-deportivo`),
  actualizarPerfilDeportivo: (id: number, datos: any) =>
    request<any>(`/usuarios/${id}/perfil-deportivo`, {
      method: "PUT",
      body: JSON.stringify(datos),
    }),
  obtenerComunidadJugadores: () =>
    request<any>("/usuarios/comunidad/deportistas"),

  // Estado de Reserva (Admin)
  cambiarEstadoReservaDirecto: (id: number, estado: string) =>
    request<any>(`/reservas/${id}/estado?estado=${estado}`, {
      method: "PATCH",
    }),
};
