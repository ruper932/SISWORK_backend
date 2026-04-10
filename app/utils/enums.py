import enum


class RolUsuarioEnum(str, enum.Enum):
    cliente = "cliente"
    profesional = "profesional"
    administrador = "administrador"
    soporte = "soporte"


class EstadoUsuarioEnum(str, enum.Enum):
    activo = "activo"
    suspendido = "suspendido"
    eliminado = "eliminado"
    bloqueado = "bloqueado"


class SexoEnum(str, enum.Enum):
    masculino = "masculino"
    femenino = "femenino"
    otro = "otro"
    prefiero_no_decir = "prefiero_no_decir"


class EstadoVerificacionEnum(str, enum.Enum):
    pendiente = "pendiente"
    en_revision = "en_revision"
    aprobado = "aprobado"
    rechazado = "rechazado"


class NivelEspecialidadEnum(str, enum.Enum):
    basico = "basico"
    intermedio = "intermedio"
    avanzado = "avanzado"
    experto = "experto"


class TipoDocumentoEnum(str, enum.Enum):
    ci = "ci"
    certificado = "certificado"
    licencia = "licencia"
    antecedente = "antecedente"
    otro = "otro"


class EstadoSolicitudEnum(str, enum.Enum):
    abierta = "abierta"
    en_proceso = "en_proceso"
    asignada = "asignada"
    completada = "completada"
    cancelada = "cancelada"


class EstadoPostulacionEnum(str, enum.Enum):
    pendiente = "pendiente"
    aceptada = "aceptada"
    rechazada = "rechazada"
    cancelada = "cancelada"


class CanalContactoEnum(str, enum.Enum):
    whatsapp = "whatsapp"
    telefono = "telefono"
    chat_interno = "chat_interno"
    otro = "otro"


class AccionAuditoriaEnum(str, enum.Enum):
    login = "login"
    logout = "logout"
    registro = "registro"
    editar_perfil = "editar_perfil"
    crear_solicitud = "crear_solicitud"
    editar_solicitud = "editar_solicitud"
    eliminar_solicitud = "eliminar_solicitud"
    postular_solicitud = "postular_solicitud"
    aceptar_postulacion = "aceptar_postulacion"
    rechazar_postulacion = "rechazar_postulacion"
    calificar_servicio = "calificar_servicio"
    subir_certificacion = "subir_certificacion"
    validar_profesional = "validar_profesional"
    rechazar_profesional = "rechazar_profesional"
    suspender_usuario = "suspender_usuario"
    activar_usuario = "activar_usuario"


class TipoReporteEnum(str, enum.Enum):
    usuarios = "usuarios"
    profesionales = "profesionales"
    solicitudes = "solicitudes"
    calificaciones = "calificaciones"
    especialidades = "especialidades"
    validaciones = "validaciones"
    dashboard = "dashboard"


class DiaSemanaEnum(str, enum.Enum):
    lunes = "lunes"
    martes = "martes"
    miercoles = "miercoles"
    jueves = "jueves"
    viernes = "viernes"
    sabado = "sabado"
    domingo = "domingo"