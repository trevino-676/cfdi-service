from app.repository.repository import Repository
from app.repository.nomina_repository import NominaMongoRepository
from app.repository.giro_repository import GiroMongoRepository

repository = NominaMongoRepository()
giro_repo = GiroMongoRepository()
