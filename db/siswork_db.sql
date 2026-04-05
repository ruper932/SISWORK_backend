-- =========================================================
-- SISWORK - Script PostgreSQL desde cero
-- Base limpia en español
-- Ejecutar primero conectado a la base "postgres"
-- =========================================================
-- =========================================================
-- 1) CREAR BASE DE DATOS
-- =========================================================
CREATE DATABASE siswork_db WITH OWNER = postgres ENCODING = 'UTF8' TEMPLATE = template0;
-- =========================================================
-- 2) CONECTARSE A LA NUEVA BASE
-- En psql o pgAdmin Query Tool ejecutar esta línea aparte
-- =========================================================
-- \c siswork_db
-- =========================================================
-- 3) EXTENSIONES
-- =========================================================
CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- =========================================================
-- 4) TIPOS ENUM
-- =========================================================
CREATE TYPE rol_usuario_enum AS ENUM (
    'cliente',
    'profesional',
    'administrador',
    'soporte'
);
CREATE TYPE estado_usuario_enum AS ENUM (
    'activo',
    'suspendido',
    'eliminado',
    'bloqueado'
);
CREATE TYPE sexo_enum AS ENUM (
    'masculino',
    'femenino',
    'otro',
    'prefiero_no_decir'
);
CREATE TYPE estado_verificacion_enum AS ENUM (
    'pendiente',
    'en_revision',
    'aprobado',
    'rechazado'
);
CREATE TYPE nivel_especialidad_enum AS ENUM (
    'basico',
    'intermedio',
    'avanzado',
    'experto'
);
CREATE TYPE tipo_documento_enum AS ENUM (
    'ci',
    'certificado',
    'licencia',
    'antecedente',
    'otro'
);
CREATE TYPE estado_solicitud_enum AS ENUM (
    'abierta',
    'en_proceso',
    'asignada',
    'completada',
    'cancelada'
);
CREATE TYPE estado_postulacion_enum AS ENUM (
    'pendiente',
    'aceptada',
    'rechazada',
    'cancelada'
);
CREATE TYPE canal_contacto_enum AS ENUM (
    'whatsapp',
    'telefono',
    'chat_interno',
    'otro'
);
CREATE TYPE accion_auditoria_enum AS ENUM (
    'login',
    'logout',
    'registro',
    'editar_perfil',
    'crear_solicitud',
    'editar_solicitud',
    'eliminar_solicitud',
    'postular_solicitud',
    'aceptar_postulacion',
    'rechazar_postulacion',
    'calificar_servicio',
    'subir_certificacion',
    'validar_profesional',
    'rechazar_profesional',
    'suspender_usuario',
    'activar_usuario'
);
CREATE TYPE tipo_reporte_enum AS ENUM (
    'usuarios',
    'profesionales',
    'solicitudes',
    'calificaciones',
    'especialidades',
    'validaciones',
    'dashboard'
);
CREATE TYPE dia_semana_enum AS ENUM (
    'lunes',
    'martes',
    'miercoles',
    'jueves',
    'viernes',
    'sabado',
    'domingo'
);
-- =========================================================
-- 5) TABLA: usuarios
-- =========================================================
CREATE TABLE usuarios (
    id_usuario UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    numero_whatsapp VARCHAR(20),
    foto_perfil_url TEXT,
    fecha_nacimiento DATE,
    sexo sexo_enum DEFAULT 'prefiero_no_decir',
    rol rol_usuario_enum NOT NULL DEFAULT 'cliente',
    estado estado_usuario_enum NOT NULL DEFAULT 'activo',
    correo_verificado_en TIMESTAMP,
    ultimo_acceso_en TIMESTAMP,
    intentos_fallidos INTEGER NOT NULL DEFAULT 0,
    token_recuperacion VARCHAR(255),
    token_recuperacion_expira_en TIMESTAMP,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    eliminado_en TIMESTAMP,
    CONSTRAINT chk_usuarios_correo_formato CHECK (position('@' in correo) > 1)
);
-- =========================================================
-- 6) TABLA: direcciones_usuario
-- =========================================================
CREATE TABLE direcciones_usuario (
    id_direccion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    departamento VARCHAR(100) NOT NULL DEFAULT 'La Paz',
    ciudad VARCHAR(100) NOT NULL DEFAULT 'La Paz',
    zona VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    referencia TEXT,
    latitud NUMERIC(10, 7),
    longitud NUMERIC(10, 7),
    es_principal BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX uq_direccion_principal_usuario ON direcciones_usuario(id_usuario)
WHERE es_principal = TRUE;
-- =========================================================
-- 7) TABLA: especialidades
-- =========================================================
CREATE TABLE especialidades (
    id_especialidad UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO especialidades (codigo, nombre, descripcion)
VALUES (
        'plomeria',
        'Plomería',
        'Servicios de plomería y gasfitería'
    ),
    (
        'electricidad',
        'Electricidad',
        'Instalaciones y reparaciones eléctricas'
    ),
    (
        'carpinteria',
        'Carpintería',
        'Trabajos en madera'
    ),
    (
        'albanileria',
        'Albañilería',
        'Obra gruesa y refacciones'
    ),
    (
        'mecanica_automotriz',
        'Mecánica automotriz',
        'Diagnóstico y reparación automotriz'
    ),
    (
        'reparacion_electrodomesticos',
        'Reparación de electrodomésticos',
        'Servicio técnico de electrodomésticos'
    ),
    (
        'pintura',
        'Pintura',
        'Pintado de interiores y exteriores'
    ),
    ('limpieza', 'Limpieza', 'Servicios de limpieza'),
    (
        'jardineria',
        'Jardinería',
        'Mantenimiento de jardines'
    );
-- =========================================================
-- 8) TABLA: perfiles_profesionales
-- =========================================================
CREATE TABLE perfiles_profesionales (
    id_perfil_profesional UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID NOT NULL UNIQUE REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    biografia TEXT,
    anos_experiencia INTEGER NOT NULL DEFAULT 0,
    zona_principal VARCHAR(100) NOT NULL,
    radio_servicio_km NUMERIC(5, 2) DEFAULT 5.00,
    referencia_trabajo TEXT,
    documento_identidad_url TEXT,
    estado_verificacion estado_verificacion_enum NOT NULL DEFAULT 'pendiente',
    verificacion_solicitada_en TIMESTAMP,
    verificacion_resuelta_en TIMESTAMP,
    verificado_por UUID REFERENCES usuarios(id_usuario) ON DELETE
    SET NULL,
        calificacion_promedio NUMERIC(3, 2) NOT NULL DEFAULT 0.00,
        cantidad_calificaciones INTEGER NOT NULL DEFAULT 0,
        cantidad_servicios_completados INTEGER NOT NULL DEFAULT 0,
        disponible_ahora BOOLEAN NOT NULL DEFAULT FALSE,
        contacto_publico_habilitado BOOLEAN NOT NULL DEFAULT TRUE,
        creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT chk_anos_experiencia CHECK (anos_experiencia >= 0),
        CONSTRAINT chk_calificacion_promedio CHECK (
            calificacion_promedio >= 0
            AND calificacion_promedio <= 5
        )
);
-- =========================================================
-- 9) TABLA: especialidades_profesional
-- =========================================================
CREATE TABLE especialidades_profesional (
    id_especialidad_profesional UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_perfil_profesional UUID NOT NULL REFERENCES perfiles_profesionales(id_perfil_profesional) ON DELETE CASCADE,
    id_especialidad UUID NOT NULL REFERENCES especialidades(id_especialidad) ON DELETE RESTRICT,
    nivel nivel_especialidad_enum NOT NULL DEFAULT 'basico',
    anos_experiencia INTEGER NOT NULL DEFAULT 0,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id_perfil_profesional, id_especialidad),
    CONSTRAINT chk_anos_exp_especialidad CHECK (anos_experiencia >= 0)
);
-- =========================================================
-- 10) TABLA: certificaciones
-- =========================================================
CREATE TABLE certificaciones (
    id_certificacion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_perfil_profesional UUID NOT NULL REFERENCES perfiles_profesionales(id_perfil_profesional) ON DELETE CASCADE,
    tipo_documento tipo_documento_enum NOT NULL DEFAULT 'certificado',
    titulo VARCHAR(200) NOT NULL,
    institucion VARCHAR(150),
    ano_emision INTEGER,
    archivo_url TEXT NOT NULL,
    verificada BOOLEAN NOT NULL DEFAULT FALSE,
    verificada_por UUID REFERENCES usuarios(id_usuario) ON DELETE
    SET NULL,
        verificada_en TIMESTAMP,
        creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT chk_ano_emision CHECK (
            ano_emision IS NULL
            OR (
                ano_emision >= 1950
                AND ano_emision <= EXTRACT(
                    YEAR
                    FROM CURRENT_DATE
                ) + 1
            )
        )
);
-- =========================================================
-- 11) TABLA: disponibilidades_profesional
-- =========================================================
CREATE TABLE disponibilidades_profesional (
    id_disponibilidad UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_perfil_profesional UUID NOT NULL REFERENCES perfiles_profesionales(id_perfil_profesional) ON DELETE CASCADE,
    dia_semana dia_semana_enum NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    disponible BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_horario_disponibilidad CHECK (hora_inicio < hora_fin),
    UNIQUE (
        id_perfil_profesional,
        dia_semana,
        hora_inicio,
        hora_fin
    )
);
-- =========================================================
-- 12) TABLA: zonas_profesional
-- =========================================================
CREATE TABLE zonas_profesional (
    id_zona_profesional UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_perfil_profesional UUID NOT NULL REFERENCES perfiles_profesionales(id_perfil_profesional) ON DELETE CASCADE,
    departamento VARCHAR(100) NOT NULL DEFAULT 'La Paz',
    ciudad VARCHAR(100) NOT NULL DEFAULT 'La Paz',
    zona VARCHAR(100) NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (
        id_perfil_profesional,
        departamento,
        ciudad,
        zona
    )
);
-- =========================================================
-- 13) TABLA: solicitudes_servicio
-- =========================================================
CREATE TABLE solicitudes_servicio (
    id_solicitud UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_cliente UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    id_especialidad UUID NOT NULL REFERENCES especialidades(id_especialidad) ON DELETE RESTRICT,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    departamento VARCHAR(100) NOT NULL DEFAULT 'La Paz',
    ciudad VARCHAR(100) NOT NULL DEFAULT 'La Paz',
    zona VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    referencia TEXT,
    fecha_preferida DATE,
    hora_preferida_inicio TIME,
    hora_preferida_fin TIME,
    presupuesto_minimo NUMERIC(10, 2),
    presupuesto_maximo NUMERIC(10, 2),
    estado estado_solicitud_enum NOT NULL DEFAULT 'abierta',
    id_profesional_asignado UUID REFERENCES perfiles_profesionales(id_perfil_profesional) ON DELETE
    SET NULL,
        canal_contacto canal_contacto_enum NOT NULL DEFAULT 'whatsapp',
        activa BOOLEAN NOT NULL DEFAULT TRUE,
        creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        cerrado_en TIMESTAMP,
        CONSTRAINT chk_presupuesto_solicitud CHECK (
            (
                presupuesto_minimo IS NULL
                AND presupuesto_maximo IS NULL
            )
            OR (
                presupuesto_minimo IS NOT NULL
                AND presupuesto_maximo IS NOT NULL
                AND presupuesto_minimo >= 0
                AND presupuesto_maximo >= presupuesto_minimo
            )
        ),
        CONSTRAINT chk_horario_preferido CHECK (
            (
                hora_preferida_inicio IS NULL
                AND hora_preferida_fin IS NULL
            )
            OR (
                hora_preferida_inicio IS NOT NULL
                AND hora_preferida_fin IS NOT NULL
                AND hora_preferida_inicio < hora_preferida_fin
            )
        )
);
-- =========================================================
-- 14) TABLA: postulaciones_solicitud
-- =========================================================
CREATE TABLE postulaciones_solicitud (
    id_postulacion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_solicitud UUID NOT NULL REFERENCES solicitudes_servicio(id_solicitud) ON DELETE CASCADE,
    id_perfil_profesional UUID NOT NULL REFERENCES perfiles_profesionales(id_perfil_profesional) ON DELETE CASCADE,
    mensaje_propuesta TEXT,
    precio_estimado NUMERIC(10, 2),
    estado estado_postulacion_enum NOT NULL DEFAULT 'pendiente',
    postulado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    respondido_en TIMESTAMP,
    cancelado_en TIMESTAMP,
    UNIQUE (id_solicitud, id_perfil_profesional),
    CONSTRAINT chk_precio_estimado CHECK (
        precio_estimado IS NULL
        OR precio_estimado >= 0
    )
);
-- =========================================================
-- 15) TABLA: contactos_solicitud
-- =========================================================
CREATE TABLE contactos_solicitud (
    id_contacto UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_solicitud UUID REFERENCES solicitudes_servicio(id_solicitud) ON DELETE
    SET NULL,
        id_cliente UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
        id_perfil_profesional UUID NOT NULL REFERENCES perfiles_profesionales(id_perfil_profesional) ON DELETE CASCADE,
        canal canal_contacto_enum NOT NULL DEFAULT 'whatsapp',
        contactado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        nota TEXT
);
-- =========================================================
-- 16) TABLA: calificaciones_servicio
-- =========================================================
CREATE TABLE calificaciones_servicio (
    id_calificacion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_solicitud UUID NOT NULL UNIQUE REFERENCES solicitudes_servicio(id_solicitud) ON DELETE CASCADE,
    id_cliente UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    id_perfil_profesional UUID NOT NULL REFERENCES perfiles_profesionales(id_perfil_profesional) ON DELETE RESTRICT,
    puntuacion INTEGER NOT NULL,
    comentario TEXT,
    verificada BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_puntuacion CHECK (
        puntuacion BETWEEN 1 AND 5
    )
);
-- =========================================================
-- 17) TABLA: profesionales_guardados
-- =========================================================
CREATE TABLE profesionales_guardados (
    id_guardado UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_perfil_profesional UUID NOT NULL REFERENCES perfiles_profesionales(id_perfil_profesional) ON DELETE CASCADE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id_usuario, id_perfil_profesional)
);
-- =========================================================
-- 18) TABLA: historial_busquedas
-- =========================================================
CREATE TABLE historial_busquedas (
    id_busqueda UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario UUID REFERENCES usuarios(id_usuario) ON DELETE
    SET NULL,
        termino_busqueda VARCHAR(255),
        id_especialidad UUID REFERENCES especialidades(id_especialidad) ON DELETE
    SET NULL,
        zona VARCHAR(100),
        calificacion_minima NUMERIC(2, 1),
        disponible_ahora BOOLEAN,
        cantidad_resultados INTEGER NOT NULL DEFAULT 0,
        buscado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT chk_calificacion_minima CHECK (
            calificacion_minima IS NULL
            OR (
                calificacion_minima >= 0
                AND calificacion_minima <= 5
            )
        )
);
-- =========================================================
-- 19) TABLA: cola_validacion_profesionales
-- =========================================================
CREATE TABLE cola_validacion_profesionales (
    id_validacion UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_perfil_profesional UUID NOT NULL UNIQUE REFERENCES perfiles_profesionales(id_perfil_profesional) ON DELETE CASCADE,
    solicitado_por UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    asignado_a_soporte UUID REFERENCES usuarios(id_usuario) ON DELETE
    SET NULL,
        estado estado_verificacion_enum NOT NULL DEFAULT 'pendiente',
        enviado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        revision_iniciada_en TIMESTAMP,
        resuelto_en TIMESTAMP,
        motivo_rechazo TEXT,
        tiempo_espera_minutos INTEGER,
        tiempo_revision_minutos INTEGER,
        creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT chk_tiempo_espera CHECK (
            tiempo_espera_minutos IS NULL
            OR tiempo_espera_minutos >= 0
        ),
        CONSTRAINT chk_tiempo_revision CHECK (
            tiempo_revision_minutos IS NULL
            OR tiempo_revision_minutos >= 0
        )
);
-- =========================================================
-- 20) TABLA: reportes_administrativos
-- =========================================================
CREATE TABLE reportes_administrativos (
    id_reporte UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    generado_por UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    tipo_reporte tipo_reporte_enum NOT NULL,
    parametros_json JSONB,
    generado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    archivo_url TEXT
);
-- =========================================================
-- 21) TABLA: registros_auditoria
-- =========================================================
CREATE TABLE registros_auditoria (
    id_registro UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_usuario_actor UUID REFERENCES usuarios(id_usuario) ON DELETE
    SET NULL,
        accion accion_auditoria_enum NOT NULL,
        entidad VARCHAR(100) NOT NULL,
        id_entidad UUID,
        valores_anteriores JSONB,
        valores_nuevos JSONB,
        direccion_ip INET,
        agente_usuario TEXT,
        creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- =========================================================
-- 22) TABLA: notas_administrativas
-- =========================================================
CREATE TABLE notas_administrativas (
    id_nota UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_autor UUID NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    entidad_relacionada VARCHAR(100) NOT NULL,
    id_entidad_relacionada UUID NOT NULL,
    nota TEXT NOT NULL,
    privada BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- =========================================================
-- 23) ÍNDICES
-- =========================================================
CREATE INDEX idx_usuarios_rol ON usuarios(rol);
CREATE INDEX idx_usuarios_estado ON usuarios(estado);
CREATE INDEX idx_usuarios_creado_en ON usuarios(creado_en);
CREATE INDEX idx_direcciones_usuario_id_usuario ON direcciones_usuario(id_usuario);
CREATE INDEX idx_direcciones_usuario_zona ON direcciones_usuario(zona);
CREATE INDEX idx_perfiles_profesionales_id_usuario ON perfiles_profesionales(id_usuario);
CREATE INDEX idx_perfiles_profesionales_estado_verificacion ON perfiles_profesionales(estado_verificacion);
CREATE INDEX idx_perfiles_profesionales_zona_principal ON perfiles_profesionales(zona_principal);
CREATE INDEX idx_perfiles_profesionales_disponible_ahora ON perfiles_profesionales(disponible_ahora);
CREATE INDEX idx_perfiles_profesionales_calificacion_promedio ON perfiles_profesionales(calificacion_promedio);
CREATE INDEX idx_especialidades_profesional_perfil ON especialidades_profesional(id_perfil_profesional);
CREATE INDEX idx_especialidades_profesional_especialidad ON especialidades_profesional(id_especialidad);
CREATE INDEX idx_certificaciones_perfil ON certificaciones(id_perfil_profesional);
CREATE INDEX idx_certificaciones_verificada ON certificaciones(verificada);
CREATE INDEX idx_disponibilidades_perfil ON disponibilidades_profesional(id_perfil_profesional);
CREATE INDEX idx_disponibilidades_dia ON disponibilidades_profesional(dia_semana);
CREATE INDEX idx_zonas_profesional_perfil ON zonas_profesional(id_perfil_profesional);
CREATE INDEX idx_zonas_profesional_zona ON zonas_profesional(zona);
CREATE INDEX idx_solicitudes_cliente ON solicitudes_servicio(id_cliente);
CREATE INDEX idx_solicitudes_especialidad ON solicitudes_servicio(id_especialidad);
CREATE INDEX idx_solicitudes_estado ON solicitudes_servicio(estado);
CREATE INDEX idx_solicitudes_zona ON solicitudes_servicio(zona);
CREATE INDEX idx_solicitudes_creado_en ON solicitudes_servicio(creado_en);
CREATE INDEX idx_solicitudes_profesional_asignado ON solicitudes_servicio(id_profesional_asignado);
CREATE INDEX idx_postulaciones_solicitud ON postulaciones_solicitud(id_solicitud);
CREATE INDEX idx_postulaciones_profesional ON postulaciones_solicitud(id_perfil_profesional);
CREATE INDEX idx_postulaciones_estado ON postulaciones_solicitud(estado);
CREATE INDEX idx_contactos_solicitud ON contactos_solicitud(id_solicitud);
CREATE INDEX idx_contactos_cliente ON contactos_solicitud(id_cliente);
CREATE INDEX idx_contactos_profesional ON contactos_solicitud(id_perfil_profesional);
CREATE INDEX idx_calificaciones_profesional ON calificaciones_servicio(id_perfil_profesional);
CREATE INDEX idx_calificaciones_cliente ON calificaciones_servicio(id_cliente);
CREATE INDEX idx_calificaciones_puntuacion ON calificaciones_servicio(puntuacion);
CREATE INDEX idx_profesionales_guardados_usuario ON profesionales_guardados(id_usuario);
CREATE INDEX idx_profesionales_guardados_profesional ON profesionales_guardados(id_perfil_profesional);
CREATE INDEX idx_historial_busquedas_usuario ON historial_busquedas(id_usuario);
CREATE INDEX idx_historial_busquedas_especialidad ON historial_busquedas(id_especialidad);
CREATE INDEX idx_historial_busquedas_buscado_en ON historial_busquedas(buscado_en);
CREATE INDEX idx_cola_validacion_estado ON cola_validacion_profesionales(estado);
CREATE INDEX idx_cola_validacion_asignado_a_soporte ON cola_validacion_profesionales(asignado_a_soporte);
CREATE INDEX idx_cola_validacion_enviado_en ON cola_validacion_profesionales(enviado_en);
CREATE INDEX idx_reportes_administrativos_generado_por ON reportes_administrativos(generado_por);
CREATE INDEX idx_reportes_administrativos_tipo ON reportes_administrativos(tipo_reporte);
CREATE INDEX idx_registros_auditoria_usuario_actor ON registros_auditoria(id_usuario_actor);
CREATE INDEX idx_registros_auditoria_accion ON registros_auditoria(accion);
CREATE INDEX idx_registros_auditoria_entidad ON registros_auditoria(entidad, id_entidad);
CREATE INDEX idx_registros_auditoria_creado_en ON registros_auditoria(creado_en);
-- =========================================================
-- 24) FUNCIÓN PARA actualizado_en
-- =========================================================
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion() RETURNS TRIGGER AS $$ BEGIN NEW.actualizado_en = CURRENT_TIMESTAMP;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;
-- =========================================================
-- 25) TRIGGERS DE ACTUALIZACIÓN
-- =========================================================
CREATE TRIGGER trg_usuarios_actualizado BEFORE
UPDATE ON usuarios FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();
CREATE TRIGGER trg_direcciones_usuario_actualizado BEFORE
UPDATE ON direcciones_usuario FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();
CREATE TRIGGER trg_perfiles_profesionales_actualizado BEFORE
UPDATE ON perfiles_profesionales FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();
CREATE TRIGGER trg_certificaciones_actualizado BEFORE
UPDATE ON certificaciones FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();
CREATE TRIGGER trg_disponibilidades_profesional_actualizado BEFORE
UPDATE ON disponibilidades_profesional FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();
CREATE TRIGGER trg_solicitudes_servicio_actualizado BEFORE
UPDATE ON solicitudes_servicio FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();
CREATE TRIGGER trg_calificaciones_servicio_actualizado BEFORE
UPDATE ON calificaciones_servicio FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();
CREATE TRIGGER trg_cola_validacion_profesionales_actualizado BEFORE
UPDATE ON cola_validacion_profesionales FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();
-- =========================================================
-- 26) FUNCIÓN: recalcular calificación profesional
-- =========================================================
CREATE OR REPLACE FUNCTION recalcular_calificacion_profesional(p_id_perfil_profesional UUID) RETURNS VOID AS $$ BEGIN
UPDATE perfiles_profesionales
SET calificacion_promedio = COALESCE(
        (
            SELECT ROUND(AVG(puntuacion)::numeric, 2)
            FROM calificaciones_servicio
            WHERE id_perfil_profesional = p_id_perfil_profesional
        ),
        0.00
    ),
    cantidad_calificaciones = (
        SELECT COUNT(*)
        FROM calificaciones_servicio
        WHERE id_perfil_profesional = p_id_perfil_profesional
    )
