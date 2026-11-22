export interface ProductoCancha {
  id: string;
  nombre: string;
  descripcion: string;
  precio: number;
  categoria: "papas" | "gatorade" | "energizante" | "agua" | "gaseosa" | "snacks" | "combo";
  imagen: string;
}

export interface ProductoSeleccionado extends ProductoCancha {
  cantidad: number;
  momentoEntrega: "inicio" | "fin";
}

// ─────────────────────────────────────────────────────────────
// 1. CANCHA CENTRAL — FÚTBOL 5 (CATÁLOGO BÁSICO)
// Encuentros pequeños (10 jugadores). Opciones rápidas e individuales.
// ─────────────────────────────────────────────────────────────
export const PRODUCTOS_FUTBOL_5: ProductoCancha[] = [
  {
    id: "f5_papas_clasicas",
    nombre: "Papas Fritas Clásicas",
    descripcion: "Paquete individual crujiente con sal marina natural. Ideal para reponer sales tras el partido.",
    precio: 4000,
    categoria: "papas",
    imagen: "https://images.unsplash.com/photo-1566478989037-eec170784d0b?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f5_gatorade_tropical",
    nombre: "Gatorade Frutas Tropicales (500 ml)",
    descripcion: "Bebida isotónica hidratante rica en electrolitos para reponer energía en partidos intensos.",
    precio: 6000,
    categoria: "gatorade",
    imagen: "https://licoresjunior.com/wp-content/uploads/2025/03/licores-jr-8.png",
  },
  {
    id: "f5_agua_manantial",
    nombre: "Agua Mineral Manantial (600 ml)",
    descripcion: "Agua pura de manantial sin gas, ultra fresca para mantener la hidratación en cada tiempo.",
    precio: 3500,
    categoria: "agua",
    imagen: "https://http2.mlstatic.com/D_NQ_NP_918382-MLA112403364748_062026-O.webp",
  },
  {
    id: "f5_gaseosa_personal",
    nombre: "Gaseosa Coca-Cola Original (400 ml)",
    descripcion: "Botella individual helada y gasificada, perfecta para disfrutar en el descanso o tercer tiempo.",
    precio: 4500,
    categoria: "gaseosa",
    imagen: "https://images.unsplash.com/photo-1554866585-cd94860890b7?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f5_redbull_clasico",
    nombre: "Bebida Energizante Red Bull (250 ml)",
    descripcion: "Lata clásica con taurina y cafeína para máxima concentración y explosión física.",
    precio: 9000,
    categoria: "energizante",
    imagen: "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?auto=format&fit=crop&w=320&q=80",
  },
];

