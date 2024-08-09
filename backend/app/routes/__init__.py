from app import app
from app.routes import users, items, graphs, authentication

app.include_router(users.router)
app.include_router(items.router)
app.include_router(graphs.router)
app.include_router(authentication.router)
