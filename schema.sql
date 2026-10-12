-- ============================================================
-- Esquema de base de datos: QuienLoTiene
-- Marketplace inverso (RFQ)
-- PostgreSQL / Supabase
-- ============================================================

-- ------------------------------------------------------------
-- TABLA: usuarios
-- Almacena tanto clientes como proveedores.
-- El campo 'rol' distingue entre ellos.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefono VARCHAR(30),
    whatsapp VARCHAR(30),
    nombre VARCHAR(150) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK(rol IN ('cliente', 'proveedor')),
    fecha_registro TIMESTAMP DEFAULT NOW(),
    activo BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(rol);
CREATE INDEX IF NOT EXISTS idx_usuarios_activo ON usuarios(activo);

-- ------------------------------------------------------------
-- TABLA: categorias
-- Jerarquia autorreferenciada. Ejemplo:
--   Materiales > Ferreteria > Tubos > PVC
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    padre_id INTEGER REFERENCES categorias(id) ON DELETE SET NULL,
    tipo VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_categorias_padre ON categorias(padre_id);

-- ------------------------------------------------------------
-- TABLA: proveedor_categorias
-- Relacion muchos-a-muchos: que categorias ofrece cada proveedor.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS proveedor_categorias (
    proveedor_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    categoria_id INTEGER NOT NULL REFERENCES categorias(id) ON DELETE CASCADE,
    PRIMARY KEY (proveedor_id, categoria_id)
);

CREATE INDEX IF NOT EXISTS idx_provcat_categoria ON proveedor_categorias(categoria_id);

-- ------------------------------------------------------------
-- TABLA: solicitudes
-- Lo que un cliente publica buscando algo.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS solicitudes (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    categoria_id INTEGER NOT NULL REFERENCES categorias(id) ON DELETE RESTRICT,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    ubicacion VARCHAR(200),
    radio_busqueda INTEGER CHECK (radio_busqueda IS NULL OR radio_busqueda > 0),
    estado VARCHAR(50) NOT NULL DEFAULT 'nueva'
        CHECK(estado IN ('nueva', 'con_ofertas', 'asignada', 'finalizada', 'cancelada')),
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solicitudes_cliente ON solicitudes(cliente_id);
CREATE INDEX IF NOT EXISTS idx_solicitudes_categoria ON solicitudes(categoria_id);
CREATE INDEX IF NOT EXISTS idx_solicitudes_estado ON solicitudes(estado);
CREATE INDEX IF NOT EXISTS idx_solicitudes_fecha ON solicitudes(fecha_creacion DESC);

-- ------------------------------------------------------------
-- TABLA: ofertas
-- Respuestas de los proveedores a una solicitud.
-- Un proveedor solo puede ofertar UNA VEZ por solicitud.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ofertas (
    id SERIAL PRIMARY KEY,
    solicitud_id INTEGER NOT NULL REFERENCES solicitudes(id) ON DELETE CASCADE,
    proveedor_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    mensaje TEXT,
    precio DECIMAL(12, 2) CHECK (precio IS NULL OR precio >= 0),
    estado VARCHAR(50) NOT NULL DEFAULT 'pendiente'
        CHECK(estado IN ('pendiente', 'aceptada', 'rechazada', 'retirada')),
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    UNIQUE (solicitud_id, proveedor_id)
);

CREATE INDEX IF NOT EXISTS idx_ofertas_solicitud ON ofertas(solicitud_id);
CREATE INDEX IF NOT EXISTS idx_ofertas_proveedor ON ofertas(proveedor_id);
CREATE INDEX IF NOT EXISTS idx_ofertas_estado ON ofertas(estado);

-- ------------------------------------------------------------
-- TABLA: notificaciones
-- El corazon del sistema RFQ: avisa a proveedores cuando
-- aparece una solicitud que coincide con sus categorias.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS notificaciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    solicitud_id INTEGER NOT NULL REFERENCES solicitudes(id) ON DELETE CASCADE,
    leida BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    UNIQUE (usuario_id, solicitud_id)
);

CREATE INDEX IF NOT EXISTS idx_notif_usuario ON notificaciones(usuario_id);
CREATE INDEX IF NOT EXISTS idx_notif_leida ON notificaciones(usuario_id, leida);