// ─────────────────────────────────────────────────────────────
// 2. CANCHA NORTE — FÚTBOL 7 (CATÁLOGO MÁS COMPLETO Y VARIADO)
// Encuentros medianos (14 jugadores). Más variedad de sabores, snacks y combos.
// ─────────────────────────────────────────────────────────────
export const PRODUCTOS_FUTBOL_7: ProductoCancha[] = [
  {
    id: "f7_papas_rizadas",
    nombre: "Papas Rizadas Mayonesa & Limón",
    descripcion: "Papas onduladas ultra crujientes con toque de limón. El snack preferido por los jugadores.",
    precio: 4500,
    categoria: "papas",
    imagen: "https://images.unsplash.com/photo-1621447504864-d8686e12698c?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f7_platanitos_maduritos",
    nombre: "Plátanos Maduritos Tostados",
    descripcion: "Crocantes chips de plátano maduro con dulce natural para aporte de carbohidratos.",
    precio: 4000,
    categoria: "snacks",
    imagen: "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f7_gatorade_mandarina",
    nombre: "Gatorade Naranja Mandarina (500 ml)",
    descripcion: "Sabor cítrico revitalizante de rápida asimilación estomacal durante el desgaste atlético.",
    precio: 6000,
    categoria: "gatorade",
    imagen: "https://licoresjunior.com/wp-content/uploads/2025/03/licores-jr-8.png",
  },
  {
    id: "f7_gatorade_coolblue",
    nombre: "Gatorade Cool Blue Mora Azul (500 ml)",
    descripcion: "Fórmula hidratante avanzada sabor moras silvestres, bien helada desde la nevera deportiva.",
    precio: 6000,
    categoria: "gatorade",
    imagen: "https://licoresjunior.com/wp-content/uploads/2025/03/licores-jr-8.png",
  },
  {
    id: "f7_monster_energy",
    nombre: "Bebida Energizante Monster Energy (473 ml)",
    descripcion: "Lata grande con potente mezcla energética para sostener el ritmo en los dos tiempos de juego.",
    precio: 11000,
    categoria: "energizante",
    imagen: "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f7_redbull_clasico",
    nombre: "Bebida Energizante Red Bull (250 ml)",
    descripcion: "Energía revitalizante premium para momentos clave y jugadas de velocidad.",
    precio: 9000,
    categoria: "energizante",
    imagen: "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f7_postobon_manzana",
    nombre: "Gaseosa Postobón Manzana (400 ml)",
    descripcion: "Tradicional bebida colombiana de manzana, helada y burbujeante.",
    precio: 4000,
    categoria: "gaseosa",
    imagen: "https://images.unsplash.com/photo-1554866585-cd94860890b7?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f7_cocacola_zero",
    nombre: "Gaseosa Coca-Cola Sin Azúcar (400 ml)",
    descripcion: "Refresco helado con todo el sabor clásico y cero calorías para deportistas.",
    precio: 4500,
    categoria: "gaseosa",
    imagen: "https://images.unsplash.com/photo-1554866585-cd94860890b7?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f7_agua_cristal",
    nombre: "Agua Mineral Manantial Fría (600 ml)",
    descripcion: "Pureza garantizada en botella ergonómica deportiva antigoteo.",
    precio: 3500,
    categoria: "agua",
    imagen: "https://http2.mlstatic.com/D_NQ_NP_918382-MLA112403364748_062026-O.webp",
  },
  {
    id: "f7_mix_frutos_secos",
    nombre: "Mix de Frutos Secos & Maní Deportivo (120 g)",
    descripcion: "Combinación de maní tostado, almendras y uvas pasas para recuperación de glucógeno.",
    precio: 5500,
    categoria: "snacks",
    imagen: "https://images.unsplash.com/photo-1599599810769-bcde5a160d32?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f7_combo_equipo",
    nombre: "Combo F7: 4 Gatorades + 2 Snacks a Elección",
    descripcion: "Paquete de ahorro especial para el medio tiempo o cierre del partido del equipo.",
    precio: 28000,
    categoria: "combo",
    imagen: "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?auto=format&fit=crop&w=320&q=80",
  },
];

