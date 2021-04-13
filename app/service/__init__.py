from app.service.service import Service
from app.repository import repository
from app.service.nomina_service import NominaService

service = NominaService(repository)
