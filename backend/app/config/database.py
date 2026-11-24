from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

# Ruta absoluta al archivo SQLite en backend/futbolzone.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "futbolzone.db")
DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{DB_PATH}"

is_sqlite = DATABASE_URL.startswith("sqlite")

engine_kwargs = {
    "echo": False,
    "pool_pre_ping": True,
}
if is_sqlite:
    engine_kwargs["connect_args"] = {"check_same_thread": False, "timeout": 30}

engine = create_engine(DATABASE_URL, **engine_kwargs)

# Habilitar claves foráneas, WAL y timeout en SQLite para concurrencia segura (API + VS Code)
if is_sqlite:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA busy_timeout=5000")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    """Verifica que la conexión con la base de datos esté activa."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"[DB Error] Fallo al verificar conexión: {e}")
        return False


def run_migrations():
    """
    Aplica migraciones incrementales seguras sobre la base de datos existente
    sin eliminar ni alterar usuarios, reservas o notificaciones previas.
    """
    if not is_sqlite:
        return

    with engine.begin() as conn:
        cols_usuarios = {
            row[1] for row in conn.execute(text("PRAGMA table_info(usuarios)")).fetchall()
        }

        if "nombre_completo" not in cols_usuarios:
            conn.execute(text("ALTER TABLE usuarios ADD COLUMN nombre_completo VARCHAR(200)"))
            conn.execute(
                text(
                    "UPDATE usuarios "
                    "SET nombre_completo = TRIM(COALESCE(nombre, '') || ' ' || COALESCE(apellido, '')) "
                    "WHERE nombre_completo IS NULL"
                )
            )
            print("[DB Migration] Columna 'nombre_completo' agregada y sincronizada en 'usuarios'.")

        if "uuid" not in cols_usuarios:
            conn.execute(text("ALTER TABLE usuarios ADD COLUMN uuid VARCHAR(36)"))
            sin_uuid = conn.execute(
                text("SELECT id FROM usuarios WHERE uuid IS NULL OR uuid = ''")
            ).fetchall()
            for (uid,) in sin_uuid:
                conn.execute(
                    text("UPDATE usuarios SET uuid = :uuid WHERE id = :id"),
                    {"uuid": str(uuid.uuid4()), "id": uid},
                )
            conn.execute(
                text("CREATE UNIQUE INDEX IF NOT EXISTS ix_usuarios_uuid ON usuarios (uuid)")
            )
            print("[DB Migration] Columna 'uuid' agregada y generada para usuarios existentes.")

        # Asegurar índices en claves foráneas para relaciones usuarios <-> reservas <-> notificaciones
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_reservas_usuario_id ON reservas (usuario_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_reservas_cancha_id ON reservas (cancha_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_notificaciones_usuario_id ON notificaciones (usuario_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_notificaciones_reserva_id ON notificaciones (reserva_id)"))