// ─────────────────────────────────────────────────────────────
// 3. CANCHA SUR — FÚTBOL 11 (CATÁLOGO MÁS AMPLIO Y AVANZADO)
// Encuentros grandes (22 jugadores) y torneos. Packs familiares, cajas grupales y promos.
// ─────────────────────────────────────────────────────────────
export const PRODUCTOS_FUTBOL_11: ProductoCancha[] = [
  {
    id: "f11_papas_mega_familiar",
    nombre: "Papas Fritas Mega Pack Familiar (250 g)",
    descripcion: "Paquete extra grande para compartir con todo el plantel en el vestuario o gradería.",
    precio: 12000,
    categoria: "papas",
    imagen: "https://images.unsplash.com/photo-1566478989037-eec170784d0b?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f11_papas_bbq_queso",
    nombre: "Papas Onduladas BBQ & Queso Cheddar (150 g)",
    descripcion: "Paquete mediano con intenso sabor ahumado y queso para botanear en grupo.",
    precio: 7000,
    categoria: "papas",
    imagen: "https://images.unsplash.com/photo-1621447504864-d8686e12698c?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f11_platanos_pack_xl",
    nombre: "Plátanos Tostaditos Pack XL Surtido",
    descripcion: "Crocantes chips de plátano verde con sal y maduritos en empaque colectivo.",
    precio: 8500,
    categoria: "snacks",
    imagen: "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f11_gatorade_frutos",
    nombre: "Gatorade Frutos Tropicales (500 ml)",
    descripcion: "Bebida isotónica clásica con iones de sodio y potasio para 90 minutos de juego.",
    precio: 6000,
    categoria: "gatorade",
    imagen: "https://licoresjunior.com/wp-content/uploads/2025/03/licores-jr-8.png",
  },
  {
    id: "f11_gatorade_bluefrost",
    nombre: "Gatorade Frost Glaciar Freeze (500 ml)",
    descripcion: "Fórmula de frescura ártica para alto rendimiento en cancha completa reglamentaria.",
    precio: 6000,
    categoria: "gatorade",
    imagen: "https://licoresjunior.com/wp-content/uploads/2025/03/licores-jr-8.png",
  },
  {
    id: "f11_gatorade_manzana",
    nombre: "Gatorade Manzana Verde Ice (500 ml)",
    descripcion: "Hidratante deportivo sabor manzana crujiente para calmar la sed más exigente.",
    precio: 6000,
    categoria: "gatorade",
    imagen: "https://licoresjunior.com/wp-content/uploads/2025/03/licores-jr-8.png",
  },
  {
    id: "f11_pack_once_titular",
    nombre: "Pack Hidratación Equipo (11 Gatorades Surtidos)",
    descripcion: "Pack completo de 11 botellas de Gatorade heladas para el once titular del equipo.",
    precio: 58000,
    categoria: "combo",
    imagen: "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f11_monster_ultra",
    nombre: "Bebida Energizante Monster Energy Ultra White (473 ml)",
    descripcion: "Lata grande cero azúcar con sabor cítrico ligero y toda la potencia de Monster.",
    precio: 11500,
    categoria: "energizante",
    imagen: "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f11_redbull_yellow",
    nombre: "Bebida Energizante Red Bull Tropical Edition (250 ml)",
    descripcion: "Edición tropical con sabor a maracuyá y frutas de verano para energía inmediata.",
    precio: 9500,
    categoria: "energizante",
    imagen: "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f11_caja_aguas_plantel",
    nombre: "Caja de Hidratación Manantial (12 Aguas x 600 ml)",
    descripcion: "Caja sellada de 12 botellas de agua pura bien frías para todo el grupo de 22 jugadores.",
    precio: 36000,
    categoria: "agua",
    imagen: "https://http2.mlstatic.com/D_NQ_NP_918382-MLA112403364748_062026-O.webp",
  },
  {
    id: "f11_cocacola_familiar",
    nombre: "Gaseosa Coca-Cola Familiar (1.5 Litros)",
    descripcion: "Botella familiar helada con vasos desechables incluidos para compartir con el equipo.",
    precio: 8500,
    categoria: "gaseosa",
    imagen: "https://images.unsplash.com/photo-1554866585-cd94860890b7?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f11_colombiana_familiar",
    nombre: "Gaseosa Postobón Colombiana Familiar (1.5 Litros)",
    descripcion: "El sabor inconfundible de nuestra tierra en presentación grande para el tercer tiempo.",
    precio: 8000,
    categoria: "gaseosa",
    imagen: "https://images.unsplash.com/photo-1554866585-cd94860890b7?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f11_super_combo_f11",
    nombre: "Super Combo F11: 10 Gatorades + 3 Snacks Grandes",
    descripcion: "La promoción definitiva para partidos oficiales de Fútbol 11. Máximo ahorro por volumen.",
    precio: 75000,
    categoria: "combo",
    imagen: "https://images.unsplash.com/photo-1579758629938-03607ccdbaba?auto=format&fit=crop&w=320&q=80",
  },
  {
    id: "f11_barras_proteina",
    nombre: "Caja de Barras de Proteína & Cereal (6 Unidades)",
    descripcion: "Barras proteicas con avena y chocolate para antes del partido o recuperación post-partido.",
    precio: 18000,
    categoria: "snacks",
    imagen: "https://images.unsplash.com/photo-1622467899862-c45c23ffdeda?auto=format&fit=crop&w=320&q=80",
  },
];

/**
 * Función que retorna el catálogo exclusivo correspondiente al tipo de cancha.
 * Si es Fútbol 5 -> PRODUCTOS_FUTBOL_5
 * Si es Fútbol 7 -> PRODUCTOS_FUTBOL_7
 * Si es Fútbol 11 -> PRODUCTOS_FUTBOL_11
 */
export function obtenerCatalogoPorCancha(cancha: any): {
  tipoModalidad: "Fútbol 5" | "Fútbol 7" | "Fútbol 11";
  productos: ProductoCancha[];
  subtitulo: string;
} {
  const nombre = (cancha?.nombre || "").toLowerCase();
  const tipo = (cancha?.tipo || "").toLowerCase();

  if (nombre.includes("sur") || tipo.includes("11")) {
    return {
      tipoModalidad: "Fútbol 11",
      productos: PRODUCTOS_FUTBOL_11,
      subtitulo: "Catálogo Avanzado & Packs Grupales para Cancha Sur (Fútbol 11)",
    };
  }

  if (nombre.includes("norte") || tipo.includes("7")) {
    return {
      tipoModalidad: "Fútbol 7",
      productos: PRODUCTOS_FUTBOL_7,
      subtitulo: "Catálogo Completo & Snacks Variados para Cancha Norte (Fútbol 7)",
    };
  }

  // Por defecto Cancha Central o Fútbol 5
  return {
    tipoModalidad: "Fútbol 5",
    productos: PRODUCTOS_FUTBOL_5,
    subtitulo: "Catálogo Básico & Hidratación Esencial para Cancha Central (Fútbol 5)",
  };
}
