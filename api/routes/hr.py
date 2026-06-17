from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def hr_status():

    return {
        "message":
        "HR endpoint ready"
    }