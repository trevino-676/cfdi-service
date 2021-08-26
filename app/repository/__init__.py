from app.repository.repository import Repository
from app.repository.nomina_repository import NominaMongoRepository
from app.repository.giro_repository import GiroMongoRepository
from app.repository.principal_repository import PrincipalMongoRepository
from app.repository.pagos_ncc_repository import PagosMongoRepository

repository = NominaMongoRepository()
giro_repo = GiroMongoRepository()
principal_repo = PrincipalMongoRepository()
pagos_repo = PagosMongoRepository()
