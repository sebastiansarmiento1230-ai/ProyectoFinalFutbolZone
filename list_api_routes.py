import sys
sys.path.insert(0, 'backend')
from main import app

routes = []
for r in app.routes:
    methods = getattr(r, 'methods', None)
    path = getattr(r, 'path', None)
    name = getattr(r, 'name', None)
    endpoint = getattr(r, 'endpoint', None)
    if methods:
        routes.append((list(methods), path, name))

routes.sort(key=lambda x: x[1])
print(f"Total API routes registered: {len(routes)}")
for m, p, n in routes:
    print(f"{','.join(m):<15} {p:<45} {n}")
