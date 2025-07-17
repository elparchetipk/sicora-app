"""Excepciones específicas del dominio de AttendanceService."""


class AttendanceServiceError(Exception):
    """Excepción base para errores del servicio de asistencia."""
    pass


class AttendanceError(AttendanceServiceError):
    """Excepción base para errores relacionados con asistencia."""
    pass


class AttendanceNotFoundError(AttendanceError):
    """Error cuando no se encuentra un registro de asistencia."""
    
    def __init__(self, attendance_id: str):
        self.attendance_id = attendance_id
        super().__init__(f"Attendance record not found: {attendance_id}")


class DuplicateAttendanceError(AttendanceError):
    """Error cuando se intenta registrar asistencia duplicada."""
    
    def __init__(self, student_id: str, date: str, block_id: str):
        self.student_id = student_id
        self.date = date
        self.block_id = block_id
        super().__init__(
            f"Attendance already registered for student {student_id} on {date} for block {block_id}"
        )


class InvalidAttendanceStatusError(AttendanceError):
    """Error cuando se proporciona un estado de asistencia inválido."""
    
    def __init__(self, status: str):
        self.status = status
        super().__init__(f"Invalid attendance status: {status}")


class AttendanceUpdateNotAllowedError(AttendanceError):
    """Error cuando no se permite actualizar un registro de asistencia."""
    
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"Attendance update not allowed: {reason}")


class InvalidQRCodeError(AttendanceError):
    """Error cuando el código QR es inválido o ha expirado."""
    
    def __init__(self, message: str = "Invalid or expired QR code"):
        super().__init__(message)


class InvalidBlockStatusError(AttendanceError):
    """Error cuando un bloque o clase no está activo."""
    
    def __init__(self, block_id: str, status: str = None):
        self.block_id = block_id
        self.status = status
        message = f"Block {block_id} is not active"
        if status:
            message += f" (current status: {status})"
        super().__init__(message)


# File Errors
class InvalidFileTypeError(AttendanceError):
    """Error cuando el tipo de archivo no es válido."""
    
    def __init__(self, file_type: str, allowed_types: list = None):
        self.file_type = file_type
        self.allowed_types = allowed_types or []
        message = f"Invalid file type: {file_type}"
        if allowed_types:
            message += f". Allowed types: {', '.join(allowed_types)}"
        super().__init__(message)


class FileTooLargeError(AttendanceError):
    """Error cuando el archivo es demasiado grande."""
    
    def __init__(self, file_size: int, max_size: int):
        self.file_size = file_size
        self.max_size = max_size
        super().__init__(f"File too large: {file_size} bytes. Maximum allowed: {max_size} bytes")


# Justification Errors
class JustificationError(Exception):
    """Excepción base para errores relacionados con justificaciones."""
    pass


class JustificationNotFoundError(JustificationError):
    """Error cuando no se encuentra una justificación."""
    
    def __init__(self, justification_id: str):
        self.justification_id = justification_id
        super().__init__(f"Justification not found: {justification_id}")


class InvalidJustificationFileError(JustificationError):
    """Error cuando el archivo de justificación es inválido."""
    
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"Invalid justification file: {reason}")


class JustificationAlreadyProcessedError(JustificationError):
    """Error cuando se intenta procesar una justificación ya procesada."""
    
    def __init__(self, justification_id: str, current_status: str):
        self.justification_id = justification_id
        self.current_status = current_status
        super().__init__(
            f"Justification {justification_id} already processed with status: {current_status}"
        )


class AlertError(Exception):
    """Excepción base para errores relacionados con alertas."""
    pass


class AlertNotFoundError(AlertError):
    """Error cuando no se encuentra una alerta."""
    
    def __init__(self, alert_id: str):
        self.alert_id = alert_id
        super().__init__(f"Alert not found: {alert_id}")


class UnauthorizedAccessError(AttendanceError):
    """Error cuando un usuario no tiene permisos para acceder a un recurso."""
    
    def __init__(self, resource: str, user_role: str):
        self.resource = resource
        self.user_role = user_role
        super().__init__(f"User with role '{user_role}' not authorized to access {resource}")


class InstructorNotAssignedError(AttendanceError):
    """Error cuando un instructor no está asignado a una ficha o bloque."""
    
    def __init__(self, instructor_id: str, ficha_id: str, block_id: str = None):
        self.instructor_id = instructor_id
        self.ficha_id = ficha_id
        self.block_id = block_id
        
        message = f"Instructor {instructor_id} not assigned to ficha {ficha_id}"
        if block_id:
            message += f" for block {block_id}"
        
        super().__init__(message)


class StudentNotInFichaError(AttendanceError):
    """Error cuando un estudiante no pertenece a una ficha."""
    
    def __init__(self, student_id: str, ficha_id: str):
        self.student_id = student_id
        self.ficha_id = ficha_id
        super().__init__(f"Student {student_id} not enrolled in ficha {ficha_id}")


class FutureDateNotAllowedError(AttendanceError):
    """Error cuando se intenta registrar asistencia para una fecha futura."""
    
    def __init__(self, date: str):
        self.date = date
        super().__init__(f"Cannot register attendance for future date: {date}")


class ExternalServiceError(AttendanceError):
    """Error de comunicación con servicios externos."""
    
    def __init__(self, service: str, message: str):
        self.service = service
        self.message = message
        super().__init__(f"Error communicating with {service}: {message}")