WHERE id_perfil_profesional = p_id_perfil_profesional;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION trg_recalcular_calificacion_profesional() RETURNS TRIGGER AS $$ BEGIN IF TG_OP = 'DELETE' THEN PERFORM recalcular_calificacion_profesional(OLD.id_perfil_profesional);
RETURN OLD;
ELSE PERFORM recalcular_calificacion_profesional(NEW.id_perfil_profesional);
RETURN NEW;
END IF;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER trg_calificaciones_recalcular_profesional
AFTER
INSERT
    OR
UPDATE
    OR DELETE ON calificaciones_servicio FOR EACH ROW EXECUTE FUNCTION trg_recalcular_calificacion_profesional();
-- =========================================================
-- 27) FUNCIÓN: recalcular servicios completados
-- =========================================================
CREATE OR REPLACE FUNCTION recalcular_servicios_completados(p_id_perfil_profesional UUID) RETURNS VOID AS $$ BEGIN
UPDATE perfiles_profesionales
SET cantidad_servicios_completados = (
        SELECT COUNT(*)
        FROM solicitudes_servicio
        WHERE id_profesional_asignado = p_id_perfil_profesional
            AND estado = 'completada'
    )
WHERE id_perfil_profesional = p_id_perfil_profesional;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION trg_recalcular_servicios_completados() RETURNS TRIGGER AS $$ BEGIN IF TG_OP = 'DELETE' THEN IF OLD.id_profesional_asignado IS NOT NULL THEN PERFORM recalcular_servicios_completados(OLD.id_profesional_asignado);
END IF;
RETURN OLD;
ELSE IF NEW.id_profesional_asignado IS NOT NULL THEN PERFORM recalcular_servicios_completados(NEW.id_profesional_asignado);
END IF;
IF TG_OP = 'UPDATE'
AND OLD.id_profesional_asignado IS NOT NULL
AND OLD.id_profesional_asignado <> NEW.id_profesional_asignado THEN PERFORM recalcular_servicios_completados(OLD.id_profesional_asignado);
END IF;
RETURN NEW;
END IF;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER trg_solicitudes_recalcular_servicios_completados
AFTER
INSERT
    OR
