from app.service.service import Service
from app.repository import repository, giro_repo, principal_repo
from app.service.nomina_service import NominaService
from app.service.giro_service import GiroService
from app.service.principal_service import PrincipalService

service = NominaService(repository)
giro_service = GiroService(giro_repo)
principal_service = PrincipalService(principal_repo)
