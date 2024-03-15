from core.handlers.welcome import router as welcome_router
from core.handlers.basic import router as basic_router
from core.handlers.admin import router as admin_router
from core.handlers.support import router as support_router
from core.handlers.registration import router as reg_router


routers = [welcome_router, basic_router, admin_router, support_router, reg_router]
