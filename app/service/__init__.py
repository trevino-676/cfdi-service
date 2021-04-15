from app.service.service import Service
from app.repository import repository, giro_repo
from app.service.nomina_service import NominaService
from app.service.giro_service import GiroService

service = NominaService(repository)
giro_service = GiroService(giro_repo)
