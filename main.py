from adapters.web.error_handlers import register_error_handlers
from adapters.web.router import create_app
from composition import CompositionRoot

composition = CompositionRoot()

app = create_app(composition)
register_error_handlers(app)
