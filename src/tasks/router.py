from fastapi import APIRouter, Depends
from src.auth.base_config import current_user

from src.tasks.tasks import send_email_report_dashboard
from src.config import SMTP_USER


router  = APIRouter(prefix="/report")


@router.get("/dashboard")
def get_dashboard_report(user=Depends(current_user)):
    send_email_report_dashboard.delay(user.username)
    return {"status": "success",
            'data':'Письмо отправлено',
            'details': None}