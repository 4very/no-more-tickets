
from . import router

@router.post('/logout')
async def logout():
    return {"message": "Hello World"}