UPDATE
    OR DELETE ON solicitudes_servicio FOR EACH ROW EXECUTE FUNCTION trg_recalcular_servicios_completados();
-- =========================================================
-- 28) VISTA: perfiles públicos
-- =========================================================
CREATE OR REPLACE VIEW vista_perfiles_publicos AS
SELECT pp.id_perfil_profesional,
    u.id_usuario,
    u.nombres,
    u.apellidos,
    CONCAT(u.nombres, ' ', u.apellidos) AS nombre_completo,
    pp.biografia,
    pp.anos_experiencia,
    pp.zona_principal,
    pp.calificacion_promedio,
    pp.cantidad_calificaciones,
    pp.cantidad_servicios_completados,
    pp.disponible_ahora,
    u.telefono,
    u.numero_whatsapp,
    (
        SELECT string_agg(
                e.nombre,
                ', '
                ORDER BY e.nombre
            )
        FROM especialidades_profesional ep
            JOIN especialidades e ON e.id_especialidad = ep.id_especialidad
        WHERE ep.id_perfil_profesional = pp.id_perfil_profesional
    ) AS especialidades,
    pp.estado_verificacion
FROM perfiles_profesionales pp
    JOIN usuarios u ON u.id_usuario = pp.id_usuario
WHERE u.estado = 'activo'
    AND pp.estado_verificacion = 'aprobado'
    AND pp.contacto_publico_habilitado = TRUE;
