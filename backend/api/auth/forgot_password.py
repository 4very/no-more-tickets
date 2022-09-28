from . import router

# POST request for password reset
@router.post('/forgot_password')
async def forgot_password():
    return {"message": "Hello World"}