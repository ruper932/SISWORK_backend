"""seed initial demo data es schema

Revision ID: 9f2d7d6c1b2a
Revises: 8bc478457236
Create Date: 2026-05-08 16:16:00
"""

from alembic import op

revision = "9f2d7d6c1b2a"
down_revision = "8bc478457236"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    INSERT INTO public.usuarios (
        idusuario, nombres, apellidos, correo, contrasenahash,
        telefono, numerowhatsapp, fotoperfilurl, fechanacimiento, sexo,
        rol, estado, correoverificadoen, ultimoaccesoen, intentosfallidos,
        tokenrecuperacion, tokenrecuperacionexpiraen, creadoen, actualizadoen, eliminadoen
    ) VALUES
        (
            '11111111-1111-4111-8111-111111111111',
            'Admin', 'SISWORK', 'admin@siswork.local',
            crypt('Admin123*', gen_salt('bf')),
            '70000000', '70000000', NULL, '1990-01-15', 'masculino',
            'administrador', 'activo', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0,
            NULL, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL
        ),
        (
            '22222222-2222-4222-8222-222222222222',
            'Soporte', 'SISWORK', 'soporte@siswork.local',
            crypt('Soporte123*', gen_salt('bf')),
            '71111111', '71111111', NULL, '1992-03-20', 'femenino',
            'soporte', 'activo', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0,
            NULL, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL
        ),
        (
            '33333333-3333-4333-8333-333333333333',
            'Carlos', 'Mamani', 'carlos@siswork.local',
            crypt('Carlos123*', gen_salt('bf')),
            '73000001', '73000001', NULL, '1995-06-10', 'masculino',
            'cliente', 'activo', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0,
            NULL, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL
        ),
        (
            '44444444-4444-4444-8444-444444444444',
            'Lucia', 'Quispe', 'lucia@siswork.local',
            crypt('Lucia123*', gen_salt('bf')),
            '73000002', '73000002', NULL, '1998-11-02', 'femenino',
            'cliente', 'activo', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0,
            NULL, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL
        ),
        (
            '55555555-5555-4555-8555-555555555555',
            'Juan', 'Perez', 'juan.pro@siswork.local',
            crypt('Juan123*', gen_salt('bf')),
            '72000001', '72000001', NULL, '1989-04-14', 'masculino',
            'profesional', 'activo', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0,
            NULL, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL
        ),
        (
            '66666666-6666-4666-8666-666666666666',
            'Maria', 'Choque', 'maria.pro@siswork.local',
            crypt('Maria123*', gen_salt('bf')),
            '72000002', '72000002', NULL, '1991-09-08', 'femenino',
            'profesional', 'activo', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0,
            NULL, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL
        )
    ON CONFLICT (correo) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.especialidades (
        idespecialidad, codigo, nombre, descripcion, activo, creadoen
    ) VALUES
        (
            'fcb9b58d-f534-4c2a-94ff-571f8bce5d89',
            'plomeria', 'Plomería', 'Servicios de plomería y gasfitería', TRUE, CURRENT_TIMESTAMP
        ),
        (
            'b04795d9-9629-41c6-86e6-b1428f91bb02',
            'electricidad', 'Electricidad', 'Instalaciones y reparaciones eléctricas', TRUE, CURRENT_TIMESTAMP
        ),
        (
            '728067a4-f1b7-4df6-bd47-aa69b9342a10',
            'carpinteria', 'Carpintería', 'Trabajos en madera y melamina', TRUE, CURRENT_TIMESTAMP
        ),
        (
            '867ff2ad-f28d-4f23-ab0d-02507be5e882',
            'pintura', 'Pintura', 'Pintado de interiores y exteriores', TRUE, CURRENT_TIMESTAMP
        ),
        (
            'df3529df-2c23-477e-8404-0792f7d45744',
            'limpieza', 'Limpieza', 'Servicios de limpieza general', TRUE, CURRENT_TIMESTAMP
        ),
        (
            '412ba633-23fd-4e80-985e-61c622c6cb52',
            'jardineria', 'Jardinería', 'Mantenimiento de jardines', TRUE, CURRENT_TIMESTAMP
        )
    ON CONFLICT (codigo) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.perfilesprofesionales (
        idperfilprofesional, idusuario, biografia, anosexperiencia, zonaprincipal,
        radioserviciokm, referenciatrabajo, documentoidentidadurl, estadoverificacion,
        verificacionsolicitadaen, verificacionresueltaen, verificadopor,
        calificacionpromedio, cantidadcalificaciones, cantidadservicioscompletados,
        disponibleahora, contactopublicohabilitado, creadoen, actualizadoen
    ) VALUES
        (
            '77777777-7777-4777-8777-777777777777',
            '55555555-5555-4555-8555-555555555555',
            'Especialista en plomería domiciliaria, fugas, grifería y mantenimiento general.',
            8, 'Sopocachi', 7.50,
            'Atención rápida en La Paz y alrededores.', NULL, 'aprobado',
            CURRENT_TIMESTAMP - INTERVAL '20 days',
            CURRENT_TIMESTAMP - INTERVAL '15 days',
            '11111111-1111-4111-8111-111111111111',
            4.70, 1, 1, TRUE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        ),
        (
            '88888888-8888-4888-8888-888888888888',
            '66666666-6666-4666-8666-666666666666',
            'Electricista para instalaciones residenciales, luminarias y mantenimiento preventivo.',
            6, 'Miraflores', 6.00,
            'Experiencia en hogares y pequeños negocios.', NULL, 'pendiente',
            CURRENT_TIMESTAMP - INTERVAL '5 days',
            NULL,
            NULL,
            0.00, 0, 0, TRUE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        )
    ON CONFLICT (idusuario) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.especialidadesprofesional (
        idespecialidadprofesional, idperfilprofesional, idespecialidad, nivel, anosexperiencia, creadoen
    ) VALUES
        (
            '99999999-9999-4999-8999-999999999991',
            '77777777-7777-4777-8777-777777777777',
            'fcb9b58d-f534-4c2a-94ff-571f8bce5d89',
            'experto', 8, CURRENT_TIMESTAMP
        ),
        (
            '99999999-9999-4999-8999-999999999992',
            '88888888-8888-4888-8888-888888888888',
            'b04795d9-9629-41c6-86e6-b1428f91bb02',
            'avanzado', 6, CURRENT_TIMESTAMP
        )
    ON CONFLICT (idperfilprofesional, idespecialidad) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.zonasprofesional (
        idzonaprofesional, idperfilprofesional, departamento, ciudad, zona, creadoen
    ) VALUES
        (
            'aaaaaaa1-aaaa-4aaa-8aaa-aaaaaaaaaaa1',
            '77777777-7777-4777-8777-777777777777',
            'La Paz', 'La Paz', 'Sopocachi', CURRENT_TIMESTAMP
        ),
        (
            'aaaaaaa2-aaaa-4aaa-8aaa-aaaaaaaaaaa2',
            '77777777-7777-4777-8777-777777777777',
            'La Paz', 'La Paz', 'San Pedro', CURRENT_TIMESTAMP
        ),
        (
            'aaaaaaa3-aaaa-4aaa-8aaa-aaaaaaaaaaa3',
            '88888888-8888-4888-8888-888888888888',
            'La Paz', 'La Paz', 'Miraflores', CURRENT_TIMESTAMP
        )
    ON CONFLICT (idperfilprofesional, departamento, ciudad, zona) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.disponibilidadesprofesional (
        iddisponibilidad, idperfilprofesional, diasemana, horainicio, horafin,
        disponible, creadoen, actualizadoen
    ) VALUES
        (
            'bbbbbbb1-bbbb-4bbb-8bbb-bbbbbbbbbbb1',
            '77777777-7777-4777-8777-777777777777',
            'lunes', '08:00', '12:00', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        ),
        (
            'bbbbbbb2-bbbb-4bbb-8bbb-bbbbbbbbbbb2',
            '77777777-7777-4777-8777-777777777777',
            'miercoles', '14:00', '18:00', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        ),
        (
            'bbbbbbb3-bbbb-4bbb-8bbb-bbbbbbbbbbb3',
            '88888888-8888-4888-8888-888888888888',
            'martes', '09:00', '13:00', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        )
    ON CONFLICT (idperfilprofesional, diasemana, horainicio, horafin) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.direccionesusuario (
        iddireccion, idusuario, departamento, ciudad, zona, direccion, referencia,
        latitud, longitud, esprincipal, creadoen, actualizadoen
    ) VALUES
        (
            'ccccccc1-cccc-4ccc-8ccc-ccccccccccc1',
            '33333333-3333-4333-8333-333333333333',
            'La Paz', 'La Paz', 'Obrajes',
            'Av. Costanera #123', 'Frente a la plaza',
            -16.5335000, -68.0873000, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        ),
        (
            'ccccccc2-cccc-4ccc-8ccc-ccccccccccc2',
            '44444444-4444-4444-8444-444444444444',
            'La Paz', 'La Paz', 'Calacoto',
            'Calle 21 #45', 'Cerca de la iglesia',
            -16.5398000, -68.0779000, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        )
    ON CONFLICT (iddireccion) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.solicitudesservicio (
        idsolicitud, idcliente, idespecialidad, titulo, descripcion, departamento, ciudad, zona,
        direccion, referencia, fechapreferida, horapreferidainicio, horapreferidafin,
        presupuestominimo, presupuestomaximo, estado, idprofesionalasignado,
        canalcontacto, activa, creadoen, actualizadoen, cerradoen
    ) VALUES
        (
            'ddddddd1-dddd-4ddd-8ddd-ddddddddddd1',
            '33333333-3333-4333-8333-333333333333',
            'fcb9b58d-f534-4c2a-94ff-571f8bce5d89',
            'Reparación de fuga en cocina',
            'Existe fuga debajo del lavaplatos y se requiere revisión urgente.',
            'La Paz', 'La Paz', 'Obrajes',
            'Av. Costanera #123', 'Edificio azul',
            CURRENT_DATE + 1, '09:00', '11:00',
            80.00, 150.00, 'completada',
            '77777777-7777-4777-8777-777777777777',
            'whatsapp', TRUE,
            CURRENT_TIMESTAMP - INTERVAL '10 days',
            CURRENT_TIMESTAMP - INTERVAL '3 days',
            CURRENT_TIMESTAMP - INTERVAL '3 days'
        ),
        (
            'ddddddd2-dddd-4ddd-8ddd-ddddddddddd2',
            '44444444-4444-4444-8444-444444444444',
            'b04795d9-9629-41c6-86e6-b1428f91bb02',
            'Instalación de lámparas LED',
            'Necesito instalar 4 lámparas LED en sala y pasillo.',
            'La Paz', 'La Paz', 'Calacoto',
            'Calle 21 #45', 'Timbre 2B',
            CURRENT_DATE + 2, '15:00', '18:00',
            120.00, 220.00, 'abierta',
            NULL,
            'telefono', TRUE,
            CURRENT_TIMESTAMP - INTERVAL '2 days',
            CURRENT_TIMESTAMP - INTERVAL '2 days',
            NULL
        ),
        (
            'ddddddd3-dddd-4ddd-8ddd-ddddddddddd3',
            '33333333-3333-4333-8333-333333333333',
            '867ff2ad-f28d-4f23-ab0d-02507be5e882',
            'Pintado de dormitorio',
            'Se requiere lijado, sellado y pintado de paredes internas.',
            'La Paz', 'La Paz', 'San Miguel',
            NULL, 'Casa color crema',
            CURRENT_DATE + 4, '08:30', '12:30',
            300.00, 500.00, 'abierta',
            NULL,
            'chatinterno', TRUE,
            CURRENT_TIMESTAMP - INTERVAL '1 day',
            CURRENT_TIMESTAMP - INTERVAL '1 day',
            NULL
        )
    ON CONFLICT (idsolicitud) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.postulacionessolicitud (
        idpostulacion, idsolicitud, idperfilprofesional, mensajepropuesta,
        precioestimado, estado, postuladoen, respondidoen, canceladoen
    ) VALUES
        (
            'eeeeeee1-eeee-4eee-8eee-eeeeeeeeeee1',
            'ddddddd2-dddd-4ddd-8ddd-ddddddddddd2',
            '88888888-8888-4888-8888-888888888888',
            'Puedo realizar la instalación completa con materiales básicos incluidos.',
            180.00, 'pendiente',
            CURRENT_TIMESTAMP - INTERVAL '1 day', NULL, NULL
        ),
        (
            'eeeeeee2-eeee-4eee-8eee-eeeeeeeeeee2',
            'ddddddd3-dddd-4ddd-8ddd-ddddddddddd3',
            '77777777-7777-4777-8777-777777777777',
            'Puedo coordinar el trabajo con apoyo técnico y supervisar el servicio.',
            420.00, 'pendiente',
            CURRENT_TIMESTAMP - INTERVAL '12 hours', NULL, NULL
        )
    ON CONFLICT (idsolicitud, idperfilprofesional) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.contactossolicitud (
        idcontacto, idsolicitud, idcliente, idperfilprofesional, canal, contactadoen, nota
    ) VALUES
        (
            'fffffff1-ffff-4fff-8fff-fffffffffff1',
            'ddddddd1-dddd-4ddd-8ddd-ddddddddddd1',
            '33333333-3333-4333-8333-333333333333',
            '77777777-7777-4777-8777-777777777777',
            'whatsapp',
            CURRENT_TIMESTAMP - INTERVAL '9 days',
            'Primer contacto para coordinar visita técnica.'
        )
    ON CONFLICT (idcontacto) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.calificacionesservicio (
        idcalificacion, idsolicitud, idcliente, idperfilprofesional,
        puntuacion, comentario, verificada, creadoen, actualizadoen
    ) VALUES
        (
            'abababa1-abab-4aba-8aba-abababababa1',
            'ddddddd1-dddd-4ddd-8ddd-ddddddddddd1',
            '33333333-3333-4333-8333-333333333333',
            '77777777-7777-4777-8777-777777777777',
            5, 'Trabajo rápido, puntual y bien ejecutado.',
            TRUE,
            CURRENT_TIMESTAMP - INTERVAL '2 days',
            CURRENT_TIMESTAMP - INTERVAL '2 days'
        )
    ON CONFLICT (idsolicitud) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.profesionalesguardados (
        idguardado, idusuario, idperfilprofesional, creadoen
    ) VALUES
        (
            'cdcdcdc1-cdcd-4cdc-8cdc-cdcdcdcdcdc1',
            '44444444-4444-4444-8444-444444444444',
            '77777777-7777-4777-8777-777777777777',
            CURRENT_TIMESTAMP - INTERVAL '1 day'
        )
    ON CONFLICT (idusuario, idperfilprofesional) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.historialbusquedas (
        idbusqueda, idusuario, terminobusqueda, idespecialidad, zona,
        calificacionminima, disponibleahora, cantidadresultados, buscadoen
    ) VALUES
        (
            'dededede-dede-4ded-8ded-dededededed1',
            '44444444-4444-4444-8444-444444444444',
            'electricista calacoto',
            'b04795d9-9629-41c6-86e6-b1428f91bb02',
            'Calacoto',
            4.0, TRUE, 1,
            CURRENT_TIMESTAMP - INTERVAL '6 hours'
        )
    ON CONFLICT (idbusqueda) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.colavalidacionprofesionales (
        idvalidacion, idperfilprofesional, solicitadopor, asignadoasoporte, estado,
        enviadoen, revisioniniciadaen, resueltoen, motivorechazo,
        tiempoesperaminutos, tiemporevisionminutos, creadoen, actualizadoen
    ) VALUES
        (
            'efefefef-efef-4efe-8efe-efefefefefe1',
            '88888888-8888-4888-8888-888888888888',
            '66666666-6666-4666-8666-666666666666',
            '22222222-2222-4222-8222-222222222222',
            'enrevision',
            CURRENT_TIMESTAMP - INTERVAL '5 days',
            CURRENT_TIMESTAMP - INTERVAL '2 days',
            NULL, NULL,
            120, 45,
            CURRENT_TIMESTAMP - INTERVAL '5 days',
            CURRENT_TIMESTAMP - INTERVAL '2 days'
        )
    ON CONFLICT (idperfilprofesional) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.notasadministrativas (
        idnota, idautor, entidadrelacionada, identidadrelacionada, nota, privada, creadoen
    ) VALUES
        (
            'f1f1f1f1-f1f1-4f11-8f11-f1f1f1f1f1f1',
            '22222222-2222-4222-8222-222222222222',
            'perfilprofesional',
            '88888888-8888-4888-8888-888888888888',
            'Perfil en revisión por validación de documento de identidad.',
            TRUE,
            CURRENT_TIMESTAMP - INTERVAL '1 day'
        )
    ON CONFLICT (idnota) DO NOTHING;
    """)

    op.execute("""
    INSERT INTO public.reportesadministrativos (
        idreporte, generadopor, tiporeporte, parametrosjson, generadoen, archivourl
    ) VALUES
        (
            'a1a1a1a1-a1a1-4a11-8a11-a1a1a1a1a1a1',
            '11111111-1111-4111-8111-111111111111',
            'dashboard',
            '{"scope":"seed","generated_for":"demo"}'::jsonb,
            CURRENT_TIMESTAMP - INTERVAL '1 hour',
            'https://example.com/reportes/dashboard-demo.pdf'
        )
    ON CONFLICT (idreporte) DO NOTHING;
    """)


def downgrade() -> None:
    op.execute("DELETE FROM public.reportesadministrativos WHERE idreporte = 'a1a1a1a1-a1a1-4a11-8a11-a1a1a1a1a1a1';")
    op.execute("DELETE FROM public.notasadministrativas WHERE idnota = 'f1f1f1f1-f1f1-4f11-8f11-f1f1f1f1f1f1';")
    op.execute("DELETE FROM public.colavalidacionprofesionales WHERE idvalidacion = 'efefefef-efef-4efe-8efe-efefefefefe1';")
    op.execute("DELETE FROM public.historialbusquedas WHERE idbusqueda = 'dededede-dede-4ded-8ded-dededededed1';")
    op.execute("DELETE FROM public.profesionalesguardados WHERE idguardado = 'cdcdcdc1-cdcd-4cdc-8cdc-cdcdcdcdcdc1';")
    op.execute("DELETE FROM public.calificacionesservicio WHERE idcalificacion = 'abababa1-abab-4aba-8aba-abababababa1';")
    op.execute("DELETE FROM public.contactossolicitud WHERE idcontacto = 'fffffff1-ffff-4fff-8fff-fffffffffff1';")
    op.execute("DELETE FROM public.postulacionessolicitud WHERE idpostulacion IN ('eeeeeee1-eeee-4eee-8eee-eeeeeeeeeee1', 'eeeeeee2-eeee-4eee-8eee-eeeeeeeeeee2');")
    op.execute("DELETE FROM public.solicitudesservicio WHERE idsolicitud IN ('ddddddd1-dddd-4ddd-8ddd-ddddddddddd1', 'ddddddd2-dddd-4ddd-8ddd-ddddddddddd2', 'ddddddd3-dddd-4ddd-8ddd-ddddddddddd3');")
    op.execute("DELETE FROM public.direccionesusuario WHERE iddireccion IN ('ccccccc1-cccc-4ccc-8ccc-ccccccccccc1', 'ccccccc2-cccc-4ccc-8ccc-ccccccccccc2');")
    op.execute("DELETE FROM public.disponibilidadesprofesional WHERE iddisponibilidad IN ('bbbbbbb1-bbbb-4bbb-8bbb-bbbbbbbbbbb1', 'bbbbbbb2-bbbb-4bbb-8bbb-bbbbbbbbbbb2', 'bbbbbbb3-bbbb-4bbb-8bbb-bbbbbbbbbbb3');")
    op.execute("DELETE FROM public.zonasprofesional WHERE idzonaprofesional IN ('aaaaaaa1-aaaa-4aaa-8aaa-aaaaaaaaaaa1', 'aaaaaaa2-aaaa-4aaa-8aaa-aaaaaaaaaaa2', 'aaaaaaa3-aaaa-4aaa-8aaa-aaaaaaaaaaa3');")
    op.execute("DELETE FROM public.especialidadesprofesional WHERE idespecialidadprofesional IN ('99999999-9999-4999-8999-999999999991', '99999999-9999-4999-8999-999999999992');")
    op.execute("DELETE FROM public.perfilesprofesionales WHERE idperfilprofesional IN ('77777777-7777-4777-8777-777777777777', '88888888-8888-4888-8888-888888888888');")
    op.execute("DELETE FROM public.especialidades WHERE codigo IN ('plomeria', 'electricidad', 'carpinteria', 'pintura', 'limpieza', 'jardineria');")
    op.execute("DELETE FROM public.usuarios WHERE correo IN ('admin@siswork.local', 'soporte@siswork.local', 'carlos@siswork.local', 'lucia@siswork.local', 'juan.pro@siswork.local', 'maria.pro@siswork.local');")