-- =========================================================
-- 29) VISTA: resumen dashboard admin
-- =========================================================
CREATE OR REPLACE VIEW vista_resumen_dashboard_admin AS
SELECT (
        SELECT COUNT(*)
        FROM usuarios
        WHERE eliminado_en IS NULL
    ) AS total_usuarios,
    (
        SELECT COUNT(*)
        FROM usuarios
        WHERE rol = 'cliente'
            AND eliminado_en IS NULL
    ) AS total_clientes,
    (
        SELECT COUNT(*)
        FROM usuarios
        WHERE rol = 'profesional'
            AND eliminado_en IS NULL
    ) AS total_profesionales,
    (
        SELECT COUNT(*)
        FROM solicitudes_servicio
    ) AS total_solicitudes,
    (
        SELECT COUNT(*)
        FROM solicitudes_servicio
        WHERE estado = 'abierta'
    ) AS solicitudes_abiertas,
    (
        SELECT COUNT(*)
        FROM solicitudes_servicio
        WHERE estado = 'completada'
    ) AS solicitudes_completadas,
    (
        SELECT COUNT(*)
        FROM cola_validacion_profesionales
        WHERE estado IN ('pendiente', 'en_revision')
    ) AS validaciones_pendientes,
    (
        SELECT ROUND(AVG(puntuacion)::numeric, 2)
        FROM calificaciones_servicio
    ) AS calificacion_promedio_plataforma;
-- =========================================================
-- 30) DATOS INICIALES
-- =========================================================
INSERT INTO usuarios (
        nombres,
        apellidos,
        correo,
        contrasena_hash,
        telefono,
        numero_whatsapp,
        rol,
        estado,
        correo_verificado_en
    )
VALUES (
        'Admin',
        'SISWORK',
        'admin@siswork.local',
        crypt('Admin123*', gen_salt('bf')),
        '70000000',
        '70000000',
        'administrador',
        'activo',
        CURRENT_TIMESTAMP
    ),
    (
        'Soporte',
        'SISWORK',
        'soporte@siswork.local',
        crypt('Soporte123*', gen_salt('bf')),
        '71111111',
        '71111111',
        'soporte',
        'activo',
        CURRENT_TIMESTAMP
    );