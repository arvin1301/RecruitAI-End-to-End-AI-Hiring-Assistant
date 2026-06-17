from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_report():

    return {
        "message":
        "Report endpoint ready"
    }